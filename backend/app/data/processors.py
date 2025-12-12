import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime, timedelta

class DataProcessor:
    def __init__(self):
        self.processing_stats = {}
        
    def process_sensor_stream(self, sensor_readings: List[Dict[str, Any]]) -> pd.DataFrame:
        df = pd.DataFrame(sensor_readings)
        
        if 'timestamp' not in df.columns:
            df['timestamp'] = pd.date_range(end=datetime.utcnow(), periods=len(df), freq='1min')
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        numeric_cols = ['temperature', 'vibration', 'pressure', 'power_consumption']
        for col in numeric_cols:
            if col in df.columns:
                df[f'{col}_ma5'] = df[col].rolling(window=5, min_periods=1).mean()
                df[f'{col}_std5'] = df[col].rolling(window=5, min_periods=1).std().fillna(0)
        
        return df
    
    def extract_features(self, df: pd.DataFrame, window_size: int = 10) -> pd.DataFrame:
        features = df.copy()
        
        for col in ['temperature', 'vibration', 'pressure', 'power_consumption']:
            if col in df.columns:
                features[f'{col}_mean'] = df[col].rolling(window=window_size, min_periods=1).mean()
                features[f'{col}_std'] = df[col].rolling(window=window_size, min_periods=1).std().fillna(0)
                features[f'{col}_max'] = df[col].rolling(window=window_size, min_periods=1).max()
                features[f'{col}_min'] = df[col].rolling(window=window_size, min_periods=1).min()
                features[f'{col}_range'] = features[f'{col}_max'] - features[f'{col}_min']
        
        return features
    
    def detect_outliers(self, df: pd.DataFrame, column: str, threshold: float = 3.0) -> pd.Series:
        mean = df[column].mean()
        std = df[column].std()
        
        z_scores = np.abs((df[column] - mean) / std)
        return z_scores > threshold
    
    def aggregate_by_machine(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'machine_id' not in df.columns:
            return df
        
        agg_dict = {
            'temperature': ['mean', 'std', 'max', 'min'],
            'vibration': ['mean', 'std', 'max', 'min'],
            'pressure': ['mean', 'std', 'max', 'min'],
            'power_consumption': ['mean', 'std', 'max', 'min']
        }
        
        available_agg_dict = {k: v for k, v in agg_dict.items() if k in df.columns}
        
        if available_agg_dict:
            aggregated = df.groupby('machine_id').agg(available_agg_dict)
            aggregated.columns = ['_'.join(col).strip() for col in aggregated.columns.values]
            return aggregated.reset_index()
        
        return df
    
    def normalize_features(self, df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        normalized = df.copy()
        
        for col in columns:
            if col in df.columns:
                min_val = df[col].min()
                max_val = df[col].max()
                
                if max_val > min_val:
                    normalized[col] = (df[col] - min_val) / (max_val - min_val)
                else:
                    normalized[col] = 0
        
        return normalized
    
    def create_time_features(self, df: pd.DataFrame, timestamp_col: str = 'timestamp') -> pd.DataFrame:
        if timestamp_col not in df.columns:
            return df
        
        df = df.copy()
        df[timestamp_col] = pd.to_datetime(df[timestamp_col])
        
        df['hour'] = df[timestamp_col].dt.hour
        df['day_of_week'] = df[timestamp_col].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_business_hours'] = df['hour'].between(8, 17).astype(int)
        
        return df