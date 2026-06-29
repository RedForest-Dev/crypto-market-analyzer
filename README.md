# crypto-market-analyzer
Python-based real-time market data monitoring and order flow analysis tool using CCXT library.
### Additional Tool: Order Book Density Monitor
`order_book_monitor.py` - Advanced analysis of market depth using three-level limit monitoring (100, 200, 300) to identify liquidity walls and market pressure before 5-minute candle closure.
The depth limits (limit1, limit2, limit3) are configurable in the script header to match specific liquidity analysis requirements.
