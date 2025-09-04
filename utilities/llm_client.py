import os
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
llm = OpenAI(model="gpt-4o-mini")