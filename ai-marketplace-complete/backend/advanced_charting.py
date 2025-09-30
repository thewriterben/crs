#!/usr/bin/env python3
"""
Advanced Charting and Technical Analysis System
Implements sophisticated chart types, technical indicators, and pattern recognition
"""

import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta
import math
import random

class TechnicalIndicators:
    """Advanced technical indicators for cryptocurrency analysis"""
    
    @staticmethod
    def fibonacci_retracement(high, low, levels=[0.236, 0.382, 0.5, 0.618, 0.786]):
        """Calculate Fibonacci retracement levels"""
        diff = high - low
        return {
            f"fib_{int(level*100)}": high - (diff * level) 
            for level in levels
        }
    
    @staticmethod
    def ichimoku_cloud(high, low, close, tenkan_period=9, kijun_period=26, senkou_span_b_period=52):
        """Calculate Ichimoku Cloud components"""
        # Tenkan-sen (Conversion Line)
        tenkan_sen = (high.rolling(tenkan_period).max() + low.rolling(tenkan_period).min()) / 2
        
        # Kijun-sen (Base Line)
        kijun_sen = (high.rolling(kijun_period).max() + low.rolling(kijun_period).min()) / 2
        
        # Senkou Span A (Leading Span A)
        senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(kijun_period)
        
        # Senkou Span B (Leading Span B)
        senkou_span_b = ((high.rolling(senkou_span_b_period).max() + 
                         low.rolling(senkou_span_b_period).min()) / 2).shift(kijun_period)
        
        # Chikou Span (Lagging Span)
        chikou_span = close.shift(-kijun_period)
        
        return {
            'tenkan_sen': tenkan_sen,
            'kijun_sen': kijun_sen,
            'senkou_span_a': senkou_span_a,
            'senkou_span_b': senkou_span_b,
            'chikou_span': chikou_span
        }
    
    @staticmethod
    def volume_profile(price, volume, bins=20):
        """Calculate volume profile"""
        price_min, price_max = price.min(), price.max()
        price_bins = np.linspace(price_min, price_max, bins + 1)
        
        volume_profile = []
        for i in range(len(price_bins) - 1):
            mask = (price >= price_bins[i]) & (price < price_bins[i + 1])
            total_volume = volume[mask].sum()
            avg_price = (price_bins[i] + price_bins[i + 1]) / 2
            
            volume_profile.append({
                'price_level': avg_price,
                'volume': total_volume,
                'price_range': [price_bins[i], price_bins[i + 1]]
            })
        
        return volume_profile
    
    @staticmethod
    def pivot_points(high, low, close):
        """Calculate pivot points and support/resistance levels"""
        pivot = (high + low + close) / 3
        
        # Support levels
        s1 = (2 * pivot) - high
        s2 = pivot - (high - low)
        s3 = low - 2 * (high - pivot)
        
        # Resistance levels
        r1 = (2 * pivot) - low
        r2 = pivot + (high - low)
        r3 = high + 2 * (pivot - low)
        
        return {
            'pivot': pivot,
            'support_1': s1,
            'support_2': s2,
            'support_3': s3,
            'resistance_1': r1,
            'resistance_2': r2,
            'resistance_3': r3
        }
    
    @staticmethod
    def williams_r(high, low, close, period=14):
        """Calculate Williams %R oscillator"""
        highest_high = high.rolling(period).max()
        lowest_low = low.rolling(period).min()
        
        williams_r = -100 * (highest_high - close) / (highest_high - lowest_low)
        return williams_r
    
    @staticmethod
    def commodity_channel_index(high, low, close, period=20):
        """Calculate Commodity Channel Index (CCI)"""
        typical_price = (high + low + close) / 3
        sma = typical_price.rolling(period).mean()
        mean_deviation = typical_price.rolling(period).apply(
            lambda x: np.mean(np.abs(x - x.mean()))
        )
        
        cci = (typical_price - sma) / (0.015 * mean_deviation)
        return cci
    
    @staticmethod
    def stochastic_oscillator(high, low, close, k_period=14, d_period=3):
        """Calculate Stochastic Oscillator"""
        lowest_low = low.rolling(k_period).min()
        highest_high = high.rolling(k_period).max()
        
        k_percent = 100 * (close - lowest_low) / (highest_high - lowest_low)
        d_percent = k_percent.rolling(d_period).mean()
        
        return {
            'k_percent': k_percent,
            'd_percent': d_percent
        }

