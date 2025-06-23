from src.states.blogstate import BlogState


class BlogNode:
    def __init__(self, llm):
        self.llm = llm

    def title_creation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            prompt = """
            You are an expert blog content writer. use markdown formatting. Generate a blog title for the {topic}. this title should be creative and SEO Friendly. 
            """

            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)

            return {"blog": {"title": response.content}}
        return None

    def content_generation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            prompt = """
            You are an expert blog writer. Use markdown formatting. Generate a blog content with detailed breakdown for the {topic}
            """

            system_message = prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)

            return {"blog": {"title": state["blog"]["title"], "content": response.content}}
        return None
