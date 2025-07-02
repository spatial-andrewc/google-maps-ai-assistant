import asyncio

from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import tool

from app.llm_agents.recommendations_graph.web_search_tool.models import WebSearchResult

serper = GoogleSerperAPIWrapper()


@tool(description="Search the web and return results for a list of search terms.")
async def web_search_tool(search_term_list: list[str]) -> list[WebSearchResult]:
    results = await asyncio.gather(*[serper.arun(query=search_term) for search_term in search_term_list])
    return [
        WebSearchResult(search_term=item[0], search_result=item[1])
        for item in zip(search_term_list, results, strict=False)
    ]
