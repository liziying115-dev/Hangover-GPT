# Repository Guidelines

## Project Structure & Module Organization
This repository is a small Streamlit app for cocktail discovery and recommendations. `app.py` is the entry point and sets global page config. Multi-page UI files live in `pages/` and use numeric prefixes such as `01_home.py` and `05_mix.py` so Streamlit shows them in order. Shared UI widgets belong in `components/`, business logic belongs in `services/`, and seeded recipe data lives in `data/recipes.json`. Project documentation is kept in `docs/`.

## Build, Test, and Development Commands
Create an environment and install dependencies with `pip install -r requirements.txt`. Run the app locally with `streamlit run app.py`. Before running features that call Anthropic, add `ANTHROPIC_API_KEY` to `.streamlit/secrets.toml`. There is no dedicated build step for this repo.

## Coding Style & Naming Conventions
Follow existing Python conventions: 4-space indentation, module-level docstrings, and type hints on public functions where practical. Use `snake_case` for files, functions, and variables; keep Streamlit page filenames in the `NN_name.py` pattern. Keep UI code in `pages/` or `components/` and avoid mixing API or matching logic into page files. Prefer small, single-purpose helpers in `services/`.

## Testing Guidelines
There is currently no automated test suite configured. For now, validate changes by running `streamlit run app.py` and exercising the affected flow manually: ingredient matching, recipe detail scaling, and mix-step progression. When adding tests, place them in a top-level `tests/` directory and use filenames like `test_matcher.py` to mirror the target module.

## Commit & Pull Request Guidelines
Recent commits use short imperative subjects such as `Move project docs into docs/ directory` and `Scaffold repo structure, seed data, and add ROADMAP`. Keep commits focused and descriptive. Pull requests should include a short summary, note any user-visible changes, link the relevant issue or roadmap item, and attach screenshots or screen recordings for page-level UI updates.

## Security & Configuration Tips
Do not commit `.streamlit/secrets.toml` or API keys. Treat `data/recipes.json` as seed data and review edits carefully, since recipe structure drives matching, scaling, and UI rendering.
