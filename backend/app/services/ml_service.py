import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
from typing import Dict, Any, List, Tuple
from datetime import datetime

class MLService:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.model_dir = "ml_models/saved"
        os.makedirs(self.model_dir, exist_ok=True)
        
    async def train_anomaly_detector(self, training_data: pd.DataFrame) -> Dict[str, Any]:
        features = ['temperature', 'vibration', 'pressure', 'power_consumption']
        X = training_data[features].values
        y = training_data['is_anomaly'].values
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=10,
            min_samples_leaf=5,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        self.models['anomaly_detector'] = model
        self.scalers['anomaly_detector'] = scaler
        
        model_path = os.path.join(self.model_dir, 'anomaly_detector.pkl')
        scaler_path = os.path.join(self.model_dir, 'anomaly_detector_scaler.pkl')
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        
        return {
            "model_name": "anomaly_detector",
            "train_accuracy": train_score,
            "test_accuracy": test_score,
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "feature_importance": dict(zip(features, model.feature_importances_)),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def train_failure_predictor(self, training_data: pd.DataFrame) -> Dict[str, Any]:
        features = ['temperature_mean', 'temperature_std', 'temperature_max',
                   'vibration_mean', 'vibration_std', 'vibration_max',
                   'high_temp_count', 'high_vibe_count']
        X = training_data[features].values
        y = training_data['failure_probability'].values
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        model = GradientBoostingRegressor(
            n_estimators=150,
            learning_rate=0.1,
            max_depth=8,
            min_samples_split=10,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        self.models['failure_predictor'] = model
        self.scalers['failure_predictor'] = scaler
        
        model_path = os.path.join(self.model_dir, 'failure_predictor.pkl')
        scaler_path = os.path.join(self.model_dir, 'failure_predictor_scaler.pkl')
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        
        return {
            "model_name": "failure_predictor",
            "train_r2_score": train_score,
            "test_r2_score": test_score,
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "feature_importance": dict(zip(features, model.feature_importances_)),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def train_rul_estimator(self, training_data: pd.DataFrame) -> Dict[str, Any]:
        features = ['cycle', 'temperature', 'vibration', 'pressure', 'power_consumption']
        X = training_data[features].values
        y = training_data['remaining_useful_life'].values
        
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        model = GradientBoostingRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=10,
            min_samples_split=15,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        y_pred = model.predict(X_test)
        mae = np.mean(np.abs(y_test - y_pred))
        rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
        
        self.models['rul_estimator'] = model
        self.scalers['rul_estimator'] = scaler
        
        model_path = os.path.join(self.model_dir, 'rul_estimator.pkl')
        scaler_path = os.path.join(self.model_dir, 'rul_estimator_scaler.pkl')
        joblib.dump(model, model_path)
        joblib.dump(scaler, scaler_path)
        
        return {
            "model_name": "rul_estimator",
            "train_r2_score": train_score,
            "test_r2_score": test_score,
            "mae": mae,
            "rmse": rmse,
            "training_samples": len(X_train),
            "test_samples": len(X_test),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def predict_anomaly(self, sensor_data: Dict[str, float]) -> Dict[str, Any]:
        if 'anomaly_detector' not in self.models:
            self.load_model('anomaly_detector')
        
        features = np.array([[
            sensor_data.get('temperature', 0),
            sensor_data.get('vibration', 0),
            sensor_data.get('pressure', 0),
            sensor_data.get('power_consumption', 0)
        ]])
        
        scaler = self.scalers['anomaly_detector']
        features_scaled = scaler.transform(features)
        
        model = self.models['anomaly_detector']
        prediction = model.predict(features_scaled)[0]
        probabilities = model.predict_proba(features_scaled)[0]
        
        return {
            "is_anomaly": bool(prediction),
            "anomaly_score": float(probabilities[1]),
            "confidence": float(max(probabilities)),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def predict_failure(self, historical_features: Dict[str, float]) -> Dict[str, Any]:
        if 'failure_predictor' not in self.models:
            self.load_model('failure_predictor')
        
        features = np.array([[
            historical_features.get('temperature_mean', 0),
            historical_features.get('temperature_std', 0),
            historical_features.get('temperature_max', 0),
            historical_features.get('vibration_mean', 0),
            historical_features.get('vibration_std', 0),
            historical_features.get('vibration_max', 0),
            historical_features.get('high_temp_count', 0),
            historical_features.get('high_vibe_count', 0)
        ]])
        
        scaler = self.scalers['failure_predictor']
        features_scaled = scaler.transform(features)
        
        model = self.models['failure_predictor']
        failure_prob = model.predict(features_scaled)[0]
        
        return {
            "failure_probability": float(failure_prob),
            "risk_level": self._classify_risk_level(failure_prob),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def estimate_rul(self, machine_data: Dict[str, float]) -> Dict[str, Any]:
        if 'rul_estimator' not in self.models:
            self.load_model('rul_estimator')
        
        features = np.array([[
            machine_data.get('cycle', 0),
            machine_data.get('temperature', 0),
            machine_data.get('vibration', 0),
            machine_data.get('pressure', 0),
            machine_data.get('power_consumption', 0)
        ]])
        
        scaler = self.scalers['rul_estimator']
        features_scaled = scaler.transform(features)
        
        model = self.models['rul_estimator']
        rul_hours = model.predict(features_scaled)[0]
        
        return {
            "remaining_useful_life_hours": float(rul_hours),
            "estimated_days": float(rul_hours / 24),
            "maintenance_recommended": rul_hours < 168,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def load_model(self, model_name: str):
        model_path = os.path.join(self.model_dir, f'{model_name}.pkl')
        scaler_path = os.path.join(self.model_dir, f'{model_name}_scaler.pkl')
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            self.models[model_name] = joblib.load(model_path)
            self.scalers[model_name] = joblib.load(scaler_path)
        else:
            raise FileNotFoundError(f"Model {model_name} not found")
    
    def _classify_risk_level(self, probability: float) -> str:
        if probability >= 0.8:
            return "critical"
        elif probability >= 0.6:
            return "high"
        elif probability >= 0.4:
            return "medium"
        else:
            return "low"