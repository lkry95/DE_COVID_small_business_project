from sqlalchemy import create_engine
import pandas as pd
import os

def update_data():

    mysql_connection = os.environ.get("group_sql_ZCW")

    #Connect to shared MySQL db
    engine = create_engine(mysql_connection)
    con = engine.connect()
    df = pd.read_sql('covid_cases_temp', con)

    #Finds records from most recent dates
    df['Date'] = pd.to_datetime(df['Date'])
    recent_date = df['Date'].max()
    new = df.loc[df['Date'] == recent_date]

    #only selects zipcode and value column from new dataframe
    df1 = new[['Zipcode', 'Value']]

    #writes data to csv
    df1.to_csv('covid_nums.csv')