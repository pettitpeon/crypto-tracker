from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

ids = ['ethereum', 'matic-network', 'polkadot', 'dogsofelon']
print(cg.get_coins_markets('usd', ids=','.join(ids)))

# for id in ids:
    # coin = cg.get_coin_by_id(id)
    # print(coin['market_data']['current_price']['usd'])
    

# sentence = ['this', 'is', 'a', 'sentence']
# print(','.join(sentence))