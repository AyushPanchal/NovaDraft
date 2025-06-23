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

        return self.graph

    def build_language_graph(self):
        """
        Build a graph for blog generation for input topic and language
        :return:
        """
        self.blog_node = BlogNode(self.llm)

        # Nodes
        self.graph.add_node("title_creation", self.blog_node.title_creation)
        self.graph.add_node("content_generation", self.blog_node.content_generation)
        self.graph.add_node("hindi_translation", )
        self.graph.add_node("french_translation", )
        self.graph.add_node("route", )

        # Add edges and conditional edges
        self.graph.add_edge(START, "title_creation")
        self.graph.add_edge("title_creation", "content_generation")
        self.graph.add_edge("content_generation", "route")

        # Conditional edge
        self.graph.add_conditional_edges("route",
                                         self.blog_node.route_decision,
                                         {"hindi": "hindi_translation", "french": "french_translation"})

        self.graph.add_edge("hindi_translation", END)
        self.graph.add_edge("french_translation", END)

        return self.graph

    def setup_graph(self, usecase):
        if usecase == "topic":
            self.build_topic_graph()

        if usecase == "language":
            self.build_language_graph()

        return self.graph.compile()


# Below code is for the langsmith langgraph studio

llm = GroqLLM().get_llm()

graph_builder = GraphBuilder(llm)

graph = graph_builder.build_topic_graph().compile()
