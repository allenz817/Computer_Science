"""
ETF analytics package - ETF-specific metrics and risk analysis
"""
from .metrics import (
    calculate_returns,
    tracking_error,
    tracking_difference,
    expense_adjusted_returns,
    premium_discount,
    liquidity_score,
    calculate_beta,
    holdings_overlap,
    tax_efficiency_score
)

from .risk import (
    annualized_return,
    annualized_volatility,
    sharpe_ratio,
    sortino_ratio,
    maximum_drawdown,
    value_at_risk,
    conditional_var,
    downside_risk,
    calmar_ratio,
    skewness,
    kurtosis,
    risk_metrics_summary
)

__all__ = [
    # Metrics
    'calculate_returns',
    'tracking_error',
    'tracking_difference',
    'expense_adjusted_returns',
    'premium_discount',
    'liquidity_score',
    'calculate_beta',
    'holdings_overlap',
    'tax_efficiency_score',
    # Risk
    'annualized_return',
    'annualized_volatility',
    'sharpe_ratio',
    'sortino_ratio',
    'maximum_drawdown',
    'value_at_risk',
    'conditional_var',
    'downside_risk',
    'calmar_ratio',
    'skewness',
    'kurtosis',
    'risk_metrics_summary'
]
