from pydantic import BaseModel, Field


class WebSearchResult(BaseModel):
    search_term: str = Field(description="The search term.")
    search_result: str = Field(description="The result of the web search.")
