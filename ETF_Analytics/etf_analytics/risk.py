"""
Risk analysis functions for ETFs
"""
import pandas as pd
import numpy as np
from config import TRADING_DAYS_PER_YEAR, RISK_FREE_RATE


def annualized_return(returns, periods_per_year=TRADING_DAYS_PER_YEAR):
    """Calculate annualized return from periodic returns"""
    total_return = (1 + returns).prod()
    n_periods = len(returns)
    years = n_periods / periods_per_year
    
    return (total_return ** (1/years)) - 1


def annualized_volatility(returns, periods_per_year=TRADING_DAYS_PER_YEAR):
    """Calculate annualized volatility"""
    return returns.std() * np.sqrt(periods_per_year)


def sharpe_ratio(returns, risk_free_rate=RISK_FREE_RATE, 
                 periods_per_year=TRADING_DAYS_PER_YEAR):
    """
    Calculate Sharpe ratio
    
    Parameters:
    -----------
    returns : pd.Series
        Return series
    risk_free_rate : float
        Annual risk-free rate
    periods_per_year : int
        Number of periods per year
    
    Returns:
    --------
    float : Sharpe ratio
    """
    excess_returns = returns - (risk_free_rate / periods_per_year)
    
    if excess_returns.std() == 0:
        return 0
    
    return np.sqrt(periods_per_year) * excess_returns.mean() / excess_returns.std()


def sortino_ratio(returns, risk_free_rate=RISK_FREE_RATE,
                  periods_per_year=TRADING_DAYS_PER_YEAR):
    """
    Calculate Sortino ratio (uses downside deviation)
    """
    excess_returns = returns - (risk_free_rate / periods_per_year)
    downside_returns = excess_returns[excess_returns < 0]
    
    if len(downside_returns) == 0 or downside_returns.std() == 0:
        return 0
    
    downside_std = downside_returns.std()
    
    return np.sqrt(periods_per_year) * excess_returns.mean() / downside_std


def maximum_drawdown(returns):
    """
    Calculate maximum drawdown
    
    Returns:
    --------
    dict with max drawdown, peak, trough dates
    """
    cumulative = (1 + returns).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    
    max_dd = drawdown.min()
    max_dd_date = drawdown.idxmin()
    
    # Find peak before drawdown
    peak_date = running_max[:max_dd_date].idxmax()
    
    return {
        'max_drawdown': max_dd,
        'peak_date': peak_date,
        'trough_date': max_dd_date
    }


def value_at_risk(returns, confidence_level=0.95, method='historical'):
    """
    Calculate Value at Risk
    
    Parameters:
    -----------
    returns : pd.Series
        Return series
    confidence_level : float
        Confidence level (e.g., 0.95 for 95%)
    method : str
        'historical' or 'parametric'
    
    Returns:
    --------
    float : VaR (negative number representing loss)
    """
    if method == 'historical':
        return returns.quantile(1 - confidence_level)
    else:  # parametric
        mean = returns.mean()
        std = returns.std()
        z_score = -1.645 if confidence_level == 0.95 else -2.326  # 95% or 99%
        return mean + z_score * std


def conditional_var(returns, confidence_level=0.95):
    """
    Calculate Conditional Value at Risk (Expected Shortfall)
    
    Returns:
    --------
    float : CVaR - average of returns below VaR threshold
    """
    var = value_at_risk(returns, confidence_level, method='historical')
    return returns[returns <= var].mean()


def downside_risk(returns, threshold=0):
    """
    Calculate downside risk (semi-deviation)
    
    Parameters:
    -----------
    returns : pd.Series
        Return series
    threshold : float
        Minimum acceptable return (default 0)
    
    Returns:
    --------
    float : Downside risk
    """
    downside_returns = returns[returns < threshold]
    return downside_returns.std()


def calmar_ratio(returns, periods_per_year=TRADING_DAYS_PER_YEAR):
    """
    Calculate Calmar ratio (return / max drawdown)
    """
    ann_return = annualized_return(returns, periods_per_year)
    max_dd = maximum_drawdown(returns)['max_drawdown']
    
    if max_dd == 0:
        return 0
    
    return ann_return / abs(max_dd)


def skewness(returns):
    """Calculate skewness of returns"""
    return returns.skew()


def kurtosis(returns):
    """Calculate excess kurtosis of returns"""
    return returns.kurtosis()


def risk_metrics_summary(returns, risk_free_rate=RISK_FREE_RATE):
    """
    Calculate comprehensive risk metrics
    
    Returns:
    --------
    dict with all risk metrics
    """
    return {
        'annualized_return': annualized_return(returns),
        'annualized_volatility': annualized_volatility(returns),
        'sharpe_ratio': sharpe_ratio(returns, risk_free_rate),
        'sortino_ratio': sortino_ratio(returns, risk_free_rate),
        'max_drawdown': maximum_drawdown(returns)['max_drawdown'],
        'var_95': value_at_risk(returns, 0.95),
        'cvar_95': conditional_var(returns, 0.95),
        'downside_risk': downside_risk(returns),
        'calmar_ratio': calmar_ratio(returns),
        'skewness': skewness(returns),
        'kurtosis': kurtosis(returns)
    }
