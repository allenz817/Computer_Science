# ETF Analytics Platform

A prototype application for analyzing ETF data with focus on data quality and reliability.

## Features

- **Multi-Source Data Fetching**: Aggregates data from multiple free sources (yfinance, Alpha Vantage, FRED)
- **Data Quality Validation**: Cross-validates prices and detects anomalies
- **ETF-Specific Metrics**: Tracking error, expense ratios, holdings analysis
- **Portfolio Analytics**: Risk metrics, correlation analysis, efficient frontier
- **Quality Scoring**: Assigns reliability scores based on data completeness and consistency

## Data Sources

1. **yfinance**: Historical price data (primary)
2. **Alpha Vantage**: Price validation and fundamentals
3. **FRED**: Risk-free rates and benchmark indices
4. **SEC EDGAR**: Holdings data (future enhancement)

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from etf_app import ETFAnalyzer

# Initialize analyzer
analyzer = ETFAnalyzer()

# Analyze single ETF
etf_data = analyzer.analyze_etf('SPY', start_date='2020-01-01')

# Compare multiple ETFs
comparison = analyzer.compare_etfs(['SPY', 'QQQ', 'IWM'], start_date='2020-01-01')

# Portfolio optimization
optimal_weights = analyzer.optimize_portfolio(['SPY', 'AGG', 'GLD'])
```

## Project Structure

```
ETF_Analytics/
├── data_fetchers/      # Data collection from various sources
├── data_quality/       # Validation and quality checks
├── etf_analytics/      # ETF-specific analysis functions
├── portfolio/          # Portfolio optimization and risk analysis
├── utils/              # Helper functions
├── etf_app.py          # Main application
└── example.py          # Usage examples
```

## Current Limitations

- Free tier API rate limits (Alpha Vantage: 25/day)
- yfinance is unofficial and may break
- Holdings data requires manual SEC filing downloads
