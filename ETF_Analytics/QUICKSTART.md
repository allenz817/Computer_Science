# ETF Analytics Platform - Quick Reference

## Installation

```bash
cd ETF_Analytics
pip install -r requirements.txt
```

**Important: Get Free API Keys**

Alpha Vantage (required for price data):
1. Visit https://www.alphavantage.co/support/#api-key
2. Get your free API key (25 calls/day, or upgrade to 500/day for $50/month)
3. Add to `config.py`: `ALPHA_VANTAGE_API_KEY = "your_key_here"`

IEX Cloud (optional for validation):
1. Visit https://iexcloud.io/console/
2. Get free tier (50,000 messages/month)
3. Add to `config.py`: `IEX_CLOUD_API_KEY = "your_key_here"`

## Quick Start

### Test Installation
```bash
python quick_test.py
```

### Run Examples
```bash
python example.py
```

### Basic Usage

```python
from etf_app import ETFAnalyzer

# Initialize
analyzer = ETFAnalyzer()

# Analyze single ETF
results = analyzer.analyze_etf('SPY', start_date='2023-01-01')
analyzer.print_analysis_report(results)

# Compare ETFs
comparison = analyzer.compare_etfs(['SPY', 'QQQ', 'IWM'], start_date='2023-01-01')
print(comparison)

# Get correlation matrix
corr = analyzer.get_correlation_matrix(['SPY', 'AGG', 'GLD'], start_date='2023-01-01')
print(corr)
```

## Key Features

### 1. Data Quality Validation
- Multi-source cross-validation
- Anomaly detection
- Completeness checking
- Quality scoring (A-F grades)

### 2. ETF Metrics
- Tracking error & tracking difference
- Expense ratio analysis
- Liquidity scoring
- Beta calculation
- Premium/discount to NAV

### 3. Risk Analysis
- Sharpe & Sortino ratios
- Maximum drawdown
- VaR & CVaR
- Downside risk
- Skewness & kurtosis

### 4. Benchmark Comparison
- Compare against SPY, QQQ, or custom benchmark
- Correlation analysis
- Performance attribution

## Data Sources

1. **Alpha Vantage (Primary)** - Historical OHLCV, fundamentals
   - Free tier: 25 API calls/day
   - Premium: 500 calls/day ($50/month)
   - Required for basic functionality

2. **IEX Cloud (Secondary)** - Price validation, company info
   - Free tier: 50,000 messages/month
   - Optional but recommended for cross-validation

3. **FRED** - Risk-free rates, market indices
   - No API key required
   - Used for benchmark data

## Configuration

Edit `config.py` to customize:
- API keys
- Quality thresholds
- Risk-free rate
- Cache settings

## API Keys (Optional)

**Alpha Vantage** (free): Get key at https://www.alphavantage.co/support/#api-key
- Add to `config.py`: `ALPHA_VANTAGE_API_KEY = "your_key"`
- Enable in analyzer: `ETFAnalyzer(use_alpha_vantage=True)`

## Output Examples

**Single ETF Analysis:**
- Performance metrics (returns, volatility, Sharpe)
- Risk metrics (VaR, drawdown, skewness)
- Benchmark comparison (tracking error, beta)
- Data quality score
- Liquidity metrics

**Multi-ETF Comparison:**
- Side-by-side table of key metrics
- Data quality grades
- Expense ratios
- AveragAPI keys are configured in `config.py`
- Verify ticker symbol is correct
- Check you haven't exceeded rate limits (25/day for Alpha Vantage free tier)

**Rate limit errors (Alpha Vantage):**
- Free tier: 25 calls/day
- Wait until next day or upgrade to premium
- Use demo key for testing (very limited)

**IEX Cloud not working:**
- It's optional - platform works without it
- Disable: `analyzer = ETFAnalyzer(use_iex=False)Try different date range

**Rate limit errors (Alpha Vantage):**
- Free tier: 25 calls/day
- Use `use_alpha_vantage=False` (default)

**Missing dependencies:**
```bash
pip install -r requirements.txt --upgrade
```

## Project Structure

```
ETF_Analytics/
├── config.py              # Configuration settings
├── etf_app.py            # Main application
├── example.py            # Usage examples
├── quick_test.py         # Installation test
├── data_fetchers/        # Data source modules
├── data_quality/         # Validation & scoring
├── etf_analytics/        # ETF metrics & risk
└── utils/                # Helper functions
```

## Next Steps

1. ✓ Run `quick_test.py` to verify setup
2. ✓ Run `example.py` to see capabilities
3. ✓ Customize `config.py` for your needs
4. ✓ Build your own analysis scripts!
