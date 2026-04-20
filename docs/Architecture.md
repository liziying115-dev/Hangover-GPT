# Architecture — Pour Decisions (HangoverGPT 🍹)

## Overview

Pour Decisions is a single-tier Streamlit web application. All logic runs server-side in Python; the browser receives rendered HTML/JS from Streamlit. External AI calls go to the Minimax API (CN endpoint, OpenAI-compatible). Recipe data is persisted locally in a JSON file or SQLite database.

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
│        │  Recipe  │  │Minimax   │  │   │
│        │  Store   │  │ Client   │  │   │
│        │(JSON/DB) │  │          │  │   │
│        └──────────┘  └────┬─────┘  │   │
└─────────────────────────────────────────┘
                            │
                   Minimax API (CN Endpoint)
                   (OpenAI-compatible)
```

---

## Directory Structure

```
pour-decisions/
├── app.py                   # Entry point — Streamlit app, page routing
├── requirements.txt
├── .streamlit/
│   ├── config.toml          # Theme and server settings
│   └── secrets.toml         # MINIMAX_API_KEY (never committed)
│
├── data/
│   └── recipes.json         # Static recipe data (15+ recipes)
│
├── services/
│   ├── matcher.py           # Ingredient-based recipe matching logic
│   ├── recommender.py       # AI recommendation — calls Minimax API
│   └── scaler.py            # Serving size scaling calculations
│
├── pages/
│   ├── 01_home.py           # Landing page — ingredient input + AI mood input
│   ├── 02_browse.py         # Browse all cocktails with search and filter
│   ├── 03_results.py        # Ingredient match results + AI recommendations
│   ├── 04_detail.py         # Recipe detail view + serving scaler
│   └── 05_mix.py            # Step-by-step mixing simulation
│
├── components/
│   ├── recipe_card.py       # Reusable recipe card widget
│   └── progress_bar.py      # Mixing progress tracker widget
│
└── docs/
    ├── Architecture.md
    ├── SPEC.md
    ├── ROADMAP.md
    └── gix-bucks.md
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
- Matching is case-insensitive; partial matches sorted by closeness

### `services/recommender.py`
- Accepts a free-text flavor/mood prompt from the user
- Constructs a structured prompt and calls the Minimax API (OpenAI-compatible client)
- Parses the response and returns 3–5 structured recipe suggestions
- Returns `[]` on `JSONDecodeError` or network failure (graceful degradation)

### `services/scaler.py`
- Takes a base recipe and a multiplier (×1, ×2, ×4)
- Returns a new ingredient list with quantities scaled proportionally

### `data/recipes.json`
- Stores 15+ recipe objects conforming to the canonical schema below
- Read-only at runtime; seeded manually
- Filter values for base spirit and flavor profile are derived dynamically from this file at runtime

---

## Data Flow

### Flow 1 — Ingredient Matching
```
User enters ingredients on 01_home.py
    → matcher.py filters recipe store
    → results stored in session_state
    → rendered in 03_results.py
    → user selects recipe → 04_detail.py
```

### Flow 2 — AI Recommendation
```
User enters flavor/mood description on 01_home.py
    → recommender.py builds prompt
    → Minimax API returns suggestions (JSON)
    → parsed suggestions cached in session_state['ai_recommendations']
    → rendered in 03_results.py alongside ingredient matches
```

### Flow 3 — Browse & Filter
```
User opens 02_browse.py
    → all recipes loaded from recipes.json
    → search bar + filter controls (base spirit, flavor, difficulty)
    → filtering done in-memory in Python
    → recipe_card components rendered in grid/list
    → clicking a card → 04_detail.py
```

### Flow 4 — Step-by-Step Mixing
```
User clicks "Start Mixing" on 04_detail.py
    → session state stores recipe + current_step_index = 0
    → 05_mix.py renders one step at a time
    → "Next Step" increments index
    → progress bar updates proportionally
    → completion message shown after final step
```

---

## External Integrations

| Service | Usage | Auth |
|---|---|---|
| Minimax API (CN Endpoint) | AI recipe recommendations | `st.secrets["MINIMAX_API_KEY"]` |
| Streamlit Community Cloud | Hosting & deployment | GitHub OAuth |

No other external services in v1.

---

## Session State Schema

```python
st.session_state = {
    "user_ingredients": [],        # list[str] — from ingredient input
    "selected_recipe": {},         # dict — full recipe object
    "current_step_index": 0,       # int — mixing simulation progress
    "serving_multiplier": 1,       # int — ×1 / ×2 / ×4
    "ai_recommendations": [],      # list[dict] — Minimax API results (cached)
}
```

---

## Data Model

All recipe data is stored as JSON objects. Below is the canonical schema.

### `Recipe`

