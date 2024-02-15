import getProjectQueue 
import pandas as pd
import warnings

class dataAnalysis:
    def __init__(self) -> None:
        self.project = getProjectQueue.projectQueue()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.table = self.project.getETUTable()

    def getAllData(self):
        return self.table

    def getTable1(self):
        """
        Method to transform the data into an ETU table
        """
        df = self.table
        new_df = df[(df['Type'] == 'ETU') & (df['W/D Date']=='')]
        new_df = new_df.replace(r'', None)
        return new_df

    def getTable2(self):
        df = self.table
        new_df = df[(df['Type'] == 'G') & (df['Unit'] == 'WT') & (df['W/D Date']=='')]
        new_df = new_df.replace(r'', None)
        return new_df




    




