# Google Maps Recommendations Agent + Automation

## Overview

A small and scrappy app to explore a few technologies I've been interested in. These are Langgraph, OpenAI Agents SDK, and Playwright. This app uses Playwright to login to a user's Google account and add's AI generated recommendations to places in a Google Maps saved list (interestingly, Google doesn't expose an API for Saved Places). The recommendations are specific to the user based on information saved in their traveller profile.


A fun next step would be to make the browser automation add recommended locations to the user's map as new saved locations.


## App Setup

**This app uses `uv` as the package manager. The app requires the following environment variable to be set:**

```env
OPENAI_API_KEY: str = <your openai api key>
LANGSMITH_TRACING: bool = <flag to enable/disable Langsmith tracing>
LANGSMITH_ENDPOINT: str = <Langsmith endpoint>
LANGSMITH_API_KEY: str = <your Langsmith api key>
LANGSMITH_PROJECT: str = <your Langsmith project name>
SERPER_API_KEY: str = <your Serper API key>
GOOGLE_EMAIL: str = <your google email address>
GOOGLE_PASSWORD: str = <your google password>
GOOGLE_2FA_SECRET: str = <secret key for your google two factor auth code>
GOOGLE_MAPS_LIST_NAME = <the name of your Google maps saved place list>
```

### To install a venv with dependencies

```bash
uv venv
uv sync
source .venv/bin/activate
```

### To add a traveller profile

Save a JSON object as `app/llm_agents/traveller_profile_agent/input/traveller_profile.json` that adheres to the [`TravellerProfile`](app/llm_agents/traveller_profile_agent/models.py) schema.


### To run the app

```bash
cd <path_to_project>
source .venv/bin/activate
uv run -m app.main
```


> **Note:** The app code isn't optimised and it doesn't include automated tests.