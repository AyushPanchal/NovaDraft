import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groq_llm import GroqLLM
import os

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


# APIs

@app.post("/blogs")
async def create_blogs(request: Request):
    data = await request.json()
    topic = data.get("topic", "")
    language = data.get("language", "")

    # Get the llm

    groq_llm = GroqLLM()
    llm = groq_llm.get_llm()

    #Graph Builder

    graph_builder = GraphBuilder(llm)
    if language and topic:
        graph = graph_builder.setup_graph(usecase="language")
        state = graph.invoke({"topic": topic, "current_language": language.lower()})
    elif topic:
        graph = graph_builder.setup_graph(usecase="topic")
        state = graph.invoke({"topic": topic})

    return {"data": state}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", reload=True, port=8000)
