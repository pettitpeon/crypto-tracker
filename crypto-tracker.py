import streamlit as st
# import requests, json
# from web3 import Web3
import pandas as pd
from pycoingecko import CoinGeckoAPI
# from IPython.core.display import HTML
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns

def get_coins():
    cg = CoinGeckoAPI()
    
    ids = ['ethereum','cardano','polkadot','matic-network','chainlink','uniswap','axie-infinity','aave','immutable-x','illuvium','dogsofelon']
    return cg.get_coins_markets('usd', ids=','.join(ids))

def get_details(coin):
    # market_cap_rank, name, symbol, current_price, price_change_percentage_24h, ath, ath_change_percentage
    c = coin
    return [c['market_cap_rank'], c['name'], c['symbol'], c['current_price'], c['price_change_percentage_24h'],
            c['ath'], c['ath_change_percentage']]

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    return f'<a target="_blank" href="{link}">{link}</a>'

def create_dataframe(coins):
    event_list = []
    for coin in coins:
        event_list.append(get_details(coin))

    df = pd.DataFrame(event_list, columns=['Rank', 'Name', 'Ticker', 'usd', '24h', 'ATH', 'ATH Change'])
    df['Ticker'] = df['Ticker'].apply(lambda s: s.upper())
    # df['usd'] = df['usd'].map('$ {:,.2f}'.format)
    # df['24h'] = df['24h'].map('{:,.2f}%'.format)
    # df['ATH'] = df['ATH'].map('$ {:,.2f}'.format)
    # df['ATH Change'] = df['ATH Change'].map('{:,.2f}%'.format)
    # df['Name'] = df['Name'].apply(make_clickable)

    return df

# link is the column with hyperlinks

st.sidebar.header("Endpoints")
endpoint_choices = ['Assets']
endpoint = st.sidebar.selectbox("Choose an Endpoint", endpoint_choices)

st.title(f"Crypto tracker - {endpoint}")

def background_grad(s, m=None, M=None, cmap='RdBu', low=0, high=0):
    if m is None:
        m = s.min().min()
    if M is None:
        M = s.max().max()
    rng = M - m
    norm = colors.Normalize(m ,M)
    normed = s.apply(lambda x: norm(x.values))
    cm = plt.cm.get_cmap(cmap)
    c = normed.applymap(lambda x: colors.rgb2hex(cm(x)))
    ret = c.applymap(lambda x: 'background-color: %s' % x)
    return ret

if endpoint == 'Assets':
    st.sidebar.header(endpoint)
    owner = st.sidebar.text_input("Owner")
    collection = st.sidebar.text_input("Collection")
    st.subheader("My Favorite")

    coins = get_coins()
    df = create_dataframe(coins)
    # df = df.to_html(escape=False)
    # st.write(df, unsafe_allow_html=True)

    cm = sns.light_palette("green", as_cmap=True)
    # df.style.background_gradient(cmap = cm)


    min_max_24h = max(max(abs(df['24h'])).real, 10)
    min_max_ath = max(max(abs(df['ATH Change'])).real, 200)
    st.dataframe(df.style
        .background_gradient(cmap = colors.LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256), vmin=-min_max_24h, vmax=min_max_24h, subset=['24h'])
        .background_gradient(cmap = colors.LinearSegmentedColormap.from_list('rg',["r", "w", "g"], N=256), vmin=-min_max_ath, vmax=min_max_ath, subset=['ATH Change'])
        .format(formatter={
            ('usd'): "$ {}",
            ('ATH'): "$ {}",
            ('24h'): "{:.2f}%",
            ('ATH Change'): "{:.2f}%",
            })
            ,
             height=1000)


    st.write(coins)

