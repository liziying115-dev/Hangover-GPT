# ROADMAP — Pour Decisions (HangoverGPT 🍹)

> **Status as of 2026-04-17:** Project revived. Repo scaffolded; zero features implemented.
> Original deadline (June 1, 2025) has passed. Timeline below is reset from current date.

---

## Design Decisions (resolved 2026-04-17)

| # | Decision |
|---|---|
| 1 | Browse page + search/filter formally added to architecture (`pages/02_browse.py`) |
| 2 | AI recommendation ACs added to Issue #3; no separate issue needed |
| 3 | `base_spirit` field added to canonical data model and `recipes.json` |
| 4 | AI model: **Minimax API (CN Endpoint)** — OpenAI-compatible, `openai` package with custom `base_url` |
| 5 | SPEC OpenAI fallback retained; Minimax is primary; OpenAI as contingency if Minimax is unavailable |

---

## Feature Backlog

### Phase 1 — Foundation (Issue #2) · ~1–2 days
- [ ] Confirm and lock data schema (`data/recipes.json`) — `base_spirit` field now canonical
- [ ] Seed `recipes.json` with 15+ real recipes covering diverse spirits and difficulties
- [ ] Configure `.streamlit/config.toml` theme
- [ ] Verify `streamlit run app.py` runs clean with the new `pages/` structure
- [ ] Set up `.streamlit/secrets.toml` locally with `MINIMAX_API_KEY` (not committed)

### Phase 2 — Core Browsing (Issues #4, #5) · ~3–4 days
- [ ] `pages/02_browse.py` — grid/list of all recipes using `recipe_card` component
- [ ] `components/recipe_card.py` — card widget (name, difficulty, base spirit, flavor tags)
- [ ] Search bar (filter by name)
- [ ] Filter controls: base spirit, flavor profile, difficulty (multi-select, combinable)
- [ ] Empty-state message when no results match

### Phase 3 — Ingredient Matching (Issue #3) · ~2–3 days
- [ ] `pages/01_home.py` — ingredient multi-select/text input
- [ ] `services/matcher.py` — case-insensitive exact + partial match, sorted by closeness
- [ ] `pages/03_results.py` — render match results with missing ingredient tags
- [ ] Empty-state message when no matches

### Phase 4 — Recipe Detail + Scaler (Issue #6) · ~1–2 days
- [ ] `pages/04_detail.py` — full recipe display
- [ ] `services/scaler.py` — ×1/×2/×4 multiplier (skip `null` amounts)
- [ ] Fractional display: `0.5 oz` → `½ oz`
- [ ] "Start Mixing" button → navigate to `05_mix`

### Phase 5 — Mixing Simulation (Issue #7) · ~2 days
- [ ] `pages/05_mix.py` — one step at a time, Next Step / Start Over
- [ ] `components/progress_bar.py` — labeled progress tracker
- [ ] Completion message after final step

### Phase 6 — AI Recommendations (Issues #3 partial, #10) · ~2–3 days
- [ ] Complete Issue #10: configure Minimax API client, test endpoint, validate JSON output shape
- [ ] `services/recommender.py` — system prompt, API call, JSON parse with `[]` fallback
- [ ] Wire into `pages/01_home.py` (flavor/mood input)
- [ ] Display in `pages/03_results.py` alongside ingredient matches
- [ ] Loading spinner + cache results in `st.session_state['ai_recommendations']`

### Phase 7 — UI Polish (Issue #8) · ~2 days
- [ ] Finalize color palette and typography in `config.toml`
- [ ] Consistent spacing and layout across all pages
- [ ] Logo / header branding for "Pour Decisions"
- [ ] Tablet responsiveness check

---

## Estimated Total: ~2–3 weeks from now (phases can overlap)

---

## Out of Scope (v1)
- User accounts / authentication
- Social sharing
- Mobile-first layout (desktop 1280px+ primary)
- Real-time inventory sync
