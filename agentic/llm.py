from dotenv import load_dotenv
from langchain_cohere import ChatCohere

load_dotenv()

llm = ChatCohere(
    model="command-a-03-2025",
    temperature=0
)