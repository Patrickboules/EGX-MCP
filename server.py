from mcp.server.fastmcp import FastMCP
from datetime import datetime
from egx_controller import EGXController


MCP = FastMCP("EGX-MCP")
controller = EGXController()

egx30_companies_dict = {
    "Abu Qir Fertilizers & Chemicals Industries": "ABUK",
    "Alexandria Mineral Oils": "AMOC",
    "Abu Dhabi Islamic Bank – Egypt": "ADIB",
    "Arab Petroleum Pipelines": "APIL",
    "Commercial International Bank – Egypt": "COMI",
    "Crédit Agricole Egypt": "CIEB",
    "EFG Hermes Holding": "HRHO",
    "Eastern Tobacco": "EAST",
    "Egypt Aluminum": "EGAL",
    "Egypt Kuwait Holding": "EKHOA",
    "Fawry for Banking & Payment Technology": "FWRY",
    "GB Corp": "GBCO",
    "Global Pensions & Insurance": "GPI",
    "Heliopolis Housing": "HELI",
    "Ibnsina Pharma": "ISPH",
    "Juhayna Food Industries": "JUFO",
    "Emaar Misr for Development": "EMFD",
    "Orascom Construction": "ORAS",
    "Orascom Hotels & Development": "ORHD",
    "Orascom Investment Holding": "ORID",
    "Palm Hills Developments": "PHDC",
    "Qalaa Holdings": "CCAP",
    "Raya Holding for Financial Investments": "RAYA",
    "Telecom Egypt": "ETEL",
    "TMG Holding": "TMGH",
    "Valmore Holding": "VLMR",
    "Biopharma": "BPHM",
    "East Delta Electricity Production": "EDEC",
    "Medinet Masr for Urban Development": "MASR",
    "Sidi Kerir Petrochemicals": "SKPC",
    "Aēon": "AEON"
}

@MCP.resource("egx://companies")
def get_egx_companies_dict():
    """
    Get the python dict for the EGX companies
    Returns: 
        egx30 dict { company: ticker}
    """
    return egx30_companies_dict

@MCP.resource("egx://companies/{company_name}")
def get_egx_companies_dict(company_name:str):
    """
    Get the ticker of the company

    Args:
        company_name: official name of the company

    Returns: 
        egx30 dict { company: ticker}
    """
    return egx30_companies_dict[company_name]

@MCP.tool("time://local")
def get_current_time():
    """
    Get the current local date and time.

    Returns:
        datetime: The current local date and time.
    """
    return datetime.now()


@MCP.tool()
def get_last_price(company_ticker:str):
    """
    Get the last closing price of a stock.

    Args:
        company_ticker: The company's ticker symbol (e.g., 'AAPL').

    Returns:
        float: The stock's closing price.
    """
    return controller.getLastDailyPrice(company_ticker)

@MCP.tool()
def get_live_price(company_ticker:str):
    """
    Get the current live price of a stock.
    Falls back to the last closing price if live data is unavailable    

    Args:
        company_ticker: The company's ticker symbol (e.g., 'COMI').

    Returns:
        float: The stock's current or last closing price."""
    return controller.getLivePrice(company_ticker)
