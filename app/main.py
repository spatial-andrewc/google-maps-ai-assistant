import asyncio

from app.browser.google_maps_travel_assistant import GoogleMapsTravelAssistant
from app.llm_agents.button_identifying_agent.agent import ButtonIdentifyingAgent
from app.llm_agents.recommendations_graph.graph import RecommendationsGraph
from app.llm_agents.traveller_profile_agent.agent import TravellerProfileAgent
from app.settings import Settings


async def main():
    settings = Settings()

    traveller_profile_agent = TravellerProfileAgent()
    traveller_profile = await traveller_profile_agent.get_profile()

    recommendations_graph = RecommendationsGraph()
    recommendations_graph.build_and_compile()

    button_identifying_agent = ButtonIdentifyingAgent()

    google_maps_travel_assistant = GoogleMapsTravelAssistant(
        google_email=settings.GOOGLE_EMAIL,
        google_password=settings.GOOGLE_PASSWORD,
        google_2fa_secret=settings.GOOGLE_2FA_SECRET,
        list_name=settings.GOOGLE_MAPS_LIST_NAME,
        traveller_profile=traveller_profile,
        button_identifying_agent=button_identifying_agent,
        recommendations_graph=recommendations_graph,
    )

    await google_maps_travel_assistant.run()


if __name__ == "__main__":
    asyncio.run(main())
