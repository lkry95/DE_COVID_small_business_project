import folium
import os
import json
import csv
from sqlalchemy import create_engine
import pandas as pd
from datetime import date, timedelta, datetime


def make_map():
    engine = create_engine(
        'mysql://group1:ZCW+G1+data1-2@ls-981afae8457656b0e311a4599e509521975ea3c7.c13c4sg7cvg0.us-east-2.rds.amazonaws.com/group1')
    con = engine.connect()
    df = pd.read_sql('covid_cases', con)

    #Finds most recent covid case rates
    df['Date'] = pd.to_datetime(df['Date'])
    recent_date = df['Date'].max()
    new = df.loc[df['Date'] == recent_date]
    current_cases = new[['Zipcode', 'Value']]

    #Finds yesterday's covid case rates
    yesterday_data = date.today() - timedelta(days=2)
    yesterday = yesterday_data.strftime('%Y%m%d')
    yesterday_date = datetime.strptime(yesterday, '%Y%m%d')
    yes_case = df.loc[(df['Date'] == yesterday_date)]
    yesterday_cases = yes_case[['Zipcode', 'Value']]



    zipcodes = os.path.join("/Users/luke/Final_Project_2/data/de_delaware_zip_codes_geo.min.json")
    #covid_data = os.path.join("/Users/luke/Final_Project_2/DE_COVID_small_business_project/covid_nums.csv")


    m = folium.Map(location = [39.1582,-75.5244], zoom_start=9)

    folium.Choropleth(
        geo_data = zipcodes,
        name = 'Current Cases',
        data = current_cases,
        columns = ['Zipcode','Value'],
        key_on = "properties.ZCTA5CE10",
        fill_color = 'YlOrRd',
        fill_opacity = 0.7,
        line_opacity = 0.3,
        legend_name = "Covid Cases (per 100,000 people)"
    ).add_to(m)

    # folium.Choropleth(
    #     geo_data=zipcodes,
    #     name="Yesterday's Cases",
    #     data= yesterday_cases,
    #     columns=['Zipcode', 'Value'],
    #     key_on="properties.ZCTA5CE10",
    #     fill_color='YlOrRd',
    #     fill_opacity=0.9,
    #     line_opacity=0.3,
    #     legend_name="Covid Cases (per 100,000 people)"
    # ).add_to(m)

    tooltip = 'Click for More Info'

    file_path = '/Users/luke/Final_Project_2/data/markers.json'
    with open(file_path, 'r') as f:
        zipcode_central = json.load(f)

    covid_cases = {}
    file = csv.reader(open('/Users/luke/Final_Project_2/covid_nums.csv'), delimiter=',')
    for line in file:
        covid_cases[line[1]] = line[2]



    # count = 0
    #Creates all markers
    for key, item in zipcode_central.items():
        zipcode_cases = 0
        if key in covid_cases:
            zipcode_cases = covid_cases[key]

        folium.Marker(location=item,
                      #pops up when clicked
                      popup = folium.Popup(
                          (f'<strong>Zip Code:</strong> {key}<br>'
                           f'<strong>Number of Reported Cases per 100,000:</strong> {zipcode_cases}'),
                          max_width=300,min_width=300),
                      #hover over it says "message"
                      tooltip=tooltip).add_to(m)




    folium.LayerControl().add_to(m)
    m.save('map.html')

make_map()