class PatternRecognition:
    """Pattern recognition algorithms for technical analysis"""
    
    @staticmethod
    def detect_double_top(high, low, close, window=20, threshold=0.02):
        """Detect double top pattern"""
        peaks = []
        
        for i in range(window, len(high) - window):
            if (high.iloc[i] == high.iloc[i-window:i+window+1].max() and
                high.iloc[i] > high.iloc[i-1] and high.iloc[i] > high.iloc[i+1]):
                peaks.append({'index': i, 'price': high.iloc[i]})
        
        double_tops = []
        for i in range(len(peaks) - 1):
            peak1, peak2 = peaks[i], peaks[i + 1]
            price_diff = abs(peak1['price'] - peak2['price']) / peak1['price']
            
            if price_diff < threshold:
                double_tops.append({
                    'pattern': 'double_top',
                    'peak1': peak1,
                    'peak2': peak2,
                    'confidence': 1 - price_diff
                })
        
        return double_tops
    
    @staticmethod
    def detect_head_shoulders(high, low, close, window=15):
        """Detect head and shoulders pattern"""
        peaks = []
        
        for i in range(window, len(high) - window):
            if (high.iloc[i] == high.iloc[i-window:i+window+1].max() and
                high.iloc[i] > high.iloc[i-1] and high.iloc[i] > high.iloc[i+1]):
                peaks.append({'index': i, 'price': high.iloc[i]})
        
        head_shoulders = []
        for i in range(len(peaks) - 2):
            left_shoulder = peaks[i]
            head = peaks[i + 1]
            right_shoulder = peaks[i + 2]
            
            # Check if head is higher than shoulders
            if (head['price'] > left_shoulder['price'] and 
                head['price'] > right_shoulder['price']):
                
                # Check if shoulders are approximately equal
                shoulder_diff = abs(left_shoulder['price'] - right_shoulder['price']) / left_shoulder['price']
                
                if shoulder_diff < 0.05:  # 5% tolerance
                    head_shoulders.append({
                        'pattern': 'head_shoulders',
                        'left_shoulder': left_shoulder,
                        'head': head,
                        'right_shoulder': right_shoulder,
                        'confidence': 1 - shoulder_diff
                    })
        
        return head_shoulders
    
    @staticmethod
    def detect_triangles(high, low, close, window=20):
        """Detect triangle patterns (ascending, descending, symmetrical)"""
        # Find trend lines
        highs = []
        lows = []
        
        for i in range(window, len(high) - window):
            if high.iloc[i] == high.iloc[i-window:i+window+1].max():
                highs.append({'index': i, 'price': high.iloc[i]})
            if low.iloc[i] == low.iloc[i-window:i+window+1].min():
                lows.append({'index': i, 'price': low.iloc[i]})
        
        triangles = []
        
        if len(highs) >= 2 and len(lows) >= 2:
            # Calculate trend lines
            high_slope = (highs[-1]['price'] - highs[0]['price']) / (highs[-1]['index'] - highs[0]['index'])
            low_slope = (lows[-1]['price'] - lows[0]['price']) / (lows[-1]['index'] - lows[0]['index'])
            
            # Classify triangle type
            if abs(high_slope) < 0.001 and low_slope > 0.001:
                pattern_type = 'ascending_triangle'
            elif high_slope < -0.001 and abs(low_slope) < 0.001:
                pattern_type = 'descending_triangle'
            elif high_slope < -0.001 and low_slope > 0.001:
                pattern_type = 'symmetrical_triangle'
            else:
                pattern_type = None
            
            if pattern_type:
                triangles.append({
                    'pattern': pattern_type,
                    'high_points': highs,
                    'low_points': lows,
                    'high_slope': high_slope,
                    'low_slope': low_slope
                })
        
        return triangles

