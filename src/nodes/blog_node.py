from src.states.blogstate import BlogState, Blog
from langchain_core.messages import HumanMessage


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

    def translation(self, state: BlogState):
        """
        Translate the content to specified language
        """

        translate_prompt = """
        Translate the following content into {current_language}/
        - Maintain the original tone, style and formatting.
        - Adapt cultural references and idioms to be appropriate for {current_language}.
        
        ORIGINAL CONTENT : 
        {blog_content}
        
        """

        blog_content = state["blog"]["content"]
        message = [
            HumanMessage(translate_prompt.format(current_language=state["current_language"],
                                                 blog_content=blog_content))
        ]

        translation_content = self.llm.with_structured_output(Blog).invoke(message)

    def route1(self, state: BlogState):
        return {"current_language": state["current_language"]}

    def route_decision(self, state: BlogState):

        if state["current_language"] == "hindi":
            return "hindi"
        elif state["current_language"] == "french":
            return "french"
        else:
            return state["current_language"]
