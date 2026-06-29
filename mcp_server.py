"""
VeraData MCP Server
Model Context Protocol (MCP) server exposing LATAM data tools.
Compatible with Claude Desktop, Claude Code, Cursor, Windsurf, Smithery, Glama.

Endpoint: POST https://api.veradata.dev/mcp (JSON-RPC 2.0)
Manifest:  GET  https://api.veradata.dev/mcp

Tools:
  - vera_rates     — Real-time LATAM central bank rates ($0.02 USDC via x402)
  - vera_sanctions — Sanctions screening OFAC+SARLAFT+CNBV+COAF+UAF ($0.05 USDC via x402)
  - vera_entity    — Company enrichment RUES/CNPJ/RFC ($0.03 USDC via x402)
  - vera_context   — AI-powered LATAM market intelligence ($0.10 USDC via x402)

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

# MCP tool definitions — these are registered in main.py GET /mcp and POST /mcp

MCP_TOOLS = [
    {
        "name": "vera_rates",
        "description": (
            "Real-time central bank rates for LATAM countries (CO, MX, BR, CL, PE). "
            "Returns TRM, DTF, IBR (Colombia), TIIE, INPC (Mexico), Selic, CDI, PTAX (Brazil), "
            "TPM, UF (Chile), BCRP rate (Peru). 5-minute cache. $0.02 USDC via x402."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "country": {
                    "type": "string",
                    "enum": ["CO", "MX", "BR", "CL", "PE"],
                    "description": "ISO 3166-1 alpha-2 country code"
                },
                "signals": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional: specific signals (e.g. usd_cop, dtf_ea, selic)"
                }
            },
            "required": ["country"]
        }
    },
    {
        "name": "vera_sanctions",
        "description": (
            "Screen persons or companies against LATAM + global sanctions lists: "
            "OFAC SDN, UN Consolidated, SARLAFT Colombia, CNBV Mexico, COAF Brazil, UAF Chile. "
            "Returns risk_score 0.0-1.0 and EU AI Act Art.13 compliant audit hash (SHA-256). "
            "20,000+ entries updated daily. $0.05 USDC via x402."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Person or company name to screen"},
                "country": {"type": "string", "description": "ISO country code (CO, MX, BR, CL, PE)"},
                "type": {"type": "string", "enum": ["person", "company"], "default": "person"}
            },
            "required": ["name", "country"]
        }
    },
    {
        "name": "vera_entity",
        "description": (
            "Company enrichment from official LATAM public registries: "
            "RUES Colombia (NIT), Receita Federal Brazil (CNPJ), SAT Mexico (RFC), SII Chile (RUT). "
            "Returns legal status, representative, CIIU/CNAE code, incorporation date. "
            "24h cache. $0.03 USDC via x402."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Company name for search"},
                "identifier": {"type": "string", "description": "NIT, CNPJ, or RFC number"},
                "country": {"type": "string", "enum": ["CO", "MX", "BR", "CL", "PE"]}
            },
            "required": ["country"]
        }
    },
    {
        "name": "vera_context",
        "description": (
            "AI-powered LATAM market intelligence. Returns market_size_usd, growth_rate_pct, "
            "key_players, regulatory_framework (regulator + key regulations + EU AI Act applicability), "
            "and market_signals. Uses live central bank rates for macro context. $0.10 USDC via x402."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "sector": {"type": "string", "description": "Industry sector (e.g. fintech, logistics)"},
                "country": {"type": "string", "enum": ["CO", "MX", "BR", "CL", "PE"]},
                "query": {"type": "string", "description": "Specific market question"}
            },
            "required": ["sector", "country"]
        }
    }
]
