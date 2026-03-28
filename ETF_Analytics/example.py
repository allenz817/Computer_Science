"""
Example usage of ETF Analytics Platform
"""
from etf_app import ETFAnalyzer
from datetime import datetime, timedelta
import pandas as pd

# Set display options for better output
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)


def example_1_single_etf_analysis():
    """Example 1: Analyze a single ETF"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Single ETF Analysis")
    print("="*70)
    
    # Initialize analyzer
    analyzer = ETFAnalyzer()
    
    # Analyze SPY (S&P 500 ETF) over the last 2 years
    start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
    
    results = analyzer.analyze_etf(
        ticker='SPY',
        start_date=start_date,
        benchmark='SPY'  # Using SPY as its own benchmark to verify tracking
    )
    
    # Print formatted report
    analyzer.print_analysis_report(results)


def example_2_compare_etfs():
    """Example 2: Compare multiple ETFs"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Compare Multiple ETFs")
    print("="*70)
    
    analyzer = ETFAnalyzer()
    
    # Compare popular ETFs
    tickers = ['SPY', 'QQQ', 'IWM', 'AGG', 'GLD']
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    comparison = analyzer.compare_etfs(tickers, start_date)
    
    print("\n📊 ETF Comparison Table:")
    print(comparison.to_string(index=False))


def example_3_correlation_analysis():
    """Example 3: Correlation analysis between ETFs"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Correlation Analysis")
    print("="*70)
    
    analyzer = ETFAnalyzer()
    
    # Analyze correlation between different asset class ETFs
    tickers = ['SPY', 'QQQ', 'AGG', 'GLD', 'VNQ']  # Stocks, Tech, Bonds, Gold, REITs
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    corr_matrix = analyzer.get_correlation_matrix(tickers, start_date)
    
    print("\n📈 Correlation Matrix:")
    print(corr_matrix.round(3).to_string())
    
    # Find lowest correlations for diversification
    print("\n🎯 Best Diversification Pairs (Lowest Correlations):")
    
    # Extract lower triangle of correlation matrix
    corr_pairs = []
    for i in range(len(corr_matrix)):
        for j in range(i+1, len(corr_matrix)):
            corr_pairs.append({
                'ETF 1': corr_matrix.index[i],
                'ETF 2': corr_matrix.columns[j],
                'Correlation': corr_matrix.iloc[i, j]
            })
    
    corr_df = pd.DataFrame(corr_pairs).sort_values('Correlation')
    print(corr_df.head(5).to_string(index=False))


def example_4_sector_etf_analysis():
    """Example 4: Analyze sector ETFs"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Sector ETF Analysis")
    print("="*70)
    
    analyzer = ETFAnalyzer()
    
    # Analyze major sector ETFs vs S&P 500
    sector_etfs = ['XLF', 'XLK', 'XLE', 'XLV', 'XLY']  # Finance, Tech, Energy, Health, Consumer
    start_date = '2023-01-01'
    
    results = []
    for ticker in sector_etfs:
        try:
            analysis = analyzer.analyze_etf(ticker, start_date, benchmark='SPY')
            
            results.append({
                'Sector ETF': ticker,
                'Ann Return': f"{analysis['risk_metrics']['annualized_return']:.2%}",
                'Volatility': f"{analysis['risk_metrics']['annualized_volatility']:.2%}",
                'Sharpe': f"{analysis['risk_metrics']['sharpe_ratio']:.2f}",
                'Beta vs SPY': f"{analysis['benchmark_analysis']['beta']:.2f}" 
                    if analysis['benchmark_analysis'] else 'N/A',
                'Tracking Error': f"{analysis['benchmark_analysis']['tracking_error']:.2%}"
                    if analysis['benchmark_analysis'] else 'N/A',
                'Quality': analysis['data_quality']['grade']
            })
        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
    
    df_results = pd.DataFrame(results)
    print("\n📊 Sector ETF Performance vs S&P 500:")
    print(df_results.to_string(index=False))


def example_5_data_quality_focus():
    """Example 5: Focus on data quality validation"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Data Quality Analysis")
    print("="*70)
    
    analyzer = ETFAnalyzer()
    
    # Test with a few ETFs to check data quality
    test_tickers = ['SPY', 'QQQ', 'IWM']
    start_date = '2024-01-01'
    
    print("\n🔍 Detailed Data Quality Scores:")
    print("-" * 70)
    
    for ticker in test_tickers:
        try:
            analysis = analyzer.analyze_etf(ticker, start_date)
            quality = analysis['data_quality']
            
            print(f"\n{ticker} - Grade: {quality['grade']} ({quality['total_score']:.1f}/100)")
            print(f"  Completeness: {quality['components']['completeness']:.1f}/40")
            print(f"  Anomaly-Free: {quality['components']['anomaly_free']:.1f}/30")
            print(f"  Validation: {quality['components']['cross_validation']:.1f}/30")
            print(f"  Data Points: {quality['completeness_details']['actual_data_points']}")
            print(f"  Anomalies: {len(quality['anomalies']['extreme_price_changes'])} price changes, "
                  f"{len(quality['anomalies']['volume_spikes'])} volume spikes")
        except Exception as e:
            print(f"\n{ticker} - Error: {e}")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("ETF ANALYTICS PLATFORM - EXAMPLES")
    print("="*70)
    print("\nRunning example analyses...")
    print("Note: This will fetch real market data. Please be patient.\n")
    
    # Run examples
    try:
        example_1_single_etf_analysis()
    except Exception as e:
        print(f"Example 1 failed: {e}")
    
    try:
        example_2_compare_etfs()
    except Exception as e:
        print(f"Example 2 failed: {e}")
    
    try:
        example_3_correlation_analysis()
    except Exception as e:
        print(f"Example 3 failed: {e}")
    
    try:
        example_4_sector_etf_analysis()
    except Exception as e:
        print(f"Example 4 failed: {e}")
    
    try:
        example_5_data_quality_focus()
    except Exception as e:
        print(f"Example 5 failed: {e}")
    
    print("\n" + "="*70)
    print("Examples completed!")
    print("="*70 + "\n")