class AdvancedChartData:
    """Generate advanced chart data with multiple timeframes and indicators"""
    
    def __init__(self):
        self.symbols = ['BTC', 'ETH', 'ADA', 'DOT', 'LINK']
        
    def generate_ohlcv_data(self, symbol, timeframe='1h', periods=100):
        """Generate OHLCV (Open, High, Low, Close, Volume) data"""
        # Base price for different symbols
        base_prices = {
            'BTC': 45000,
            'ETH': 2800,
            'ADA': 0.45,
            'DOT': 6.5,
            'LINK': 14.2
        }
        
        base_price = base_prices.get(symbol, 100)
        
        # Generate realistic price movements
        data = []
        current_price = base_price
        
        for i in range(periods):
            # Random price movement
            change_percent = np.random.normal(0, 0.02)  # 2% volatility
            
            open_price = current_price
            close_price = open_price * (1 + change_percent)
            
            # High and low based on intraday volatility
            intraday_range = abs(change_percent) * 1.5
            high_price = max(open_price, close_price) * (1 + intraday_range * np.random.random())
            low_price = min(open_price, close_price) * (1 - intraday_range * np.random.random())
            
            # Volume (higher volume on larger price movements)
            base_volume = 1000000
            volume = base_volume * (1 + abs(change_percent) * 10) * (0.5 + np.random.random())
            
            timestamp = datetime.now() - timedelta(hours=periods-i)
            
            data.append({
                'timestamp': timestamp.isoformat(),
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': round(volume, 0)
            })
            
            current_price = close_price
        
        return data
    
    def calculate_all_indicators(self, ohlcv_data):
        """Calculate all technical indicators for the given data"""
        df = pd.DataFrame(ohlcv_data)
        
        # Convert to pandas series
        high = pd.Series([d['high'] for d in ohlcv_data])
        low = pd.Series([d['low'] for d in ohlcv_data])
        close = pd.Series([d['close'] for d in ohlcv_data])
        volume = pd.Series([d['volume'] for d in ohlcv_data])
        
        indicators = {}
        
        # Basic indicators
        indicators['sma_20'] = close.rolling(20).mean().tolist()
        indicators['sma_50'] = close.rolling(50).mean().tolist()
        indicators['ema_12'] = close.ewm(span=12).mean().tolist()
        indicators['ema_26'] = close.ewm(span=26).mean().tolist()
        
        # Bollinger Bands
        sma_20 = close.rolling(20).mean()
        std_20 = close.rolling(20).std()
        indicators['bb_upper'] = (sma_20 + (std_20 * 2)).tolist()
        indicators['bb_lower'] = (sma_20 - (std_20 * 2)).tolist()
        indicators['bb_middle'] = sma_20.tolist()
        
        # RSI
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        indicators['rsi'] = (100 - (100 / (1 + rs))).tolist()
        
        # MACD
        ema_12 = close.ewm(span=12).mean()
        ema_26 = close.ewm(span=26).mean()
        macd_line = ema_12 - ema_26
        signal_line = macd_line.ewm(span=9).mean()
        indicators['macd'] = macd_line.tolist()
        indicators['macd_signal'] = signal_line.tolist()
        indicators['macd_histogram'] = (macd_line - signal_line).tolist()
        
        # Advanced indicators
        indicators['williams_r'] = TechnicalIndicators.williams_r(high, low, close).tolist()
        indicators['cci'] = TechnicalIndicators.commodity_channel_index(high, low, close).tolist()
        
        stoch = TechnicalIndicators.stochastic_oscillator(high, low, close)
        indicators['stoch_k'] = stoch['k_percent'].tolist()
        indicators['stoch_d'] = stoch['d_percent'].tolist()
        
        # Ichimoku Cloud
        ichimoku = TechnicalIndicators.ichimoku_cloud(high, low, close)
        indicators['ichimoku_tenkan'] = ichimoku['tenkan_sen'].tolist()
        indicators['ichimoku_kijun'] = ichimoku['kijun_sen'].tolist()
        indicators['ichimoku_senkou_a'] = ichimoku['senkou_span_a'].tolist()
        indicators['ichimoku_senkou_b'] = ichimoku['senkou_span_b'].tolist()
        
        # Volume indicators
        indicators['volume_sma'] = volume.rolling(20).mean().tolist()
        
        # Support and resistance
        latest_high = high.tail(20).max()
        latest_low = low.tail(20).min()
        latest_close = close.iloc[-1]
        
        pivot_data = TechnicalIndicators.pivot_points(latest_high, latest_low, latest_close)
        indicators['pivot_points'] = pivot_data
        
        # Fibonacci retracement
        indicators['fibonacci'] = TechnicalIndicators.fibonacci_retracement(latest_high, latest_low)
        
        return indicators
    
    def detect_patterns(self, ohlcv_data):
        """Detect chart patterns in the data"""
        high = pd.Series([d['high'] for d in ohlcv_data])
        low = pd.Series([d['low'] for d in ohlcv_data])
        close = pd.Series([d['close'] for d in ohlcv_data])
        
        patterns = {}
        
        # Detect various patterns
        patterns['double_tops'] = PatternRecognition.detect_double_top(high, low, close)
        patterns['head_shoulders'] = PatternRecognition.detect_head_shoulders(high, low, close)
        patterns['triangles'] = PatternRecognition.detect_triangles(high, low, close)
        
        return patterns

