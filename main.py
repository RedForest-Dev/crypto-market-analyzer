import ccxt
import time
from datetime import datetime
import sys

exchange = ccxt.binance({'enableRateLimit': True})
symbol = 'BTC/USDT'

# Хранилище для предыдущего замера
prev_buy_pct = None
print(f"[{datetime.now().strftime('%H:%M:%S')}] МОНИТОРИНГ ДИНАМИКИ СДЕЛОК ЗАПУЩЕН...")

while True:
    try:
        now = datetime.now()
        
        # Срабатываем в начале каждой минуты (01 сек), чтобы собрать данные за прошедшую 60с
        if now.second == 1:
            
            # 1. Запрос сделок строго за последние 60 секунд
            since = exchange.milliseconds() - 60000 
            trades = exchange.fetch_trades(symbol, since=since)
            
            m_buy = sum([t['amount'] for t in trades if t['side'] == 'buy'])
            m_sell = sum([t['amount'] for t in trades if t['side'] == 'sell'])
            total = m_buy + m_sell

            if total > 0:
                # Расчет текущих процентов
                buy_pct = (m_buy / total) * 100
                sell_pct = (m_sell / total) * 100
                
                # Вывод основной строки
                print(f"\nВремя {now.strftime('%H:%M')}  BUY: {m_buy:.2f} | SELL: {m_sell:.2f} BTC ({buy_pct:.0f}/{sell_pct:.0f}%)")
                
                # 2. Анализ динамики по сравнению с прошлой минутой
                if prev_buy_pct is not None:
                    # Разница в процентах
                    diff = buy_pct - prev_buy_pct
                    
                    if diff > 0:
                        trend_text = f"Дин. Покупателей усил. на {abs(diff):.1f}%"
                    elif diff < 0:
                        trend_text = f"Дин. Продавцов усил. на {abs(diff):.1f}%"
                    else:
                        trend_text = "Динамика без изменений"
                        
                    # Оценка силы
                    if buy_pct > 55:
                        power_text = "Покуп. сильнее."
                    elif sell_pct > 55:
                        power_text = "Прод. сильнее."
                    else:
                        power_text = "Силы равны."
                        
                    print(f"{trend_text} {power_text} ({buy_pct:.0f}/{sell_pct:.0f})")
                
                # Сохраняем текущий процент для следующего круга
                prev_buy_pct = buy_pct
            
            # Чтобы не сработало несколько раз в одну секунду
            time.sleep(2)
            
        time.sleep(0.5)

    except KeyboardInterrupt:
        sys.exit()
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(1)
