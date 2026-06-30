"""
VeraData MCP Server
Model Context Protocol (MCP) server exposing LATAM data tools.
Compatible with Claude Desktop, Claude Code, Cursor, Windsurf, Smithery, Glama.

Endpoint: POST https://api.veradata.dev/mcp (JSON-RPC 2.0)
Manifest:  GET  https://api.veradata.dev/mcp

Tools:
  - vera_rates       — Real-time LATAM central bank rates ($0.02 USDC via x402)
  - vera_sanctions   — Sanctions screening OFAC+SARLAFT+CNBV+COAF+UAF ($0.05 USDC via x402)
  - vera_entity      — Company enrichment RUES/CNPJ/RFC ($0.03 USDC via x402)
  - vera_context     — AI-powered LATAM market intelligence ($0.10 USDC via x402)
  - vera_defi_report — DeFi compliance: sanctions+entity+FX+clearance ($0.10 USDC via x402)
  - vera_kyb         — KYB: entity+sanctions in one call ($0.08 USDC via x402)
  - vera_wallet      — Wallet sanctions screening ($0.05 USDC via x402)
  - vera_signal      — Macro signals for trading/DeFi agents ($0.05 USDC via x402)
  - vera_compliance  — Enterprise audit report PASS/REVIEW/FAIL ($0.25 USDC via x402)

Usage in Claude Desktop (claude_desktop_config.json):
{
  "mcpServers": {
    "veradata": {
      "url": "https://api.veradata.dev/mcp"
    }
  }
}

Usage in Claude Code:
  claude mcp add veradata --url https://api.veradata.dev/mcp

The MCP server is implemented in main.py via the /mcp endpoint.
See GET /mcp for the full tool manifest (schema_version v1).
"""

# MCP tool definitions — registered in main.py GET /mcp and POST /mcp
# All tools are readOnly (no side effects) and non-destructive.

