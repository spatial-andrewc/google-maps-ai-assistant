from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.llm_agents.recommendations_graph.models import State
from app.llm_agents.recommendations_graph.search_term_tool.tool import search_term_tool
from app.llm_agents.recommendations_graph.web_search_tool.tool import web_search_tool

worker_llm = ChatOpenAI(model="gpt-4o-mini")
worker_llm_with_tools = worker_llm.bind_tools([search_term_tool, web_search_tool])


def worker_node(state: State):
    system_message = """
    You are a helpful travel assistant generating personalized travel overviews for specific destinations.

    You will receive:
    - A destination the traveler is interested in
    - A detailed traveler profile (including interests, personality, and preferences)

    Your task:
    1. Generate relevant search terms based on the traveler's profile and destination
    2. Use the web search tool to gather supporting information for each search term
    3. Write a personalized overview of the destination, combining your general knowledge with the research

    The overview will be saved as a note on a Google Maps location, so keep the tone clear and informative — avoid unnecessary fluff,
    exaggerated language, or excessive wordiness. Craft your response knowing that the user will be the person reading it. Refer to
    the person in first person, do not refer to the user in third person. Speak to the user as if you're make the user think tailored recommendations are the norm.
    Focus on practical insights a first-time visitor would find helpful and relevant to their interests.

    The final response must be in plain text only (no markdown or formatting). It should be a paragraph without sections or headings.
    """  # noqa: E501

    user_message = f"""
    The traveller's specific location of interest is: {state.location}.
    The traveller's profile is: {state.traveller_profile}.
    """

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_message),
    ] + state.messages

    response = worker_llm_with_tools.invoke(messages)

    return {
        "messages": [response],
    }
