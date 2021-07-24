"""Service to generate a map displaying COVID-19 news around the world."""

import pandas as pd
import plotly.express as px
import re
import textwrap

from typing import List
from plotly.offline import plot

def format_text(dataframe: pd.DataFrame, column):
    article_text = dataframe[column]
    article_text = article_text.apply(lambda x: x[0:800] + "[...]" if len(x) > 800 else x)
    article_text = article_text.apply(
        lambda body: '<br>'.join(['<br>'.join(textwrap.wrap(line, 90,
                 break_long_words=False, replace_whitespace=False))
                 for line in body.splitlines() if line.strip() != ''])
    )
    return article_text
    
def format_date(dataframe,column):
    """
    Convert date to string and split with "/"
    (for example: 20201210 -> "2020/12/10")
    """
    dates = dataframe[column]
    dates = dates.apply( lambda y: (lambda x=str(y): x[0:4] + "/" + x[4:6] + "/" + x[6:8])())
    return dates

def format_location(dataframe,column):
    """
    keep only state and country (last 2)
    in order to remove redundancy found in some strings
    (for example: tehran, tehran, Iran -> tehran, Iran)
    """
    dates = dataframe[column]
    dates = dates.apply( lambda y: (lambda x=y.split(", "): ", ".join(x[-2:]))())
    return dates

def generate_map(dataframe: pd.DataFrame):
    """
    Function to generate map from Pandas dataframe.
    Args:
        dataframe: pd.DataFrame
    Returns:
        plotly_map:
    """
    dataframe = dataframe.dropna(subset=['GDELT.Actor1Geo_Fullname']).copy()
    dataframe['TEXT_FORMATTED'] = format_text(dataframe, 'ARTICLE.TEXT')
    dataframe['TITLE_FORMATTED'] = format_text(dataframe, 'ARTICLE.TITLE')
    dataframe['DATE_FORMATTED'] = format_date(dataframe, 'GDELT.Day')
    dataframe['LOCATION_FORMATTED'] = format_location(dataframe,'GDELT.Actor1Geo_Fullname')
    plotly_map = px.scatter_mapbox(
        dataframe,
        lat='GDELT.Actor1Geo_Lat',
        lon='GDELT.Actor1Geo_Long',
        hover_name='TITLE_FORMATTED',
        custom_data = ['GDELT.SOURCEURL','DATE_FORMATTED','LOCATION_FORMATTED','TEXT_FORMATTED'],
        color_discrete_sequence=px.colors.sequential.Peach_r,
        zoom=1,
        height=750,
    )

    plotly_map.update_layout(mapbox_style='open-street-map')
    plotly_map.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    plotly_map = add_hyperlinks(plotly_map)
    
    dataframe = dataframe.drop(['TEXT_FORMATTED','TITLE_FORMATTED'], axis = 1);

    return plotly_map

def add_hyperlinks(plotly_map):
    # Get HTML representation of plotly.js and this figure

    fig = plotly_map
    fig = fig.update_layout(
            hoverlabel=dict(
                bgcolor="white",
                font_size=16,
                font_family="Rockwell"
            )
        )
    fig = fig.update_traces(hovertemplate='<b>%{hovertext}</b> <br>%{customdata[2]} (%{customdata[1]}) <br><br>%{customdata[3]}') #

    plot_div = plot(fig, output_type='div', include_plotlyjs=True)

    # Get id of html div element that looks like
    # <div id="301d22ab-bfba-4621-8f5d-dc4fd855bb33" ... >
    res = re.search('<div id="([^"]*)"', plot_div)
    div_id = res.groups()[0]

    # Build JavaScript callback for handling clicks
    # and opening the URL in the trace's customdata
    js_callback = """
    <script>
    var plot_element = document.getElementById("{div_id}");
    plot_element.on('plotly_click', function(data){{
        console.log(data);
        var point = data.points[0];
        if (point) {{
            url = point.customdata[0]
            console.log(point);
            window.open(url);
        }}
    }})
    </script>
    """.format(div_id=div_id)

    # Build HTML string
    html_str = """
    <html>
    <body>
    <h1> Coronavirus News Map </h1>
    {plot_div}
    {js_callback}
    </body>
    </html>
    """.format(plot_div=plot_div, js_callback=js_callback)

    return html_str
