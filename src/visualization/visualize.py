import os
sys_path = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import sys
sys.path.append(sys_path)
import plotly.graph_objects as go
import plotly.express as px

from dash import Dash, dcc, html, Output, Input, State, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

#import from data piplines
from src.data.make_dataset import *

#visualization with a candlestick plot, Open, high, low and close prices
def candlestick_plot(data_frame,
                     open_col, high_col, low_col, close_col,
                     title = 'Gold',
                     start_date = start_date, end_date = end_date,
                     yaxis = 'Gold', yaxis_currency = 'USD'):
    fig = go.Figure(data = [go.Candlestick(x = data_frame.index,
                                               open = data_frame[open_col],
                                               high = data_frame[high_col],
                                               low = data_frame[low_col],
                                               close = data_frame[close_col])])
    fig.update_layout(title = 'Candlestick Plot of {0} Price from {1} to {2}.'
                        .format(title, start_date, end_date), xaxis_rangeslider_visible = False)

    #interactive visualization w/ plotly
    fig.update_xaxes(
        rangeslider_visible = True,
        rangeselector = dict(
            buttons = list([
                dict(count = 1, label = '1m', step = 'month', stepmode = 'backward'),
                dict(count = 3, label = '3m', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6m', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = '1y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')
            ])
        )
    )

    fig.update_layout(yaxis = dict(title = '{0} [{1}/oz]'.format(yaxis, yaxis_currency)))

    return fig

#visualization with a Time Series plot
def time_series_plot(data_frame, y_axis,
                     title = 'Gold',
                     start_date = start_date, end_date = end_date,
                     yaxis = 'Gold', yaxis_unit = 'USD/oz'):
    fig = px.line(data_frame, x = data_frame.index, y = data_frame[y_axis])

    fig.update_layout(title = 'Time Series Analysis of {0} from {1} to {2}.'
                      .format(title, start_date, end_date), xaxis_rangeslider_visible = False)

    #interactive visualization w/ plotly
    fig.update_xaxes(
       rangeslider_visible = True,
       rangeselector = dict(
           buttons = list([
               dict(count = 1, label = '1m', step = 'month', stepmode = 'backward'),
                dict(count = 3, label = '3m', step = 'month', stepmode = 'backward'),
                dict(count = 6, label = '6m', step = 'month', stepmode = 'backward'),
                dict(count = 1, label = '1y', step = 'year', stepmode = 'backward'),
                dict(step = 'all')
                           ])
                           )
                   )

    fig.update_layout(yaxis = dict(title = '{0} [{1}]'
                                   .format(yaxis, yaxis_unit)))

    return fig

#create dashboard w/ Dash
#create components
app = Dash(__name__, external_stylesheets = [dbc.themes.SOLAR])

#1st row components
title = dcc.Markdown(children = '# Gold & Silver Dashboard')

#2nd row components
investment_vehicle = dcc.RadioItems(['Gold', 'Silver'], 'Gold')
au_ag_usd_data_selection = dcc.RadioItems(['SPOT', 'LBMA'], 'SPOT')
au_ag_usd_plot_selection = dcc.RadioItems(['Candlestick [only SPOT]', 'Time Series'],
                                          'Candlestick [only SPOT]') 
#3rd row components
#gold/silver ratio component
#initial gold/silver ratio plot
au_ag_ratio = time_series_plot(yf_df, 'Gold/Silver_Ratio', title = 'Au/Ag Ratio',
                               start_date = start_date, end_date = end_date, yaxis = 'Gold/Silver Ratio',
                               yaxis_unit = '-')
au_ag_ratio = dcc.Graph(figure = au_ag_ratio)

#gold or silver candlestick or time series plots from SPOT/ LBMA
#initial gold candlestick plot [USD/oz] - SPOT
initial_au_usd = candlestick_plot(yf_df,
                     'Open_Gold', 'High_Gold', 'Low_Gold', 'Close_Gold',
                     title = 'Gold - SPOT',
                     start_date = start_date, end_date = end_date,
                     yaxis = 'Gold', yaxis_currency = 'USD')
au_ag_usd = dcc.Graph(figure = initial_au_usd)

#4th row components
au_ag_ratio_latest_val = html.Div('Latest value: {0} from {1}'
                                  .format(round(yf_df['Gold/Silver_Ratio'][-1],2),
                                          yf_df.index[-1].strftime("%Y-%m-%d")))
spot_lbma_latest_val = html.Div('Latest value: {0} USD from {1}'
                                                .format(round(yf_df['Close_Gold'][-1],2),
                                                        yf_df.index[-1].strftime("%Y-%m-%d")))
#5th row components
#initail USD/PLN exchange rate plot
usd_pln = time_series_plot(nbp_exchange_rates, 'Average Exchange Rate of USD', title = 'USD/PLN',
                           start_date = nbp_start_date, end_date = end_date, yaxis = 'USD/PLN',
                           yaxis_unit = 'PLN')
usd_pln = dcc.Graph(figure = usd_pln)

#initial gold plot [PLN/oz] - NBP
au_pln = time_series_plot(nbp_gold_price, 'NBP Gold Price [PLN/oz]', title = 'Gold - NBP',
                          yaxis = 'NBP Gold Price', yaxis_unit = 'PLN/oz')
au_pln = dcc.Graph(figure = au_pln)
#6th row components
usd_pln_latest_val = html.Div('Latest value: {0} PLN from {1}'
                              .format(round(nbp_exchange_rates['Average Exchange Rate of USD'][-1],2),
                                      nbp_exchange_rates.index[-1]))
au_pln_latest_val = html.Div('Latest value: {0} PLN from {1}'
                                .format(round(nbp_gold_price['NBP Gold Price [PLN/oz]'][-1],2),
                                        nbp_gold_price.index[-1]))

#create layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([title], width = 12,
               style = {'display':'flex', 'flex-direction':'column', 'align-items':'center'}),
    ]),
    dbc.Row([
        dbc.Col([], width = 6),
        dbc.Col([investment_vehicle], width = 1,
               style = {'display':'flex', 'flex-direction':'column', 'align-items':'flex-start'}),
        dbc.Col([au_ag_usd_data_selection], width = 1,
               style = {'display':'flex', 'flex-direction':'column', 'align-items':'flex-start'}),
        dbc.Col([au_ag_usd_plot_selection], width = 4,
                style = {'display':'flex', 'flex-direction':'column', 'align-items':'center'})
    ]),
    dbc.Row([
        dbc.Col([au_ag_ratio], width = 6,
               style = {'display':'flex', 'flex-direction':'column', 'align-items':'center'}),
        dbc.Col([au_ag_usd], width = 6,
               style = {'display':'flex', 'flex-direction':'column', 'align-items':'center'})
    ]),
    dbc.Row([
        dbc.Col([au_ag_ratio_latest_val], width = 6,
               style = {'whiteSpace': 'nowrap', 'overflow': 'hidden', 'textOverflow': 'ellipsis',
                       'text-align': 'center'}),
         dbc.Col([spot_lbma_latest_val], width = 6,
                 style = {'whiteSpace': 'nowrap', 'overflow': 'hidden', 'textOverflow': 'ellipsis',
                          'text-align': 'center'})  
    ]),
    dbc.Row([
        dbc.Col([usd_pln], width = 6,
               style = {'display':'flex', 'flex-direction':'column', 'align-items':'center'}),
        dbc.Col([au_pln], width = 6,
                style = {'display':'flex', 'flex-direction':'column', 'align-items':'center'})
    ]),
    dbc.Row([
        dbc.Col([usd_pln_latest_val], width = 6,
               style = {'whiteSpace': 'nowrap', 'overflow': 'hidden', 'textOverflow': 'ellipsis',
                       'text-align': 'center'}),
         dbc.Col([au_pln_latest_val], width = 6,
                 style = {'whiteSpace': 'nowrap', 'overflow': 'hidden', 'textOverflow': 'ellipsis',
                          'text-align': 'center'})  
    ])           
])

