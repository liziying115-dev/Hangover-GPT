# Architecture — Pour Decisions (HangoverGPT 🍹)

## Overview

Pour Decisions is a single-tier Streamlit web application. All logic runs server-side in Python; the browser receives rendered HTML/JS from Streamlit. External AI calls go to the Anthropic Claude API. Recipe data is persisted locally in a JSON file or SQLite database.

---

## System Diagram

```
Browser (User)
     │  HTTP (Streamlit)
     ▼
┌─────────────────────────────────────────┐
│           Streamlit App (app.py)        │
│                                         │
│  ┌─────────────┐   ┌─────────────────┐  │
│  │   UI Layer  │   │  Business Logic │  │
│  │  (pages/)   │──▶│   (services/)   │  │
│  └─────────────┘   └────────┬────────┘  │
│                             │           │
│              ┌──────────────┼──────┐    │
│              ▼              ▼      ▼    │
│        ┌──────────┐  ┌──────────┐  │   │
│        │  Recipe  │  │ Claude   │  │   │
│        │  Store   │  │  Client  │  │   │
│        │(JSON/DB) │  │(api.py)  │  │   │
│        └──────────┘  └────┬─────┘  │   │
└─────────────────────────────────────────┘
                            │
                   Anthropic Claude API
                   (claude-3-5-sonnet)
```

---

## Directory Structure

```
pour-decisions/
├── app.py                   # Entry point — Streamlit app, page routing
├── requirements.txt
├── .streamlit/
│   └── secrets.toml         # ANTHROPIC_API_KEY (never committed)
│
├── data/
│   └── recipes.json         # (or recipes.db) — static recipe data
│
├── services/
│   ├── matcher.py           # Ingredient-based recipe matching logic
│   ├── recommender.py       # AI recommendation — calls Claude API
│   └── scaler.py            # Serving size scaling calculations
│
├── pages/
│   ├── 01_home.py           # Landing page / ingredient input
│   ├── 02_results.py        # Recipe match results list
│   ├── 03_detail.py         # Recipe detail view + serving scaler
│   └── 04_mix.py            # Step-by-step mixing simulation
│
└── components/
    ├── recipe_card.py       # Reusable recipe card widget
    └── progress_bar.py      # Mixing progress tracker widget
```

---

## Module Responsibilities

### `app.py`
- Initializes Streamlit session state
- Handles top-level page routing and navigation
- Sets global theme/config via `st.set_page_config`

### `services/matcher.py`
- Accepts a list of user-supplied ingredients
- Queries the recipe store and returns exact and partial matches
- Tags each result with missing ingredients and difficulty level

### `services/recommender.py`
- Accepts a free-text flavor/mood prompt from the user
- Constructs a structured prompt and calls the Claude API
- Parses the response and returns 3–5 structured recipe suggestions

### `services/scaler.py`
- Takes a base recipe and a multiplier (×1, ×2, ×4)
- Returns a new ingredient list with quantities scaled proportionally

### `data/recipes.json` (or `recipes.db`)
- Stores recipe objects with: `name`, `ingredients[]`, `steps[]`, `difficulty`, `flavor_tags`, `serving_size`
- Read-only at runtime; seeded manually or via a setup script

---

## Data Flow

### Flow 1 — Ingredient Matching
```
User enters ingredients
    → matcher.py filters recipe store
    → results list rendered in 02_results.py
    → user selects recipe → 03_detail.py
```

### Flow 2 — AI Recommendation
```
User enters flavor/mood description
    → recommender.py builds prompt
    → Claude API returns suggestions (JSON)
    → parsed suggestions rendered in 02_results.py
```

### Flow 3 — Step-by-Step Mixing
```
User picks a recipe
    → session state stores recipe + current step index
    → 04_mix.py renders one step at a time
    → "Next Step" increments index
    → progress bar updates proportionally
```

---

## External Integrations

| Service | Usage | Auth |
|---|---|---|
| Anthropic Claude API | AI recipe recommendations | `st.secrets["ANTHROPIC_API_KEY"]` |
| Streamlit Community Cloud | Hosting & deployment | GitHub OAuth |

No other external services in v1.

---

## Session State Schema

