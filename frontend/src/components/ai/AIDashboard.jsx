import React, { useState, useEffect, useMemo, useCallback, memo } from 'react';
import { api } from '@/lib/api.js';
import './AIDashboard.css';

const AIDashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedSymbol, setSelectedSymbol] = useState('BTC');
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = useCallback(async () => {
    try {
      const data = await api.ai.getDashboardData();
      setDashboardData(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Memoize formatters to avoid recreating on every render
  const formatCurrency = useMemo(() => {
    return (value) => {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(value);
    };
  }, []);

  const formatPercentage = useCallback((value) => {
    return `${(value * 100).toFixed(2)}%`;
  }, []);

  const getSentimentColor = useCallback((sentiment) => {
    if (sentiment > 0.3) return '#10b981'; // Green
    if (sentiment < -0.3) return '#ef4444'; // Red
    return '#f59e0b'; // Yellow
  }, []);

  const getRecommendationColor = useCallback((recommendation) => {
    switch (recommendation) {
      case 'STRONG_BUY': return '#10b981';
      case 'BUY': return '#22c55e';
      case 'HOLD': return '#f59e0b';
      case 'SELL': return '#f97316';
      case 'STRONG_SELL': return '#ef4444';
      default: return '#6b7280';
    }
  }, []);

  if (loading) {
    return (
      <div className="ai-dashboard">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading AI Dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="ai-dashboard">
        <div className="error-container">
          <h3>Error Loading AI Dashboard</h3>
          <p>{error}</p>
          <button onClick={fetchDashboardData} className="retry-button">
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="ai-dashboard">
      <div className="dashboard-header">
        <h1>🤖 AI Analytics Dashboard</h1>
        <div className="last-updated">
          Last updated: {new Date(dashboardData?.timestamp).toLocaleTimeString()}
        </div>
      </div>

      <div className="dashboard-tabs">
        <button 
          className={`tab ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button 
          className={`tab ${activeTab === 'predictions' ? 'active' : ''}`}
          onClick={() => setActiveTab('predictions')}
        >
          Predictions
        </button>
        <button 
          className={`tab ${activeTab === 'sentiment' ? 'active' : ''}`}
          onClick={() => setActiveTab('sentiment')}
        >
          Sentiment
        </button>
        <button 
          className={`tab ${activeTab === 'bots' ? 'active' : ''}`}
          onClick={() => setActiveTab('bots')}
        >
          Trading Bots
        </button>
      </div>

      {activeTab === 'overview' && (
        <div className="overview-tab">
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Market Mood</h3>
              <div className="stat-value" style={{
                color: getSentimentColor(dashboardData?.market_intelligence?.market_sentiment || 0)
              }}>
                {dashboardData?.market_intelligence?.market_mood || 'NEUTRAL'}
              </div>
              <div className="stat-subtitle">
                Sentiment: {formatPercentage(dashboardData?.market_intelligence?.market_sentiment || 0)}
              </div>
            </div>

            <div className="stat-card">
              <h3>Fear & Greed Index</h3>
              <div className="stat-value">
                {Math.round(dashboardData?.market_intelligence?.market_fear_greed || 50)}
              </div>
              <div className="stat-subtitle">
                {dashboardData?.market_intelligence?.market_fear_greed > 50 ? 'Greed' : 'Fear'}
              </div>
            </div>

            <div className="stat-card">
              <h3>Active Trading Bots</h3>
              <div className="stat-value">
                {dashboardData?.trading_bots?.active_bots || 0}
              </div>
              <div className="stat-subtitle">
                Total: {dashboardData?.trading_bots?.total_bots || 0}
              </div>
            </div>

            <div className="stat-card">
              <h3>Market Signals</h3>
              <div className="stat-value">
                {dashboardData?.market_signals?.length || 0}
              </div>
              <div className="stat-subtitle">
                Active signals detected
              </div>
            </div>
          </div>

          <div className="trending-topics">
            <h3>🔥 Trending Topics</h3>
            <div className="topics-grid">
              {dashboardData?.trending_topics?.map((topic, index) => (
                <div key={index} className="topic-card">
                  <div className="topic-name">{topic.topic}</div>
                  <div className="topic-mentions">{topic.mentions} mentions</div>
                  <div 
                    className="topic-sentiment"
                    style={{ color: getSentimentColor(topic.sentiment) }}
                  >
                    {topic.sentiment_label}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'predictions' && (
        <div className="predictions-tab">
          <div className="symbol-selector">
            <label>Select Symbol:</label>
            <select 
              value={selectedSymbol} 
              onChange={(e) => setSelectedSymbol(e.target.value)}
            >
              {Object.keys(dashboardData?.predictions || {}).map(symbol => (
                <option key={symbol} value={symbol}>{symbol}</option>
              ))}
            </select>
          </div>

          {dashboardData?.predictions?.[selectedSymbol] && (
            <div className="prediction-details">
              <div className="prediction-header">
                <h3>{selectedSymbol} Price Prediction</h3>
                <div 
                  className="recommendation-badge"
                  style={{ 
                    backgroundColor: getRecommendationColor(
                      dashboardData.predictions[selectedSymbol].recommendation
                    )
                  }}
                >
                  {dashboardData.predictions[selectedSymbol].recommendation}
                </div>
              </div>

              <div className="prediction-grid">
                <div className="prediction-card">
                  <h4>Current Price</h4>
                  <div className="price-value">
                    {formatCurrency(dashboardData.predictions[selectedSymbol].current_price)}
                  </div>
                </div>

                <div className="prediction-card">
                  <h4>Predicted Price</h4>
                  <div className="price-value">
                    {formatCurrency(dashboardData.predictions[selectedSymbol].predicted_price)}
                  </div>
                </div>

                <div className="prediction-card">
                  <h4>Price Change</h4>
                  <div 
                    className="price-value"
                    style={{
                      color: dashboardData.predictions[selectedSymbol].price_change > 0 ? '#10b981' : '#ef4444'
                    }}
                  >
                    {dashboardData.predictions[selectedSymbol].price_change > 0 ? '+' : ''}
                    {formatPercentage(dashboardData.predictions[selectedSymbol].price_change_percent / 100)}
                  </div>
                </div>

                <div className="prediction-card">
                  <h4>Confidence</h4>
                  <div className="confidence-bar">
                    <div 
                      className="confidence-fill"
                      style={{ 
                        width: `${dashboardData.predictions[selectedSymbol].confidence * 100}%` 
                      }}
                    ></div>
                  </div>
                  <div className="confidence-text">
                    {formatPercentage(dashboardData.predictions[selectedSymbol].confidence)}
                  </div>
                </div>
              </div>

              <div className="model-consensus">
                <h4>Model Consensus</h4>
                <div className="consensus-grid">
                  {Object.entries(dashboardData.predictions[selectedSymbol].model_consensus || {}).map(([model, prediction]) => (
                    <div key={model} className="consensus-item">
                      <span className="model-name">{model.replace('_', ' ')}</span>
                      <span className="model-prediction">{formatCurrency(prediction)}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'sentiment' && (
        <div className="sentiment-tab">
          <div className="sentiment-overview">
            <h3>Market Sentiment Overview</h3>
            <div className="sentiment-grid">
              {Object.entries(dashboardData?.sentiment_summary || {}).map(([symbol, sentiment]) => (
                <div key={symbol} className="sentiment-card">
                  <div className="sentiment-symbol">{symbol}</div>
                  <div 
                    className="sentiment-score"
                    style={{ color: getSentimentColor(sentiment.overall_sentiment) }}
                  >
                    {sentiment.sentiment_label}
                  </div>
                  <div className="sentiment-details">
                    <div>Score: {sentiment.overall_sentiment.toFixed(3)}</div>
                    <div>Trend: {sentiment.sentiment_trend}</div>
                    <div>News: {sentiment.news_volume}</div>
                    <div>Social: {sentiment.social_mentions}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="market-intelligence">
            <h3>Market Intelligence</h3>
            <div className="intelligence-stats">
              <div className="intel-stat">
                <span>Total News Volume:</span>
                <span>{dashboardData?.market_intelligence?.total_news_volume || 0}</span>
              </div>
              <div className="intel-stat">
                <span>Social Mentions:</span>
                <span>{dashboardData?.market_intelligence?.total_social_mentions || 0}</span>
              </div>
              <div className="intel-stat">
                <span>Trending Topics:</span>
                <span>{dashboardData?.market_intelligence?.trending_topics || 0}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'bots' && (
        <div className="bots-tab">
          <div className="bots-overview">
            <h3>Trading Bots Overview</h3>
            <div className="bots-stats">
              <div className="bot-stat">
                <span>Total Bots:</span>
                <span>{dashboardData?.trading_bots?.total_bots || 0}</span>
              </div>
              <div className="bot-stat">
                <span>Active Bots:</span>
                <span>{dashboardData?.trading_bots?.active_bots || 0}</span>
              </div>
            </div>
          </div>

          <div className="bots-list">
            <h4>Active Trading Bots</h4>
            {dashboardData?.trading_bots?.bots?.length > 0 ? (
              <div className="bots-grid">
                {dashboardData.trading_bots.bots.map((bot, index) => (
                  <div key={index} className="bot-card">
                    <div className="bot-header">
                      <div className="bot-name">{bot.name}</div>
                      <div className={`bot-status ${bot.status}`}>
                        {bot.status.toUpperCase()}
                      </div>
                    </div>
                    <div className="bot-details">
                      <div>Strategy: {bot.strategy}</div>
                      <div>Balance: {formatCurrency(bot.current_balance)}</div>
                      <div>P&L: {formatCurrency(bot.total_pnl)}</div>
                      <div>Trades: {bot.total_trades}</div>
                      <div>Positions: {bot.active_positions}</div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-bots">
                <p>No trading bots active</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AIDashboard;

