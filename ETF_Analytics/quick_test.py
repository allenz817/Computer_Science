"""
Quick test to verify installation and basic functionality
Run: python quick_test.py
"""
from etf_app import ETFAnalyzer
from datetime import datetime, timedelta


def test_basic_functionality():
    """Test basic ETF analysis functionality"""
    print("\n" + "="*70)
    print("QUICK TEST - ETF Analytics Platform")
    print("="*70)
    
    print("\n1. Initializing ETF Analyzer...")
    try:
        analyzer = ETFAnalyzer()
        print("   ✓ Analyzer initialized successfully")
    except Exception as e:
        print(f"   ✗ Failed to initialize: {e}")
        return False
    
    print("\n2. Fetching SPY data (last 30 days)...")
    try:
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        data = analyzer.yahoo_fetcher.fetch_prices('SPY', start_date)
        
        if not data.empty:
            print(f"   ✓ Successfully fetched {len(data)} days of data")
            print(f"   Latest close: ${data['Close'].iloc[-1]:.2f}")
        else:
            print("   ✗ No data returned")
            return False
    except Exception as e:
        print(f"   ✗ Failed to fetch data: {e}")
        return False
    
    print("\n3. Testing data quality validation...")
    try:
        from data_quality import DataQualityValidator
        validator = DataQualityValidator()
        
        end_date = datetime.now().strftime('%Y-%m-%d')
        completeness = validator.validate_completeness(data, start_date, end_date)
        print(f"   ✓ Completeness check passed")
        print(f"   Data completeness: {completeness['completeness_pct']:.1%}")
    except Exception as e:
        print(f"   ✗ Validation failed: {e}")
        return False
    
    print("\n4. Testing ETF metrics calculation...")
    try:
        from etf_analytics import calculate_returns, risk_metrics_summary
        
        returns = calculate_returns(data['Adj Close'])
        metrics = risk_metrics_summary(returns.dropna())
        
        print(f"   ✓ Metrics calculated successfully")
        print(f"   Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
        print(f"   Max Drawdown: {metrics['max_drawdown']:.2%}")
    except Exception as e:
        print(f"   ✗ Metric calculation failed: {e}")
        return False
    
    print("\n" + "="*70)
    print("✓ ALL TESTS PASSED - Platform is ready to use!")
    print("="*70)
    print("\nNext steps:")
    print("  - Run 'python example.py' to see more examples")
    print("  - Customize config.py with your API keys")
    print("  - Review README.md for full documentation")
    print("\n")
    
    return True


if __name__ == "__main__":
    success = test_basic_functionality()
    exit(0 if success else 1)