Streamlit session state is used to pass data between pages without re-fetching.

```python
st.session_state = {
    "user_ingredients": [],        # list[str] — from ingredient input
    "selected_recipe": {},         # dict — full recipe object
    "current_step_index": 0,       # int — mixing simulation progress
    "serving_multiplier": 1,       # int — ×1 / ×2 / ×4
    "ai_recommendations": [],      # list[dict] — Claude API results
}
```

---

## Data Model

All recipe data is stored as JSON objects (or equivalent SQLite rows). Below is the canonical schema.

### `Recipe`

```json
{
  "id": "margarita-classic",
  "name": "Classic Margarita",
  "description": "A tart, citrusy tequila cocktail with a salted rim.",
  "difficulty": "easy",
  "serving_size": 1,
  "flavor_tags": ["citrus", "tart", "refreshing"],
  "ingredients": [
    { "name": "tequila",        "amount": 2,    "unit": "oz" },
    { "name": "lime juice",     "amount": 1,    "unit": "oz" },
    { "name": "triple sec",     "amount": 0.5,  "unit": "oz" },
    { "name": "salt",           "amount": null, "unit": "pinch" }
  ],
  "steps": [
    { "order": 1, "action": "Rim a glass with salt.", "tip": "Use a lime wedge to wet the rim first." },
    { "order": 2, "action": "Combine tequila, lime juice, and triple sec in a shaker with ice." },
    { "order": 3, "action": "Shake vigorously for 15 seconds.", "tip": "Shake until the outside of the shaker feels cold." },
    { "order": 4, "action": "Strain into the prepared glass over fresh ice." }
  ]
}
```

### Field Reference

| Field | Type | Description |
|---|---|---|
| `id` | `string` | URL-safe unique identifier |
| `name` | `string` | Display name |
| `description` | `string` | One-line summary |
| `difficulty` | `enum` | `easy` \| `medium` \| `hard` |
| `serving_size` | `int` | Base number of servings (default: 1) |
| `flavor_tags` | `string[]` | Used for AI matching and display filters |
| `ingredients[].name` | `string` | Canonical ingredient name (used for matching) |
| `ingredients[].amount` | `float \| null` | Quantity at base serving size; `null` = to taste |
| `ingredients[].unit` | `string` | `oz`, `ml`, `tsp`, `tbsp`, `pinch`, `dash`, etc. |
| `steps[].order` | `int` | 1-indexed step sequence |
| `steps[].action` | `string` | Instruction shown to the user |
| `steps[].tip` | `string?` | Optional contextual tip |

### Scaling Rule

When the user selects a multiplier `m`, ingredient amounts are scaled as:

```
scaled_amount = base_amount × m   (if amount is not null)
```

`null` amounts (e.g., salt to taste) are left as-is regardless of multiplier.

### AI Recommendation Response Schema

`recommender.py` instructs Claude to return structured JSON. The expected shape:

```json
[
  {
    "name": "Watermelon Mule",
    "description": "Sweet and refreshing with a ginger kick.",
    "flavor_tags": ["sweet", "fruity", "spicy"],
    "difficulty": "easy",
    "ingredients": ["vodka", "watermelon juice", "ginger beer", "lime"],
    "why": "Matches your 'sweet and fruity' preference with a refreshing finish."
  }
]
```

---

## Tech Stack Justification

| Technology | Choice | Rationale |
|---|---|---|
| **Language** | Python 3.10+ | Native ecosystem for AI/ML libraries; all team members familiar; Anthropic SDK is Python-first |
| **Framework** | Streamlit | Eliminates frontend/backend split — UI and logic in one Python file; built-in state management; one-command deployment to Streamlit Cloud; ideal for data-centric apps with rapid iteration needs |
| **AI** | Anthropic Claude API | Specified in SPEC; strong instruction-following for structured JSON output; reliable for culinary/recipe domain knowledge |
| **Data Storage** | JSON (→ SQLite) | JSON requires zero setup for v1 and is human-readable for seeding recipes; SQLite swap is non-breaking since all access goes through `matcher.py`; no user-generated data to persist in v1 |
| **Secrets** | `st.secrets` | Native Streamlit secret management; key never hits the repo; same interface locally (`.streamlit/secrets.toml`) and in production (dashboard injection) |
| **Deployment** | Streamlit Community Cloud | Free tier sufficient for v1; GitHub-native CI (push to deploy); no DevOps configuration required |
| **Version Control** | GitHub | Standard; required by Streamlit Cloud's GitHub integration |