MCP_TOOLS = [
    {
        "name": "vera_rates",
        "description": (
            "Real-time central bank rates for LATAM countries (CO, MX, BR, CL, PE, AR). "
            "Returns TRM, DTF, IBR (Colombia), TIIE, INPC (Mexico), Selic, CDI, PTAX (Brazil), "
            "TPM, UF (Chile), BCRP rate (Peru), dólar blue + oficial + MEP + CCL (Argentina). "
            "5-minute cache. $0.02 USDC via x402."
        ),
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "enum": ["CO", "MX", "BR", "CL", "PE", "AR"],
                    "description": "ISO 3166-1 alpha-2 country code"
                },
                "signals": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional: specific signals (e.g. usd_cop, dtf_ea, selic, usd_ars_blue)"
                }
            },
            "required": ["country"],
            "examples": [
                {"country": "CO"},
                {"country": "AR"},
                {"country": "BR", "signals": ["usd_brl", "selic"]}
            ]
        }
    },
    {
        "name": "vera_sanctions",
        "description": (
            "Screen persons or companies against LATAM + global sanctions lists: "
            "OFAC SDN, UN Consolidated, SARLAFT Colombia, CNBV Mexico, COAF Brazil, UAF Chile. "
            "Returns risk_score 0.0-1.0, risk_category, matches, and EU AI Act Art.12/13 "
            "compliant SHA-256 hash chain audit trail (AAT). 20,000+ entries. $0.05 USDC via x402."
        ),
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Person or company name to screen"},
                "country": {"type": "string", "description": "ISO country code (CO, MX, BR, CL, PE, AR)"},
                "type": {"type": "string", "enum": ["person", "company"], "default": "person"},
                "agent_id": {"type": "string", "description": "Persistent agent ID for AAT hash chain"}
            },
            "required": ["name", "country"],
            "examples": [
                {"name": "Juan Garcia Lopez", "country": "CO", "type": "person"},
                {"name": "Bancolombia S.A.", "country": "CO", "type": "company", "agent_id": "my-agent-001"}
            ]
        }
    },
    {
        "name": "vera_entity",
        "description": (
            "Company enrichment from official LATAM public registries: "
            "RUES Colombia (NIT), Receita Federal Brazil (CNPJ), SAT Mexico (RFC), SII Chile (RUT). "
            "Returns legal status, representative, CIIU/CNAE code, incorporation date, data_confidence. "
            "24h cache. $0.03 USDC via x402."
        ),
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Company name for search"},
                "identifier": {"type": "string", "description": "NIT, CNPJ, or RFC number"},
                "country": {"type": "string", "enum": ["CO", "MX", "BR", "CL", "PE"]}
            },
            "required": ["country"],
            "examples": [
                {"identifier": "890903938", "country": "CO"},
                {"identifier": "00000000000191", "country": "BR"},
                {"name": "Bancolombia", "country": "CO"}
            ]
        }
    },
    {
        "name": "vera_context",
        "description": (
            "AI-powered LATAM market intelligence via Claude Sonnet 4.6. "
            "Returns market_size_usd, growth_rate_pct, key_players, opportunity_score, "
            "regulatory_framework (regulator + key regulations + EU AI Act applicability), "
            "growth_drivers, entry_barriers, and market_signals. "
            "Uses live central bank rates for macro context. $0.10 USDC via x402."
        ),
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "inputSchema": {
            "type": "object",
            "properties": {
                "sector": {"type": "string", "description": "Industry sector (e.g. fintech, logistics, healthtech)"},
                "country": {"type": "string", "enum": ["CO", "MX", "BR", "CL", "PE", "AR"]},
                "query": {"type": "string", "description": "Specific market question"}
            },
            "required": ["sector", "country"],
            "examples": [
                {"sector": "fintech", "country": "CO", "query": "neobanks 2026"},
                {"sector": "logistics", "country": "MX"},
                {"sector": "healthtech", "country": "BR", "query": "telemedicine regulation"}
            ]
        }
    },
    {
        "name": "vera_defi_report",
        "description": (
            "Unified DeFi compliance report for LATAM counterparties. "
            "Combines sanctions screening + entity verification + FX rates in one call. "
            "Returns defi_clearance: APPROVED | REVIEW | BLOCKED with full audit trail. "
            "Designed for DeFi protocols, DEXs, lending markets operating in LATAM. $0.10 USDC via x402."
        ),
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {"type": "string", "enum": ["CO", "MX", "BR", "CL", "PE", "AR"]},
                "entity_id": {"type": "string", "description": "NIT/CNPJ/RFC for company screening"},
                "wallet": {"type": "string", "description": "Wallet address for on-chain context"},
                "agent_id": {"type": "string", "description": "Persistent agent ID for AAT"}
            },
            "required": ["country"],
            "examples": [
                {"country": "CO", "entity_id": "Bancolombia"},
                {"country": "AR", "wallet": "0xB33429f6d1DFF5A4add080636d213a9F182Fd671"}
            ]
        }
    },
    {
        "name": "vera_kyb",
        "description": (
            "Know Your Business (KYB) for LATAM companies. "
            "Combines registry lookup + entity enrichment + sanctions screening. "
            "Returns kyb_status: VERIFIED | UNVERIFIED | BLOCKED. "
            "One call replaces 2-3 separate API calls. $0.08 USDC via x402."
        ),
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "inputSchema": {
            "type": "object",
            "properties": {
                "identifier": {"type": "string", "description": "NIT/CNPJ/RFC"},
                "country": {"type": "string", "enum": ["CO", "MX", "BR", "CL", "PE"]},
                "check_sanctions": {"type": "boolean", "default": True}
            },
            "required": ["identifier", "country"],
            "examples": [
                {"identifier": "890903938", "country": "CO"},
                {"identifier": "00000000000191", "country": "BR", "check_sanctions": True}
            ]
        }
    },
    {
        "name": "vera_wallet",
        "description": (
            "Screen a blockchain wallet address against LATAM + global sanctions lists. "
            "Returns recommended_action: ALLOW | REVIEW | BLOCK. "
            "Designed for DeFi protocols that need to screen wallets before processing transactions. "
            "OFAC + SARLAFT + CNBV + COAF + UAF. $0.05 USDC via x402."
        ),
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "inputSchema": {
            "type": "object",
            "properties": {
                "wallet": {"type": "string", "description": "Blockchain wallet address"},
                "country": {"type": "string", "default": "CO"},
                "check_entity": {"type": "string", "description": "Optional company name associated with wallet"}
            },
            "required": ["wallet"],
            "examples": [
                {"wallet": "0xB33429f6d1DFF5A4add080636d213a9F182Fd671", "country": "CO"},
                {"wallet": "giu4VciTkfWJNG1oeP6SzHEJwmabikJSMB91GaFNWE4", "country": "AR"}
            ]
        }
    },
    {
        "name": "vera_signal",
        "description": (
            "Real-time macro market signals for LATAM trading and DeFi agents. "
            "Returns FX rates, central bank rates, spreads, and arbitrage indicators. "
            "Argentina dólar blue + MEP + CCL + spread included. "
            "Designed for HFT agents, arbitrage bots, and DeFi AMM calibration. $0.05 USDC via x402."
        ),
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {"type": "string", "enum": ["CO", "MX", "BR", "CL", "PE", "AR"]},
                "signals": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["country"],
            "examples": [
                {"country": "AR"},
                {"country": "CO", "signals": ["usd_cop", "dtf_ea", "ibr_90"]}
            ]
        }
    },
    {
        "name": "vera_compliance",
        "description": (
            "Enterprise-grade compliance report with full audit trail. "
            "Generates a regulator-ready document: multi-source sanctions screening + "
            "entity verification + SHA-256 hash chain (EU AI Act Art.12/13 + DIFC Reg.10 + CBUAE). "
            "Returns overall_status: PASS | REVIEW | FAIL. $0.25 USDC via x402."
        ),
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "inputSchema": {
            "type": "object",
            "properties": {
                "entity_id": {"type": "string", "description": "Company identifier (NIT/CNPJ/RFC) or name"},
                "country": {"type": "string", "enum": ["CO", "MX", "BR", "CL", "PE", "AR"]},
                "report_type": {"type": "string", "enum": ["full", "sanctions_only", "entity_only"], "default": "full"},
                "purpose": {"type": "string", "enum": ["onboarding", "transaction", "periodic_review"]}
            },
            "required": ["entity_id", "country"],
            "examples": [
                {"entity_id": "Bancolombia", "country": "CO", "purpose": "onboarding"},
                {"entity_id": "890903938", "country": "CO", "report_type": "full", "purpose": "periodic_review"}
            ]
        }
    }
]
