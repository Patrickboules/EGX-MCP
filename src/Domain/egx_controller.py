from datetime import datetime
from egxpy.download import get_OHLCV_data, get_EGX_intraday_data, get_EGXdata
from src.Domain.date_parser import DateParser

class EGXController:
    __egx30_companies_dict = {
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
    parser = DateParser()

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
