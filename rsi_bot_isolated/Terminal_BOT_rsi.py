from Library import BOT_Library
import time
import re
import bot_users
import statistics


def main(coin, frame, user_dict):
    print (coin)
    currency_settings = BOT_Library.currency_settings(coin)
    j=float(re.sub(r'[\D]',r'',frame))
    while True:
        timeutc = time.localtime()
        if int(timeutc[5]) == 0: 
            bot_signal = BOT_Library.Signal_rsi(coin,frame)
            if bot_signal == False:
                time.sleep(1)
                print ('In search')
            else:
                print (f'time {timeutc[3]}:{timeutc[4]}:{timeutc[5]}, signal {bot_signal}')
                open('Log_loh.txt','a').write (f'time {timeutc[3]}:{timeutc[4]}:{timeutc[5]}, signal {bot_signal}\n')
                BOT_Library.open_position(user_dict, coin, bot_signal, True)
                enter_price = BOT_Library.ticker_price(coin)
                take_target = round(enter_price * 1.012 if bot_signal == 'long' else enter_price* 0.994,6)
                print (f'{bot_signal=}, {enter_price= }, {take_target= }')
                history_of_enter = []
                history_of_enter.append(enter_price)
                count_enter = 1
                if bot_signal == 'long':
                    while True:
                        timeutc = time.localtime()
                        if int(timeutc[5]) == 0 and count_enter <=4:
                            fresh_bot_signal = BOT_Library.Signal_rsi(coin,frame)
                            if fresh_bot_signal == bot_signal:
                                print ('Есть новый вход')
                                count_enter += 1
                                for o in range (count_enter):
                                    BOT_Library.open_position(user_dict, coin, fresh_bot_signal,True)
                                    history_of_enter.append(BOT_Library.ticker_price(coin))
                                new_avg_enter = statistics.mean(history_of_enter)
                                take_target = round(new_avg_enter *(1.012+0.0005*len(history_of_enter)),6)
                                print(f'{history_of_enter= }, {new_avg_enter= }, {take_target=}')
                                
                        current_price = round(BOT_Library.ticker_price(coin),6)
                        if current_price >= take_target:
                            BOT_Library.close_position(user_dict,coin,currency_settings[1],currency_settings[0], True)
                            print (f'long position close in {round((current_price/statistics.mean(history_of_enter)-1)*100,5)}')
                            open('Log.txt','a').write(f'position long with enters {history_of_enter}, avg price {statistics.mean(history_of_enter)}, was closed {round((current_price/statistics.mean(history_of_enter)-1)*100,5)}%, date {time.localtime()[2]}.{time.localtime()[1]}.{time.localtime()[0]} {time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}\n')
                            break
                        else:
                            pass
                '''elif bot_signal == 'short':
                    while True:
                        timeutc = time.localtime()
                        if int(timeutc[5]) == 0 and count_enter <=4:
                            fresh_bot_signal = BOT_Library.Signal_rsi(coin,frame)
                            if fresh_bot_signal == bot_signal:
                                print ('Есть новый вход')
                                count_enter += 1
                                for o in range (count_enter):
                                    BOT_Library.open_position(user_dict, coin, fresh_bot_signal, True)
                                    history_of_enter.append(BOT_Library.ticker_price(coin))
                                new_avg_enter = statistics.mean(history_of_enter)
                                take_target = round(new_avg_enter * (0.994 + 0.0005 * len(history_of_enter)),6)
                                print(f'{history_of_enter= }, {new_avg_enter= }, {take_target=}')
                                
                        current_price = round(BOT_Library.ticker_price(coin),6)
                        if current_price <= take_target:
                            BOT_Library.close_position(user_dict,coin,currency_settings[1],currency_settings[0], True)
                            print (f'short позиция закрыта в {abs(current_price/statistics.mean(history_of_enter)-1)}')
                            open('Log.txt','a').write(f'position short with enters {history_of_enter}, avg price {statistics.mean(history_of_enter)}, was closed {abs(round((current_price/statistics.mean(history_of_enter)-1)*100, 5))}%, date {time.localtime()[2]}.{time.localtime()[1]}.{time.localtime()[0]} {time.localtime()[3]}:{time.localtime()[4]}:{time.localtime()[5]}\n')
                            break
                        else:
                            pass'''
        else: 
            pass

        
if __name__ == '__main__':
    
    bot_accs = bot_users.active_users
    main('ETH','1m',bot_accs)
                

    