@app.callback(
    [Output(au_ag_usd, component_property = 'figure', ),
    Output(au_ag_usd_plot_selection, component_property = 'value'),
    Output(spot_lbma_latest_val, component_property = 'children')],

    [Input(investment_vehicle, component_property = 'value'),
    Input(au_ag_usd_data_selection, component_property = 'value'),
    Input(au_ag_usd_plot_selection, component_property = 'value')]
)

def plots_func(investment_vehicle, au_ag_usd_data_selection, au_ag_usd_plot_selection):
      
    #Gold/ silver in USD interaction code
    if investment_vehicle == 'Gold':
        if au_ag_usd_data_selection == 'SPOT':
            if au_ag_usd_plot_selection == 'Candlestick [only SPOT]':
                au_ag_usd = candlestick_plot(yf_df,
                                                 'Open_Gold', 'High_Gold', 'Low_Gold', 'Close_Gold',
                                                 title = 'Gold - SPOT',
                                                 start_date = start_date, end_date = end_date,
                                                 yaxis = 'Gold', yaxis_currency = 'USD')
                spot_lbma_latest_val = html.Div('Latest value: {0} USD from {1}'
                                                .format(round(yf_df['Close_Gold'][-1],2),
                                                        yf_df.index[-1].strftime("%Y-%m-%d")))
            elif au_ag_usd_plot_selection == 'Time Series':
                au_ag_usd = time_series_plot(yf_df, 'Close_Gold',
                                                 title = 'Gold - SPOT',
                                                 start_date = start_date, end_date = end_date,
                                                 yaxis = 'Gold', yaxis_unit = 'USD/oz')
                spot_lbma_latest_val = html.Div('Latest value: {0} USD from {1}'
                                                .format(round(yf_df['Close_Gold'][-1],2),
                                                        yf_df.index[-1].strftime("%Y-%m-%d")))
        elif au_ag_usd_data_selection == 'LBMA':
            au_ag_usd = time_series_plot(lbma_df, 'LBMA/GOLD - USD (PM)',
                                             title = 'Gold - LBMA (pm)',
                                             start_date = start_date, end_date = end_date,
                                             yaxis = 'Gold', yaxis_unit = 'USD/oz')
            au_ag_usd_plot_selection = 'Time Series'
            spot_lbma_latest_val = html.Div('Latest value: {0} USD from {1}'
                                                .format(round(lbma_df['LBMA/GOLD - USD (PM)'][-1],2),
                                                        lbma_df.index[-1].strftime("%Y-%m-%d")))
    elif investment_vehicle == 'Silver':
        if au_ag_usd_data_selection == 'SPOT':
            if au_ag_usd_plot_selection == 'Candlestick [only SPOT]':
                au_ag_usd = candlestick_plot(yf_df,
                                                 'Open_Silver', 'High_Silver', 'Low_Silver',
                                                 'Close_Silver',
                                                 title = 'Silver - SPOT',
                                                 start_date = start_date, end_date = end_date,
                                                 yaxis = 'Silver', yaxis_currency = 'USD')
                spot_lbma_latest_val = html.Div('Latest value: {0} USD from {1}'
                                                .format(round(yf_df['Close_Silver'][-1],2),
                                                        yf_df.index[-1].strftime("%Y-%m-%d")))
            elif au_ag_usd_plot_selection == 'Time Series':
                au_ag_usd = time_series_plot(yf_df, 'Close_Silver',
                                                 title = 'Silver - SPOT',
                                                 start_date = start_date, end_date = end_date,
                                                 yaxis = 'Silver', yaxis_unit = 'USD/oz')
                spot_lbma_latest_val = html.Div('Latest value: {0} USD from {1}'
                                                .format(round(yf_df['Close_Silver'][-1],2),
                                                        yf_df.index[-1].strftime("%Y-%m-%d")))
        elif au_ag_usd_data_selection == 'LBMA':
            au_ag_usd = time_series_plot(lbma_df, 'LBMA/SILVER - USD',
                                             title = 'Silver - LBMA',
                                             start_date = start_date, end_date = end_date,
                                             yaxis = 'Silver', yaxis_unit = 'USD/oz')
            au_ag_usd_plot_selection = 'Time Series'
            spot_lbma_latest_val = html.Div('Latest value: {0} USD from {1}'
                                                .format(round(lbma_df['LBMA/SILVER - USD'][-1],2),
                                                        lbma_df.index[-1].strftime("%Y-%m-%d")))
    
    return au_ag_usd, au_ag_usd_plot_selection, spot_lbma_latest_val

if __name__ == '__main__':
    app.run_server(debug = False, host='0.0.0.0', port = 8050)