import pybithumb
import telegram

# 코인별 상승 / 하락 반환
def bull_market(ticker):
    df = pybithumb.get_ohlcv(ticker)
    ma5 = df['close'].rolling(window=5).mean()
    price = pybithumb.get_current_price(ticker)
    last_ma5 = ma5[-2]

    if price > last_ma5:
        return True
    else:
        return False

# massage 만들기
def make_massage(total_count, high_count, low_count, high_text, low_text):
    
    text = "코인 총갯수 : {}개\n상승장 : {}개\n하락장 : {}개\n".format(total_count, high_count,low_count)
    
    text += '\n※ 상승장 리스트\n'
    
    text += high_text + '\n'
    
    text += '\n※ 하락장 리스트\n'
    
    text += low_text + '\n'
    
    return text
    
# This function send coin list by your telegram.
def message_send(coin_information):
    
    my_token = ""         # insert your token
    chat_id = ""          # insert your chat_id
    
    bot = telegram.Bot(token=my_token)
    bot.sendMessage(chat_id=chat_id, text=coin_information)


# main code
if __name__ == "__main__":
    
    high_list = []
    high_count = 0

    low_list = []
    low_count = 0

    # 상승장 하락장 리스트 얻기
    tickers = pybithumb.get_tickers()
    for ticker in tickers:
        is_bull = bull_market(ticker)
        if is_bull:
            high_count += 1
            high_list.append(str(ticker))
        else:
            low_count += 1
            low_list.append(str(ticker))
            
    total_count = high_count + low_count
    
    high_text = ''
    low_text = ''

    # 상승리스트 정리
    for i in range(len(high_list)):
        if i % 10 == 0:
            high_text+='\n'
        else:
            high_text+=high_list[i] + ', '

    # 하락리스트 정리      
    for i in range(len(low_list)):
        if i % 10 == 0:
            low_text+='\n'
        else:
            low_text+= low_list[i] + ', '
            
    telegram_text = make_massage(total_count, high_count, low_count, high_text, low_text)
    
    message_send(telegram_text)