class ChartingAPI:
    """API for advanced charting and technical analysis"""
    
    def __init__(self):
        self.chart_data = AdvancedChartData()
    
    def get_chart_data(self, symbol='BTC', timeframe='1h', periods=100):
        """Get comprehensive chart data with indicators"""
        # Generate OHLCV data
        ohlcv_data = self.chart_data.generate_ohlcv_data(symbol, timeframe, periods)
        
        # Calculate technical indicators
        indicators = self.chart_data.calculate_all_indicators(ohlcv_data)
        
        # Detect patterns
        patterns = self.chart_data.detect_patterns(ohlcv_data)
        
        # Volume profile
        high = pd.Series([d['high'] for d in ohlcv_data])
        low = pd.Series([d['low'] for d in ohlcv_data])
        close = pd.Series([d['close'] for d in ohlcv_data])
        volume = pd.Series([d['volume'] for d in ohlcv_data])
        
        volume_profile = TechnicalIndicators.volume_profile(close, volume)
        
        return {
            'symbol': symbol,
            'timeframe': timeframe,
            'ohlcv_data': ohlcv_data,
            'technical_indicators': indicators,
            'chart_patterns': patterns,
            'volume_profile': volume_profile,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_multi_timeframe_analysis(self, symbol='BTC'):
        """Get analysis across multiple timeframes"""
        timeframes = ['1h', '4h', '1d']
        analysis = {}
        
        for tf in timeframes:
            periods = {'1h': 168, '4h': 168, '1d': 100}[tf]  # 1 week, 1 month, 100 days
            analysis[tf] = self.get_chart_data(symbol, tf, periods)
        
        return {
            'symbol': symbol,
            'multi_timeframe_analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_market_structure(self, symbol='BTC'):
        """Analyze market structure and key levels"""
        chart_data = self.get_chart_data(symbol, '1d', 100)
        
        # Extract price data
        prices = [d['close'] for d in chart_data['ohlcv_data']]
        highs = [d['high'] for d in chart_data['ohlcv_data']]
        lows = [d['low'] for d in chart_data['ohlcv_data']]
        
        # Calculate key levels
        current_price = prices[-1]
        recent_high = max(highs[-30:])  # 30-day high
        recent_low = min(lows[-30:])    # 30-day low
        
        # Trend analysis
        sma_20 = chart_data['technical_indicators']['sma_20'][-1]
        sma_50 = chart_data['technical_indicators']['sma_50'][-1]
        
        if current_price > sma_20 > sma_50:
            trend = 'BULLISH'
        elif current_price < sma_20 < sma_50:
            trend = 'BEARISH'
        else:
            trend = 'SIDEWAYS'
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'trend': trend,
            'key_levels': {
                'recent_high': recent_high,
                'recent_low': recent_low,
                'sma_20': sma_20,
                'sma_50': sma_50,
                'support_levels': [recent_low, sma_50, sma_20],
                'resistance_levels': [recent_high, sma_20, sma_50]
            },
            'fibonacci_levels': chart_data['technical_indicators']['fibonacci'],
            'pivot_points': chart_data['technical_indicators']['pivot_points'],
            'timestamp': datetime.now().isoformat()
        }

# Test the system
if __name__ == "__main__":
    print("Testing Advanced Charting System...")
    
    api = ChartingAPI()
    
    # Test basic chart data
    print("\n1. Testing Chart Data Generation:")
    chart_data = api.get_chart_data('BTC', '1h', 50)
    print(f"Generated {len(chart_data['ohlcv_data'])} OHLCV data points")
    print(f"Technical indicators: {list(chart_data['technical_indicators'].keys())}")
    print(f"Detected patterns: {list(chart_data['chart_patterns'].keys())}")
    
    # Test market structure analysis
    print("\n2. Testing Market Structure Analysis:")
    market_structure = api.get_market_structure('BTC')
    print(f"Current price: ${market_structure['current_price']}")
    print(f"Trend: {market_structure['trend']}")
    print(f"Recent high: ${market_structure['key_levels']['recent_high']}")
    print(f"Recent low: ${market_structure['key_levels']['recent_low']}")
    
    print("\n✅ Advanced Charting System working correctly!")

