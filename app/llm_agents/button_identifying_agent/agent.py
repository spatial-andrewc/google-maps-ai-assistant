from agents import Agent, AgentOutputSchema, Runner

from app.llm_agents.button_identifying_agent.models import (
    GooglePlaceButtonResult,
)

SYSTEM_PROMPT = """
You are a Python developer. Your job is to convert a HTML element's ARIA snapshot (provided as a text block)
into a Python object. The snapshot may represent **any button** on the Google Maps web UI.

Your task is to:
1. Determine if it likely represents a **saved place button** using your geographical knowledge and provided examples as a guide.
2. Extract the metadata into the provided schema.
3. Return the result in the specified output type.

### Example of saved place button:
- button "Maroubra Beach 4.7 stars 3,461 Reviews Beach":
  - text: Maroubra Beach
  - img "4.7 stars 3,461 Reviews"

### Example of the expected output:
{
    "is_google_place_button": True,
    "aria_snapshot": "- button "Maroubra Beach 4.7 stars 3,461 Reviews Beach":\n- text: Maroubra Beach\n- img "4.7 stars 3,461 Reviews"",
    "rationale": <enter rationale string>
    "button": {
        "button_name": "Maroubra Beach 4.7 stars 3,461 Reviews Beach",
        "place_name": "Maroubra Beach",
        "children": [
            {"text": "Maroubra Beach"},
            {"img": "4.7 stars 3,461 Reviews"},
            {"text": "Beach"}
        ]
    }
}

### Example of another saved place button:
- button "Lecce Province of Lecce Italy"

### Example of the expected output:
{
    "is_google_place_button": True,
    "aria_snapshot": - button "Lecce Province of Lecce Italy",
    "rationale": <enter rationale string>
    "button": {
        "button_name": "Lecce Province of Lecce Italy",
        "place_name": "Lecce Province of Lecce Italy",
        "children": []
    }
}

---

### Examples of non-place buttons:
- button "Privacy"
- button "Send product feedback"
- button "1 km"
- button
- button "5 places Bondi Beach & Bronte"
- button "Euro Summer"
- button "Japan 2025"

### Example of the expected output
{
    "is_google_place_button": False,
    "aria_snapshot": - button "Send product feedback",
    "rationale": <enter rationale string>
    "button": None
}
"""  # noqa: E501


class ButtonIdentifyingAgent:
    """An agent that identifies buttons for places on Google Maps web page"""

    def __init__(self):
        self.agent = Agent(
            name="Google Maps Place Button Identifier",
            instructions=SYSTEM_PROMPT,
            model="gpt-4o-mini",
            output_type=AgentOutputSchema(GooglePlaceButtonResult, strict_json_schema=False),
        )

    async def identify_button(self, button_input: str) -> GooglePlaceButtonResult | None:
        result = await Runner.run(self.agent, input=button_input)

        if not isinstance(result.final_output, GooglePlaceButtonResult):
            return None

        return result.final_output
