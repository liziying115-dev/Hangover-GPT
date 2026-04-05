# HangoverGPT 🍹

An AI-powered cocktail simulator website built with Python and Streamlit. Visit the site, tell us what ingredients you have or what mood you're in, and get personalized cocktail recipes with interactive step-by-step mixing guidance — no account needed, just open and enjoy.

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
| **AI Integration** | Anthropic Claude API via `st.secrets` |
| **Data Storage** | JSON file or SQLite for recipe data |
| **Deployment** | Streamlit Community Cloud |

---

## Team

| Role | Name |
|---|---|
| **Client** | Phoenix |
| **Developer** | Lisa Li |

---

## Development Timeline

**Project Start:** April 5, 2025
**Final Deadline:** June 1, 2025

### Check-in 1 — April 20
- Project repository set up and dependencies configured
- Basic Streamlit app skeleton running locally
- Recipe data structure defined (JSON/SQLite schema)
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

## Getting Started

```bash
# Clone the repository
git clone <repo-url>
cd pour-decisions

# Install dependencies
pip install -r requirements.txt

# Set up API key
# Add your Anthropic API key to .streamlit/secrets.toml:
# ANTHROPIC_API_KEY = "your-key-here"

# Run the app
streamlit run app.py
```

---

## License

This project was created as part of TECHIN 510 at the Global Innovation Exchange (GIX), University of Washington.
