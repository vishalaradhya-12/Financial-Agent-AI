from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()

# Web Agent for fetching news
web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources."],
    show_tool_calls=True,
    markdown=True
)

# Finance Agent for stock data
finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data.",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data."],
    show_tool_calls=True,
    markdown=True,
)

# Test individual agents first
print("\n🔹 Fetching news from Web Agent...")
news_response = web_agent.print_response("Get latest news for NVDA", stream=False)

print("\n🔹 Fetching finance data from Finance Agent...")
finance_response = finance_agent.print_response("Get analyst recommendations for NVDA", stream=False)

# Fix: Define `additional_information` as an empty string explicitly
print("\n🔹 Fetching combined data from Agent Team...")
agent_team = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    team=[web_agent, finance_agent],
    instructions=["Always include sources.", "Use tables to display data."],
    show_tool_calls=True,
    markdown=True,
)

# Fix: Explicitly set `additional_information=""`
agent_team.print_response(
    "Summarize analyst recommendations and share the latest news for NVDA",
    additional_information="",
    stream=False
)
