from egxpy.download import get_OHLCV_data,get_EGX_intraday_data
from datetime import date, timedelta


class EGXController:
    def getLastDailyPrice(ticker: str):
        response = get_OHLCV_data(ticker, "EGX", "Daily", 1)
        return response['close'].tolist()[0]
    
    def getLivePrice(ticker:str):
        today = date.today().strftime('%Y-%m-%d')
        response = get_EGX_intraday_data([ticker],"1 Minute",today, today)
        return response[ticker].tolist()[-1]