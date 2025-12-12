import pandas as pd
import numpy as np
import requests
from io import StringIO
from typing import Dict, Any, Tuple
import os

class DatasetLoader:
    def __init__(self):
        self.datasets = {}
        self.data_dir = "data/raw"
        os.makedirs(self.data_dir, exist_ok=True)
        
    async def load_sensor_faults_dataset(self) -> pd.DataFrame:
        file_path = os.path.join(self.data_dir, 'sensor_faults.csv')
        
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = self._generate_sensor_faults_data()
            df.to_csv(file_path, index=False)
        
        df = self._preprocess_sensor_faults(df)
        self.datasets['sensor_faults'] = df
        return df
    
    def _generate_sensor_faults_data(self) -> pd.DataFrame:
        n_samples = 10000
        
        np.random.seed(42)
        
        temperature = np.random.normal(60, 15, n_samples)
        vibration = np.random.normal(0.4, 0.2, n_samples)
        pressure = np.random.normal(60, 15, n_samples)
        power_consumption = np.random.normal(45, 15, n_samples)
        
        fault_indices = np.random.choice(n_samples, size=int(n_samples * 0.15), replace=False)
        
        temperature[fault_indices] = np.random.normal(90, 10, len(fault_indices))
        vibration[fault_indices] = np.random.normal(0.85, 0.1, len(fault_indices))
        pressure[fault_indices] = np.random.choice([np.random.normal(15, 5, 1)[0], np.random.normal(110, 10, 1)[0]], len(fault_indices))
        power_consumption[fault_indices] = np.random.normal(80, 10, len(fault_indices))
        
        is_anomaly = np.zeros(n_samples, dtype=int)
        is_anomaly[fault_indices] = 1
        
        df = pd.DataFrame({
            'temperature': temperature,
            'vibration': vibration,
            'pressure': pressure,
            'power_consumption': power_consumption,
            'is_anomaly': is_anomaly,
            'timestamp': pd.date_range('2024-01-01', periods=n_samples, freq='1min')
        })
        
        return df
    
    def _preprocess_sensor_faults(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna()
        
        df['temperature'] = df['temperature'].clip(0, 150)
        df['vibration'] = df['vibration'].clip(0, 2)
        df['pressure'] = df['pressure'].clip(0, 150)
        df['power_consumption'] = df['power_consumption'].clip(0, 150)
        
        return df
    
    async def load_failure_dataset(self) -> pd.DataFrame:
        file_path = os.path.join(self.data_dir, 'failure_data.csv')
        
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = self._generate_failure_data()
            df.to_csv(file_path, index=False)
        
        df = self._preprocess_failure_data(df)
        self.datasets['failure_data'] = df
        return df
    
    def _generate_failure_data(self) -> pd.DataFrame:
        n_machines = 500
        
        np.random.seed(42)
        
        data = []
        for i in range(n_machines):
            n_cycles = np.random.randint(50, 200)
            
            temp_trend = np.linspace(60, 90, n_cycles) + np.random.normal(0, 5, n_cycles)
            vibe_trend = np.linspace(0.3, 0.8, n_cycles) + np.random.normal(0, 0.1, n_cycles)
            
            for cycle in range(n_cycles):
                failure_prob = min(1.0, cycle / n_cycles * 1.2)
                
                data.append({
                    'machine_id': f'M{i:04d}',
                    'cycle': cycle,
                    'temperature': temp_trend[cycle],
                    'vibration': vibe_trend[cycle],
                    'pressure': np.random.normal(60, 10),
                    'power_consumption': np.random.normal(50, 15),
                    'failure_probability': failure_prob,
                    'remaining_useful_life': n_cycles - cycle
                })
        
        return pd.DataFrame(data)
    
    def _preprocess_failure_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.sort_values(['machine_id', 'cycle'])
        
        df['temperature_mean'] = df.groupby('machine_id')['temperature'].transform(lambda x: x.rolling(10, min_periods=1).mean())
        df['temperature_std'] = df.groupby('machine_id')['temperature'].transform(lambda x: x.rolling(10, min_periods=1).std().fillna(0))
        df['temperature_max'] = df.groupby('machine_id')['temperature'].transform(lambda x: x.rolling(10, min_periods=1).max())
        
        df['vibration_mean'] = df.groupby('machine_id')['vibration'].transform(lambda x: x.rolling(10, min_periods=1).mean())
        df['vibration_std'] = df.groupby('machine_id')['vibration'].transform(lambda x: x.rolling(10, min_periods=1).std().fillna(0))
        df['vibration_max'] = df.groupby('machine_id')['vibration'].transform(lambda x: x.rolling(10, min_periods=1).max())
        
        df['high_temp_count'] = df.groupby('machine_id')['temperature'].transform(lambda x: (x.rolling(10, min_periods=1).apply(lambda y: (y > 80).sum())))
        df['high_vibe_count'] = df.groupby('machine_id')['vibration'].transform(lambda x: (x.rolling(10, min_periods=1).apply(lambda y: (y > 0.7).sum())))
        
        return df
    
    async def load_vibration_dataset(self) -> pd.DataFrame:
        file_path = os.path.join(self.data_dir, 'vibration_data.csv')
        
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            df = self._generate_vibration_data()
            df.to_csv(file_path, index=False)
        
        self.datasets['vibration_data'] = df
        return df
    
    def _generate_vibration_data(self) -> pd.DataFrame:
        n_samples = 5000
        
        np.random.seed(42)
        
        healthy_vibration = np.random.normal(0.3, 0.05, n_samples // 2)
        faulty_vibration = np.random.normal(0.8, 0.15, n_samples // 2)
        
        vibration = np.concatenate([healthy_vibration, faulty_vibration])
        labels = np.concatenate([np.zeros(n_samples // 2), np.ones(n_samples // 2)])
        
        bearing_condition = ['healthy'] * (n_samples // 2) + ['faulty'] * (n_samples // 2)
        
        df = pd.DataFrame({
            'vibration_amplitude': vibration,
            'is_faulty': labels.astype(int),
            'bearing_condition': bearing_condition,
            'frequency_hz': np.random.uniform(50, 200, n_samples),
            'timestamp': pd.date_range('2024-01-01', periods=n_samples, freq='10s')
        })
        
        return df
    
    async def load_all_datasets(self) -> Dict[str, pd.DataFrame]:
        sensor_faults = await self.load_sensor_faults_dataset()
        failure_data = await self.load_failure_dataset()
        vibration_data = await self.load_vibration_dataset()
        
        return {
            'sensor_faults': sensor_faults,
            'failure_data': failure_data,
            'vibration_data': vibration_data
        }