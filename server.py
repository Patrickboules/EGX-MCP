from mcp.server.fastmcp import FastMCP
from datetime import datetime,timedelta
from Domain.egx_controller import EGXController
from Domain.gold_controller import GoldController


mcp = FastMCP("EGX-MCP")
stocks = EGXController()
gold = GoldController()


@mcp.resource("egx://companies",name="egx_companies")
def get_egx_companies_dict():
    """
    Get the python dict for the EGX companies
    Returns: 
        egx30 dict { company: ticker}
    """
    return stocks.getEGXCompanies()

@mcp.resource("egx://companies/{company_name}", name="egx_company_ticker")
def get_egx_companies_dict(company_name:str):
    """
    Get the ticker of the company

    Args:
        company_name: official name of the company

    Returns: 
        egx30 dict { company: ticker}
    """
    return stocks.getEGXCompanies()[company_name]

@mcp.tool()
def get_current_time():
    """
    Get the current local date and time.

    Returns:
        datetime: The current local date and time.
    """
    return datetime.now()

@mcp.tool()
def get_timeperiod_date(todays_date:datetime,timeperiod: int):
    """
    Get the date of an old day based on todays date and last date needed
    use the get_current_time function

    Args:
        todays_date: today's date
        timeperiod: the total number of days in a time period (eg., week -> 7 days)
    
    Returns:
        datetime: The date of the difference between the current day and the time period.

    """
    return todays_date - timedelta(days=timeperiod)

@mcp.tool()
def get_last_price(company_ticker:str):
    """
    Get the last closing price of a stock.

    Args:
        company_ticker: The company's ticker symbol (e.g., 'COMI').

    Returns:
        float: The stock's closing price.
    """
    return stocks.getLastDailyPrice(company_ticker)

@mcp.tool()
def get_live_price(company_ticker:str):
    """
    Get the current live price of a stock.
    Falls back to the last closing price if live data is unavailable    

    Args:
        company_ticker: The company's ticker symbol (e.g., 'COMI').

    Returns:
        float: The stock's current or last closing price."""
    return stocks.getLivePrice(company_ticker)

@mcp.tool()
def get_price_change(todays_date:datetime, end_date:datetime, company_ticker:str):
    """
    Get the change of a stock's price based on a start date and end date
     
    Args:
       todays_date: Today's date using get_current_date.
       end_date: The end date of a time period using get_timeperiod_date.
       company_ticker: The company's ticker symbol (e.g., 'COMI').
    
    Returns:
        List[float]: The intial price
    """
    return stocks.getPriceChange(todays_date,end_date,company_ticker)

@mcp.tool()
def get_current_gold_price():
    """
    Get the current live price of a 5 gold karats.

    Returns:
        List[dict{karat name, sell, buy}]: The stock's current or last closing price.
    """

    return gold.getCurrentGoldPrices()

@mcp.tool()
def get_intraday_readings(company_ticker:str, todays_date:datetime):
    """
    Gets the intraday price changes of stock
    Falls back to the last closing price if live data is unavailable or date is invalid   
    Args: 
        company_ticker: The company's ticker symbol (e.g., 'COMI').
        todays_date: today's date

    Returns:
        List[float]: The stock's intraday price.
    """
    return stocks.getIntraday(company_ticker,todays_date)

mcp.tool()
def get_risers_overtime(todays_date:datetime, end_date:datetime, n_companies:int = 5):
    """
    Get the top N stocks that increased in value over a period of time
    Args
        todays_date: Today's date using get_current_date.
        end_date: The end date of a time period using get_timeperiod_date.
        n_companies: the number of companies asked about
    Returns
        {ticker:List[float]}: dicts of a ticker and its prices
    """
    return stocks.getPeriodRisers(todays_date,end_date,n_companies)

@mcp.tool()
def get_riser_intraday(todays_date:datetime, n_companies:int = 5):
    """
    Get the top N stocks that increased in value today
    Args
        todays_date: Today's date using get_current_date.
        n_companies: the number of companies asked about
    Returns
        {ticker:List[float]}: dicts of a ticker and its prices
    """
    return stocks.getIntradayRiser(todays_date,n_companies)