from langgraph.graph import StateGraph, START, END
from src.llms.groq_llm import GroqLLM
from src.nodes.blog_node import BlogNode
from src.states.blogstate import BlogState


class GraphBuilder:
    def __init__(self, llm):
        self.blog_node = None
        self.llm = llm
        self.graph = StateGraph(BlogState)

    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on a topic
        """

        self.blog_node = BlogNode(self.llm)

        # Nodes
        self.graph.add_node("title_creation", self.blog_node.title_creation)
        self.graph.add_node("content_generation", self.blog_node.content_generation)

        # Edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", END)

        return self.graph.compile()
