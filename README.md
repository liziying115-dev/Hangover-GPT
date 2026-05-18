# HangoverGPT 🍹

An AI-powered cocktail simulator built with Python and Streamlit. Tell us what ingredients you have or what mood you're in, and get personalized cocktail recipes with interactive step-by-step mixing guidance.

---

## Live Demo

> **[https://pour-decisions.streamlit.app](https://pour-decisions.streamlit.app)**

The app is deployed on Streamlit Community Cloud and auto-redeploys on every push to `main`.

---

## Features

- **Ingredient-based Recipe Matching** — Enter the ingredients you have and discover cocktails you can make right now
- **AI-Powered Recommendations** — Describe your flavor preferences or mood and get personalized recipe suggestions
- **Step-by-Step Mixing Simulation** — Follow guided mixing instructions one step at a time with a progress tracker
- **Recipe Detail View** — View full recipe details with a serving size scaler that adjusts ingredient quantities automatically

---

## Tech Stack

| Item | Details |
|---|---|
| **Language** | Python 3.10+ |
| **Framework** | Streamlit |
| **AI Integration** | Minimax API (CN Endpoint, OpenAI-compatible) via `st.secrets` |
| **Data Storage** | `data/recipes.json` (static, 15+ recipes) |
| **Hosting** | [Streamlit Community Cloud](https://streamlit.io/cloud) |
| **CI** | GitHub Actions (`.github/workflows/ci.yml`) |

---

## Team

| Role | Name |
|---|---|
| **Client** | Phoenix |
| **Developer** | Lisa Li |

---

## Getting Started (Local)

```bash
# 1. Clone the repo
git clone https://github.com/<your-org>/pour-decisions.git
cd pour-decisions

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure secrets
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
# Edit .streamlit/secrets.toml and add your Minimax API key

# 4. Run the app
streamlit run app.py
```

---

## Environment Variables

All secrets are managed via Streamlit's native secrets system, **not** `.env` files.

| Variable | Required | Default | Description |
|---|---|---|---|
| `MINIMAX_API_KEY` | **Yes** | — | Minimax API key from [minimaxi.com](https://www.minimaxi.com/) |
| `MINIMAX_BASE_URL` | No | `https://api.minimax.chat/v1` | Minimax regional endpoint |

### Local development

Add these to `.streamlit/secrets.toml` (already in `.gitignore` — never commit this file):

```toml
MINIMAX_API_KEY = "your-key-here"
MINIMAX_BASE_URL = "https://api.minimax.chat/v1"
```

See `.env.example` and `.streamlit/secrets.example.toml` for reference templates.

### Production (Streamlit Community Cloud)

1. Open your app in the [Streamlit Cloud dashboard](https://share.streamlit.io)
2. Go to **⋮ → Settings → Secrets**
3. Paste the TOML key-value pairs and save — changes apply immediately without a redeploy

---

## Deployment

The app is hosted on **Streamlit Community Cloud** (free tier).

### Auto-deploy from `main`

Streamlit Cloud watches the `main` branch and automatically triggers a new production build on every push. No manual steps are needed after the initial setup.

### Initial setup (one-time)

1. Push the repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with your GitHub account.
3. Click **New app** → select this repository → set **Main file path** to `app.py` → click **Deploy**.
4. In **Settings → Secrets**, paste your `MINIMAX_API_KEY` (and optionally `MINIMAX_BASE_URL`).
5. The app will build and publish at `https://<your-app-name>.streamlit.app`.

### CI checks

GitHub Actions runs on every push to `main` and on every pull request:

- Python syntax validation for all source files
- `data/recipes.json` integrity check
- Service and component import smoke tests

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for the full workflow.

---

## Development Timeline

**Project Start:** April 5, 2025  
**Final Deadline:** June 1, 2025

### Check-in 1 — April 20
- Project repository set up and dependencies configured
- Basic Streamlit app skeleton running locally
- Recipe data structure defined (JSON schema)
- Initial architecture PR submitted and reviewed

### Check-in 2 — May 4
- Ingredient input & recipe matching feature complete
- AI-powered recommendation feature integrated and functional
- Basic page layout and navigation in place

### Check-in 3 — May 18
- Step-by-step mixing simulation complete
- Recipe detail view with serving size scaler complete
- Overall UI styling and layout polished

### Final Delivery — June 1
- All features complete and tested
- Bug fixes and edge cases handled
- Deployed to Streamlit Community Cloud
- Final documentation updated

---

## License

This project was created as part of TECHIN 510 at the Global Innovation Exchange (GIX), University of Washington.
