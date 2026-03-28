"""
ETF-specific analysis functions
"""
import pandas as pd
import numpy as np
from config import TRADING_DAYS_PER_YEAR, RISK_FREE_RATE


def calculate_returns(prices, method='simple'):
    """
    Calculate returns from price series
    
    Parameters:
    -----------
    prices : pd.Series or pd.DataFrame
        Price data
    method : str
        'simple' or 'log' returns
    
    Returns:
    --------
    pd.Series or pd.DataFrame with returns
    """
    if method == 'log':
        return np.log(prices / prices.shift(1))
    else:
        return prices.pct_change()


def tracking_error(etf_returns, benchmark_returns, annualize=True):
    """
    Calculate tracking error - standard deviation of return differences
    
    Parameters:
    -----------
    etf_returns : pd.Series
        ETF daily returns
    benchmark_returns : pd.Series
        Benchmark daily returns
    annualize : bool
        Whether to annualize the tracking error
    
    Returns:
    --------
    float : Annualized tracking error
    """
    # Align the series
    aligned = pd.DataFrame({
        'etf': etf_returns,
        'benchmark': benchmark_returns
    }).dropna()
    
    # Calculate tracking difference
    tracking_diff = aligned['etf'] - aligned['benchmark']
    
    # Calculate standard deviation
    te = tracking_diff.std()
    
    if annualize:
        te = te * np.sqrt(TRADING_DAYS_PER_YEAR)
    
    return te


def tracking_difference(etf_returns, benchmark_returns, annualize=True):
    """
    Calculate tracking difference - mean return difference
    
    Parameters:
    -----------
    etf_returns : pd.Series
        ETF daily returns
    benchmark_returns : pd.Series
        Benchmark daily returns
    annualize : bool
        Whether to annualize the result
    
    Returns:
    --------
    float : Tracking difference
    """
    aligned = pd.DataFrame({
        'etf': etf_returns,
        'benchmark': benchmark_returns
    }).dropna()
    
    td = (aligned['etf'] - aligned['benchmark']).mean()
    
    if annualize:
        td = td * TRADING_DAYS_PER_YEAR
    
    return td


def expense_adjusted_returns(returns, expense_ratio, frequency='daily'):
    """
    Adjust returns for expense ratio
    
    Parameters:
    -----------
    returns : pd.Series
        Returns series
    expense_ratio : float
        Annual expense ratio (e.g., 0.0009 for 0.09%)
    frequency : str
        'daily', 'monthly', or 'annual'
    
    Returns:
    --------
    pd.Series : Expense-adjusted returns
    """
    if frequency == 'daily':
        daily_expense = expense_ratio / TRADING_DAYS_PER_YEAR
    elif frequency == 'monthly':
        daily_expense = expense_ratio / 12
    else:  # annual
        daily_expense = expense_ratio
    
    return returns - daily_expense


def premium_discount(nav, market_price):
    """
    Calculate premium/discount to NAV
    
    Parameters:
    -----------
    nav : pd.Series
        Net Asset Value series
    market_price : pd.Series
        Market price series
    
    Returns:
    --------
    pd.Series : Premium (+) or Discount (-) percentages
    """
    return (market_price - nav) / nav


def liquidity_score(volume, avg_volume_period=20):
    """
    Calculate liquidity score based on trading volume
    
    Parameters:
    -----------
    volume : pd.Series
        Daily volume series
    avg_volume_period : int
        Period for moving average
    
    Returns:
    --------
    float : Average daily volume and liquidity metrics
    """
    avg_volume = volume.rolling(window=avg_volume_period).mean()
    
    return {
        'avg_daily_volume': volume.mean(),
        'median_volume': volume.median(),
        'volume_std': volume.std(),
        'volume_consistency': 1 - (volume.std() / volume.mean())  # Lower std = more consistent
    }


def calculate_beta(etf_returns, market_returns):
    """
    Calculate beta relative to market
    
    Parameters:
    -----------
    etf_returns : pd.Series
        ETF returns
    market_returns : pd.Series
        Market returns
    
    Returns:
    --------
    float : Beta coefficient
    """
    # Align series
    aligned = pd.DataFrame({
        'etf': etf_returns,
        'market': market_returns
    }).dropna()
    
    # Calculate covariance and variance
    covariance = aligned['etf'].cov(aligned['market'])
    market_variance = aligned['market'].var()
    
    beta = covariance / market_variance
    
    return beta


def holdings_overlap(holdings1, holdings2, top_n=None):
    """
    Calculate overlap between two ETF holdings
    
    Parameters:
    -----------
    holdings1 : dict or list
        First ETF holdings
    holdings2 : dict or list
        Second ETF holdings
    top_n : int, optional
        Consider only top N holdings
    
    Returns:
    --------
    dict with overlap metrics
    """
    # Convert to sets for comparison
    if isinstance(holdings1, dict):
        set1 = set(list(holdings1.keys())[:top_n] if top_n else holdings1.keys())
    else:
        set1 = set(holdings1[:top_n] if top_n else holdings1)
    
    if isinstance(holdings2, dict):
        set2 = set(list(holdings2.keys())[:top_n] if top_n else holdings2.keys())
    else:
        set2 = set(holdings2[:top_n] if top_n else holdings2)
    
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    overlap_pct = len(intersection) / len(union) if union else 0
    
    return {
        'common_holdings': list(intersection),
        'overlap_percentage': overlap_pct,
        'unique_to_first': list(set1 - set2),
        'unique_to_second': list(set2 - set1)
    }


def tax_efficiency_score(distributions, capital_gains, price_appreciation):
    """
    Calculate tax efficiency score
    
    Parameters:
    -----------
    distributions : pd.Series
        Distribution payments
    capital_gains : pd.Series
        Capital gains distributions
    price_appreciation : float
        Total price appreciation
    
    Returns:
    --------
    float : Tax efficiency score (higher is better)
    """
    total_distributions = distributions.sum() + capital_gains.sum()
    
    if price_appreciation + total_distributions == 0:
        return 0
    
    # Higher score when more returns come from price appreciation vs distributions
    efficiency = price_appreciation / (price_appreciation + total_distributions)
    
    return efficiency