**Why not Flask/FastAPI + React?** The SPEC targets a single developer (Lisa Li) with a June 1 deadline. A full frontend/backend split would double the surface area without adding user-facing value in v1. Streamlit's constraint — server-side rendering — is acceptable given the desktop-first, no-auth requirement.

**Why not LangChain or similar?** The AI integration is a single prompt-response call (no chaining, no memory, no agents). Adding a framework layer would increase dependency complexity for no functional gain in v1.

---

## Agentic Engineering Plan

The AI feature in Pour Decisions is a **single-turn, structured-output call** — not a full autonomous agent. The plan below describes how to engineer it reliably.

### What "Agentic" Means Here

The recommender is given a user's natural language preference and must autonomously decide which recipes to surface, why, and in what format — without hard-coded rules. The engineering challenge is making that output consistent and parseable.

### Prompt Design

`recommender.py` uses a **system prompt + user prompt** pattern:

```
SYSTEM:
You are a professional cocktail consultant. When given a flavor preference or mood,
return ONLY a JSON array of 3–5 cocktail recommendations. No prose, no markdown fences.
Each object must have: name, description, flavor_tags (array), difficulty (easy/medium/hard),
ingredients (array of strings), why (one sentence explaining the match).

USER:
I want something sweet and fruity, not too strong.
```

Key design choices:
- **JSON-only output** instruction in system prompt prevents prose leakage
- **Exact field names** specified so parsing is deterministic
- **`why` field** makes the recommendation transparent to the user (explainability)
- **Difficulty constraint** keeps output within the app's existing schema

### Parsing & Error Handling

```python
import json, anthropic

def get_recommendations(preference: str) -> list[dict]:
    client = anthropic.Anthropic()
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": preference}]
    )
    raw = response.content[0].text.strip()
    try:
        results = json.loads(raw)
        return results if isinstance(results, list) else []
    except json.JSONDecodeError:
        return []   # Graceful degradation — UI shows fallback message
```

### Guardrails

| Risk | Mitigation |
|---|---|
| Model returns prose instead of JSON | System prompt enforces JSON-only; `try/except` on parse |
| Response exceeds latency target (10s) | `max_tokens=1024` caps response size; Claude typically responds in 2–4s |
| Model hallcinates unavailable ingredients | `why` field is shown to user — they self-filter; no automated ingredient validation in v1 |
| Prompt injection via user input | User input goes only into the `user` turn, not the system prompt; no shell/eval exposure |

### Iteration Plan by Check-in

**Check-in 2 (May 4) — Basic integration:**
- Hardcoded test prompt → verify JSON shape is returned
- `st.secrets` wired up; API key confirmed working
- Basic error state shown in UI on parse failure

**Check-in 3 (May 18) — Polish:**
- Prompt tuned based on test runs across 10+ preference strings
- Loading spinner shown during API call (`st.spinner`)
- Results cached in `st.session_state` so re-renders don't re-call the API

**Final Delivery (June 1):**
- Edge cases handled: empty input, very short input, non-English input (graceful fallback)
- Response time validated against 10s NFR under normal network conditions

---

## Key Design Decisions

**Single-file entry point (`app.py`)** — Streamlit's multi-page routing via `pages/` keeps features isolated while sharing session state naturally.

**Service layer (`services/`)** — Business logic is decoupled from UI widgets, making unit testing and future API extraction straightforward.

**`st.secrets` for API key** — The key never touches the codebase; Streamlit Cloud injects it at runtime from the dashboard secrets config.

**JSON recipe store (v1)** — Avoids database setup complexity for the initial release. SQLite can replace it without changing the service interfaces if the dataset grows.

---

## Out of Scope (v1)

- User accounts / authentication
- Social sharing
- Real-time inventory sync
- Mobile-first responsive layout (desktop 1280px+ is primary target)
