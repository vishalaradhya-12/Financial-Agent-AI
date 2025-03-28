from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

# Load environment variables (if any)
load_dotenv()

# Function to get company symbol
def get_company_symbol(company: str) -> str:
    """Retrieve the stock symbol for a given company."""
    symbols = {
        "Phidata": "MSFT",
        "Infosys": "INFY",
        "Tesla": "TSLA",
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Amazon": "AMZN",
        "Google": "GOOGL",
    }
    result = symbols.get(company, "Unknown")
    print(f"Company: {company}, Symbol: {result}")  # Debugging log
    return result

# Initialize the agent
agent = Agent(
    model=Groq(id="llama-3-70b"),  # Ensure correct model ID
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True),
        get_company_symbol
    ],
    instructions=[
        "Use tables to display data.",
        "If you need to find the symbol for a company, use the get_company_symbol tool.",
    ],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

# Create an instance of YFinanceTools
yfinance_tools = YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True)

# Get symbols for companies
symbol_tsla = get_company_symbol("Tesla")
symbol_msft = get_company_symbol("Phidata")  # Uses MSFT instead

# Fetch analyst recommendations using the instance
analyst_tsla = yfinance_tools.get_analyst_recommendations(symbol=symbol_tsla)
analyst_msft = yfinance_tools.get_analyst_recommendations(symbol=symbol_msft)

# Fetch stock fundamentals using the instance
fundamentals_tsla = yfinance_tools.get_stock_fundamentals(symbol=symbol_tsla)
fundamentals_msft = yfinance_tools.get_stock_fundamentals(symbol=symbol_msft)

# Print results in a markdown-style table
print("\n### Analyst Recommendations for TSLA and MSFT\n")
print("| Symbol | Analyst Recommendations |")
print("|--------|-------------------------|")
print(f"| {symbol_tsla} | {analyst_tsla} |")
print(f"| {symbol_msft} | {analyst_msft} |")

print("\n### Fundamentals for TSLA and MSFT\n")
print("| Symbol | Fundamentals |")
print("|--------|-------------|")
print(f"| {symbol_tsla} | {fundamentals_tsla} |")
print(f"| {symbol_msft} | {fundamentals_msft} |")
