#!/usr/bin/env python3
"""
VeraData — Python Agent Example
Complete M2M flow: discover → pay → consume
pip install httpx eth-account
"""
import asyncio
import base64
import json
import os
import secrets
import time

import httpx

VERADATA_BASE = "https://api.veradata.dev"
AGENT_ID      = "my-compliance-agent-001"  # persistent ID for AAT chain


# ── Step 1: Discover VeraData capabilities ────────────────────────────────────
async def discover():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{VERADATA_BASE}/.well-known/a2a-agent.json")
        manifest = r.json()
        print(f"Agent: {manifest['name']} v{manifest['version']}")
        print(f"Skills: {[s['id'] for s in manifest['skills']]}")
        return manifest


# ── Step 2: Probe endpoint → get 402 payment requirements ────────────────────
async def get_payment_requirements(endpoint: str, body: dict) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{VERADATA_BASE}{endpoint}",
            json=body,
            headers={"Content-Type": "application/json"},
        )
        assert r.status_code == 402, f"Expected 402, got {r.status_code}"
        header = r.headers.get("PAYMENT-REQUIRED", "")
        return json.loads(base64.b64decode(header + "==").decode())


# ── Step 3: Sign EIP-3009 payment (Base mainnet USDC) ────────────────────────
def sign_payment(
    private_key: str,
    wallet_address: str,
    pay_to: str,
    amount_usdc: float,
) -> str:
    """
    Sign EIP-3009 TransferWithAuthorization for USDC on Base.
    Returns base64-encoded X-PAYMENT token.
    """
    from eth_account import Account
    from eth_account.messages import encode_structured_data

    USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    amount_units = int(amount_usdc * 1_000_000)
    nonce = "0x" + secrets.token_hex(32)
    valid_before = int(time.time()) + 300

    structured_data = {
        "domain": {
            "name": "USD Coin",
            "version": "2",
            "chainId": 8453,
            "verifyingContract": USDC_BASE,
        },
        "types": {
            "EIP712Domain": [
                {"name": "name",              "type": "string"},
                {"name": "version",           "type": "string"},
                {"name": "chainId",           "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "TransferWithAuthorization": [
                {"name": "from",        "type": "address"},
                {"name": "to",          "type": "address"},
                {"name": "value",       "type": "uint256"},
                {"name": "validAfter",  "type": "uint256"},
                {"name": "validBefore", "type": "uint256"},
                {"name": "nonce",       "type": "bytes32"},
            ],
        },
        "primaryType": "TransferWithAuthorization",
        "message": {
            "from":        wallet_address,
            "to":          pay_to,
            "value":       amount_units,
            "validAfter":  0,
            "validBefore": valid_before,
            "nonce":       nonce,
        },
    }

    account = Account.from_key(private_key)
    signed = account.sign_message(encode_structured_data(structured_data))

    token = {
        "x402Version": 2,
        "scheme": "exact",
        "network": "eip155:8453",
        "payload": {
            "signature": signed.signature.hex(),
            "authorization": {
                "from":        wallet_address,
                "to":          pay_to,
                "value":       str(amount_units),
                "validAfter":  "0",
                "validBefore": str(valid_before),
                "nonce":       nonce,
            },
        },
    }
    return base64.b64encode(json.dumps(token).encode()).decode()


# ── Step 4: Call endpoint with payment ────────────────────────────────────────
async def call_with_payment(
    endpoint: str,
    body: dict,
    x_payment: str,
) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            f"{VERADATA_BASE}{endpoint}",
            json=body,
            headers={
                "Content-Type": "application/json",
                "X-PAYMENT": x_payment,
            },
        )
        return r.json()


# ── Main: full compliance workflow ────────────────────────────────────────────
async def main():
    # Configuration — set via environment variables
    PRIVATE_KEY    = os.environ.get("ETH_PRIVATE_KEY", "")
    WALLET_ADDRESS = os.environ.get("ETH_WALLET_ADDRESS", "")

    if not PRIVATE_KEY or not WALLET_ADDRESS:
        print("Demo mode — using X-TRIAL header (5 free calls/day)")
        # Trial mode
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{VERADATA_BASE}/sanctions",
                json={"name": "Juan Garcia Lopez", "country": "CO", "agent_id": AGENT_ID},
                headers={"Content-Type": "application/json", "X-TRIAL": "true"},
            )
            result = r.json()
            print(json.dumps(result, indent=2))
        return

    # Step 1: Discover
    manifest = await discover()

    # Step 2: Sanctions screening workflow
    body = {"name": "Bancolombia S.A.", "country": "CO", "type": "company", "agent_id": AGENT_ID}
    endpoint = "/sanctions"

    # Step 3: Get payment requirements
    reqs = await get_payment_requirements(endpoint, body)
    accepts = reqs["accepts"]
    base_accept = next(a for a in accepts if "eip155:8453" in a["network"])
    price_usdc  = float(base_accept["amount"])
    pay_to      = base_accept["payTo"]

    print(f"\nPayment required: {price_usdc} USDC to {pay_to}")

    # Step 4: Sign payment
    x_payment = sign_payment(PRIVATE_KEY, WALLET_ADDRESS, pay_to, price_usdc)

    # Step 5: Call with payment
    result = await call_with_payment(endpoint, body, x_payment)
    print(f"\nResult: {json.dumps(result, indent=2)}")

    # AAT chain hash — use for next call
    if "aat" in result:
        print(f"\nAAT chain_hash: {result['aat']['chain_hash']}")
        print(f"Pass agent_id='{AGENT_ID}' in next call to extend the chain.")


if __name__ == "__main__":
    asyncio.run(main())
