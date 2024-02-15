from bs4 import BeautifulSoup
import requests
import pandas as pd


class projectQueue:
    def __init__(self) -> None:
        self.url = 'https://irtt.iso-ne.com/reports/external'

    def getETUTable(self):
        r = requests.get(self.url,verify=False)
        soup = BeautifulSoup(r.text,features='html5lib')
        table = soup.find('table')

        headers = []
        for i in table.find_all('th'):
            headers.append(i.text)

        df = pd.DataFrame(columns=headers)
        for j in table.find_all('tr')[1:]:
            row_data = j.find_all('td')
            df.loc[len(df)] = [i.text for i in row_data]   

        for header in headers:
            df[header] = df[header].fillna(0) 
        
        # REMOVING THE SIS DUPLICATE COLUMN
        df = df.loc[:,~df.columns.duplicated()]

        return df

        
