from datetime import datetime
from egxpy.download import get_OHLCV_data, get_EGX_intraday_data, get_EGXdata
from Domain.date_parser import DateParser

class EGXController:
    parser = DateParser()

    __egx30_companies_dict = {
    "Abu Qir Fertilizers & Chemicals Industries": "ABUK",
    "Alexandria Mineral Oils": "AMOC",
    "Abu Dhabi Islamic Bank – Egypt": "ADIB",
    "Commercial International Bank – Egypt": "COMI",
    "Crédit Agricole Egypt": "CIEB",
    "EFG Hermes Holding": "HRHO",
    "Eastern Tobacco": "EAST",
    "Egypt Aluminum": "EGAL",
    "Fawry for Banking & Payment Technology": "FWRY",
    "GB Corp": "GBCO",
    "Heliopolis Housing": "HELI",
    "Ibnsina Pharma": "ISPH",
    "Juhayna Food Industries": "JUFO",
    "Emaar Misr for Development": "EMFD",
    "Orascom Construction": "ORAS",
    "Orascom Hotels & Development": "ORHD",
    "Palm Hills Developments": "PHDC",
    "Qalaa Holdings": "CCAP",
    "Raya Holding for Financial Investments": "RAYA",
    "Telecom Egypt": "ETEL",
    "TMG Holding": "TMGH",
    "Valmore Holding": "VLMR",
    "Medinet Masr for Urban Development": "MASR",
    "Sidi Kerir Petrochemicals": "SKPC",
}

    def getEGXCompanies(self):
        return self.__egx30_companies_dict
    
    def getLastDailyPrice(self,ticker: str):
        response = get_OHLCV_data(ticker, "EGX", "Daily", 1)
        return response['close'].tolist()[0]
    
    def getLivePrice(self,todays_date:datetime,ticker:str):
        today = self.parser.stringfyDates(todays_date)
        response = get_EGX_intraday_data([ticker],"1 Minute",today, today)
        return response[ticker].tolist()[-1]
    
    def getPriceChange(self,todays_date:datetime,
                       end_date:datetime,
                       ticker:str):
        today = self.parser.stringfyDates(todays_date)
        initial_date = self.parser.stringfyDates(end_date)
        response = get_EGXdata([ticker],"Daily",initial_date,today)
        return response[ticker].tolist()
    
    def getIntraday(self,ticker,todays_date):
        today = self.parser.stringfyDates(todays_date)
        response = get_EGX_intraday_data([ticker],'1 Minute',today,today)
        return response[ticker].tolist()

    def getPeriodRisers(self,todays_date:datetime,beginning_date:datetime,NCompanies):
        return self.__getRisers(todays_date,beginning_date,get_EGXdata,'Daily',NCompanies)
        
    def getIntradayRiser(self,todays_date:datetime,NCompanies:int = 5):
        return self.__getRisers(todays_date,todays_date,get_EGX_intraday_data,'1 Minute',NCompanies)

    def __getRisers(self,todays_date:datetime,end_date:datetime,func,timing,NCompanies):
        tickers = [ticker for ticker in self.__egx30_companies_dict.values()]
        today = self.parser.stringfyDates(todays_date)
        beginning = self.parser.stringfyDates(end_date)
        response = func(tickers,timing,beginning,today)
        deltas = {
            t: ((response[t].tolist()[-1] - response[t].tolist()[0]) / response[t].tolist()[0]) * 100
            for t in response
            }
        topN = sorted(deltas, key=lambda t: deltas[t],reverse=True)[::NCompanies]
        return {ticker:response[ticker].tolist() for ticker in topN}

        
