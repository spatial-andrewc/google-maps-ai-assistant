from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

from app.llm_agents.recommendations_graph.search_term_tool.models import (
    SearchTermResults,
)

search_term_llm = ChatOpenAI(model="gpt-4o-mini")
search_term_llm_with_output = search_term_llm.with_structured_output(SearchTermResults)


@tool(
    description="Generates search terms for a traveler based on their profile and destination.",
)
def search_term_tool(location: str, traveller_profile: str) -> SearchTermResults:
    system_message = """
    You are a search term generator who generates search terms for a traveller that intends to research
    a given location. You use the context from the travellers profile to tailor appropriate search terms.
    Return at least 7 search terms in your response.
    """

    user_message = f"""
    The location is: {location}.
    The traveller's profile is: {traveller_profile}.
    """

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message),
    ]

    result = search_term_llm_with_output.invoke(messages)

    return result
