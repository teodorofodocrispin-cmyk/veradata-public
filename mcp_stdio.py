#!/usr/bin/env python3
"""
VeraData MCP stdio wrapper for Glama quality checks.
Zero external dependencies — pure Python stdlib only.
Implements JSON-RPC 2.0 over stdio (MCP protocol).
"""
import sys
import json
import urllib.request
import urllib.error

API_URL = "http://localhost:8000"

TOOLS = [
    {
        "name": "vera_rates",
        "description": "Real-time central bank rates for LATAM countries (CO, MX, BR, CL, PE). Returns TRM, DTF, IBR, TIIE, Selic, UF. 5-min cache. $0.02 USDC via x402.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {"type": "string", "enum": ["CO", "MX", "BR", "CL", "PE"]},
                "signals": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["country"]
        }
    },
    {
        "name": "vera_sanctions",
        "description": "Sanctions screening — OFAC SDN + SARLAFT CO + CNBV MX + COAF BR + UAF CL. Returns risk_score 0-1 + EU AI Act Art.13 audit hash. $0.05 USDC via x402.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "country": {"type": "string"},
                "type": {"type": "string", "enum": ["person", "company"], "default": "person"}
            },
            "required": ["name", "country"]
        }
    },
    {
        "name": "vera_entity",
        "description": "Company enrichment from LATAM public registries: RUES CO, CNPJ BR, RFC MX. Returns NIT/CNPJ, status, representative, industry. $0.03 USDC via x402.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "identifier": {"type": "string"},
                "country": {"type": "string", "enum": ["CO", "MX", "BR", "CL", "PE"]}
            },
            "required": ["country"]
        }
    },
    {
        "name": "vera_context",
        "description": "AI-powered LATAM market context. Sector + country → market_size, key_players, regulations, growth signals. $0.10 USDC via x402.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sector": {"type": "string"},
                "country": {"type": "string", "enum": ["CO", "MX", "BR", "CL", "PE"]},
                "query": {"type": "string"}
            },
            "required": ["sector", "country"]
        }
    }
]

BODIES = {
    "vera_rates":     lambda a: {"country": a.get("country", "CO"), "signals": a.get("signals")},
    "vera_sanctions": lambda a: {"name": a.get("name", ""), "country": a.get("country", "CO"), "type": a.get("type", "person")},
    "vera_entity":    lambda a: {"identifier": a.get("identifier"), "name": a.get("name"), "country": a.get("country", "CO")},
    "vera_context":   lambda a: {"sector": a.get("sector", ""), "country": a.get("country", "CO"), "query": a.get("query")},
}

ENDPOINTS = {
    "vera_rates": "/rates",
    "vera_sanctions": "/sanctions",
    "vera_entity": "/entity",
    "vera_context": "/context",
}


def call_api(endpoint, body):
    payload = json.dumps({k: v for k, v in body.items() if v is not None}).encode()
    req = urllib.request.Request(
        f"{API_URL}{endpoint}",
        data=payload,
        headers={"Content-Type": "application/json", "X-TRIAL": "true"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        return {"error": f"HTTP {e.code}", "detail": body[:200]}
    except Exception as e:
        return {"error": str(e)}


def handle(request):
    method = request.get("method", "")
    req_id = request.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0", "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "veradata", "version": "1.0.0"}
            }
        }

    if method == "notifications/initialized":
        return None

    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": TOOLS}}

    if method == "tools/call":
        params = request.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})

        if name in ENDPOINTS:
            body = BODIES[name](args)
            result = call_api(ENDPOINTS[name], body)
            return {
                "jsonrpc": "2.0", "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]}
            }

    return {
        "jsonrpc": "2.0", "id": req_id,
        "error": {"code": -32601, "message": f"Method not found: {method}"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle(request)
            if response is not None:
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
        except Exception as e:
            error = {
                "jsonrpc": "2.0", "id": None,
                "error": {"code": -32700, "message": str(e)}
            }
            sys.stdout.write(json.dumps(error) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
