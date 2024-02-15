import streamlit as st
import pandas as pd
import altair as alt
import data
import text # Module to store the general text data
import datetime

class App:
    def __init__(self) -> None:
        st.set_page_config(layout='wide',page_icon=':bar_chart:',page_title='IsoNE Interconnection Queue') # MUST BE FIRST
        st.title(':bar_chart: ISO NE Interconnection Queue')
        st.write(text.GENERAL_DESCRIPTION)
        #------------------------------------------------------------------------------- 
        # Caching the dataframe to prevent the app from re-running the script more than once
        @st.cache_data
        def getData():
            df = data.dataAnalysis().getAllData()
            table1 = data.dataAnalysis().getTable1()
            table2 = data.dataAnalysis().getTable2()
            return df,table1,table2
        
        self.df,self.table1,self.table2 = getData()
        #-------------------------------------------------------------------------------
        # Adding a download button
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')

        csv = convert_df(self.df)
        self.sidebar(csv)
        self.tab1, self.tab2, self.tab3 = st.tabs(['Main Data','ETU Info','Gen Info'])
        self.mainDataTab()
        self.ETUTab()
        self.GenTab()

    def sidebar(self,csv):
        st.sidebar.write("### Downloading data")
        st.sidebar.write("Press the button below to download the main dataframe scraped from the website.")
        st.sidebar.download_button(
            "Download",
            csv,
            "file.csv",
            "text/csv",
            key='download-csv'
        )

    #-------------------------------------------------------------------------------.
    # Main Data Tab
    def mainDataTab(self):
        df = self.df
        rawBtn = self.tab1.checkbox(label='Click me to show all raw data')
        if rawBtn:
            self.tab1.dataframe(df,use_container_width=True,hide_index=True)

        col1,col2 = self.tab1.columns(2)
        date = col1.date_input('Requested Date (will filter anything after this date)',value=datetime.date(1999,1,1),max_value=datetime.date(year=2050,month=12,day=31))
        state = col2.multiselect('Select State (can select multiple)',df['ST'].unique())
        eversource = self.tab1.checkbox('Check me to filter only look for Eversource in POI')


        # Updating requested value to new datetime object
        df['Requested'] = pd.to_datetime(df['Requested']).dt.date
    
        if len(state) == 0:
            tmp_df = df[df['Requested'] >= date]
        else:
           tmp_df = df[df["ST"].isin(state)]

        if eversource:
            tmp_df = tmp_df[tmp_df['POI'].str.contains('Eversource')]

        self.tab1.dataframe(tmp_df,use_container_width=True,hide_index=True)

    #-------------------------------------------------------------------------------.
    # ETU Info Tab
    def ETUTab(self):
        df = self.table1                # Saving the dataframe to make it easier to reference

        # Main Description for the tab----------------------------------------------------------
        self.tab2.write(text.TABLE1_DESCRIPTION)
        # Showing the data if the checkbox is checked----------------------------------------------------------
        t2_chk = self.tab2.checkbox('Click to show Data Table')
        if t2_chk:
            self.tab2.dataframe(df,use_container_width=True,hide_index=True)       

        # CREATING A PIE CHART ----------------------------------------------------------
        # Below is filtering the data to create a dataframe to hold only the unique 
            # zones along with the counted number
        zones = list(pd.unique(df['Zone']))
        zone_count = []
        for zone in zones:
            tmp = df[df['Zone'] == zone]
            zone_count.append(tmp['Zone'].count())

        plot_df = pd.DataFrame(columns=['value','count'])
        for val in range(len(zones)):
            plot_df.loc[len(plot_df)] = [zones[val],zone_count[val]]

        c = (alt.Chart(plot_df).mark_arc(innerRadius=50).encode(
               color="value", theta="count")
        )
        self.tab2.altair_chart(c,use_container_width=True)

        # Selectable filter for the dataframe----------------------------------------------------------
        self.tab2.divider()
        filter = self.tab2.selectbox('Zone Select',options=pd.unique(df['Zone']))
        filtered_df = df[df['Zone'] == filter]
        self.tab2.dataframe(filtered_df,use_container_width=True,hide_index=True)
    
    #-------------------------------------------------------------------------------.
    # Gen Info Tab
    def GenTab(self):
        df = self.table2
        self.tab3.write(text.TABLE2_DESCRIPTION)
        t3_chk = self.tab3.checkbox('Check me to see data table')
        if t3_chk:
            self.tab3.dataframe(df,use_container_width=True,hide_index=True)

        chrt_zone = pd.DataFrame(columns=['Zone','count'])
        zones = list(df['Zone'].unique())
        for zone in zones:
            if zone != None:
                chrt_zone.loc[len(chrt_zone)] = [zone,len(df[df['Zone']==zone])]

        c = (alt.Chart(chrt_zone).mark_arc(innerRadius=50).encode(
               color="Zone", theta="count")
        )
        self.tab3.altair_chart(c,use_container_width=True)

        self.tab3.divider()

        col1, col2 = self.tab3.columns(2)
        zone_filter = col1.selectbox('Zone Filter',df['Zone'].unique())
        cnt = df[df['Zone'] == zone_filter]
        col2.metric(f'Number of values for zone {zone_filter}',cnt['Zone'].count())

        self.tab3.dataframe(df[df['Zone'] == zone_filter],use_container_width=True,hide_index=True)

if __name__ == '__main__':
    App()

