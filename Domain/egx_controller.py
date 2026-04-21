from datetime import datetime
import logging
import os
from egxpy.download import get_OHLCV_data, get_EGX_intraday_data, get_EGXdata
from Domain.date_parser import DateParser


logger = logging.getLogger("egx_ctrl")
logger.setLevel(logging.DEBUG)  # Capture all levels
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EGXController:
    parser = DateParser()

    __egx30_companies_dict = {
    "Abou Kir Fertilizers": "ABUK",
    "Abu Dhabi Islamic Bank- Egypt": "ADIB",
    "Act Financial": "ACTF",
    "Al Khair River For Development Agricultural Investment&Envir": "KRDI",
    "Al Tawfeek Leasing Company-A.T.LEASE": "ATLC",
    "Alexandria Containers and goods": "ALCN",
    "Alexandria Flour Mills": "AFMC",
    "Alexandria Mineral Oils Company": "AMOC",
    "Amer Group Holding": "AMER",
    "Arab Developers Holding": "ARAB",
    "Arab Moltaka Investments Co": "AMIA",
    "Arabia for Investment and Development": "AIDC",
    "Arabia Investments Holding": "AIHC",
    "Arabian Cement Company": "ARCC",
    "ASEC Company For Mining - ASCOM": "ASCM",
    "Aspire Capital Holding For Financial Investments": "ASPI",
    "Beltone Holding": "BTFH",
    "Cairo Oils & Soap": "COSG",
    "Cairo Poultry": "POUL",
    "Canal Shipping Agencies": "CSAG",
    "Ceramic & Porcelain": "PRCL",
    "Commercial International Bank-Egypt (CIB)": "COMI",
    "Contact Financial Holding": "CNFN",
    "Credit Agricole Egypt": "CIEB",
    "Development & Engineering Consultants": "DAPH",
    "Dice Sport & Casual Wear": "DSCW",
    "Eastern Company": "EAST",
    "Edita Food Industries S.A.E": "EFID",
    "EFG Holding": "HRHO",
    "E-finance For Digital and Financial Investments": "EFIH",
    "Egypt Aluminum": "EGAL",
    "Egyptian Chemical Industries (Kima)": "EGCH",
    "Egyptian for Tourism Resorts": "EGTS",
    "Egyptian International Pharmaceuticals (EIPICO)": "PHAR",
    "Egyptian Media Production City": "MPRC",
    "Egyptian Transport (EGYTRANS)": "ETRS",
    "Egyptians Housing Development & Reconstruction": "EHDR",
    "El Ahli Investment and Development": "AFDI",
    "El Ezz Porcelain (Gemma)": "ECAP",
    "El Nasr Clothes & Textiles (Kabo)": "KABO",
    "El Obour Real Estate Investment": "OBRI",
    "El Shams Housing & Urbanization": "ELSH",
    "El-Nile Co. For Pharmaceuticals And Chemical Industries": "NIPH",
    "Elsaeed Contracting& Real Estate Investment Company SCCD": "UEGC",
    "ELSWEDY ELECTRIC": "SWDY",
    "Emaar Misr for Development": "EMFD",
    "Engineering Industries (ICON)": "ENGC",
    "Export Development Bank of Egypt": "EXPA",
    "Extracted Oils": "ZEOT",
    "Fawry For Banking Technology And Electronic Payment": "FWRY",
    "GB Corp": "GBCO",
    "Glaxo Smith Kline": "BIOC",
    "GPI For Urban Growth": "GPIM",
    "Heliopolis Housing": "HELI",
    "Housing & Development Bank": "HDBK",
    "Ibnsina Pharma": "ISPH",
    "Industrial & Engineering Projects": "IEEC",
    "International Agricultural Products": "IFAP",
    "International Company For Fertilizers & Chemicals": "ICFC",
    "Iron And Steel for Mines and Quarries": "ISMQ",
    "Ismailia Development and Real Estate Co": "IDRE",
    "Ismailia Misr Poultry": "ISMA",
    "Juhayna Food Industries": "JUFO",
    "Lecico Egypt": "LCSW",
    "Macro Group Pharmaceuticals -Macro Capital": "MCRO",
    "Madinet Masr For Housing and Development": "MASR",
    "Mansourah Poultry": "MPCO",
    "Medical Packaging Company": "MEPA",
    "Memphis Pharmaceuticals": "MPCI",
    "Misr Cement (Qena)": "MCQE",
    "Misr Fertilizers Production Company - Mopco": "MFPC",
    "Misr National Steel - Ataqa": "ATQA",
    "MM Group For Industry And International Trade": "MTIE",
    "Nasr Company for Civil Works": "NCCW",
    "O B  Financial Holding": "OFH",
    "Orascom Construction PLC": "ORAS",
    "Orascom Development Egypt": "ORHD",
    "Orascom Investment Holding": "OIH",
    "Oriental Weavers": "ORWE",
    "Palm Hills Development Company": "PHDC",
    "QALA For Financial Investments": "CCAP",
    "Raya Customer Experience": "RACC",
    "Raya Holding For Financial Investments": "RAYA",
    "Sabaa International Company for Pharmaceutical and Chemical": "SIPC",
    "Sharm Dreams Co. for Tourism Investment": "SDTI",
    "Sidi Kerir Petrochemicals - SIDPEC": "SKPC",
    "Sinai Cement": "SCEM",
    "Six of October Development & Investment (SODIC)": "OCDI",
    "South Valley Cement": "SVCE",
    "T M G Holding": "TMGH",
    "Taaleem Management Services": "TALM",
    "Tanmiya for Real Estate Investment": "TANM",
    "Taqa Arabia": "TAQA",
    "Telecom Egypt": "ETEL",
    "Tenth Of Ramadan Pharmaceutical Industries&Diagnostic-Rameda": "RMDA",
    "The Egyptian Modern Education Systems": "MOED",
    "U Consumer Finance": "VALU",
    "Universal For Paper and Packaging Materials (Unipack": "UNIP",
    "Valmore Holding": "VLMR",
    "Valmore Holding-EGP": "VLMRA",
    "Zahraa Maadi Investment & Development": "ZMID",
}

    def getEGXCompanies(self):
        return self.__egx30_companies_dict
    
    def getLastDailyPrice(self,ticker: str):
        response = get_OHLCV_data(ticker, "EGX", "Daily", 1)
        return float(response['close'].tolist()[0])

    def getLivePrice(self,ticker:str):
        today = self.parser.stringfyDates(datetime.today())
        response = get_EGX_intraday_data([ticker],"1 Minute",today, today)
        return float(response[ticker].tolist()[-1])

    def getPriceChange(self,todays_date:datetime,
                       beginning_date:datetime,
                       ticker:str):
        try:
            today = self.parser.stringfyDates(todays_date)
            initial_date = self.parser.stringfyDates(beginning_date)
            response = get_EGXdata([ticker],"Daily",initial_date,today)
            logger.info(type(response), response)
            return [float(x) for x in response[ticker].tolist()]
        except Exception as e:
            logger.error(f"Error fetching price change for {ticker}: {e}")
            return []

    def getIntraday(self,ticker,todays_date):
        today = self.parser.stringfyDates(todays_date)
        response = get_EGX_intraday_data([ticker],'1 Minute',today,today)
        return [float(x) for x in response[ticker].tolist()]

    # ToDo: Refactor the timing parameter to be more flexible and not hardcoded
    def getPeriodRisers(self,todays_date:datetime,beginning_date:datetime,NCompanies):
        return self.__getRisers(todays_date,beginning_date,get_EGXdata,'Daily',NCompanies)

    # ToDo: Refactor the timing parameter to be more flexible and not hardcoded
    def getIntradayRiser(self,todays_date:datetime,NCompanies:int = 5):
        return self.__getRisers(todays_date,todays_date,get_EGX_intraday_data,'1 Minute',NCompanies)

    def __getRisers(self,todays_date:datetime,end_date:datetime,func,timing,NCompanies):
        """
        ToDo: Fix issue: MCP error -32001: Request timed out when calling this function with get_EGXdata and a long time period. 
        Consider implementing pagination or batching to handle large data requests. 
        Also check for top gainers trackers APIs from egxpy or tvfeeds to avoid fetching unnecessary data for all companies 
        when only the top risers are needed.
        Args:
            todays_date (datetime): The current date for which to calculate the risers.
            end_date (datetime): The starting date for the period over which to calculate the risers.
            func (function): The function to fetch data, either get_EGXdata or get_EGX_intraday_data.
            timing (str): The timing parameter for the data fetch function, either 'Daily' or '1 Minute'.
            NCompanies (int): The number of top risers to return.
        """
        tickers = [ticker for ticker in self.__egx30_companies_dict.values()]
        today = self.parser.stringfyDates(todays_date)
        beginning = self.parser.stringfyDates(end_date)
        response = func(tickers,timing,beginning,today)
        deltas = {
            t: ((float(response[t].tolist()[-1]) - float(response[t].tolist()[0])) / float(response[t].tolist()[0])) * 100
            for t in response
            }
        topN = sorted(deltas, key=lambda t: deltas[t],reverse=True)[:NCompanies]
        return {ticker:[float(x) for x in response[ticker].tolist()] for ticker in topN}

        
