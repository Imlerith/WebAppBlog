import json
import os
from glob import glob

import pandas as pd
import plotly
import plotly.graph_objects as go
from flask import current_app
from plotly.subplots import make_subplots


def create_sentiment_index_plot(filename):

    data_path = os.path.join(current_app.root_path, current_app.config['FILES_FOLDER'])
    ticker = filename.split('_')[0]
    ticker_upper = ticker.upper()
    sent_price_df = pd.read_csv(os.path.join(data_path, filename))

    # ----- create the figure object
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # ----- add traces
    fig.add_trace(
        go.Scatter(x=sent_price_df['date'], y=sent_price_df['sentiment_classfn'], name=f"{ticker_upper} Sentiment"),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=sent_price_df['date'], y=sent_price_df[ticker + '_price'], name=f"{ticker_upper} Price"),
        secondary_y=True,
    )

    # # ----- add figure title
    # fig.update_layout(
    #     title_text=f"Sentiment Index and {ticker_upper} Price"
    # )

    # # ----- set x-axis title
    # fig.update_xaxes(title_text="Date")

    # ----- set y-axes titles
    fig.update_yaxes(title_text=f"<b>{ticker_upper} Sentiment Index</b>", color='#636EFA', secondary_y=False)
    fig.update_yaxes(title_text=f"<b>{ticker_upper} Price</b>", color='#EF553B', secondary_y=True)

    # ----- add rangeslider
    fig.update_xaxes(rangeslider_visible=True)

    # ----- legend position
    fig.update_layout(showlegend=False, margin=dict(l=10, r=10, t=30, b=30))
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graph_json, ticker_upper


def create_msgs_vols_mkt_caps_plot():
    data_path = os.path.join(current_app.root_path, current_app.config['FILES_FOLDER'])
    crypto_files = glob(data_path + "*_price.csv")

    # --- get mapping between tickers and crypto files
    ticker_fname_map = pd.DataFrame.from_records([(x.split('/')[-1].split('_')[0].upper(),
                                                   x.split('/')[-1]) for x in crypto_files])
    ticker_fname_map.columns = ['symbol', 'filename']
    ticker_fname_map['symbol'] = ticker_fname_map['symbol'] + '.X'

    # --- get cryptos' messages', mkt caps' stats, ranked filenames (criterion=msgs' volume)
    top_cryptos = pd.read_csv(data_path + 'top_5_cryptos_df.csv')
    top_cryptos.columns = ['symbol', 'msgs_volume']
    cryptos_infos_path = data_path + 'filtered_cryptos_infos.json'
    with open(cryptos_infos_path, "r", encoding="utf-8") as f:
        cryptos_infos = json.load(f)
    top_cryptos_infos = [(x['symbol_name'], x['mkt_cap'], x['title']) for x in cryptos_infos if x['symbol_name']
                         in top_cryptos['symbol'].values]
    top_cryptos_infos_df = pd.DataFrame.from_records(top_cryptos_infos, columns=['symbol', 'mkt_cap', 'name'])
    top_cryptos_all = top_cryptos.set_index('symbol').join(top_cryptos_infos_df.set_index('symbol'))\
        .join(ticker_fname_map.set_index('symbol')).reset_index()
    filenames = top_cryptos_all['filename'].values.tolist()
    cryptonames = top_cryptos_all['name'].values.tolist()

    # --- create the interactive figure
    fig = go.Figure()
    fig.add_trace(go.Bar(x=top_cryptos_all['symbol'], y=top_cryptos_all['msgs_volume'],
                         name="Messages' Volume", visible=True))
    fig.add_trace(go.Bar(x=top_cryptos_all['symbol'], y=top_cryptos_all['mkt_cap'],
                         name="Market Cap", visible=False))
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=0.7,
                y=1.2,
                showactive=True,
                buttons=list(
                    [
                        dict(
                            label="<b>Messages' Volume</b>",
                            method="update",
                            args=[{"x": [top_cryptos_all['symbol']], "y": [top_cryptos_all['msgs_volume']],
                                   'marker.color': '#636EFA', 'visible': [True, False]}],
                        ),
                        dict(
                            label="<b>Market Cap</b>",
                            method="update",
                            args=[{"x": [top_cryptos_all.sort_values(by='mkt_cap', ascending=False)['symbol']],
                                   "y": [top_cryptos_all.sort_values(by='mkt_cap', ascending=False)['mkt_cap']],
                                   'marker.color': '#EF553B', 'visible': [False, True]}],
                        ),
                    ]
                ),
            )
        ],
        font=dict(
            size=16,
        ),
        hoverlabel=dict(namelength=-1)
    )

    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graph_json, filenames, cryptonames
