from math import nan
from binance_api import Binance
import time
import indicator
class BOT_Library ():

    bot = Binance('test','test')
    free_agent = Binance('1','1')

    def currency_settings(coin):
        info = BOT_Library.bot.exchangeInfo()
        info_symbols = info['symbols']
        currency_info = []
        for i in info_symbols:
            if i["symbol"] == coin+'USDT':
                currency_info.append(int(i['quotePrecision']))
                for j in i['filters']:
                    if j['filterType'] == 'LOT_SIZE':
                        currency_info.append(float(j['stepSize']))
        return currency_info

    def Traling_stop (traling_coefficient,coin):
        first_price = round(float(BOT_Library.bot.tickerPrice(symbol=coin+'USDT')['price']),6)
        first_stop_price = round(first_price * (1+traling_coefficient*0.01),6)
        print (f'{first_price =}, {first_stop_price =}')
        while True:
            time.sleep(5)
            print ('трейлинг работает')
            current_price = round(float(BOT_Library.bot.tickerPrice(symbol=coin+'USDT')['price']),6)
            if traling_coefficient > 0:
                if current_price >= first_stop_price:
                    return True
                    break
                else:
                    new_stop_price = round(current_price * (1+traling_coefficient*0.01),6)
                    if new_stop_price < first_stop_price:
                        first_stop_price = new_stop_price
                    else:
                        pass
            else:
                if current_price <= first_stop_price:
                    return True
                    break
                else:
                    new_stop_price = round(current_price * (1+traling_coefficient*0.01),6)
                    if new_stop_price > first_stop_price:
                        first_stop_price = new_stop_price
                    else:
                        pass

    def Signal_rsi (coin,frame):
        try:
            candle = BOT_Library.bot.klines(
                symbol=coin+'USDT',
                interval=frame,
                limit=1000)
            closes = [float(x[4]) for x in candle]
            rsi = indicator.RSI(closes, 14)
            if rsi[-1] > 80:
                return 'short'
            elif rsi[-1] < 20:
                return 'long'
            else:
                return False
        except Exception:
            return BOT_Library.Signal_rsi(coin,frame)

    def close_position(user_dict,coin,step,precision, isIsolated = False):
        try:
            for user in user_dict:
                position = 0
                user_agent = Binance(API_KEY = user_dict[user][0], API_SECRET = user_dict[user][1])
                if isIsolated == True:
                    balance = user_agent.magrinIsolatedAccount(
                        recWindow = 59999,
                        symbols = coin+'USDT'
                    )
                    position = float(balance['assets'][0]['baseAsset']['netAsset'])
                else:
                    balance = user_agent.marginAccount()
                    for token in balance['userAssets']:
                        if token['asset'] == coin:
                            position = float(token['netAsset'])
                if abs(position)*float(BOT_Library.bot.tickerPrice(symbol=coin+'USDT')['price']) < 11:
                    pass
                if position < 0:
                    user_agent.marginCreateOrder(
                                                symbol = coin+'USDT',
                                                side = "BUY",
                                                type = 'MARKET',
                                                quantity = round(abs(position)-abs(position)%float(step),int(precision)),
                                                sideEffectType = 'AUTO_REPAY',
                                                recvWindow=59999,
                                                isIsolated = isIsolated
                                                )
                else:
                    user_agent.marginCreateOrder(
                                                symbol = coin+'USDT',
                                                side = "SELL",
                                                type = 'MARKET',
                                                quantity = round(abs(position)-abs(position)%float(step),int(precision)),
                                                sideEffectType = 'AUTO_REPAY',
                                                recvWindow=59999,
                                                isIsolated = isIsolated
                                                )
        except Exception:
            if isIsolated == True:
                time.sleep(1)
                BOT_Library.close_position(user_dict,coin,step,precision,True)
            else:
                time.sleep(1)
                BOT_Library.close_position(user_dict,coin,step,precision)

    def open_position(user_dict, coin, position, isIsolated = False):
        for user in user_dict:
            try:
                user_agent = Binance(API_KEY = user_dict[user][0], API_SECRET = user_dict[user][1])
                if position == 'short':
                    user_agent.marginCreateOrder(
                                                symbol = coin+'USDT',
                                                side = "SELL",
                                                type = 'MARKET',
                                                quoteOrderQty = float(user_dict[user][2]),
                                                sideEffectType = 'MARGIN_BUY',
                                                recvWindow=59999,
                                                isIsolated = isIsolated,
                                                newOrderRespType = 'RESULT'
                                                )
                if position == 'long':
                    user_agent.marginCreateOrder(
                                                symbol = coin+'USDT',
                                                side = "BUY",
                                                type = 'MARKET',
                                                quoteOrderQty = float(user_dict[user][2]),
                                                sideEffectType = 'MARGIN_BUY',
                                                recvWindow=59999,
                                                isIsolated = isIsolated,
                                                newOrderRespType = 'RESULT'
                                                )
            except Exception:
                if isIsolated == True:
                    time.sleep(1)
                    BOT_Library.open_position(user_dict, coin, position, True)
                else:
                    time.sleep(1)
                    BOT_Library.open_position(user_dict, coin, position)

    def ticker_price (coin):
        try:
           return float(BOT_Library.bot.tickerPrice(symbol=coin+'USDT')['price'])
        except Exception:
            return BOT_Library.ticker_price (coin)


if __name__ == '__main__':
    
    
