from pydantic import BaseModel, Field


class SearchTerm(BaseModel):
    term: str = Field(description="The search term.")
    rationale: str = Field(description="The reason why this search term is relevant to the traveller.")


class SearchTermResults(BaseModel):
    results: list[SearchTerm] = Field(description="The search term results.")
