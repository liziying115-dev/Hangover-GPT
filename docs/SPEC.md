# SPEC.md — HangoverGPT 🍹

## Project Overview

**Pour Decisions** is an AI-powered cocktail simulator web application built with Python and Streamlit. It targets home mixologists, cocktail enthusiasts, and beginners who want personalized recipe recommendations and an interactive, guided mixing experience — all from their browser.

---

## Developer & Agreement

| Field | Details |
|---|---|
| **Client** | Phoenix |
| **Developer** | Lisa Li |
| **Agreed Development Fee** | 35 GIX Bucks |

---

## User Stories

### As a beginner home bartender,
- I want to input the ingredients I have at home so that I can discover cocktails I can actually make right now.
- I want to follow step-by-step mixing instructions so that I don't make mistakes during preparation.
- I want to see difficulty ratings for each recipe so that I can choose something appropriate for my skill level.

### As a cocktail enthusiast,
- I want AI-powered recipe recommendations based on my flavor preferences so that I can discover new drinks I'll enjoy.
- I want to customize ingredient quantities so that I can scale a recipe for more people.

### As any user,
- I want a clean, intuitive interface so that I can navigate the website without confusion.
- I want the website to load quickly and respond smoothly so that my mixing session isn't interrupted.

---

## Functional Specifications

### 1. Ingredient Input & Recipe Matching
- User can enter a list of available ingredients via a text input or multi-select UI.
- The website returns a list of cocktail recipes that can be made with those ingredients (exact match and partial match).
- Each result displays: recipe name, required ingredients, missing ingredients (if partial match), and difficulty level.

### 2. AI-Powered Recipe Recommendation
- User can describe flavor preferences (e.g., "sweet and fruity", "strong and smoky") or mood.
- The website sends the prompt to an AI model and returns 3–5 personalized recipe suggestions with brief explanations.
- Recommendations include ingredient list, preparation steps, and flavor profile tags.

### 3. Browse & Search
- User can browse all available cocktails in a grid/list layout without entering ingredients.
- User can search by name and filter by base spirit, flavor profile, and difficulty.
- Multiple filters can be applied simultaneously.

### 4. Interactive Step-by-Step Mixing Simulation
- User selects a recipe and enters a guided mixing mode.
- Each step is shown one at a time with a "Next Step" button.
- Steps include action description, ingredient amounts, and optional tips.
- A progress bar shows how far along the user is in the process.

### 5. Recipe Detail View
- Displays full recipe: name, description, ingredients with quantities, steps, flavor tags, difficulty, and serving size.
- User can adjust serving size (e.g., ×1, ×2, ×4) and ingredient quantities update proportionally.

---

## Technical Specifications

| Item | Details |
|---|---|
| **Language** | Python 3.10+ |
| **Framework** | Streamlit |
| **AI Integration** | Minimax API (CN Endpoint, OpenAI-compatible) via `st.secrets`; OpenAI API as contingency |
| **Data Storage** | JSON file or SQLite for recipe data |
| **Deployment** | Streamlit Community Cloud (or local) |
| **Version Control** | GitHub |

---

## Out of Scope (v1)

- User accounts, login, or authentication
- Social sharing features
- Real-time inventory syncing with smart devices

---

## Non-Functional Requirements

- The website should load the main page in under 3 seconds.
- AI recommendation response should appear within 10 seconds.
- UI must be fully usable on a standard desktop browser (1280px+ width) and reasonably accessible on tablet browsers.
- Code should include docstrings and inline comments for maintainability.
