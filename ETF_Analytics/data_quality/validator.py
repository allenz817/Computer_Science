"""
Data quality validation and scoring module
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config import QUALITY_THRESHOLDS


class DataQualityValidator:
    """Validates and scores data quality from multiple sources"""
    
    def __init__(self):
        self.thresholds = QUALITY_THRESHOLDS
        
    def validate_completeness(self, data, start_date, end_date):
        """
        Check data completeness
        
        Returns:
        --------
        dict with completeness metrics
        """
        # Calculate expected trading days (approximately)
        total_days = (pd.to_datetime(end_date) - pd.to_datetime(start_date)).days
        expected_trading_days = total_days * (5/7)  # Rough estimate
        
        actual_days = len(data)
        completeness_pct = actual_days / expected_trading_days if expected_trading_days > 0 else 0
        
        # Check for gaps
        date_diffs = data.index.to_series().diff()
        large_gaps = date_diffs[date_diffs > timedelta(days=7)]
        
        # Count missing values
        missing_values = data.isnull().sum()
        missing_pct = (missing_values / len(data)).to_dict()
        
        return {
            'actual_data_points': actual_days,
            'expected_data_points': int(expected_trading_days),
            'completeness_pct': completeness_pct,
            'large_gaps_count': len(large_gaps),
            'missing_values': missing_pct,
            'passes_threshold': actual_days >= self.thresholds['min_data_points']
        }
    
    def detect_anomalies(self, data):
        """
        Detect price and volume anomalies
        
        Returns:
        --------
        dict with anomaly information
        """
        anomalies = {
            'extreme_price_changes': [],
            'volume_spikes': [],
            'negative_prices': [],
            'ohlc_violations': []
        }
        
        # Calculate daily returns
        returns = data['Close'].pct_change()
        
        # Extreme price changes
        extreme_changes = returns[abs(returns) > self.thresholds['price_change_threshold']]
        if not extreme_changes.empty:
            anomalies['extreme_price_changes'] = extreme_changes.to_dict()
        
        # Volume spikes
        avg_volume = data['Volume'].rolling(window=20).mean()
        volume_ratio = data['Volume'] / avg_volume
        volume_spikes = volume_ratio[volume_ratio > self.thresholds['volume_spike_threshold']]
        if not volume_spikes.empty:
            anomalies['volume_spikes'] = volume_spikes.to_dict()
        
        # Negative prices
        negative_prices = data[(data[['Open', 'High', 'Low', 'Close']] < 0).any(axis=1)]
        if not negative_prices.empty:
            anomalies['negative_prices'] = negative_prices.index.tolist()
        
        # OHLC violations
        ohlc_violations = data[
            (data['High'] < data['Low']) | 
            (data['Close'] > data['High']) |
            (data['Close'] < data['Low']) |
            (data['Open'] > data['High']) |
            (data['Open'] < data['Low'])
        ]
        if not ohlc_violations.empty:
            anomalies['ohlc_violations'] = ohlc_violations.index.tolist()
        
        return anomalies
    
    def cross_validate_sources(self, data_dict):
        """
        Cross-validate data from multiple sources
        
        Parameters:
        -----------
        data_dict : dict
            Dictionary with source names as keys and DataFrames as values
        
        Returns:
        --------
        dict with validation results
        """
        if len(data_dict) < 2:
            return {'status': 'insufficient_sources', 'correlation': None}
        
        # Align all data sources to common dates
        common_dates = None
        for source, data in data_dict.items():
            if common_dates is None:
                common_dates = set(data.index)
            else:
                common_dates = common_dates.intersection(set(data.index))
        
        common_dates = sorted(list(common_dates))
        
        if len(common_dates) < 10:
            return {'status': 'insufficient_overlap', 'correlation': None}
        
        # Extract close prices for comparison
        close_prices = pd.DataFrame()
        for source, data in data_dict.items():
            close_prices[source] = data.loc[common_dates, 'Close']
        
        # Calculate correlations
        correlations = close_prices.corr()
        
        # Calculate price differences
        price_diffs = {}
        sources = list(data_dict.keys())
        for i in range(len(sources)):
            for j in range(i+1, len(sources)):
                s1, s2 = sources[i], sources[j]
                diff_pct = abs((close_prices[s1] - close_prices[s2]) / close_prices[s1]).mean()
                price_diffs[f"{s1}_vs_{s2}"] = diff_pct
        
        # Determine if validation passes
        min_correlation = correlations.min().min()
        passes = min_correlation >= self.thresholds['correlation_threshold']
        
        return {
            'status': 'validated' if passes else 'correlation_low',
            'correlation_matrix': correlations.to_dict(),
            'min_correlation': min_correlation,
            'avg_price_differences': price_diffs,
            'common_data_points': len(common_dates),
            'passes_threshold': passes
        }
    
    def calculate_quality_score(self, data, start_date, end_date, 
                                validation_result=None, anomalies=None):
        """
        Calculate overall data quality score (0-100)
        
        Parameters:
        -----------
        data : pd.DataFrame
            Price data
        start_date : str or datetime
            Start date of analysis
        end_date : str or datetime
            End date of analysis
        validation_result : dict, optional
            Cross-validation results
        anomalies : dict, optional
            Anomaly detection results
        
        Returns:
        --------
        dict with quality score and components
        """
        score_components = {}
        
        # Completeness score (40 points)
        completeness = self.validate_completeness(data, start_date, end_date)
        completeness_score = min(40, completeness['completeness_pct'] * 40)
        score_components['completeness'] = completeness_score
        
        # Anomaly score (30 points)
        if anomalies is None:
            anomalies = self.detect_anomalies(data)
        
        anomaly_count = (
            len(anomalies['extreme_price_changes']) +
            len(anomalies['volume_spikes']) +
            len(anomalies['negative_prices']) +
            len(anomalies['ohlc_violations'])
        )
        anomaly_score = max(0, 30 - (anomaly_count * 2))  # -2 points per anomaly
        score_components['anomaly_free'] = anomaly_score
        
        # Validation score (30 points)
        if validation_result and validation_result.get('passes_threshold'):
            validation_score = 30
        elif validation_result and validation_result.get('min_correlation'):
            validation_score = validation_result['min_correlation'] * 30
        else:
            validation_score = 15  # Moderate score if no validation
        score_components['cross_validation'] = validation_score
        
        total_score = sum(score_components.values())
        
        return {
            'total_score': round(total_score, 2),
            'grade': self._score_to_grade(total_score),
            'components': score_components,
            'completeness_details': completeness,
            'anomalies': anomalies,
            'validation': validation_result
        }
    
    def _score_to_grade(self, score):
        """Convert numeric score to letter grade"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
