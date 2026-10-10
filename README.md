# SafePath

**Privacy-preserving safe routing — no accounts, no tracking, no server.**

Built at Hacklanta. Targets: Social Good (Cox Automotive), Creative (Adobe),
AI/ML, Fintech, and the "no user data" constraint.

---

## What it does

SafePath finds walking routes scored on **safety** (lighting, path type)
and **accessibility** (wheelchair access, incline, curb ramps) using
OpenStreetMap tags. You can ask in plain language — *"safe route to the
library, avoid steep hills"* — and see exactly *why* a route scored the
way it did. It also compares the cost of walking, transit, and rideshare
for the same trip.

Everything runs on-device. No account. No location history. No server.

---

## Why it matters

People don't just want the *fastest* route. Night-shift workers, wheelchair
users, students walking home after dark, and anyone without a car need a
route they can trust. Existing map apps optimize for speed and quietly log
every trip. SafePath optimizes for **safety and access** — and proves it
collects nothing.

---

## How the privacy claim is enforced

We don't ask you to trust us. We wrote tests.

| Test | Claim it proves |
|---|---|
| `test_session_has_no_forbidden_fields` | No name, email, user ID, IP, device ID, or history field exists |
| `test_session_rejects_pii_if_someone_adds_it` | If any dev ever adds PII, validation fails loudly |
| `test_session_rejects_unknown_fields` | Schema is a strict whitelist, not a blacklist |
| `test_session_is_pure_dict_no_io` | Using a session writes zero files to disk |
| `test_no_db_files_in_project_root` | We ship no database, no history file |
| `test_routing_code_does_not_open_sockets` | Routing runs on a locally cached graph — no network calls |
| `test_schema_is_whitelist_not_blacklist` | Adding a field is a conscious decision, not an accident |

Run them yourself:

```bash
pytest tests/test_privacy.py -v
┌─────────────────────────────────────────┐
│  PRESENTATION  (Streamlit + Folium)     │
│  - Query input                          │
│  - Map with route                       │
│  - Score breakdown panel                │
│  - Cost comparison                      │
└─────────────────────────────────────────┘
                  ▲
┌─────────────────────────────────────────┐
│  LOGIC  (pure Python, no UI)            │
│  - Edge scoring from OSM tags           │
│  - Weighted shortest path (networkx)    │
│  - Query parser → weight modifiers      │
│  - Cost model                           │
└─────────────────────────────────────────┘
                  ▲
┌─────────────────────────────────────────┐
│  DATA  (local, cached)                  │
│  - OSM walk graph (graph.graphml)       │
│  - Static fare table                    │
│  - In-memory session only               │
└─────────────────────────────────────────┘
Newest version