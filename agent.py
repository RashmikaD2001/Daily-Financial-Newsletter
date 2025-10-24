from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.chains import LLMMathChain
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain.tools import Tool

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required")

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.5,
    google_api_key=API_KEY,
)

# Initialize tools
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)
math_tool = Tool(  # <-- wrap the math chain
    name="Calculator",
    func=math_chain.run,
    description="Useful for answering math questions."
)

yahoo_fin = YahooFinanceNewsTool()
tools = [wikipedia, math_tool, yahoo_fin]

# Initialize Agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,  # lets LLM call tools automatically
    verbose=True,
)

# Define prompt
prompt_template = ChatPromptTemplate.from_messages([
    ("system",
     "You are a financial newsletter assistant. "
     "You will analyze financial news and company data. "
     "Use tools like Wikipedia for background research and Math for calculations. "
     "Summarize the findings into a precise, accurate daily newsletter."),
    ("user", "{news_data}")
])

def news_generator(news_data):
    formatted_input = prompt_template.format_prompt(news_data=news_data).to_messages()
   
    try:
        result = agent.invoke(formatted_input)
        model_output = {'response' : True, 'news' : result['output']}
        return model_output
    except Exception as e:
        model_output = {'response' : False, 'msg' : f'{e}'}
        return model_output