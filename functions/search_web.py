from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv()

search = TavilySearch(
    max_results=5,
    topic="general",
    search_depth="basic",
    include_answer=False,
    include_raw_content=False
)

def search_tool(query: str) -> str:
    try:
        result = search.invoke({"query": query})

        formatted = []

        for item in result.get("results", []):
            formatted.append(
                f"Title: {item['title']}\n"
                f"URL: {item['url']}\n"
                f"Content: {item['content']}\n"
                f"Score: {item['score']}"
            )

        return "\n\n".join(formatted)

    except Exception as e:
        return f"Web search failed: {str(e)}"