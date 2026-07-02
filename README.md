<p align="center">
  <img src="https://api.veradata.dev/static/logo.png" alt="VeraData" width="220">
</p>

<p align="center">
  <a href="https://api.veradata.dev/demo"><b>🔍 Try the live demo — no account needed</b></a>
</p>

# VeraData — Verified Latin American Data for Autonomous AI Agents

> **M2M-native. x402 payments. Zero accounts. Zero API keys. Latin America first.**
>
> Built by the creator of [Intelica](https://api.intelica.dev) and [TrustBoost](https://api.trustboost.dev).

> **API:** `https://api.veradata.dev` | **Version:** v1.6.0 | **Countries:** CO, MX, BR, CL, PE, AR
>
> This repo contains the public interface, MCP server definitions, and developer kit.
> The core API is deployed at [api.veradata.dev](https://api.veradata.dev).


---

## MCP Server (Model Context Protocol)

VeraData exposes a native **MCP server** at , compatible with Claude Desktop, Claude Code, Cursor, Windsurf, Smithery, and Glama.

### Connect in Claude Desktop

Add to :

```json
{
  "mcpServers": {
    "veradata": {
      "url": "https://api.veradata.dev/mcp"
    }
  }
}
```

### Connect in Claude Code

```bash
claude mcp add veradata --url https://api.veradata.dev/mcp
```

### MCP Tools

| Tool | Description | Price |
|---|---|---|
|  | Real-time LATAM central bank rates (CO, MX, BR, CL, PE) | /bin/sh.02 USDC |
|  | Sanctions screening — OFAC + SARLAFT + CNBV + COAF + UAF | /bin/sh.05 USDC |
|  | Company enrichment from RUES/CNPJ/RFC registries | /bin/sh.03 USDC |
|  | AI-powered LATAM market intelligence (Claude Haiku) | /bin/sh.10 USDC |

### MCP Protocol

- **Transport:** HTTP (Streamable HTTP, JSON-RPC 2.0)
- **Manifest:** 
- **Tools:**  with 
- **Payment:** x402 micropayments on Base () and Solana

Tool definitions are in [](./mcp_server.py).

---

## The Problem This Solves

On June 28, 2026, Agentic Market has 1,357 x402 services. Person enrichment exists for the US and Europe. Sanctions screening exists for OFAC. Financial signals exist for BTC/ETH.

**Nothing exists for Latin America.**

No x402 service covers:
- Colombian NIT / DIAN registry lookups
- SARLAFT sanctions screening (mandatory for Colombian financial entities)
- Brazilian CNPJ / Receita Federal verification
- Mexican RFC / SAT status
- LATAM central bank rates (DTF, TIIE, Selic)
- Regional compliance verification for EU AI Act Art.13

This is a gap in a market processing $1.2M/day in agentic transactions. VeraData fills it.

---

## What VeraData Is

A single FastAPI service with 5 endpoints, each payable per-call via x402 on Base and Solana. Pure M2M — no human interaction required. Any agent with a wallet can discover it via CDP Bazaar, Agentic Market, or 402 Index, pay in USDC, and receive structured JSON instantly.

**Stack:** FastAPI + Supabase + Render (same as Intelica/TrustBoost — proven in production)

**Payment:** x402 v2, CAIP-2 compliant (`eip155:8453` + `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`)

**Distribution:** CDP Bazaar + Agentic Market + 402 Index (all channels proven with Intelica)

---

## The 5 Endpoints

### 1. `POST /entity` — Entity Enrichment LATAM — `$0.03 USDC`

Given a company name + country, returns structured entity data from public registries.

```json
// Request
{ "name": "Bancolombia", "country": "CO" }

// Response
{
  "nit": "890903938-8",
  "razon_social": "Bancolombia S.A.",
  "estado": "ACTIVA",
  "camara_comercio": "Bogotá",
  "fecha_constitucion": "1945-01-24",
  "representante_legal": "Juan Carlos Mora Uribe",
  "ciiu": "6412",
  "pep_check": false,
  "data_source": "RUES_CO",
  "verified_at": "2026-06-28T14:00:00Z"
}
```

**Data sources:** RUES (Colombia), Receita Federal (Brazil), SAT (Mexico), SRI (Ecuador), SBS (Peru)

**Price:** `$0.03` — refreshed every 24h, cached in Supabase

---

### 2. `POST /sanctions` — Sanctions & Compliance Screen — `$0.05 USDC`

Screens an entity or person against LATAM + global sanctions lists. Returns risk score + EU AI Act compliant audit hash.

```json
// Request
{ "name": "Juan García López", "country": "CO", "type": "person" }

// Response
{
  "risk_score": 0.02,
  "risk_category": "CLEAN",
  "lists_checked": ["OFAC_SDN", "SARLAFT_CO", "CNBV_MX", "COAF_BR", "UAF_CL"],
  "matches": [],
  "pep_status": false,
  "audit_hash": "sha256:abc123...",
  "compliance": ["EU_AI_ACT_ART13", "SARLAFT_2024", "FATF_R16"],
  "checked_at": "2026-06-28T14:00:01Z"
}
```

**Lists covered:**
- 🇨🇴 SARLAFT (Colombia) — updated daily
- 🇲🇽 CNBV Lista Negra (Mexico)
- 🇧🇷 COAF/BACEN (Brazil)
- 🇨🇱 UAF (Chile)
- 🌍 OFAC SDN (USA/Global)
- 🌍 UN Security Council Consolidated List
- 🌍 EU Consolidated Sanctions List

**Regulatory moat:** EU AI Act Art.13 enforcement begins **August 2, 2026** — any European company with AI agents operating in LATAM needs this endpoint.

**Price:** `$0.05` — highest margin module, mandatory for fintech

---

### 3. `POST /registry` — Business Registry Lookup — `$0.05 USDC`

Real-time lookup of business registration data from official public registries.

```json
// Request
{ "identifier": "890903938", "country": "CO", "id_type": "nit" }

// Response
{
  "identifier": "890903938-8",
  "razon_social": "Bancolombia S.A.",
  "tipo_empresa": "Sociedad Anónima",
  "estado_juridico": "ACTIVA",
  "fecha_registro": "1945-01-24",
  "domicilio": "Medellín, Antioquia, Colombia",
  "objeto_social": "Actividades de banca comercial",
  "capital_suscrito_cop": 1076956260000,
  "registro_mercantil": "890903938-8",
  "renovado_hasta": "2026-12-31",
  "fuente": "Cámara de Comercio de Medellín",
  "verified_at": "2026-06-28T14:00:02Z"
}
```

**Countries:** Colombia (RUES + Cámaras), Mexico (SAT + IMSS), Brazil (CNPJ / Receita Federal), Chile (SRCeI), Peru (SUNARP/SUNAT)

**Price:** `$0.05`

---

### 4. `POST /rates` — Financial Signal LATAM — `$0.02 USDC`

Real-time rates and macro indicators from LATAM central banks. No AI — raw data, structured JSON, 5-minute cache.

```json
// Request
{ "country": "CO", "signals": ["usd_cop", "dtf", "ipc_monthly"] }

// Response
{
  "country": "CO",
  "timestamp": "2026-06-28T14:00:03Z",
  "usd_cop": 4187.35,
  "dtf_ea": 10.85,
  "ipc_monthly_pct": 0.47,
  "ipc_annual_pct": 6.12,
  "banrep_rate_pct": 9.75,
  "trm_official": 4187.35,
  "source": "Banco de la República de Colombia",
  "cache_ttl_seconds": 300
}
```

**Countries + signals:**
- 🇨🇴 Colombia: TRM, DTF, IPC, IBR, tasa Banrep
- 🇲🇽 Mexico: TIIE, INPC, UDIS, tasa Banxico
- 🇧🇷 Brazil: Selic, CDI, IPCA, PTAX
- 🇨🇱 Chile: TPM, UF, IPC, USD/CLP
- 🇵🇪 Peru: BCRP rate, USD/PEN, IPC

**Price:** `$0.02` — highest volume module, called every agent cycle

---

### 5. `POST /context` — Market Context LATAM — `$0.10 USDC`

AI-powered market context for a sector + country. Reuses Intelica's LLM layer but focused on LATAM. Returns regulatory environment, key players, market size, growth signals.

```json
// Request
{ "sector": "fintech", "country": "CO", "query": "neobanks competitive landscape 2026" }

// Response
{
  "sector": "fintech",
  "country": "CO",
  "market_size_usd": "2.1B",
  "growth_rate_pct": 34,
  "key_players": ["Nequi", "Daviplata", "Rappipay", "Lulo Bank", "Movii"],
  "regulatory_framework": {
    "regulator": "Superintendencia Financiera de Colombia",
    "key_regulations": ["Decreto 1234/2023 sandbox", "SARLAFT 3.0", "Ley 1328 consumidor financiero"],
    "eu_ai_act_applicable": true
  },
  "market_signals": [
    "BancoEstado LATAM expansion signals 12% YoY neobank account growth",
    "SFC approved 3 new sandbox licenses Q1 2026"
  ],
  "audit_hash": "sha256:def456...",
  "source": "VeraData Market Context Engine v1.0"
}
```

**Price:** `$0.10` — highest value, AI-powered, lowest frequency

---

## Revenue Model

| Endpoint | Price | Conservative calls/day | Revenue/month |
|---|---|---|---|
| `/entity` | $0.03 | 500 | $450 |
| `/sanctions` | $0.05 | 300 | $450 |
| `/registry` | $0.05 | 200 | $300 |
| `/rates` | $0.02 | 2,000 | $1,200 |
| `/context` | $0.10 | 100 | $300 |
| **Total conservador** | | **3,100/day** | **$2,700/month** |
| **Con 1 fintech activo** | | **20,000/day** | **$18,000/month** |

**Why `/rates` dominates:** Agents de trading, DeFi, y treasury que operan en LATAM necesitan las tasas en cada ciclo — cada 5 minutos. 2,000 calls/day conservador es bajo para ese perfil.

---

## Technical Architecture

### Stack (100% reutilizable desde Intelica/TrustBoost)

```
FastAPI (Python 3.11)
  ├── x402 middleware (CDP Bazaar + PayAI)
  ├── Supabase (caché + audit log + rate limiting)
  └── Render (AWS us-east, misma infra)

Payment Stack:
  ├── CDP Facilitator (Bazaar indexing — probado)
  ├── PayAI (fallback — probado)
  └── Wallets: Base + Solana (mismas de Intelica)

Data Sources (todas públicas y gratuitas):
  ├── RUES Colombia — API pública
  ├── Receita Federal Brasil — scraping + API
  ├── SAT México — API pública
  ├── Banco de la República — API JSON
  ├── Banxico — SIE API (gratuita, registro simple)
  ├── BCB Brasil — API REST pública
  ├── OFAC SDN — descarga diaria CSV
  ├── SARLAFT — actualización mensual UIAF
  └── COAF/UAF/CNBV — listas públicas
```

### Database Schema (Supabase)

```sql
-- Caché de entidades (evita llamadas repetidas a registros)
CREATE TABLE entity_cache (
  id BIGSERIAL PRIMARY KEY,
  identifier TEXT NOT NULL,
  country CHAR(2) NOT NULL,
  data JSONB NOT NULL,
  fetched_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ,
  UNIQUE(identifier, country)
);

-- Listas de sancionados (actualizadas diariamente)
CREATE TABLE sanctions_lists (
  id BIGSERIAL PRIMARY KEY,
  list_name TEXT NOT NULL,      -- OFAC_SDN, SARLAFT_CO, etc.
  entity_name TEXT NOT NULL,
  entity_type TEXT,             -- person, company
  country TEXT,
  identifiers JSONB,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tasas de cambio y macro (caché 5 minutos)
CREATE TABLE rates_cache (
  id BIGSERIAL PRIMARY KEY,
  country CHAR(2) NOT NULL,
  signal TEXT NOT NULL,
  value NUMERIC NOT NULL,
  fetched_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(country, signal)
);

-- Audit log x402 (mismo patrón de Intelica)
CREATE TABLE vera_audit (
  id BIGSERIAL PRIMARY KEY,
  seq_id BIGSERIAL,
  ip_hash TEXT,
  endpoint TEXT,
  country TEXT,
  network TEXT,
  price_usdc NUMERIC,
  trace_id UUID,
  audit_hash TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### x402 Payment Flow (idéntico a Intelica — probado en producción)

```
Agent → POST /sanctions (sin X-PAYMENT)
Server → 402 + PAYMENT-REQUIRED header (con extensions.bazaar)
Agent → firma EIP-3009 con wallet Base
Agent → POST /sanctions + X-PAYMENT header
Server → CDP verify → CDP settle → extensions.bazaar → "processing"
Server → response JSON + audit_hash
CDP Bazaar → indexa automáticamente (probado Jun 28, 2026)
```

---

## Build Plan — 4 Fases

### Fase 1 — MVP: `/rates` + `/sanctions` (Semana 1)

**Por qué estas dos primero:**
- `/rates` es el módulo de mayor volumen potencial y el más simple técnicamente — llamadas a APIs públicas de bancos centrales sin IA
- `/sanctions` convierte TrustBoost existente en un módulo con LATAM coverage — 70% del trabajo ya está hecho

**Deliverables:**
- [ ] Repo `veradata` con FastAPI base (fork de TrustBoost)
- [ ] Scraper/fetcher de Banco de la República (Colombia)
- [ ] Scraper/fetcher de Banxico (México)
- [ ] Scraper/fetcher de BCB (Brasil)
- [ ] Módulo de descarga y parsing de OFAC SDN CSV
- [ ] Parsing de lista UIAF SARLAFT Colombia
- [ ] Parsing de lista CNBV México
- [ ] Endpoints `/rates` y `/sanctions` con x402
- [ ] Deploy en Render
- [ ] Registro en CDP Bazaar (proceso ya conocido)
- [ ] Registro en 402 Index
- [ ] Registro en Agentic Market

**Revenue estimado Fase 1:** $600-$1,800/mes

---

### Fase 2 — `/entity` + `/registry` (Semana 2-3)

- [ ] Integración RUES Colombia (API REST pública, sin auth)
- [ ] Integración CNPJ Receita Federal (API pública)
- [ ] Integración RFC SAT México (SOAP, parser)
- [ ] Caché de 24h en Supabase
- [ ] Endpoint `/entity` y `/registry` con x402

**Revenue estimado Fase 2:** $1,500-$4,500/mes acumulado

---

### Fase 3 — `/context` (Semana 4)

- [ ] Reutilizar LLM layer de Intelica (Claude Haiku)
- [ ] Prompt especializado en mercados LATAM
- [ ] Integración con `/rates` para contexto macro real-time
- [ ] Endpoint `/context` con x402 ($0.10)

**Revenue estimado Fase 3:** $2,700-$8,000/mes acumulado

---

### Fase 4 — Discovery y escala (Semana 5+)

- [ ] Orthogonal skill registration (mismo proceso que Intelica PR #60)
- [ ] awesome-x402 PR
- [ ] Blog post técnico en dev.to con caso de uso real
- [ ] TrustBoost cross-promotion (usuarios de TB → VeraData)
- [ ] Intelica cross-promotion (análisis de mercado LATAM usa `/rates` y `/entity`)

---

## Competitive Advantages

### Por qué VeraData puede ganar

1. **First mover en x402 LATAM** — Agentic Market tiene 1,357 servicios. Cero para datos estructurados de Colombia, México, Brasil via x402. La ventana es de 6-12 meses.

2. **EU AI Act como catalyst** — Enforcement August 2, 2026. Empresas europeas con agentes IA en LATAM necesitan `/sanctions` para compliance Art.13. No es opcional.

3. **Stack probado** — FastAPI + Supabase + Render + x402 + CDP Bazaar ya están en producción con Intelica y TrustBoost. No hay que aprender nada nuevo.

4. **Datos gratuitos** — A diferencia de servicios como Clearbit ($99+/mes) o APIs comerciales de bureaus de crédito, las fuentes primarias de VeraData son todas públicas. Margen neto > 90%.

5. **Demanda probada** — `/rates` tiene análogo directo en servicios de alto volumen en Agentic Market (crypto liquidation maps, DeFi signals). El patrón de uso es idéntico pero para LATAM.

6. **Intelica sinergy** — El módulo `/context` reutiliza el grafo de 3,744 nodos de Intelica con foco LATAM. Un agente que usa Intelica para análisis competitivo puede llamar VeraData para datos macro en el mismo workflow.

---

## Discovery Channels

El mismo playbook que funcionó con Intelica:

| Canal | Acción | Tiempo |
|---|---|---|
| CDP Bazaar | Deploy + primer pago con `intelica_pay.html` | Día 1 |
| 402 Index | `curl -X POST https://402index.io/api/v1/register` | Día 1 |
| Agentic Market | Auto-indexado via CDP Bazaar | Día 1 |
| punkpeye/awesome-mcp-servers | PR (sección Security/Data) | Semana 1 |
| xpaysh/awesome-x402 | PR (sección Live Services) | Semana 1 |
| Orthogonal | SKILL.md (mismo proceso PR #60) | Semana 2 |
| 402 Index TrustBoost | Ya verificado — cross-list VeraData | Semana 1 |

---

## Key Decisions & Constraints

### Regla de oro (heredada de Intelica/TrustBoost)
- **Nunca alterar el modelo central** — todos los cambios son aditivos
- **Nunca borrar datos de Supabase** sin confirmación explícita
- **Siempre CAIP-2** en `accepts[]`: `eip155:8453` y `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`

### Stack decisions
- **Python 3.11** — mismo que Intelica/TrustBoost, no cambiar
- **Claude Haiku** — modelo LLM para `/context` ($0.10 precio justifica costo)
- **Supabase Colombia project** — nuevo proyecto separado de Intelica y TrustBoost
- **Render free tier** — suficiente para MVP, upgrade al primer $500/mes

### Data freshness strategy
| Endpoint | Cache TTL | Fuente |
|---|---|---|
| `/entity` | 24 horas | Registros públicos (cambian raro) |
| `/sanctions` | 24 horas | Listas actualizadas diariamente |
| `/rates` | 5 minutos | APIs bancos centrales (tiempo real) |
| `/registry` | 24 horas | Registros mercantiles |
| `/context` | 1 hora | LLM + `/rates` real-time |

---

## Files Structure

```
veradata/
├── main.py              # FastAPI app principal
├── requirements.txt     # FastAPI, httpx, supabase, PyJWT, cryptography
├── .env.example         # Variables de entorno requeridas
├── README.md            # Este archivo
├── CONTEXT.md           # Historial de decisiones y sesiones
├── fetchers/
│   ├── banrep.py        # Banco de la República Colombia
│   ├── banxico.py       # Banco de México
│   ├── bcb.py           # Banco Central do Brasil
│   ├── rues.py          # RUES Colombia
│   ├── receita.py       # Receita Federal Brasil
│   └── sat.py           # SAT México
├── sanctions/
│   ├── ofac.py          # OFAC SDN downloader + parser
│   ├── sarlaft.py       # UIAF SARLAFT Colombia
│   ├── cnbv.py          # CNBV México
│   ├── coaf.py          # COAF Brasil
│   └── uaf.py           # UAF Chile
└── llms-full.txt        # Machine-readable docs para agentes
```

---

## Environment Variables

```bash
# Supabase (nuevo proyecto VeraData)
SUPABASE_URL=
SUPABASE_SERVICE_KEY=

# x402 Payment
WALLET_ADDRESS=           # Base mainnet (misma de Intelica)
WALLET_SOLANA=            # Solana mainnet (misma de Intelica)
CDP_API_KEY_ID=           # organizations/xxx/apiKeys/xxx (mismo de Intelica)
CDP_API_KEY_SECRET=       # EC private key PEM

# LLM (solo para /context)
ANTHROPIC_API_KEY=

# Pricing
PRICE_ENTITY=0.03
PRICE_SANCTIONS=0.05
PRICE_REGISTRY=0.05
PRICE_RATES=0.02
PRICE_CONTEXT=0.10

# Banxico API (registro gratuito en sie.banxico.org.mx)
BANXICO_TOKEN=
```

---

## Context & Provenance

VeraData es el tercer producto del mismo founder que construyó:

- **TrustBoost** (`api.trustboost.dev`) — PII sanitization API, 500+ downloads en ClawHub, verificado en 402 Index, awesome-mcp-servers PR #6415 mergeado
- **Intelica** (`api.intelica.dev`) — Competitive intelligence API, en CDP Bazaar y Agentic Market desde Jun 28, 2026, primer pago x402 via CDP facilitator verificado

El stack, el proceso de deployment, y el playbook de discovery están probados en producción. VeraData aplica las mismas lecciones aprendidas con velocidad de ejecución máxima.

---

## Start Building

```bash
# Clonar y configurar
git clone https://github.com/teodorofodocrispin-cmyk/veradata-public-public
cd veradata
pip install fastapi uvicorn httpx supabase pyjwt cryptography anthropic

# Configurar variables
cp .env.example .env
# Editar .env con tus valores

# Correr localmente
uvicorn main:app --reload --port 8001

# Test /rates (primer endpoint a construir)
curl -X POST http://localhost:8001/rates \
  -H "Content-Type: application/json" \
  -d '{"country": "CO", "signals": ["usd_cop", "dtf"]}'
# → 402 Payment Required (correcto — x402 funcionando)
```

---

*VeraData — Built in Bogotá, Colombia. Jun 28, 2026.*
