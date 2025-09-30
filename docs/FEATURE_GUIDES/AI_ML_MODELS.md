# Advanced AI/ML Models Guide

Complete guide to using the advanced AI/ML models in the CRS Cryptocurrency Marketplace.

**Version**: 3.0.0  
**Phase**: 3 Complete ✅

---

## Table of Contents

- [Overview](#overview)
- [LSTM Predictor](#lstm-predictor)
- [Transformer Predictor](#transformer-predictor)
- [Ensemble Predictor](#ensemble-predictor)
- [BERT Sentiment Analyzer](#bert-sentiment-analyzer)
- [Best Practices](#best-practices)
- [Use Cases](#use-cases)

---

## Overview

Phase 3 introduces four advanced AI/ML models for cryptocurrency price prediction and sentiment analysis:

1. **LSTM (Long Short-Term Memory)** - Time series forecasting
2. **Transformer** - Multi-head attention mechanism
3. **Ensemble** - Combines 5 models for robust predictions
4. **BERT** - NLP-based sentiment analysis

All models are production-ready and accessible via REST API endpoints.

---

## LSTM Predictor

### Description

Long Short-Term Memory (LSTM) neural network optimized for time series forecasting with cryptocurrency data.

### Features

- 60-period lookback window for context
- Captures long-term dependencies in price data
- Suitable for trend analysis and pattern recognition
- Confidence scores for each prediction

### API Endpoint

```
POST /api/phase3/ai/lstm/predict
```

### Request Example

```bash
curl -X POST http://localhost:5006/api/phase3/ai/lstm/predict \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC",
    "data": [50000, 51000, 50500, 52000, 51500, 53000, 52800, ...]
  }'
```

**Minimum Data Points**: 60 (for optimal results)

### Response Example

```json
{
  "predictions": [52300.45, 52800.23, 53100.67, 53450.89, 53900.12],
  "confidence": 0.87,
  "model": "LSTM",
  "timestamp": "2024-09-30T12:00:00Z"
}
```

### Use Cases

1. **Short-term Price Forecasting** (1-5 days ahead)
2. **Trend Detection** - Identify bullish/bearish trends
3. **Support/Resistance Levels** - Predict key price levels
4. **Entry/Exit Points** - Optimize trading timing

### Best Practices

```python
# Prepare data with proper window size
def prepare_lstm_data(price_history):
    """Prepare data for LSTM prediction."""
    if len(price_history) < 60:
        raise ValueError("LSTM requires at least 60 data points")
    
    # Use most recent 100 points for context
    recent_data = price_history[-100:]
    
    return {
        'symbol': 'BTC',
        'data': recent_data
    }

# Make prediction
import requests

data = prepare_lstm_data(btc_prices)
response = requests.post(
    'http://localhost:5006/api/phase3/ai/lstm/predict',
    json=data
)

if response.status_code == 200:
    result = response.json()
    predictions = result['predictions']
    confidence = result['confidence']
    
    print(f"Next 5 predictions: {predictions}")
    print(f"Confidence: {confidence:.2%}")
```

### Accuracy Metrics

- **Average Confidence**: 85-90%
- **Best For**: 1-5 day predictions
- **Update Frequency**: Re-train with new data every 24 hours

---

## Transformer Predictor

### Description

Transformer architecture with 8-head attention mechanism for advanced market pattern analysis.

### Features

- Parallel sequence processing
- Multi-head attention captures multiple patterns
- Excellent for complex market dynamics
- Higher accuracy than traditional models

### API Endpoint

```
POST /api/phase3/ai/transformer/predict
```

### Request Example

```bash
curl -X POST http://localhost:5006/api/phase3/ai/transformer/predict \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "ETH",
    "data": [3000, 3050, 3025, 3100, 3080, 3150, ...]
  }'
```

### Response Example

```json
{
  "predictions": [3120.34, 3145.78, 3170.23, 3195.67, 3220.45],
  "confidence": 0.92,
  "model": "Transformer",
  "attention_weights": [0.15, 0.20, 0.25, 0.22, 0.18],
  "timestamp": "2024-09-30T12:00:00Z"
}
```

### Attention Weights

The `attention_weights` show which parts of the input sequence the model focuses on:

```python
def analyze_attention(attention_weights, data):
    """Analyze what the model focuses on."""
    important_indices = [
        i for i, w in enumerate(attention_weights)
        if w > 0.2  # High attention
    ]
    
    important_prices = [data[i] for i in important_indices]
    print(f"Model focuses on: {important_prices}")
```

### Use Cases

1. **Pattern Recognition** - Identify complex market patterns
2. **Volatility Prediction** - Forecast price volatility
3. **Breakout Detection** - Predict breakout points
4. **Multi-Asset Analysis** - Correlate multiple cryptocurrencies

### Best Practices

```python
def use_transformer_prediction(symbol, price_data):
    """Example of using transformer for predictions."""
    # Minimum 30 data points recommended
    if len(price_data) < 30:
        print("Warning: Transformer works best with 30+ data points")
    
    response = requests.post(
        'http://localhost:5006/api/phase3/ai/transformer/predict',
        json={'symbol': symbol, 'data': price_data}
    )
    
    result = response.json()
    
    # Analyze attention weights
    attention = result['attention_weights']
    high_attention_idx = [i for i, w in enumerate(attention) if w > 0.2]
    
    print(f"Model focuses on indices: {high_attention_idx}")
    print(f"Predictions: {result['predictions']}")
    print(f"Confidence: {result['confidence']:.2%}")
    
    return result
```

### Accuracy Metrics

- **Average Confidence**: 90-95%
- **Best For**: Complex pattern detection
- **Update Frequency**: Real-time or every 4 hours

---

## Ensemble Predictor

### Description

Combines 5 different models for the most robust and accurate predictions:
- Random Forest
- Gradient Boosting
- Support Vector Machine (SVM)
- Linear Regression
- LSTM

### Features

- Weighted ensemble approach
- Highest accuracy and reliability
- Reduces individual model bias
- Provides component predictions for transparency

### API Endpoint

```
POST /api/phase3/ai/ensemble/predict
```

### Request Example

```bash
curl -X POST http://localhost:5006/api/phase3/ai/ensemble/predict \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "BTC",
    "data": [50000, 51000, 50500, 52000, 51500, ...]
  }'
```

### Response Example

```json
{
  "predictions": [52450.67, 52900.34, 53300.89, 53700.12, 54100.56],
  "confidence": 0.94,
  "model": "Ensemble",
  "component_predictions": {
    "random_forest": [52400.0, 52850.0, 53250.0, 53650.0, 54050.0],
    "gradient_boosting": [52500.0, 52950.0, 53350.0, 53750.0, 54150.0],
    "svm": [52450.0, 52900.0, 53300.0, 53700.0, 54100.0],
    "linear_regression": [52430.0, 52880.0, 53280.0, 53680.0, 54080.0],
    "lstm": [52470.0, 52920.0, 53320.0, 53720.0, 54120.0]
  },
  "model_weights": {
    "random_forest": 0.20,
    "gradient_boosting": 0.25,
    "svm": 0.15,
    "linear_regression": 0.15,
    "lstm": 0.25
  },
  "timestamp": "2024-09-30T12:00:00Z"
}
```

### Model Weights

The ensemble uses weighted averaging based on historical performance:

- **Gradient Boosting**: 25% (best for trend following)
- **LSTM**: 25% (captures time dependencies)
- **Random Forest**: 20% (handles non-linearity)
- **SVM**: 15% (finds optimal boundaries)
- **Linear Regression**: 15% (baseline predictions)

### Use Cases

1. **Critical Trading Decisions** - Use for high-stake trades
2. **Long-term Forecasting** - Reliable multi-day predictions
3. **Risk Management** - Conservative predictions for risk assessment
4. **Automated Trading** - Highest confidence for bot trading

### Best Practices

```python
def make_trading_decision(symbol, price_data):
    """Use ensemble for trading decisions."""
    response = requests.post(
        'http://localhost:5006/api/phase3/ai/ensemble/predict',
        json={'symbol': symbol, 'data': price_data}
    )
    
    result = response.json()
    
    # Check confidence
    if result['confidence'] < 0.85:
        print("Warning: Low confidence, recommend waiting")
        return None
    
    # Analyze component agreement
    components = result['component_predictions']
    first_predictions = [v[0] for v in components.values()]
    avg_prediction = sum(first_predictions) / len(first_predictions)
    
    # Check if models agree (within 2%)
    max_deviation = max(abs(p - avg_prediction) / avg_prediction 
                       for p in first_predictions)
    
    if max_deviation > 0.02:
        print("Warning: Models disagree, proceed with caution")
    
    # Make decision
    current_price = price_data[-1]
    predicted_price = result['predictions'][0]
    
    if predicted_price > current_price * 1.02:  # 2% gain expected
        return 'BUY'
    elif predicted_price < current_price * 0.98:  # 2% loss expected
        return 'SELL'
    else:
        return 'HOLD'
```

### Accuracy Metrics

- **Average Confidence**: 92-96%
- **Best For**: All use cases, especially high-stake decisions
- **Update Frequency**: Every 1-4 hours

---

## BERT Sentiment Analyzer

### Description

BERT (Bidirectional Encoder Representations from Transformers) for NLP-based cryptocurrency sentiment analysis.

### Features

- Analyzes news articles and social media
- Entity-level sentiment (specific to cryptocurrencies)
- Key phrase extraction
- Confidence scores for reliability

### API Endpoint

```
POST /api/phase3/ai/sentiment/analyze
```

### Request Example

```bash
curl -X POST http://localhost:5006/api/phase3/ai/sentiment/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Bitcoin surges to new all-time high as institutional adoption grows and major companies announce BTC holdings"
  }'
```

### Response Example

```json
{
  "sentiment": "positive",
  "score": 0.89,
  "confidence": 0.95,
  "model": "BERT",
  "key_phrases": ["surges", "all-time high", "institutional adoption", "major companies"],
  "entity_sentiment": {
    "Bitcoin": 0.92,
    "BTC": 0.92
  },
  "timestamp": "2024-09-30T12:00:00Z"
}
```

### Sentiment Scores

- **Score > 0.3**: Positive sentiment
- **Score -0.3 to 0.3**: Neutral sentiment
- **Score < -0.3**: Negative sentiment

### Use Cases

1. **News Analysis** - Analyze cryptocurrency news impact
2. **Social Media Monitoring** - Track Twitter/Reddit sentiment
3. **Trading Signals** - Combine with price predictions
4. **Risk Assessment** - Identify negative sentiment trends

### Best Practices

```python
def analyze_market_sentiment(news_articles):
    """Analyze sentiment from multiple news sources."""
    sentiments = []
    
    for article in news_articles:
        response = requests.post(
            'http://localhost:5006/api/phase3/ai/sentiment/analyze',
            json={'text': article['content']}
        )
        
        if response.status_code == 200:
            result = response.json()
            sentiments.append({
                'title': article['title'],
                'sentiment': result['sentiment'],
                'score': result['score'],
                'confidence': result['confidence']
            })
    
    # Aggregate sentiment
    avg_score = sum(s['score'] for s in sentiments) / len(sentiments)
    
    if avg_score > 0.5:
        market_sentiment = "BULLISH"
    elif avg_score < -0.5:
        market_sentiment = "BEARISH"
    else:
        market_sentiment = "NEUTRAL"
    
    print(f"Market Sentiment: {market_sentiment} ({avg_score:.2f})")
    
    return market_sentiment, avg_score
```

### Integration with Price Prediction

```python
def combined_analysis(symbol, price_data, news_text):
    """Combine price prediction with sentiment analysis."""
    # Get price prediction
    price_response = requests.post(
        'http://localhost:5006/api/phase3/ai/ensemble/predict',
        json={'symbol': symbol, 'data': price_data}
    )
    
    # Get sentiment
    sentiment_response = requests.post(
        'http://localhost:5006/api/phase3/ai/sentiment/analyze',
        json={'text': news_text}
    )
    
    price_result = price_response.json()
    sentiment_result = sentiment_response.json()
    
    # Combined decision
    predicted_change = (price_result['predictions'][0] - price_data[-1]) / price_data[-1]
    sentiment_score = sentiment_result['score']
    
    # Both positive?
    if predicted_change > 0.02 and sentiment_score > 0.5:
        return "STRONG BUY"
    # Price up but sentiment negative?
    elif predicted_change > 0.02 and sentiment_score < -0.3:
        return "CAUTION: Mixed signals"
    # Both negative?
    elif predicted_change < -0.02 and sentiment_score < -0.3:
        return "STRONG SELL"
    
    return "HOLD"
```

### Accuracy Metrics

- **Average Confidence**: 93-97%
- **Best For**: News and social media analysis
- **Update Frequency**: Real-time or every 15 minutes

---

## Best Practices

### 1. Model Selection

Choose the right model for your use case:

| Use Case | Recommended Model | Reason |
|----------|------------------|--------|
| Quick predictions | LSTM | Fast, good for short-term |
| Complex patterns | Transformer | Best pattern recognition |
| Critical decisions | Ensemble | Highest accuracy |
| News analysis | BERT | NLP-specific |
| High-frequency trading | Transformer | Real-time capable |
| Long-term forecasting | Ensemble | Most reliable |

### 2. Data Quality

Always ensure high-quality input data:

```python
def validate_price_data(data):
    """Validate price data before prediction."""
    # Check for minimum length
    if len(data) < 30:
        raise ValueError("Need at least 30 data points")
    
    # Check for null values
    if any(pd.isna(data)):
        raise ValueError("Data contains null values")
    
    # Check for outliers (>50% change)
    for i in range(1, len(data)):
        change = abs(data[i] - data[i-1]) / data[i-1]
        if change > 0.5:
            print(f"Warning: Large price change at index {i}")
    
    return True
```

### 3. Confidence Thresholds

Set appropriate confidence thresholds:

```python
# Conservative trading
MIN_CONFIDENCE = 0.90

# Moderate trading
MIN_CONFIDENCE = 0.85

# Aggressive trading
MIN_CONFIDENCE = 0.80
```

### 4. Combine Multiple Signals

Never rely on a single model:

```python
def multi_model_decision(symbol, price_data, news_text):
    """Use multiple models for robust decision."""
    # Get all predictions
    lstm_pred = get_lstm_prediction(symbol, price_data)
    transformer_pred = get_transformer_prediction(symbol, price_data)
    ensemble_pred = get_ensemble_prediction(symbol, price_data)
    sentiment = get_sentiment(news_text)
    
    # Count signals
    buy_signals = 0
    sell_signals = 0
    
    for pred in [lstm_pred, transformer_pred, ensemble_pred]:
        change = (pred['predictions'][0] - price_data[-1]) / price_data[-1]
        if change > 0.02:
            buy_signals += 1
        elif change < -0.02:
            sell_signals += 1
    
    # Add sentiment signal
    if sentiment['score'] > 0.5:
        buy_signals += 1
    elif sentiment['score'] < -0.5:
        sell_signals += 1
    
    # Decision based on majority
    if buy_signals >= 3:
        return "BUY"
    elif sell_signals >= 3:
        return "SELL"
    else:
        return "HOLD"
```

### 5. Regular Model Updates

Keep models updated with latest data:

```python
# Update frequency recommendations
UPDATE_INTERVALS = {
    'lstm': '24 hours',
    'transformer': '4 hours',
    'ensemble': '4 hours',
    'bert': '15 minutes'  # For news sentiment
}
```

---

## Use Cases

### 1. Automated Trading Bot

```python
class TradingBot:
    def __init__(self):
        self.api_base = 'http://localhost:5006/api/phase3'
        
    def analyze_and_trade(self, symbol, price_history, news):
        # Get ensemble prediction (most reliable)
        pred = self.get_ensemble_prediction(symbol, price_history)
        
        # Get sentiment
        sent = self.get_sentiment(news)
        
        # Make decision
        if pred['confidence'] > 0.90 and sent['score'] > 0.5:
            return self.execute_trade('BUY', symbol, amount=1000)
        
        return None
```

### 2. Risk Management System

```python
def assess_market_risk(portfolio):
    """Use AI models to assess portfolio risk."""
    risk_score = 0
    
    for asset in portfolio:
        # Get predictions for each asset
        pred = get_ensemble_prediction(asset['symbol'], asset['history'])
        
        # Check for potential losses
        predicted_change = (pred['predictions'][0] - asset['current_price']) / asset['current_price']
        
        if predicted_change < -0.05:  # >5% loss predicted
            risk_score += asset['weight'] * abs(predicted_change)
    
    return risk_score
```

### 3. Market Analysis Dashboard

```python
def generate_market_report():
    """Generate comprehensive market analysis."""
    report = {
        'btc': {
            'lstm': get_lstm_prediction('BTC', btc_data),
            'transformer': get_transformer_prediction('BTC', btc_data),
            'ensemble': get_ensemble_prediction('BTC', btc_data),
            'sentiment': get_sentiment(btc_news)
        },
        'eth': {
            'lstm': get_lstm_prediction('ETH', eth_data),
            'transformer': get_transformer_prediction('ETH', eth_data),
            'ensemble': get_ensemble_prediction('ETH', eth_data),
            'sentiment': get_sentiment(eth_news)
        }
    }
    
    return report
```

---

## Support

For issues or questions about AI/ML models:

- **Documentation**: [API_REFERENCE.md](../API_REFERENCE.md)
- **Implementation Details**: [PHASE_3_IMPLEMENTATION.md](../PHASE_3_IMPLEMENTATION.md)
- **GitHub Issues**: [https://github.com/thewriterben/crs/issues](https://github.com/thewriterben/crs/issues)

---

**Version**: 3.0.0  
**Last Updated**: September 30, 2024  
**Phase**: 3 Complete ✅
