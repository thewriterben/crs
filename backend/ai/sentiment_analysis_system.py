#!/usr/bin/env python3
"""
Sentiment Analysis and Market Intelligence System
Advanced AI-powered sentiment analysis for cryptocurrency markets
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import random
import re
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import uuid
import requests
from collections import defaultdict

class SentimentScore(Enum):
    VERY_NEGATIVE = -2
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1
    VERY_POSITIVE = 2

class NewsSource(Enum):
    TWITTER = "twitter"
    REDDIT = "reddit"
    NEWS_SITES = "news_sites"
    TELEGRAM = "telegram"
    DISCORD = "discord"

@dataclass
class SentimentData:
    """Structure for sentiment analysis results"""
    symbol: str
    sentiment_score: float
    confidence: float
    sentiment_label: str
    source: NewsSource
    text: str
    timestamp: datetime
    influence_score: float
    keywords: List[str]

@dataclass
class MarketIntelligence:
    """Structure for market intelligence data"""
    symbol: str
    overall_sentiment: float
    sentiment_trend: str
    news_volume: int
    social_mentions: int
    influencer_sentiment: float
    fear_greed_index: float
    market_cap_sentiment: float
    trading_volume_sentiment: float
    timestamp: datetime

@dataclass
class TrendingTopic:
    """Structure for trending topics"""
    topic: str
    mentions: int
    sentiment: float
    related_symbols: List[str]
    growth_rate: float
    timestamp: datetime

class SentimentAnalyzer:
    """Advanced sentiment analysis engine"""
    
    def __init__(self):
        self.positive_keywords = [
            'bullish', 'moon', 'pump', 'buy', 'hodl', 'diamond hands', 'to the moon',
            'breakout', 'rally', 'surge', 'gains', 'profit', 'green', 'up', 'rise',
            'adoption', 'partnership', 'upgrade', 'innovation', 'breakthrough'
        ]
        
        self.negative_keywords = [
            'bearish', 'dump', 'sell', 'crash', 'dip', 'red', 'down', 'fall',
            'panic', 'fear', 'fud', 'scam', 'hack', 'regulation', 'ban',
            'bubble', 'overvalued', 'correction', 'decline', 'loss'
        ]
        
        self.crypto_symbols = {
            'BTC': ['bitcoin', 'btc', '$btc'],
            'ETH': ['ethereum', 'eth', '$eth', 'ether'],
            'DGD': ['digital gold', 'dgd', '$dgd'],
            'ADA': ['cardano', 'ada', '$ada'],
            'SOL': ['solana', 'sol', '$sol'],
            'DOT': ['polkadot', 'dot', '$dot'],
            'LINK': ['chainlink', 'link', '$link'],
            'MATIC': ['polygon', 'matic', '$matic'],
            'AVAX': ['avalanche', 'avax', '$avax'],
            'ATOM': ['cosmos', 'atom', '$atom']
        }
        
        self.sentiment_cache = {}
        self.cache_duration = 300  # 5 minutes
    
    def analyze_text(self, text: str, symbol: Optional[str] = None) -> Tuple[float, float, List[str]]:
        """Analyze sentiment of text content"""
        text_lower = text.lower()
        
        # Extract keywords
        found_keywords = []
        positive_score = 0
        negative_score = 0
        
        # Check for positive keywords
        for keyword in self.positive_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
                positive_score += 1
        
        # Check for negative keywords
        for keyword in self.negative_keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
                negative_score += 1
        
        # Calculate sentiment score (-1 to 1)
        total_keywords = positive_score + negative_score
        if total_keywords == 0:
            sentiment_score = 0.0
            confidence = 0.3  # Low confidence for neutral
        else:
            sentiment_score = (positive_score - negative_score) / total_keywords
            confidence = min(0.95, 0.5 + (total_keywords * 0.1))
        
        # Adjust for symbol-specific mentions
        if symbol:
            symbol_mentions = self.crypto_symbols.get(symbol, [])
            for mention in symbol_mentions:
                if mention in text_lower:
                    confidence += 0.1
                    break
        
        confidence = min(0.99, confidence)
        
        return sentiment_score, confidence, found_keywords
    
    def get_sentiment_label(self, score: float) -> str:
        """Convert sentiment score to label"""
        if score >= 0.6:
            return "VERY_POSITIVE"
        elif score >= 0.2:
            return "POSITIVE"
        elif score <= -0.6:
            return "VERY_NEGATIVE"
        elif score <= -0.2:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
    
    def analyze_social_media(self, symbol: str, source: NewsSource) -> List[SentimentData]:
        """Analyze social media sentiment for a symbol"""
        # Simulate social media data collection
        sample_texts = self._generate_sample_social_media_data(symbol, source)
        
        sentiment_results = []
        for text_data in sample_texts:
            sentiment_score, confidence, keywords = self.analyze_text(text_data['text'], symbol)
            
            sentiment_data = SentimentData(
                symbol=symbol,
                sentiment_score=sentiment_score,
                confidence=confidence,
                sentiment_label=self.get_sentiment_label(sentiment_score),
                source=source,
                text=text_data['text'],
                timestamp=text_data['timestamp'],
                influence_score=text_data['influence_score'],
                keywords=keywords
            )
            
            sentiment_results.append(sentiment_data)
        
        return sentiment_results
    
    def _generate_sample_social_media_data(self, symbol: str, source: NewsSource) -> List[Dict]:
        """Generate sample social media data for demonstration"""
        templates = {
            NewsSource.TWITTER: [
                f"{symbol} is looking bullish! Great breakout pattern forming 🚀",
                f"Just bought more {symbol}, this dip won't last long #HODL",
                f"{symbol} dump incoming? Seeing some bearish signals",
                f"Why is {symbol} pumping so hard? FOMO is real",
                f"{symbol} to the moon! Diamond hands only 💎🙌",
                f"Selling my {symbol} bags, this market is too volatile",
                f"{symbol} partnership announcement soon? Bullish if true",
                f"FUD around {symbol} is getting ridiculous, buying more"
            ],
            NewsSource.REDDIT: [
                f"DD: Why {symbol} is undervalued and ready for massive gains",
                f"{symbol} technical analysis - bearish divergence spotted",
                f"Should I buy {symbol} now or wait for a bigger dip?",
                f"{symbol} whale movements detected, something big coming",
                f"Unpopular opinion: {symbol} is overvalued at current prices",
                f"{symbol} adoption is accelerating, bullish long term",
                f"Warning: {symbol} showing signs of distribution phase",
                f"{symbol} community is the strongest in crypto, very bullish"
            ],
            NewsSource.NEWS_SITES: [
                f"{symbol} announces major upgrade to improve scalability",
                f"Regulatory concerns impact {symbol} price negatively",
                f"{symbol} forms strategic partnership with Fortune 500 company",
                f"Market analysts predict {symbol} could reach new highs",
                f"{symbol} faces technical challenges in latest update",
                f"Institutional investors show growing interest in {symbol}",
                f"{symbol} network experiences temporary outage",
                f"{symbol} developer activity reaches all-time high"
            ]
        }
        
        texts = templates.get(source, templates[NewsSource.TWITTER])
        
        sample_data = []
        for i in range(random.randint(5, 15)):
            text = random.choice(texts)
            sample_data.append({
                'text': text,
                'timestamp': datetime.now() - timedelta(hours=random.randint(0, 24)),
                'influence_score': random.uniform(0.1, 1.0)
            })
        
        return sample_data

class MarketIntelligenceEngine:
    """Market intelligence aggregation and analysis"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.intelligence_cache = {}
        self.trending_topics = []
        self.fear_greed_history = []
    
    def generate_market_intelligence(self, symbol: str) -> MarketIntelligence:
        """Generate comprehensive market intelligence for a symbol"""
        # Collect sentiment from multiple sources
        all_sentiment_data = []
        
        for source in [NewsSource.TWITTER, NewsSource.REDDIT, NewsSource.NEWS_SITES]:
            sentiment_data = self.sentiment_analyzer.analyze_social_media(symbol, source)
            all_sentiment_data.extend(sentiment_data)
        
        # Calculate overall sentiment metrics
        if all_sentiment_data:
            sentiment_scores = [data.sentiment_score for data in all_sentiment_data]
            overall_sentiment = np.mean(sentiment_scores)
            
            # Calculate sentiment trend (comparing recent vs older data)
            recent_sentiment = np.mean([data.sentiment_score for data in all_sentiment_data[:len(all_sentiment_data)//2]])
            older_sentiment = np.mean([data.sentiment_score for data in all_sentiment_data[len(all_sentiment_data)//2:]])
            
            if recent_sentiment > older_sentiment + 0.1:
                sentiment_trend = "IMPROVING"
            elif recent_sentiment < older_sentiment - 0.1:
                sentiment_trend = "DECLINING"
            else:
                sentiment_trend = "STABLE"
        else:
            overall_sentiment = 0.0
            sentiment_trend = "STABLE"
        
        # Calculate other metrics
        news_volume = len([data for data in all_sentiment_data if data.source == NewsSource.NEWS_SITES])
        social_mentions = len([data for data in all_sentiment_data if data.source in [NewsSource.TWITTER, NewsSource.REDDIT]])
        
        # Simulate additional metrics
        influencer_sentiment = overall_sentiment + random.uniform(-0.2, 0.2)
        fear_greed_index = self._calculate_fear_greed_index(symbol)
        market_cap_sentiment = overall_sentiment + random.uniform(-0.15, 0.15)
        trading_volume_sentiment = overall_sentiment + random.uniform(-0.1, 0.1)
        
        return MarketIntelligence(
            symbol=symbol,
            overall_sentiment=overall_sentiment,
            sentiment_trend=sentiment_trend,
            news_volume=news_volume,
            social_mentions=social_mentions,
            influencer_sentiment=influencer_sentiment,
            fear_greed_index=fear_greed_index,
            market_cap_sentiment=market_cap_sentiment,
            trading_volume_sentiment=trading_volume_sentiment,
            timestamp=datetime.now()
        )
    
    def _calculate_fear_greed_index(self, symbol: str) -> float:
        """Calculate Fear & Greed Index for the symbol"""
        # Simulate fear & greed calculation based on multiple factors
        base_score = random.uniform(0, 100)
        
        # Adjust based on recent market sentiment
        if hasattr(self, 'recent_sentiment'):
            if self.recent_sentiment > 0.3:
                base_score += 20  # More greed
            elif self.recent_sentiment < -0.3:
                base_score -= 20  # More fear
        
        return max(0, min(100, base_score))
    
    def detect_trending_topics(self) -> List[TrendingTopic]:
        """Detect trending topics in cryptocurrency discussions"""
        # Simulate trending topic detection
        topics = [
            "DeFi Summer 2.0", "NFT Gaming", "Layer 2 Scaling", "Central Bank Digital Currencies",
            "Metaverse Integration", "Green Mining", "Institutional Adoption", "Regulatory Clarity",
            "Cross-chain Bridges", "AI Trading Bots", "Quantum Resistance", "Web3 Social Media"
        ]
        
        trending = []
        for topic in random.sample(topics, random.randint(3, 6)):
            trending.append(TrendingTopic(
                topic=topic,
                mentions=random.randint(100, 5000),
                sentiment=random.uniform(-0.5, 0.8),
                related_symbols=random.sample(['BTC', 'ETH', 'DGD', 'ADA', 'SOL'], random.randint(1, 3)),
                growth_rate=random.uniform(-0.2, 2.0),
                timestamp=datetime.now()
            ))
        
        self.trending_topics = trending
        return trending
    
    def get_sentiment_summary(self, symbols: List[str]) -> Dict[str, Dict]:
        """Get sentiment summary for multiple symbols"""
        summary = {}
        
        for symbol in symbols:
            intelligence = self.generate_market_intelligence(symbol)
            
            summary[symbol] = {
                'overall_sentiment': intelligence.overall_sentiment,
                'sentiment_label': self.sentiment_analyzer.get_sentiment_label(intelligence.overall_sentiment),
                'sentiment_trend': intelligence.sentiment_trend,
                'news_volume': intelligence.news_volume,
                'social_mentions': intelligence.social_mentions,
                'fear_greed_index': intelligence.fear_greed_index,
                'confidence': random.uniform(0.7, 0.95),
                'last_updated': intelligence.timestamp.isoformat()
            }
        
        return summary
    
    def get_market_mood(self) -> Dict:
        """Get overall market mood and sentiment"""
        symbols = ['BTC', 'ETH', 'DGD', 'ADA', 'SOL']
        sentiment_summary = self.get_sentiment_summary(symbols)
        
        # Calculate overall market sentiment
        overall_sentiments = [data['overall_sentiment'] for data in sentiment_summary.values()]
        market_sentiment = np.mean(overall_sentiments)
        
        # Calculate market fear & greed
        fear_greed_values = [data['fear_greed_index'] for data in sentiment_summary.values()]
        market_fear_greed = np.mean(fear_greed_values)
        
        # Determine market mood
        if market_sentiment > 0.3:
            mood = "BULLISH"
        elif market_sentiment < -0.3:
            mood = "BEARISH"
        else:
            mood = "NEUTRAL"
        
        return {
            'market_mood': mood,
            'market_sentiment': market_sentiment,
            'market_fear_greed': market_fear_greed,
            'total_news_volume': sum(data['news_volume'] for data in sentiment_summary.values()),
            'total_social_mentions': sum(data['social_mentions'] for data in sentiment_summary.values()),
            'trending_topics': len(self.trending_topics),
            'timestamp': datetime.now().isoformat()
        }

class SentimentAPI:
    """API interface for sentiment analysis and market intelligence"""
    
    def __init__(self):
        self.intelligence_engine = MarketIntelligenceEngine()
        self.cache = {}
        self.cache_duration = 300  # 5 minutes
    
    def get_sentiment_analysis(self, symbol: str) -> Dict:
        """Get sentiment analysis for a specific symbol"""
        cache_key = f"sentiment_{symbol}"
        now = datetime.now()
        
        # Check cache
        if cache_key in self.cache:
            cached_time, cached_result = self.cache[cache_key]
            if (now - cached_time).seconds < self.cache_duration:
                return cached_result
        
        try:
            intelligence = self.intelligence_engine.generate_market_intelligence(symbol)
            
            result = {
                'symbol': intelligence.symbol,
                'overall_sentiment': intelligence.overall_sentiment,
                'sentiment_label': self.intelligence_engine.sentiment_analyzer.get_sentiment_label(intelligence.overall_sentiment),
                'sentiment_trend': intelligence.sentiment_trend,
                'confidence': random.uniform(0.75, 0.95),
                'news_volume': intelligence.news_volume,
                'social_mentions': intelligence.social_mentions,
                'influencer_sentiment': intelligence.influencer_sentiment,
                'fear_greed_index': intelligence.fear_greed_index,
                'market_cap_sentiment': intelligence.market_cap_sentiment,
                'trading_volume_sentiment': intelligence.trading_volume_sentiment,
                'timestamp': intelligence.timestamp.isoformat()
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
    
    def get_market_intelligence(self) -> Dict:
        """Get overall market intelligence"""
        return self.intelligence_engine.get_market_mood()
    
    def get_trending_topics(self) -> List[Dict]:
        """Get trending topics in cryptocurrency"""
        topics = self.intelligence_engine.detect_trending_topics()
        
        return [
            {
                'topic': topic.topic,
                'mentions': topic.mentions,
                'sentiment': topic.sentiment,
                'sentiment_label': self.intelligence_engine.sentiment_analyzer.get_sentiment_label(topic.sentiment),
                'related_symbols': topic.related_symbols,
                'growth_rate': topic.growth_rate,
                'timestamp': topic.timestamp.isoformat()
            }
            for topic in topics
        ]
    
    def get_sentiment_summary(self, symbols: List[str] = None) -> Dict:
        """Get sentiment summary for multiple symbols"""
        if symbols is None:
            symbols = ['BTC', 'ETH', 'DGD', 'ADA', 'SOL']
        
        return self.intelligence_engine.get_sentiment_summary(symbols)
    
    def analyze_custom_text(self, text: str, symbol: str = None) -> Dict:
        """Analyze sentiment of custom text"""
        sentiment_score, confidence, keywords = self.intelligence_engine.sentiment_analyzer.analyze_text(text, symbol)
        
        return {
            'text': text,
            'sentiment_score': sentiment_score,
            'sentiment_label': self.intelligence_engine.sentiment_analyzer.get_sentiment_label(sentiment_score),
            'confidence': confidence,
            'keywords': keywords,
            'symbol': symbol,
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Test the sentiment analysis system
    print("Testing Sentiment Analysis System...")
    
    api = SentimentAPI()
    
    # Test sentiment analysis for BTC
    btc_sentiment = api.get_sentiment_analysis('BTC')
    print(f"BTC Sentiment: {json.dumps(btc_sentiment, indent=2)}")
    
    # Test market intelligence
    market_intel = api.get_market_intelligence()
    print(f"Market Intelligence: {json.dumps(market_intel, indent=2)}")
    
    # Test trending topics
    trending = api.get_trending_topics()
    print(f"Trending Topics: {len(trending)} topics detected")
    
    # Test custom text analysis
    custom_analysis = api.analyze_custom_text("Bitcoin is looking very bullish! To the moon! 🚀", "BTC")
    print(f"Custom Text Analysis: {json.dumps(custom_analysis, indent=2)}")
    
    # Test sentiment summary
    summary = api.get_sentiment_summary(['BTC', 'ETH', 'DGD'])
    print(f"Sentiment Summary: {len(summary)} symbols analyzed")
    
    print("Sentiment Analysis System test completed successfully!")

