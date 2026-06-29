# VeraData Roadmap

> Last updated: Jun 29, 2026 — v1.6.0

## Done ✅

### v1.0.0 — Jun 28, 2026
- 5 endpoints: `/rates`, `/sanctions`, `/entity`, `/registry`, `/context`
- x402 v2 on Base (eip155:8453) + Solana
- CDP Bazaar + 402 Index + Agentic Market + Smithery + Glama
- MCP server at `/mcp` — Claude Desktop, Claude Code, Cursor, Windsurf compatible
- Countries: CO, MX, BR, CL, PE
- 20,000+ sanctions entries (OFAC SDN + UN Consolidated)

### v1.1.0 — Jun 29, 2026
- Circuit breaker per facilitator (CDP → PayAI failover, 3 failures → OPEN 60s)
- `X-Data-Freshness` header on `/rates`
- `/health` with real-time facilitator latency

### v1.2.0 — Jun 29, 2026
- **AAT (Agent Audit Trail)** — EU AI Act Art.12 compliant hash chain
- SHA-256 chain: `genesis → query_hash → event_hash → chain_hash`
- `policy_ref`: `veradata-sanctions-v1.1.0-EU-AI-ACT-ART12-ART13-SARLAFT2024-FATF-R16`
- Table `vera_aat` with per-agent chain history

### v1.3.0 — Jun 29, 2026
- `/context` upgraded: Claude Haiku → **Claude Sonnet 4.6**
- Structured output: `opportunity_score`, `growth_drivers`, `entry_barriers`, `data_confidence`

### v1.4.0 — Jun 29, 2026
- **Per-agent budget caps** — `POST /budget`, `GET /budget/{agent_id}`
- Operators set daily/weekly/monthly USDC limits per agent
- `X-Budget-Exhausted` header on rejection

### v1.5.0 — Jun 29, 2026
- Real-time facilitator latency in `/health`
- **Recipient allowlist** — rejects payments to unauthorized wallets
- Budget caps expanded to all 5 endpoints

### v1.6.0 — Jun 29, 2026
- **A2A manifest** — `/.well-known/a2a-agent.json` (Google A2A protocol)
- **Argentina** — `/rates/AR` with dólar blue, MEP, CCL, BCRA tasa
- `data_confidence` scoring in `/entity` (HIGH/MEDIUM/LOW)
- M2M developer kit: Python, TypeScript, cURL examples

---

## Near Term (next 2 weeks) 🔜

### v1.7.0 — AAT expansion
- [ ] AAT chain on `/entity` (not just `/sanctions`)
- [ ] AAT chain on `/rates` for trading agents
- [ ] `/aat/{agent_id}` — full chain history endpoint
- [ ] AAT export endpoint (GDPR Art.20 data portability)

### v1.8.0 — Data quality
- [ ] Cross-verification RUES × DIAN Colombia
- [ ] Cross-verification CNPJ × Receita Federal secondary sources
- [ ] `data_lineage` field: which sources were queried
- [ ] Freshness metadata: last update date of each source

### v1.9.0 — SARLAFT + regional lists seeding
- [ ] SARLAFT Colombia seed in Supabase
- [ ] CNBV Mexico seed
- [ ] COAF Brazil seed
- [ ] UAF Chile seed
- [ ] Daily cron via GitHub Actions

---

## Mid Term (30 days) 📅

### v2.0.0 — Geographic expansion
- [ ] Uruguay (BCU, BROU)
- [ ] Paraguay (BCP)
- [ ] Panama (SBP)
- [ ] Regional PEP (Politically Exposed Persons) database

### v2.1.0 — Streaming & real-time
- [ ] Server-Sent Events for `/rates` (push on change)
- [ ] WebSocket feed for high-frequency trading agents
- [ ] Sub-5s cache for FX rates

### v2.2.0 — MPP (Stripe) protocol
- [ ] Secondary payment protocol for enterprise high-frequency
- [ ] Session-based streaming payments
- [ ] Fiat + crypto hybrid

---

## Long Term (60-90 days) 🌐

### v3.0.0 — Oracle Network
- [ ] Decentralized node operators validating LATAM data on-chain
- [ ] Chainlink-compatible oracle interface
- [ ] On-chain attestation of RUES/CNPJ/RFC data

### v3.1.0 — White-label B2B
- [ ] Private deployments for banks and fintechs
- [ ] Custom sanctions lists
- [ ] SLA guarantees + dedicated infrastructure

### v3.2.0 — AP2 (Google) integration
- [ ] Mandate-based controls
- [ ] A2A ecosystem full integration
- [ ] Google Cloud Marketplace listing

---

## Not planned ❌

- General-purpose LLM wrapper (not our domain)
- US/EU data (competitive market, no moat)
- Crypto price feeds (commoditized)
- B2C / human-facing dashboard

---

## Metrics targets (90 days)

| Metric | Today | Target |
|---|---|---|
| Daily paid calls | ~10 | 5,000 |
| Revenue/month | $0 | $15,000 |
| Countries covered | 6 (+ AR) | 10 |
| Sanctions entries | 20,124 | 100,000+ |
| p95 latency /rates | ~300ms | <100ms |
| Uptime | 99.9% | 99.95% |

---

Built in Bogotá, Colombia by [@teodorofodocrispin-cmyk](https://github.com/teodorofodocrispin-cmyk)
Questions: open an issue or reach out via [Glama](https://glama.ai/mcp/servers/teodorofodocrispin-cmyk/veradata)
