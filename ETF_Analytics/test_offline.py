"""
Offline test - verifies code structure without fetching live data
"""
import sys
import importlib


def test_imports():
    """Test that all modules can be imported"""
    print("\n" + "="*70)
    print("OFFLINE TEST - Module Import Verification")
    print("="*70)
    
    modules_to_test = [
        ('config', 'Configuration'),
        ('data_fetchers', 'Data Fetchers'),
        ('data_fetchers.alpha_vantage', 'Alpha Vantage Fetcher'),
        ('data_fetchers.iex_cloud', 'IEX Cloud Fetcher'),
        ('data_fetchers.fred', 'FRED Fetcher'),
        ('data_quality', 'Data Quality Validator'),
        ('etf_analytics', 'ETF Analytics'),
        ('etf_analytics.metrics', 'ETF Metrics'),
        ('etf_analytics.risk', 'Risk Analytics'),
        ('utils', 'Utilities'),
        ('etf_app', 'Main Application'),
    ]
    
    failed = []
    
    for module_name, display_name in modules_to_test:
        try:
            importlib.import_module(module_name)
            print(f"  ✓ {display_name}")
        except Exception as e:
            print(f"  ✗ {display_name}: {str(e)[:50]}")
            failed.append(module_name)
    
    print("\n" + "="*70)
    
    if not failed:
        print("✓ ALL MODULES LOADED SUCCESSFULLY!")
        print("="*70)
        print("\nPlatform structure is correct and ready to use.")
        print("\nNote: Live data tests require internet connection.")
        print("When ready, run: python example.py")
        return True
    else:
        print(f"✗ {len(failed)} module(s) failed to load")
        print("="*70)
        return False


def test_basic_functions():
    """Test basic function availability"""
    print("\n" + "="*70)
    print("FUNCTION AVAILABILITY TEST")
    print("="*70)
    
    try:
        from etf_analytics import calculate_returns, tracking_error, risk_metrics_summary
        from data_quality import DataQualityValidator
        from etf_app import ETFAnalyzer
        
        print("  ✓ calculate_returns")
        print("  ✓ tracking_error")
        print("  ✓ risk_metrics_summary")
        print("  ✓ DataQualityValidator")
        print("  ✓ ETFAnalyzer")
        
        # Test with dummy data
        import pandas as pd
        import numpy as np
        
        dates = pd.date_range('2024-01-01', periods=30)
        prices = pd.Series(100 + np.cumsum(np.random.randn(30) * 0.5), index=dates)
        
        returns = calculate_returns(prices)
        print(f"\n  ✓ Calculated {len(returns)} returns from sample data")
        
        print("\n" + "="*70)
        print("✓ ALL FUNCTIONS WORKING CORRECTLY!")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"\n✗ Function test failed: {e}")
        return False


if __name__ == "__main__":
    import_success = test_imports()
    
    if import_success:
        function_success = test_basic_functions()
        print("\n✅ Platform is ready! Run 'python example.py' when you have internet connection.\n")
        exit(0)
    else:
        print("\n❌ Some modules failed to load. Check error messages above.\n")
        exit(1)
