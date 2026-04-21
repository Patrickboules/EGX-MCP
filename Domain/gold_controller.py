import requests
from bs4 import BeautifulSoup

class GoldController:
    __headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Referer': 'https://gold-era.eg/'
    }

    def getCurrentGoldPrices(self):
        url = "https://gold-era.eg/gold-price/"
        response = requests.get(url, headers=self.__headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')  
        rows = table.find('tbody').find_all('tr')
        gold_price = []

        for i in range(0,5):
            cols = rows[i].find_all('td')
            if len(cols) == 3:
                karat = cols[0].text.strip()
                sell = cols[1].text.strip().replace(',', '')
                buy = cols[2].text.strip().replace(',', '')
                gold_price.append(
                    {
                    'karat':karat,
                    'sell': int(sell.replace("£","")),
                    'buy': int(buy.replace("£","")) 
                    })
                
        return gold_price
    
