#!/bin/bash
# VeraData — cURL flow example
# Demonstrates the complete x402 M2M flow

BASE="https://api.veradata.dev"

echo "=== Step 1: Discover VeraData A2A manifest ==="
curl -s "$BASE/.well-known/a2a-agent.json" | python3 -m json.tool | head -30

echo ""
echo "=== Step 2: Check health + facilitator latency ==="
curl -s "$BASE/health" | python3 -m json.tool

echo ""
echo "=== Step 3: Probe /sanctions — get 402 payment requirements ==="
curl -s -X POST "$BASE/sanctions" \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "country": "CO"}' | python3 -m json.tool

echo ""
echo "=== Step 4: Trial call — 5 free per endpoint per day ==="
curl -s -X POST "$BASE/sanctions" \
  -H "Content-Type: application/json" \
  -H "X-TRIAL: true" \
  -d '{"name": "Juan Garcia", "country": "CO", "agent_id": "my-agent-001"}' \
  | python3 -m json.tool

echo ""
echo "=== Step 5: Rates — Colombia (trial) ==="
curl -s -X POST "$BASE/rates" \
  -H "Content-Type: application/json" \
  -H "X-TRIAL: true" \
  -d '{"country": "CO"}' | python3 -m json.tool

echo ""
echo "=== Step 6: Argentina dólar blue (trial) ==="
curl -s -X POST "$BASE/rates" \
  -H "Content-Type: application/json" \
  -H "X-TRIAL: true" \
  -d '{"country": "AR"}' | python3 -m json.tool

echo ""
echo "=== Step 7: Entity enrichment — NIT Colombia (trial) ==="
curl -s -X POST "$BASE/entity" \
  -H "Content-Type: application/json" \
  -H "X-TRIAL: true" \
  -d '{"identifier": "890903938", "country": "CO"}' | python3 -m json.tool

echo ""
echo "=== Step 8: Budget status ==="
curl -s "$BASE/budget/my-agent-001" | python3 -m json.tool

echo ""
echo "=== Payment flow (requires wallet) ==="
echo "For paid calls, build the X-PAYMENT token:"
echo "1. POST $BASE/sanctions — receive 402 + PAYMENT-REQUIRED header"
echo "2. Decode base64 header → get payTo address and amount"
echo "3. Sign EIP-3009 TransferWithAuthorization with your USDC wallet"
echo "4. Retry POST with X-PAYMENT: <base64-encoded-token>"
echo "See python_agent.py for complete implementation."
