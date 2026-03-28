"""
ETF ANALYTICS PLATFORM - QUICK REFERENCE CARD
═══════════════════════════════════════════════════════════════════

INSTALLATION
────────────
cd ETF_Analytics
pip install -r requirements.txt
python test_offline.py  # Verify setup


BASIC USAGE
───────────
from etf_app import ETFAnalyzer

analyzer = ETFAnalyzer()

# Single ETF analysis
results = analyzer.analyze_etf('SPY', start_date='2023-01-01')
analyzer.print_analysis_report(results)

# Compare multiple ETFs
comparison = analyzer.compare_etfs(['SPY', 'QQQ', 'IWM'], 
                                   start_date='2023-01-01')
print(comparison)

# Correlation matrix
corr = analyzer.get_correlation_matrix(['SPY', 'AGG', 'GLD'],
                                       start_date='2023-01-01')


KEY METRICS AVAILABLE
─────────────────────
📈 Performance:
  • Total return, Annualized return
  • Annualized volatility
  • Price summary (min/max/range)

⚖️ Risk:
  • Sharpe ratio, Sortino ratio
  • Maximum drawdown
  • VaR (95%), CVaR (95%)
  • Downside risk, Calmar ratio
  • Skewness, Kurtosis

🎯 ETF-Specific:
  • Tracking error (vs benchmark)
  • Tracking difference
  • Beta, Correlation
  • Expense ratio impact
  • Liquidity score

✅ Data Quality:
  • A-F Grade (0-100 score)
  • Completeness percentage
  • Anomaly detection
  • Cross-source validation


COMMON PATTERNS
───────────────

1. Quick ETF Check
   results = analyzer.analyze_etf('SPY', start_date='2024-01-01')
   print(f"Sharpe: {results['risk_metrics']['sharpe_ratio']:.2f}")
   print(f"Quality: {results['data_quality']['grade']}")

2. Sector Comparison
   sectors = ['XLF', 'XLK', 'XLE', 'XLV', 'XLY']
   comp = analyzer.compare_etfs(sectors, start_date='2023-01-01')

3. Track vs Benchmark
   results = analyzer.analyze_etf('VOO', 
                                   start_date='2023-01-01',
                                   benchmark='SPY')
   te = results['benchmark_analysis']['tracking_error']
   print(f"Tracking Error: {te:.2%}")

4. Diversification Check
   etfs = ['SPY', 'AGG', 'GLD', 'VNQ', 'TLT']
   corr = analyzer.get_correlation_matrix(etfs, '2023-01-01')
   # Look for low correlations (<0.3)


ACCESSING RAW DATA
──────────────────
# Get just the price data
data = analyzer.yahoo_fetcher.fetch_prices('SPY', '2023-01-01')
# Returns: DataFrame with OHLCV

# Get ETF info
info = analyzer.yahoo_fetcher.fetch_info('SPY')
# Returns: dict with name, expense ratio, AUM, etc.

# Calculate custom metrics
from etf_analytics import calculate_returns, sharpe_ratio
returns = calculate_returns(data['Adj Close'])
sharpe = sharpe_ratio(returns.dropna())


CUSTOMIZATION
─────────────
Edit config.py:

# Add Alpha Vantage key
ALPHA_VANTAGE_API_KEY = "your_key_here"

# Adjust quality thresholds
QUALITY_THRESHOLDS = {
    'min_data_points': 20,
    'max_missing_pct': 0.05,
    'price_change_threshold': 0.25,
    'volume_spike_threshold': 5.0
}

# Change risk-free rate
RISK_FREE_RATE = 0.04  # 4%


EXPORTING RESULTS
─────────────────
from utils import save_results_to_json, save_results_to_csv

# Save analysis to JSON
results = analyzer.analyze_etf('SPY', start_date='2023-01-01')
save_results_to_json(results, 'spy_analysis.json')

# Save comparison to CSV
comparison = analyzer.compare_etfs(['SPY', 'QQQ'], '2023-01-01')
save_results_to_csv(comparison, 'etf_comparison.csv')


TROUBLESHOOTING
───────────────
Issue: "No data returned"
  → Check ticker symbol
  → Verify date range (use recent dates)
  → Wait a few minutes (rate limit)

Issue: "Rate limit error"
  → yfinance: Wait 5-10 minutes
  → Alpha Vantage: 25 calls/day free tier
  → Disable Alpha Vantage: use_alpha_vantage=False

Issue: "Module not found"
  → pip install -r requirements.txt
  → Check you're in ETF_Analytics directory


DATA SOURCES
────────────
Primary:    Yahoo Finance (yfinance) - Historical prices, info
Validation: Alpha Vantage (optional) - Cross-check prices
Benchmark:  FRED - Risk-free rates, market indices


FILE STRUCTURE
──────────────
etf_app.py         → Main application
example.py         → Usage examples
config.py          → Settings
data_fetchers/     → Data collection
data_quality/      → Validation
etf_analytics/     → Metrics & risk
utils/             → Helpers


EXAMPLES PROVIDED
─────────────────
Run: python example.py

1. Single ETF Analysis (SPY)
2. Multi-ETF Comparison
3. Correlation Analysis
4. Sector ETF Analysis
5. Data Quality Focus


NEXT STEPS
──────────
1. Run test_offline.py to verify setup
2. Try example.py to see capabilities
3. Analyze your favorite ETFs
4. Customize config.py for your needs
5. Build your own analysis scripts!


SUPPORT
───────
Documentation: README.md, PROJECT_SUMMARY.md
Architecture:  python ARCHITECTURE.py
Quick start:   QUICKSTART.md


═══════════════════════════════════════════════════════════════════

Happy Analyzing! 🚀

For questions or issues, check the documentation files.
"""

if __name__ == "__main__":
    print(__doc__)
