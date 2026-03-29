# Migration Guide: Yahoo Finance Removed

## What Changed

**Yahoo Finance (yfinance) has been removed** due to reliability issues and frequent rate limiting. The platform now uses:

- ✅ **Alpha Vantage** (Primary) - More reliable, official API
- ✅ **IEX Cloud** (Secondary) - Professional-grade data
- ✅ **FRED** (Benchmarks) - Still available

## Why This Change?

1. **Yahoo Finance** had frequent rate limits and downtime
2. **Unofficial API** - yfinance could break at any time
3. **Better alternatives** exist with official support

## Action Required

### 1. Get API Keys (Required)

**Alpha Vantage** (REQUIRED):
```
Visit: https://www.alphavantage.co/support/#api-key
Free tier: 25 API calls/day
Premium: 500 calls/day for $50/month
```

**IEX Cloud** (Optional but recommended):
```
Visit: https://iexcloud.io/console/
Free tier: 50,000 messages/month
```

### 2. Update config.py

```python
# Before
ALPHA_VANTAGE_API_KEY = "demo"  # Limited demo key
IEX_CLOUD_API_KEY = None

# After (add your real keys)
ALPHA_VANTAGE_API_KEY = "YOUR_KEY_HERE"  # Get from alphavantage.co
IEX_CLOUD_API_KEY = "YOUR_KEY_HERE"     # Optional - get from iexcloud.io
```

### 3. Update Your Code

**Before:**
```python
analyzer = ETFAnalyzer()
# Used Yahoo Finance by default
```

**After:**
```python
# Option 1: Use both sources (recommended)
analyzer = ETFAnalyzer(
    alpha_vantage_key="your_key",
    iex_cloud_key="your_key",  # optional
    use_iex=True
)

# Option 2: Alpha Vantage only
analyzer = ETFAnalyzer(
    alpha_vantage_key="your_key",
    use_iex=False
)
```

### 4. Reinstall Dependencies

```bash
# Remove old dependencies
pip uninstall yfinance -y

# Install updated requirements
pip install -r requirements.txt
```

## Code Changes Summary

### Removed Files
- ❌ `data_fetchers/yahoo_finance.py`

### New Files
- ✅ `data_fetchers/iex_cloud.py`

### Modified Files
- 📝 `config.py` - Updated data source priorities
- 📝 `etf_app.py` - New initialization parameters
- 📝 `requirements.txt` - Removed yfinance
- 📝 All documentation files

## Rate Limits to Know

| Source | Free Tier | Premium |
|--------|-----------|---------|
| Alpha Vantage | 25 calls/day | 500 calls/day ($50/mo) |
| IEX Cloud | 50k msgs/month | More at higher tiers |
| FRED | Unlimited | N/A |

## Tips for Free Tier

**Manage Rate Limits:**
```python
# Analyze carefully to stay under 25 calls/day
results = analyzer.analyze_etf('SPY', start_date='2024-01-01')  # 2-3 calls
comparison = analyzer.compare_etfs(['SPY', 'QQQ'], '2024-01-01')  # 4-6 calls
```

**Use IEX Cloud for More Calls:**
- IEX Cloud has much higher free tier (50k/month)
- Use it as primary if you need more daily calls

**Cache Results:**
```python
# Save results to avoid re-fetching
from utils import save_results_to_json
save_results_to_json(results, 'spy_analysis.json')
```

## Benefits of New Sources

✅ **More Reliable** - Official APIs with SLAs
✅ **Better Data Quality** - Professional-grade sources
✅ **Cross-Validation** - Two sources for verification
✅ **Future-Proof** - Won't break unexpectedly
✅ **Higher Limits** - 50k/month with IEX Cloud free tier

## Common Issues

**"No data returned"**
- You need to configure API keys in config.py
- Free demo key is very limited

**"Rate limit exceeded"**
- Alpha Vantage: 25 calls/day on free tier
- Wait until tomorrow or upgrade
- Use IEX Cloud as alternative

**"API key invalid"**
- Check you copied the full key
- Verify key is active on provider website
- Make sure no extra spaces

## Getting Help

1. Check your API key is correct in `config.py`
2. Run `python test_offline.py` to verify installation
3. Check API provider's status page
4. Review rate limit quotas

## Example: Fresh Install

```bash
# 1. Navigate to project
cd ETF_Analytics

# 2. Update dependencies
pip install -r requirements.txt

# 3. Get API keys
# - Visit alphavantage.co/support/#api-key
# - Visit iexcloud.io/console/

# 4. Edit config.py
# Add your API keys

# 5. Test
python test_offline.py
python quick_test.py

# 6. Run examples
python example.py
```

## Questions?

- Alpha Vantage docs: https://www.alphavantage.co/documentation/
- IEX Cloud docs: https://iexcloud.io/docs/
- Platform docs: See README.md and QUICKSTART.md
