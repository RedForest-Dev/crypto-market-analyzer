import ccxt
import time
from datetime import datetime
import sys

exchange = ccxt.binance({'enableRateLimit': True})
symbol = 'BTC/USDT'

# Задаем три параметра лимита
limit1 = 100
limit2 = 200
limit3 = 300

print(f"[{datetime.now().strftime('%H:%M:%S')}] ТРОЙНОЙ МОНИТОРИНГ (L300 -> L100) ЗАПУЩЕН...")

while True:
    try:
        now = datetime.now()
        
        # Срабатываем за 10 секунд до закрытия 5-минутки
        if (now.minute + 1) % 5 == 0 and now.second == 50:
            
            # 1. ЗАПРОС СДЕЛКОВ
            since = exchange.milliseconds() - 300000 
            trades = exchange.fetch_trades(symbol, since=since)
            market_buy = sum([t['amount'] for t in trades if t['side'] == 'buy'])
            market_sell = sum([t['amount'] for t in trades if t['side'] == 'sell'])

            # Получаем текущую цену
            ticker = exchange.fetch_ticker(symbol)
            current_price = ticker['last']

            print(f"\n{'='*55}")
            print(f" ВРЕМЯ: {now.strftime('%H:%M:%S')} (Предварительный анализ)")
            print(f" ЦЕНА:  {current_price} USDT")
            print(f"{'='*55}")

            # 2. ЗАПРОСЫ СТАКАНА В ОБРАТНОМ ПОРЯДКЕ (300, 200, 100)
            for current_limit in [limit3, limit2, limit1]:
                ob = exchange.fetch_order_book(symbol, limit=current_limit)
                
                b_top = ob['bids'][0][0]
                b_bottom = ob['bids'][-1][0]
                a_top = ob['asks'][0][0]
                a_bottom = ob['asks'][-1][0]
                
                d_bids = b_top - b_bottom
                d_asks = a_bottom - a_top
                
                v_bids = sum([x[1] for x in ob['bids']])
                v_asks = sum([x[1] for x in ob['asks']])
                
                den_b = v_bids / d_bids if d_bids > 0 else 0
                den_a = v_asks / d_asks if d_asks > 0 else 0
                
                print(f" ДИСТАНЦИЯ (L{current_limit}):  BIDS: -{d_bids:<8.2f} | ASKS: +{d_asks:.2f}")
                print(f" ВЕС В СТАКАНЕ:     BIDS: {v_bids:<8.2f} | ASKS: {v_asks:.2f} BTC")
                print(f" ПЛОТНОСТЬ (BTC/$): BIDS: {den_b:<8.2f} | ASKS: {den_a:.2f}")
                print(f"{'='*55}")

            # 3. ИТОГОВЫЙ БЛОК МАРКЕТА
            print(f" ВЛИТО ПО РЫНКУ (5m): BUY: {market_buy:<8.2f} | SELL: {market_sell:.2f} BTC")
            print(f"{'='*55}")

            time.sleep(15)
        
        time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nОстановка мониторинга.")
        sys.exit()
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(1)
