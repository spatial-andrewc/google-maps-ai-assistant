import asyncio
import uuid

from langchain_core.runnables.config import RunnableConfig
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.llm_agents.recommendations_graph.models import State
from app.llm_agents.recommendations_graph.search_term_tool.tool import search_term_tool
from app.llm_agents.recommendations_graph.web_search_tool.tool import web_search_tool
from app.llm_agents.recommendations_graph.worker_node.agent import worker_node


class GraphNotCompiledError(Exception):
    def __init__(self):
        super().__init__("Graph is not compiled")


class RecommendationsGraph:
    def __init__(self):
        self.graph_builder = StateGraph(State)
        self.graph = None
        self.worker_node = worker_node
        self.search_term_tool = search_term_tool
        self.web_search_tool = web_search_tool

    def _add_nodes(self):
        self.graph_builder.add_node("worker", self.worker_node)
        self.graph_builder.add_node("tools", ToolNode(tools=[self.search_term_tool, self.web_search_tool]))

    def _add_edges(self):
        self.graph_builder.add_edge("tools", "worker")
        self.graph_builder.add_conditional_edges("worker", tools_condition)

    def _build(self):
        self._add_nodes()
        self._add_edges()
        self.graph_builder.set_entry_point("worker")
        self.graph_builder.set_finish_point("worker")

    def build_and_compile(self):
        self._build()
        self.graph = self.graph_builder.compile()

    async def _run_async(self, state: State):
        config = RunnableConfig({"configurable": {"thread_id": self.create_thread_id()}})
        if self.graph:
            result = await self.graph.ainvoke(state, config=config)
            return result

    async def get_recommendations(self, locations: list[str], traveller_profile: str) -> list[str]:
        if not self.graph:
            raise GraphNotCompiledError()

        states = [State(location=location, traveller_profile=traveller_profile) for location in locations]
        recommendation_tasks = [self._run_async(state) for state in states]

        results = await asyncio.gather(*recommendation_tasks)

        return [result["messages"][-1].content for result in results if result]

    @staticmethod
    def create_thread_id() -> str:
        return str(uuid.uuid4())