```json
{
  "id": "margarita-classic",
  "name": "Classic Margarita",
  "description": "A tart, citrusy tequila cocktail with a salted rim.",
  "difficulty": "easy",
  "serving_size": 1,
  "base_spirit": "tequila",
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
| `id` | `string` | URL-safe unique identifier (kebab-case) |
| `name` | `string` | Display name |
| `description` | `string` | One-line summary |
| `difficulty` | `enum` | `easy` \| `medium` \| `hard` |
| `serving_size` | `int` | Base number of servings (default: 1) |
| `base_spirit` | `string` | Primary spirit (e.g. `vodka`, `rum`, `gin`, `tequila`, `whiskey`, `non-alcoholic`) |
| `flavor_tags` | `string[]` | Used for AI matching and display filters |
| `ingredients[].name` | `string` | Canonical ingredient name (used for matching) |
| `ingredients[].amount` | `float \| null` | Quantity at base serving size; `null` = to taste |
| `ingredients[].unit` | `string` | `oz`, `ml`, `tsp`, `tbsp`, `pinch`, `dash`, etc. |
| `steps[].order` | `int` | 1-indexed step sequence |
| `steps[].action` | `string` | Instruction shown to the user |
| `steps[].tip` | `string?` | Optional contextual tip |

### Scaling Rule

```
scaled_amount = base_amount × m   (if amount is not null)
```

`null` amounts (e.g., salt to taste) are left as-is regardless of multiplier.

### AI Recommendation Response Schema

`recommender.py` instructs the model to return structured JSON only. Expected shape:

```json
[
  {
    "name": "Watermelon Mule",
    "description": "Sweet and refreshing with a ginger kick.",
    "flavor_tags": ["sweet", "fruity", "spicy"],
    "difficulty": "easy",
    "base_spirit": "vodka",
    "ingredients": ["vodka", "watermelon juice", "ginger beer", "lime"],
    "why": "Matches your 'sweet and fruity' preference with a refreshing finish."
  }
]
```

---

## Tech Stack Justification

| Technology | Choice | Rationale |
|---|---|---|
| **Language** | Python 3.10+ | Native ecosystem for AI/ML libraries; Minimax OpenAI-compatible client is Python-first |
| **Framework** | Streamlit | Eliminates frontend/backend split; built-in state management; one-command deployment; ideal for rapid iteration |
| **AI** | Minimax API (CN Endpoint) | OpenAI-compatible — uses `openai` Python package with custom `base_url`; no extra SDK dependency |
| **Data Storage** | JSON (→ SQLite) | Zero setup for v1; human-readable for seeding; SQLite swap is non-breaking since all access goes through `matcher.py` |
| **Secrets** | `st.secrets` | Key never hits the repo; same interface locally (`.streamlit/secrets.toml`) and in production |
| **Deployment** | Streamlit Community Cloud | Free tier sufficient; GitHub-native push-to-deploy |

---

## Agentic Engineering Plan

The AI feature is a **single-turn, structured-output call** — not a full autonomous agent.

### Prompt Design

`recommender.py` uses a **system prompt + user prompt** pattern:

```
SYSTEM:
You are a professional cocktail consultant. When given a flavor preference or mood,
return ONLY a JSON array of 3–5 cocktail recommendations. No prose, no markdown fences.
Each object must have: name, description, flavor_tags (array), difficulty (easy/medium/hard),
base_spirit, ingredients (array of strings), why (one sentence explaining the match).

USER:
I want something sweet and fruity, not too strong.
```

### Parsing & Error Handling

```python
import json
from openai import OpenAI
import streamlit as st

def get_recommendations(preference: str) -> list[dict]:
    client = OpenAI(
        api_key=st.secrets["MINIMAX_API_KEY"],
        base_url="https://api.minimax.chat/v1",  # CN endpoint
    )
    response = client.chat.completions.create(
        model="MiniMax-Text-01",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": preference},
        ],
    )
    raw = response.choices[0].message.content.strip()
    try:
        results = json.loads(raw)
        return results if isinstance(results, list) else []
    except json.JSONDecodeError:
        return []
```

### Guardrails

| Risk | Mitigation |
|---|---|
| Model returns prose instead of JSON | System prompt enforces JSON-only; `try/except` on parse |
| Response exceeds latency target (10s) | `max_tokens=1024` caps response size |
| Prompt injection via user input | User input goes only into the `user` turn, not the system prompt |

---

## Key Design Decisions

**Browse page added (`02_browse.py`)** — Covers use case of users exploring without a specific ingredient list. Filter values (base spirit, flavor) are derived dynamically from `recipes.json`, not hardcoded.

**Single-file entry point (`app.py`)** — Streamlit's multi-page routing via `pages/` keeps features isolated while sharing session state naturally.

**Service layer (`services/`)** — Business logic is decoupled from UI widgets.

**`st.secrets` for API key** — The key never touches the codebase; Streamlit Cloud injects it at runtime.

**JSON recipe store (v1)** — Avoids database setup complexity. SQLite can replace it without changing service interfaces.

---

## Out of Scope (v1)

- User accounts / authentication
- Social sharing
- Real-time inventory sync
- Mobile-first responsive layout (desktop 1280px+ is primary target)
