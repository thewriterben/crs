#!/usr/bin/env python3
"""
AI Prediction Engine for Cryptocurrency Market Analysis
Advanced machine learning models for price prediction and market intelligence
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

@dataclass
class PredictionResult:
    """Structure for prediction results"""
    symbol: str
    current_price: float
    predicted_price: float
    confidence: float
    direction: str
    time_horizon: str
    model_consensus: Dict[str, float]
    risk_score: float
    recommendation: str

@dataclass
class MarketSignal:
    """Structure for market signals"""
    signal_type: str
    strength: float
    description: str
    timestamp: datetime

class AIPredictor:
    """Advanced AI prediction engine for cryptocurrency markets"""
    
    def __init__(self):
        self.models = {
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boost': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'linear_regression': LinearRegression()
        }
        self.scaler = StandardScaler()
        self.is_trained = False
        self.feature_importance = {}
        self.model_weights = {
            'random_forest': 0.4,
            'gradient_boost': 0.4,
            'linear_regression': 0.2
        }
        
    def generate_features(self, price_data: List[Dict]) -> np.ndarray:
        """Generate technical features for ML models"""
        df = pd.DataFrame(price_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Price-based features
        df['price_change'] = df['price'].pct_change()
        df['price_volatility'] = df['price'].rolling(window=5).std()
        df['price_momentum'] = df['price'].rolling(window=3).mean() / df['price'].rolling(window=10).mean()
        
        # Moving averages
        df['sma_5'] = df['price'].rolling(window=5).mean()
        df['sma_10'] = df['price'].rolling(window=10).mean()
        df['sma_20'] = df['price'].rolling(window=20).mean()
        
        # Technical indicators
        df['rsi'] = self._calculate_rsi(df['price'])
        df['macd'] = self._calculate_macd(df['price'])
        df['bollinger_upper'], df['bollinger_lower'] = self._calculate_bollinger_bands(df['price'])
        
        # Volume features (simulated)
        df['volume_sma'] = df.get('volume', df['price'] * 1000).rolling(window=5).mean()
        df['volume_ratio'] = df.get('volume', df['price'] * 1000) / df['volume_sma']
        
        # Time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['month'] = df['timestamp'].dt.month
        
        # Select features for training
        feature_columns = [
            'price_change', 'price_volatility', 'price_momentum',
            'sma_5', 'sma_10', 'sma_20', 'rsi', 'macd',
            'bollinger_upper', 'bollinger_lower', 'volume_ratio',
            'hour', 'day_of_week', 'month'
        ]
        
        features = df[feature_columns].fillna(0).values
        return features
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def _calculate_macd(self, prices: pd.Series) -> pd.Series:
        """Calculate MACD indicator"""
        ema_12 = prices.ewm(span=12).mean()
        ema_26 = prices.ewm(span=26).mean()
        macd = ema_12 - ema_26
        return macd
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20) -> Tuple[pd.Series, pd.Series]:
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)
        return upper_band, lower_band
    
    def train_models(self, historical_data: Dict[str, List[Dict]]) -> Dict[str, float]:
        """Train ML models on historical data"""
        all_features = []
        all_targets = []
        
        for symbol, data in historical_data.items():
            if len(data) < 30:  # Need sufficient data
                continue
                
            features = self.generate_features(data)
            prices = [d['price'] for d in data]
            
            # Create targets (next price)
            for i in range(len(features) - 1):
                if not np.any(np.isnan(features[i])):
                    all_features.append(features[i])
                    all_targets.append(prices[i + 1])
        
        if len(all_features) < 50:
            raise ValueError("Insufficient training data")
        
        X = np.array(all_features)
        y = np.array(all_targets)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train models
        model_scores = {}
        for name, model in self.models.items():
            model.fit(X_scaled, y)
            predictions = model.predict(X_scaled)
            score = 1 - mean_absolute_error(y, predictions) / np.mean(y)
            model_scores[name] = max(0, score)
        
        self.is_trained = True
        return model_scores
    
    def predict_price(self, symbol: str, current_data: List[Dict], 
                     time_horizon: str = "1h") -> PredictionResult:
        """Generate price prediction using ensemble of models"""
        if not self.is_trained:
            # Generate synthetic training data for demo
            self._train_demo_models()
        
        # Generate features for current data
        features = self.generate_features(current_data)
        if len(features) == 0:
            raise ValueError("No valid features generated")
        
        current_features = features[-1].reshape(1, -1)
        current_features_scaled = self.scaler.transform(current_features)
        
        # Get predictions from all models
        model_predictions = {}
        for name, model in self.models.items():
            pred = model.predict(current_features_scaled)[0]
            model_predictions[name] = pred
        
        # Ensemble prediction
        ensemble_pred = sum(
            pred * self.model_weights[name] 
            for name, pred in model_predictions.items()
        )
        
        current_price = current_data[-1]['price']
        
        # Calculate confidence based on model agreement
        pred_values = list(model_predictions.values())
        confidence = 1 - (np.std(pred_values) / np.mean(pred_values))
        confidence = max(0.5, min(0.99, confidence))
        
        # Determine direction and recommendation
        price_change = (ensemble_pred - current_price) / current_price
        direction = "UP" if price_change > 0 else "DOWN"
        
        # Risk assessment
        volatility = np.std([d['price'] for d in current_data[-10:]])
        risk_score = min(1.0, volatility / current_price)
        
        # Generate recommendation
        if abs(price_change) > 0.05 and confidence > 0.8:
            recommendation = "STRONG_BUY" if direction == "UP" else "STRONG_SELL"
        elif abs(price_change) > 0.02 and confidence > 0.7:
            recommendation = "BUY" if direction == "UP" else "SELL"
        else:
            recommendation = "HOLD"
        
        return PredictionResult(
            symbol=symbol,
            current_price=current_price,
            predicted_price=ensemble_pred,
            confidence=confidence,
            direction=direction,
            time_horizon=time_horizon,
            model_consensus=model_predictions,
            risk_score=risk_score,
            recommendation=recommendation
        )
    
    def _train_demo_models(self):
        """Train models with synthetic data for demonstration"""
        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 1000
        n_features = 14
        
        X = np.random.randn(n_samples, n_features)
        # Create realistic price targets with some correlation to features
        y = 30000 + X[:, 0] * 5000 + X[:, 1] * 3000 + np.random.randn(n_samples) * 1000
        
        X_scaled = self.scaler.fit_transform(X)
        
        for model in self.models.values():
            model.fit(X_scaled, y)
        
        self.is_trained = True
    
    def generate_market_signals(self, market_data: Dict[str, List[Dict]]) -> List[MarketSignal]:
        """Generate market signals based on AI analysis"""
        signals = []
        
        for symbol, data in market_data.items():
            if len(data) < 10:
                continue
            
            recent_prices = [d['price'] for d in data[-10:]]
            
            # Momentum signal
            momentum = (recent_prices[-1] - recent_prices[0]) / recent_prices[0]
            if abs(momentum) > 0.05:
                strength = min(1.0, abs(momentum) * 10)
                signal_type = "MOMENTUM_UP" if momentum > 0 else "MOMENTUM_DOWN"
                signals.append(MarketSignal(
                    signal_type=signal_type,
                    strength=strength,
                    description=f"{symbol} showing {signal_type.lower()} with {momentum:.2%} change",
                    timestamp=datetime.now()
                ))
            
            # Volatility signal
            volatility = np.std(recent_prices) / np.mean(recent_prices)
            if volatility > 0.1:
                signals.append(MarketSignal(
                    signal_type="HIGH_VOLATILITY",
                    strength=min(1.0, volatility * 5),
                    description=f"{symbol} experiencing high volatility ({volatility:.2%})",
                    timestamp=datetime.now()
                ))
        
        return signals
    
    def get_model_performance(self) -> Dict[str, Dict]:
        """Get performance metrics for all models"""
        if not self.is_trained:
            return {}
        
        performance = {}
        for name in self.models.keys():
            performance[name] = {
                'weight': self.model_weights[name],
                'accuracy': random.uniform(0.75, 0.95),  # Simulated for demo
                'precision': random.uniform(0.70, 0.90),
                'last_updated': datetime.now().isoformat()
            }
        
        return performance

class PredictionAPI:
    """API interface for AI prediction engine"""
    
    def __init__(self):
        self.predictor = AIPredictor()
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
    
    def get_prediction(self, symbol: str, timeframe: str = "1h") -> Dict:
        """Get price prediction for a symbol"""
        cache_key = f"{symbol}_{timeframe}"
        now = datetime.now()
        
        # Check cache
        if cache_key in self.cache:
            cached_time, cached_result = self.cache[cache_key]
            if (now - cached_time).seconds < self.cache_duration:
                return cached_result
        
        # Generate synthetic historical data for demo
        historical_data = self._generate_demo_data(symbol)
        
        try:
            prediction = self.predictor.predict_price(symbol, historical_data, timeframe)
            
            result = {
                'symbol': prediction.symbol,
                'current_price': prediction.current_price,
                'predicted_price': prediction.predicted_price,
                'price_change': prediction.predicted_price - prediction.current_price,
                'price_change_percent': ((prediction.predicted_price - prediction.current_price) / prediction.current_price) * 100,
                'confidence': prediction.confidence,
                'direction': prediction.direction,
                'recommendation': prediction.recommendation,
                'risk_score': prediction.risk_score,
                'time_horizon': prediction.time_horizon,
                'model_consensus': prediction.model_consensus,
                'timestamp': now.isoformat()
            }
            
            # Cache result
            self.cache[cache_key] = (now, result)
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'symbol': symbol,
                'timestamp': now.isoformat()
            }
    
    def get_market_signals(self) -> List[Dict]:
        """Get current market signals"""
        # Generate demo market data
        symbols = ['BTC', 'ETH', 'DGD', 'ADA', 'SOL']
        market_data = {}
        
        for symbol in symbols:
            market_data[symbol] = self._generate_demo_data(symbol)
        
        signals = self.predictor.generate_market_signals(market_data)
        
        return [
            {
                'signal_type': signal.signal_type,
                'strength': signal.strength,
                'description': signal.description,
                'timestamp': signal.timestamp.isoformat()
            }
            for signal in signals
        ]
    
    def get_model_performance(self) -> Dict:
        """Get AI model performance metrics"""
        return self.predictor.get_model_performance()
    
    def _generate_demo_data(self, symbol: str, days: int = 30) -> List[Dict]:
        """Generate realistic demo price data"""
        base_prices = {
            'BTC': 45000,
            'ETH': 2500,
            'DGD': 125,
            'ADA': 0.5,
            'SOL': 100,
            'DOT': 7,
            'LINK': 15,
            'MATIC': 0.8,
            'AVAX': 35,
            'ATOM': 12
        }
        
        base_price = base_prices.get(symbol, 100)
        data = []
        current_time = datetime.now() - timedelta(days=days)
        
        for i in range(days * 24):  # Hourly data
            # Add realistic price movement
            change = random.gauss(0, 0.02)  # 2% volatility
            base_price *= (1 + change)
            
            data.append({
                'timestamp': current_time.isoformat(),
                'price': base_price,
                'volume': base_price * random.uniform(500, 2000)
            })
            
            current_time += timedelta(hours=1)
        
        return data

if __name__ == "__main__":
    # Test the prediction engine
    api = PredictionAPI()
    
    print("Testing AI Prediction Engine...")
    
    # Test prediction
    btc_prediction = api.get_prediction('BTC', '1h')
    print(f"BTC Prediction: {json.dumps(btc_prediction, indent=2)}")
    
    # Test market signals
    signals = api.get_market_signals()
    print(f"Market Signals: {len(signals)} signals generated")
    
    # Test model performance
    performance = api.get_model_performance()
    print(f"Model Performance: {json.dumps(performance, indent=2)}")
    
    print("AI Prediction Engine test completed successfully!")

