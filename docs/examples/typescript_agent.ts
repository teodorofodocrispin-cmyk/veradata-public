/**
 * VeraData — TypeScript/Node.js Agent Example
 * Complete M2M flow with Viem for EIP-3009 signing
 * npm install viem
 */

import { createWalletClient, http, encodePacked, keccak256, toHex } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';

const VERADATA_BASE = 'https://api.veradata.dev';
const USDC_BASE     = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913' as `0x${string}`;
const AGENT_ID      = 'my-ts-agent-001';

// Step 1: Discover capabilities
async function discover() {
  const res = await fetch(`${VERADATA_BASE}/.well-known/a2a-agent.json`);
  const manifest = await res.json();
  console.log(`Agent: ${manifest.name} v${manifest.version}`);
  console.log(`Skills: ${manifest.skills.map((s: any) => s.id).join(', ')}`);
  return manifest;
}

// Step 2: Get payment requirements
async function getPaymentRequirements(endpoint: string, body: object) {
  const res = await fetch(`${VERADATA_BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const header = res.headers.get('PAYMENT-REQUIRED') || '';
  return JSON.parse(Buffer.from(header, 'base64').toString());
}

// Step 3: Sign EIP-3009 and build X-PAYMENT token
async function signPayment(
  privateKey: `0x${string}`,
  walletAddress: `0x${string}`,
  payTo: `0x${string}`,
  amountUsdc: number
): Promise<string> {
  const account = privateKeyToAccount(privateKey);
  const client  = createWalletClient({ account, chain: base, transport: http() });

  const amountUnits = BigInt(Math.round(amountUsdc * 1_000_000));
  const nonce       = toHex(crypto.getRandomValues(new Uint8Array(32)));
  const validBefore = BigInt(Math.floor(Date.now() / 1000) + 300);

  const signature = await client.signTypedData({
    domain: { name: 'USD Coin', version: '2', chainId: 8453n, verifyingContract: USDC_BASE },
    types: {
      TransferWithAuthorization: [
        { name: 'from',        type: 'address' },
        { name: 'to',          type: 'address' },
        { name: 'value',       type: 'uint256' },
        { name: 'validAfter',  type: 'uint256' },
        { name: 'validBefore', type: 'uint256' },
        { name: 'nonce',       type: 'bytes32' },
      ],
    },
    primaryType: 'TransferWithAuthorization',
    message: {
      from: walletAddress, to: payTo,
      value: amountUnits, validAfter: 0n, validBefore, nonce: nonce as `0x${string}`,
    },
  });

  const token = {
    x402Version: 2, scheme: 'exact', network: 'eip155:8453',
    payload: {
      signature,
      authorization: {
        from: walletAddress, to: payTo,
        value: amountUnits.toString(),
        validAfter: '0', validBefore: validBefore.toString(), nonce,
      },
    },
  };
  return Buffer.from(JSON.stringify(token)).toString('base64');
}

// Step 4: Call with payment
async function callWithPayment(endpoint: string, body: object, xPayment: string) {
  const res = await fetch(`${VERADATA_BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-PAYMENT': xPayment },
    body: JSON.stringify(body),
  });
  return res.json();
}

// Trial call (no payment needed — 5 free/day)
async function trialCall(endpoint: string, body: object) {
  const res = await fetch(`${VERADATA_BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-TRIAL': 'true' },
    body: JSON.stringify(body),
  });
  return res.json();
}

// Main workflow
async function main() {
  // Discover
  await discover();

  // Trial sanctions check
  console.log('\n--- Trial sanctions check ---');
  const sanctions = await trialCall('/sanctions', {
    name: 'Bancolombia', country: 'CO', type: 'company', agent_id: AGENT_ID,
  });
  console.log(JSON.stringify(sanctions, null, 2));

  // Trial rates — Argentina dólar blue
  console.log('\n--- Argentina rates (dólar blue) ---');
  const rates = await trialCall('/rates', { country: 'AR' });
  console.log(JSON.stringify(rates, null, 2));

  // Paid flow (requires PRIVATE_KEY env var)
  const privateKey = process.env.ETH_PRIVATE_KEY as `0x${string}`;
  const walletAddress = process.env.ETH_WALLET_ADDRESS as `0x${string}`;

  if (privateKey && walletAddress) {
    const body = { name: 'Bancolombia S.A.', country: 'CO', agent_id: AGENT_ID };
    const reqs = await getPaymentRequirements('/sanctions', body);
    const baseAccept = reqs.accepts.find((a: any) => a.network === 'eip155:8453');
    const xPayment = await signPayment(privateKey, walletAddress, baseAccept.payTo, parseFloat(baseAccept.amount));
    const result = await callWithPayment('/sanctions', body, xPayment);
    console.log('\n--- Paid result ---');
    console.log(JSON.stringify(result, null, 2));
  }
}

main().catch(console.error);
