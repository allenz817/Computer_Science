# ⚡ Yahoo Finance Removed - Platform Updated

## ✅ What's New

**Yahoo Finance has been removed** and replaced with more reliable sources:

### New Data Sources:
1. **Alpha Vantage** (Primary) - Official API, 25 calls/day free
2. **IEX Cloud** (Secondary) - Professional data, 50k messages/month free  
3. **FRED** (Benchmarks) - Unchanged

## 🔑 Setup Required

### Get Free API Keys:

**Alpha Vantage (Required):**
```
1. Visit: https://www.alphavantage.co/support/#api-key
2. Get free API key (instant, no credit card)
3. Add to config.py: ALPHA_VANTAGE_API_KEY = "your_key"
```

**IEX Cloud (Optional but Recommended):**
```
1. Visit: https://iexcloud.io/console/
2. Sign up for free (50,000 messages/month)
3. Add to config.py: IEX_CLOUD_API_KEY = "your_key"
```

### Update config.py:

```python
# Add your API keys here
ALPHA_VANTAGE_API_KEY = "YOUR_ALPHA_VANTAGE_KEY"
IEX_CLOUD_API_KEY = "YOUR_IEX_KEY"  # Optional
```

## 📝 Usage Changes

**Before (Old - Yahoo Finance):**
```python
analyzer = ETFAnalyzer()  # Used yfinance automatically
```

**After (New - Alpha Vantage + IEX):**
```python
# Recommended: Use both sources for validation
analyzer = ETFAnalyzer(
    alpha_vantage_key="your_key",  # or set in config.py
    iex_cloud_key="your_key",      # optional
    use_iex=True
)

# Or: Alpha Vantage only
analyzer = ETFAnalyzer(alpha_vantage_key="your_key", use_iex=False)

# Or: Use keys from config.py (recommended)
analyzer = ETFAnalyzer()  # Reads from config.py
```

## 🚀 Quick Start

```bash
# 1. Update dependencies
pip install -r requirements.txt

# 2. Get API keys (see above)

# 3. Edit config.py and add your keys

# 4. Test
python test_offline.py  # Should pass
python quick_test.py    # Requires API keys + internet

# 5. Run examples
python example.py
```

## ⚡ Benefits

✅ **More Reliable** - Official APIs with SLAs
✅ **Better Data Quality** - Cross-validation between sources  
✅ **Future-Proof** - Won't break unexpectedly
✅ **Higher Free Limits** - 50k messages/month with IEX Cloud
✅ **Professional Grade** - Same data sources hedge funds use

## 📊 Rate Limits

| Source | Free Tier | Typical Usage |
|--------|-----------|---------------|
| Alpha Vantage | 25 calls/day | ~8-12 ETF analyses/day |
| IEX Cloud | 50k msgs/month | ~1,600 ETF analyses/month |

## 🔧 Troubleshooting

**"No data returned"**
- Check API keys are configured in config.py
- Verify keys work on provider websites
- Alpha Vantage demo key is very limited

**"Rate limit exceeded"**
- Alpha Vantage: Wait until tomorrow or upgrade ($50/mo for 500/day)
- Use IEX Cloud as alternative (higher free tier)

**"API key invalid"**
- Copy full key without spaces
- Check key status on provider website
- Regenerate if needed

## 📚 More Info

- See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed migration steps
- See [README.md](README.md) for full documentation
- See [QUICKSTART.md](QUICKSTART.md) for quick reference

---

Platform is ready to use with more reliable data sources! 🎉
