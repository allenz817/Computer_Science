"""
Main ETF Analyzer Application
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data_fetchers import AlphaVantageFetcher, IEXCloudFetcher, FREDFetcher
from data_quality import DataQualityValidator
from etf_analytics import *
import warnings
warnings.filterwarnings('ignore')


class ETFAnalyzer:
    """
    Main ETF analysis application
    Aggregates data from multiple sources and performs comprehensive analysis
    """
    
    def __init__(self, alpha_vantage_key=None, iex_cloud_key=None, use_iex=True):
        """
        Initialize analyzer with data sources
        
        Parameters:
        -----------
        alpha_vantage_key : str, optional
            Alpha Vantage API key (get free at alphavantage.co)
        iex_cloud_key : str, optional
            IEX Cloud API key (get free at iexcloud.io)
        use_iex : bool
            Whether to use IEX Cloud for validation (default True)
        """
        self.alpha_fetcher = AlphaVantageFetcher(alpha_vantage_key)
        self.fred_fetcher = FREDFetcher()
        self.validator = DataQualityValidator()
        
        self.use_iex = use_iex
        if use_iex:
            self.iex_fetcher = IEXCloudFetcher(iex_cloud_key)
        else:
            self.iex_fetcher = None
        
        self.cache = {}
    
    def fetch_etf_data(self, ticker, start_date, end_date=None):
        """
        Fetch ETF data from multiple sources
        
        Returns:
        --------
        dict with data from each source
        """
        if end_date is None:
            end_date = datetime.now()
        
        print(f"\nFetching data for {ticker}...")
        
        data_sources = {}
        
        # Primary source: Alpha Vantage
        print(f"  - Fetching from Alpha Vantage...")
        try:
            alpha_data = self.alpha_fetcher.fetch_prices(ticker, start_date, end_date)
            if not alpha_data.empty:
                data_sources['Alpha Vantage'] = alpha_data
                print(f"    ✓ Got {len(alpha_data)} days of data")
        except Exception as e:
            print(f"    Warning: Alpha Vantage fetch failed: {e}")
        
        # Secondary source: IEX Cloud (if enabled)
        if self.use_iex and self.iex_fetcher:
            print(f"  - Fetching from IEX Cloud...")
            try:
                iex_data = self.iex_fetcher.fetch_prices(ticker, start_date, end_date)
                if not iex_data.empty:
                    data_sources['IEX Cloud'] = iex_data
                    print(f"    ✓ Got {len(iex_data)} days of data")
            except Exception as e:
                print(f"    Warning: IEX Cloud fetch failed: {e}")
        
        return data_sources
    
    def analyze_etf(self, ticker, start_date, end_date=None, benchmark='SPY'):
        """
        Comprehensive ETF analysis
        
        Parameters:
        -----------
        ticker : str
            ETF ticker symbol
        start_date : str or datetime
            Start date for analysis
        end_date : str or datetime, optional
            End date for analysis
        benchmark : str
            Benchmark ticker for comparison
        
        Returns:
        --------
        dict with complete analysis results
        """
        # Fetch data
        data_sources = self.fetch_etf_data(ticker, start_date, end_date)
        
        if not data_sources:
            raise ValueError(f"No data available for {ticker}")
        
        # Use primary source (Alpha Vantage or first available)
        primary_data = data_sources.get('Alpha Vantage', list(data_sources.values())[0])
        
        # Data quality validation
        print(f"\nValidating data quality...")
        completeness = self.validator.validate_completeness(
            primary_data, start_date, end_date or datetime.now()
        )
        anomalies = self.validator.detect_anomalies(primary_data)
        
        # Cross-validate if multiple sources
        validation_result = None
        if len(data_sources) > 1:
            validation_result = self.validator.cross_validate_sources(data_sources)
        
        # Calculate quality score
        quality_score = self.validator.calculate_quality_score(
            primary_data, start_date, end_date or datetime.now(),
            validation_result, anomalies
        )
        
        # Calculate returns
        print(f"Calculating returns and metrics...")
        returns = calculate_returns(primary_data['Adj Close'])
        
        # Risk metrics
        risk_metrics = risk_metrics_summary(returns.dropna())
        
        # Fetch ETF info
        etf_info = self.alpha_fetcher.fetch_info(ticker)
        if not etf_info or etf_info.get('name') == ticker:
            # Try IEX Cloud if Alpha Vantage didn't work
            if self.use_iex and self.iex_fetcher:
                etf_info = self.iex_fetcher.fetch_info(ticker)
        
        # Benchmark comparison
        benchmark_analysis = None
        if benchmark and benchmark != ticker:
            try:
                # Try to get benchmark data from primary source
                benchmark_data_sources = self.fetch_etf_data(benchmark, start_date, end_date)
                if benchmark_data_sources:
                    benchmark_data = list(benchmark_data_sources.values())[0]
                    
                    if not benchmark_data.empty:
                        benchmark_returns = calculate_returns(benchmark_data['Adj Close'])
                        
                        # Align returns
                        aligned_returns = pd.DataFrame({
                            'etf': returns,
                            'benchmark': benchmark_returns
                        }).dropna()
                        
                        benchmark_analysis = {
                            'benchmark_ticker': benchmark,
                            'tracking_error': tracking_error(
                                aligned_returns['etf'], 
                                aligned_returns['benchmark']
                            ),
                            'tracking_difference': tracking_difference(
                                aligned_returns['etf'],
                                aligned_returns['benchmark']
                            ),
                            'beta': calculate_beta(
                                aligned_returns['etf'],
                                aligned_returns['benchmark']
                            ),
                            'correlation': aligned_returns.corr().iloc[0, 1]
                        }
            except Exception as e:
                print(f"  Warning: Benchmark analysis failed: {e}")
        
        # Liquidity metrics
        liquidity = liquidity_score(primary_data['Volume'])
        
        # Compile results
        results = {
            'ticker': ticker,
            'analysis_period': {
                'start': primary_data.index[0].strftime('%Y-%m-%d'),
                'end': primary_data.index[-1].strftime('%Y-%m-%d'),
                'trading_days': len(primary_data)
            },
            'etf_info': etf_info,
            'data_quality': quality_score,
            'risk_metrics': risk_metrics,
            'benchmark_analysis': benchmark_analysis,
            'liquidity': liquidity,
            'price_summary': {
                'start_price': primary_data['Adj Close'].iloc[0],
                'end_price': primary_data['Adj Close'].iloc[-1],
                'total_return': (primary_data['Adj Close'].iloc[-1] / 
                               primary_data['Adj Close'].iloc[0] - 1),
                'min_price': primary_data['Adj Close'].min(),
                'max_price': primary_data['Adj Close'].max()
            }
        }
        
        return results
    
    def compare_etfs(self, tickers, start_date, end_date=None):
        """
        Compare multiple ETFs
        
        Parameters:
        -----------
        tickers : list
            List of ETF ticker symbols
        start_date : str or datetime
            Start date for comparison
        end_date : str or datetime, optional
            End date for comparison
        
        Returns:
        --------
        pd.DataFrame with comparison metrics
        """
        print(f"\nComparing {len(tickers)} ETFs...")
        
        results = []
        
        for ticker in tickers:
            try:
                analysis = self.analyze_etf(ticker, start_date, end_date, benchmark=None)
                
                results.append({
                    'Ticker': ticker,
                    'Name': analysis['etf_info'].get('name', ticker),
                    'Data Quality': analysis['data_quality']['grade'],
                    'Ann. Return': f"{analysis['risk_metrics']['annualized_return']:.2%}",
                    'Ann. Vol': f"{analysis['risk_metrics']['annualized_volatility']:.2%}",
                    'Sharpe Ratio': f"{analysis['risk_metrics']['sharpe_ratio']:.2f}",
                    'Max Drawdown': f"{analysis['risk_metrics']['max_drawdown']:.2%}",
                    'Expense Ratio': f"{analysis['etf_info'].get('expense_ratio', 0):.2%}" 
                        if analysis['etf_info'].get('expense_ratio') else 'N/A',
                    'Avg Volume': f"{analysis['liquidity']['avg_daily_volume']:,.0f}"
                })
            except Exception as e:
                print(f"  Error analyzing {ticker}: {e}")
                results.append({
                    'Ticker': ticker,
                    'Name': ticker,
                    'Data Quality': 'F',
                    'Error': str(e)
                })
        
        return pd.DataFrame(results)
    
    def get_correlation_matrix(self, tickers, start_date, end_date=None):
        """
        Calculate correlation matrix for multiple ETFs
        
        Returns:
        --------
        pd.DataFrame with correlation matrix
        """
        print(f"\nCalculating correlation matrix for {len(tickers)} ETFs...")
        
        returns_dict = {}
        
        for ticker in tickers:
            try:
                # Fetch data for correlation
                data_sources = self.fetch_etf_data(ticker, start_date, end_date)
                if data_sources:
                    data = list(data_sources.values())[0]
                    if not data.empty:
                        returns = calculate_returns(data['Adj Close'])
                        returns_dict[ticker] = returns
            except Exception as e:
                print(f"  Warning: Could not fetch {ticker}: {e}")
        
        if not returns_dict:
            raise ValueError("No data available for correlation calculation")
        
        returns_df = pd.DataFrame(returns_dict).dropna()
        correlation_matrix = returns_df.corr()
        
        return correlation_matrix
    
    def print_analysis_report(self, analysis_results):
        """
        Print formatted analysis report
        """
        results = analysis_results
        
        print("\n" + "="*70)
        print(f"ETF ANALYSIS REPORT: {results['ticker']}")
        print("="*70)
        
        print(f"\n📊 {results['etf_info']['name']}")
        print(f"Analysis Period: {results['analysis_period']['start']} to {results['analysis_period']['end']}")
        print(f"Trading Days: {results['analysis_period']['trading_days']}")
        
        print(f"\n📈 PERFORMANCE")
        print(f"  Total Return: {results['price_summary']['total_return']:.2%}")
        print(f"  Annualized Return: {results['risk_metrics']['annualized_return']:.2%}")
        print(f"  Annualized Volatility: {results['risk_metrics']['annualized_volatility']:.2%}")
        print(f"  Sharpe Ratio: {results['risk_metrics']['sharpe_ratio']:.2f}")
        print(f"  Max Drawdown: {results['risk_metrics']['max_drawdown']:.2%}")
        
        print(f"\n⚠️  RISK METRICS")
        print(f"  VaR (95%): {results['risk_metrics']['var_95']:.2%}")
        print(f"  CVaR (95%): {results['risk_metrics']['cvar_95']:.2%}")
        print(f"  Sortino Ratio: {results['risk_metrics']['sortino_ratio']:.2f}")
        print(f"  Skewness: {results['risk_metrics']['skewness']:.2f}")
        print(f"  Kurtosis: {results['risk_metrics']['kurtosis']:.2f}")
        
        if results['benchmark_analysis']:
            print(f"\n🎯 BENCHMARK COMPARISON ({results['benchmark_analysis']['benchmark_ticker']})")
            print(f"  Tracking Error: {results['benchmark_analysis']['tracking_error']:.2%}")
            print(f"  Tracking Difference: {results['benchmark_analysis']['tracking_difference']:.2%}")
            print(f"  Beta: {results['benchmark_analysis']['beta']:.2f}")
            print(f"  Correlation: {results['benchmark_analysis']['correlation']:.2f}")
        
        print(f"\n💧 LIQUIDITY")
        print(f"  Avg Daily Volume: {results['liquidity']['avg_daily_volume']:,.0f}")
        print(f"  Volume Consistency: {results['liquidity']['volume_consistency']:.2f}")
        
        print(f"\n✅ DATA QUALITY")
        print(f"  Overall Score: {results['data_quality']['total_score']:.1f}/100 (Grade: {results['data_quality']['grade']})")
        print(f"  Completeness: {results['data_quality']['completeness_details']['completeness_pct']:.1%}")
        print(f"  Anomalies Detected: {len(results['data_quality']['anomalies']['extreme_price_changes'])}")
        
        if results['etf_info'].get('expense_ratio'):
            print(f"\n💰 COSTS")
            print(f"  Expense Ratio: {results['etf_info']['expense_ratio']:.2%}")
        
        print("\n" + "="*70)
