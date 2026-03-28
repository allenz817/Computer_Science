"""
Utility functions for ETF Analytics
"""
import pandas as pd
import numpy as np
from datetime import datetime
import json


def format_currency(value):
    """Format value as currency"""
    if value >= 1e9:
        return f"${value/1e9:.2f}B"
    elif value >= 1e6:
        return f"${value/1e6:.2f}M"
    elif value >= 1e3:
        return f"${value/1e3:.2f}K"
    else:
        return f"${value:.2f}"


def format_percentage(value):
    """Format value as percentage"""
    return f"{value:.2%}"


def save_results_to_json(results, filename):
    """Save analysis results to JSON file"""
    # Convert numpy types to Python types for JSON serialization
    def convert(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Timestamp):
            return obj.strftime('%Y-%m-%d')
        return obj
    
    serializable_results = json.loads(
        json.dumps(results, default=convert)
    )
    
    with open(filename, 'w') as f:
        json.dump(serializable_results, f, indent=2)
    
    print(f"Results saved to {filename}")


def save_results_to_csv(comparison_df, filename):
    """Save comparison results to CSV"""
    comparison_df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")


def generate_trading_calendar(start_date, end_date):
    """
    Generate approximate US trading calendar
    (excludes weekends, but doesn't account for holidays)
    """
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')  # Business days
    return date_range


def calculate_rebalancing_dates(start_date, end_date, frequency='quarterly'):
    """
    Generate rebalancing dates
    
    Parameters:
    -----------
    start_date : str or datetime
        Start date
    end_date : str or datetime
        End date
    frequency : str
        'monthly', 'quarterly', 'semi-annual', or 'annual'
    
    Returns:
    --------
    list of dates
    """
    freq_map = {
        'monthly': 'M',
        'quarterly': 'Q',
        'semi-annual': '6M',
        'annual': 'A'
    }
    
    freq = freq_map.get(frequency, 'Q')
    dates = pd.date_range(start=start_date, end=end_date, freq=freq)
    
    return dates.tolist()


def merge_aligned_data(data_dict):
    """
    Merge data from multiple sources, aligned by date
    
    Parameters:
    -----------
    data_dict : dict
        Dictionary with source names as keys and DataFrames as values
    
    Returns:
    --------
    pd.DataFrame with multi-level columns
    """
    merged = pd.DataFrame()
    
    for source, data in data_dict.items():
        for col in data.columns:
            merged[(source, col)] = data[col]
    
    return merged


def calculate_portfolio_return(weights, returns):
    """
    Calculate portfolio returns given weights and individual returns
    
    Parameters:
    -----------
    weights : dict or pd.Series
        Portfolio weights (must sum to 1)
    returns : pd.DataFrame
        Returns for each asset
    
    Returns:
    --------
    pd.Series : Portfolio returns
    """
    if isinstance(weights, dict):
        weights = pd.Series(weights)
    
    # Ensure weights sum to 1
    weights = weights / weights.sum()
    
    # Calculate weighted returns
    portfolio_returns = (returns * weights).sum(axis=1)
    
    return portfolio_returns


def performance_attribution(portfolio_returns, benchmark_returns):
    """
    Simple performance attribution
    
    Returns:
    --------
    dict with attribution metrics
    """
    total_return = (1 + portfolio_returns).prod() - 1
    benchmark_total = (1 + benchmark_returns).prod() - 1
    
    excess_return = total_return - benchmark_total
    
    return {
        'portfolio_return': total_return,
        'benchmark_return': benchmark_total,
        'excess_return': excess_return,
        'information_ratio': excess_return / (portfolio_returns - benchmark_returns).std()
            if (portfolio_returns - benchmark_returns).std() != 0 else 0
    }
