import json
import os
import pathlib

from agents import Agent, Runner

from app.llm_agents.traveller_profile_agent.models import TravellerProfile

DATA_PATH = "app/llm_agents/traveller_profile_agent"
TRAVELLER_PROFILE_JSON_PATH = os.path.join(DATA_PATH, "input/traveller_profile.json")
TRAVELLER_PROFILE_PATH = os.path.join(DATA_PATH, "output/traveller_profile.md")


class TravellerProfileJSONNotFound(Exception):
    def __init__(self):
        super().__init__(f"Traveller profile JSON not found at {TRAVELLER_PROFILE_JSON_PATH}")


SYSTEM_PROMPT = """
You are a helpful assistant working for an AI travel agency. You are provided with a fully populated JSON data model that
describes a traveller's profile.

Your task is to convert this structured data into a clear, engaging textual profile written in markdown.
The profile should accurately reflect the traveller's characteristics and preferences — as if you are preparing them to be matched with
a perfect holiday by another agent.

Refer to the JSON key names to understand what each value represents. Do not embellish or exaggerate any aspect. Stay true to the data.

Pay special attention to the personality.textual_overview field. This paragraph was written by the user and offers insight into their
tone and personal voice. Use it to infer their personality where appropriate.

The final output should be a concise, accurate markdown-formatted profile that feels natural and informative.
Only return the actual profile as output, nothing else.
"""  # noqa: E501


class TravellerProfileAgent:
    """An agent that creates a traveller's profile"""

    def __init__(self):
        self.agent = Agent(
            name="Traveller Profile Creator",
            instructions=SYSTEM_PROMPT,
            model="gpt-4o-mini",
        )

    def _save_profile_md(self, profile: str):
        with pathlib.Path(TRAVELLER_PROFILE_PATH).open("w") as fp:
            fp.write(profile)

    async def _create_profile(self) -> str:
        if not os.path.exists(TRAVELLER_PROFILE_JSON_PATH):
            raise TravellerProfileJSONNotFound()

        with pathlib.Path(TRAVELLER_PROFILE_JSON_PATH).open("r") as fp:
            profile_raw = json.loads(fp.read())
            profile_model = TravellerProfile(**profile_raw)

        result = await Runner.run(
            self.agent,
            input=f"Here is the user's profile: {profile_model.model_dump()}",
        )

        self._save_profile_md(result.final_output)

        return result.final_output

    def _get_cached_profile(self):
        with pathlib.Path(TRAVELLER_PROFILE_PATH).open("r") as fp:
            return fp.read()

    async def get_profile(self) -> str:
        if os.path.exists(TRAVELLER_PROFILE_PATH):
            return self._get_cached_profile()
        return await self._create_profile()
