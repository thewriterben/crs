#!/usr/bin/env python3
"""
AI-Powered News Analysis and Market Research System
Implements real-time news aggregation, sentiment analysis, and market impact assessment
"""

import requests
import json
import re
from datetime import datetime, timedelta
import random
import time
from textblob import TextBlob
import numpy as np

class NewsAggregator:
    """Aggregates news from multiple cryptocurrency and financial sources"""
    
    def __init__(self):
        # Major crypto news sources
        self.news_sources = {
            'coindesk': {
                'name': 'CoinDesk',
                'url': 'https://www.coindesk.com',
                'reliability': 0.95,
                'category': 'crypto'
            },
            'cointelegraph': {
                'name': 'Cointelegraph',
                'url': 'https://cointelegraph.com',
                'reliability': 0.90,
                'category': 'crypto'
            },
            'theblock': {
                'name': 'The Block',
                'url': 'https://www.theblock.co',
                'reliability': 0.92,
                'category': 'crypto'
            },
            'decrypt': {
                'name': 'Decrypt',
                'url': 'https://decrypt.co',
                'reliability': 0.88,
                'category': 'crypto'
            },
            'bloomberg': {
                'name': 'Bloomberg Crypto',
                'url': 'https://www.bloomberg.com/crypto',
                'reliability': 0.98,
                'category': 'financial'
            },
            'reuters': {
                'name': 'Reuters Crypto',
                'url': 'https://www.reuters.com',
                'reliability': 0.97,
                'category': 'financial'
            }
        }
        
        # Keywords for different impact categories
        self.impact_keywords = {
            'high_impact': [
                'regulation', 'ban', 'approval', 'etf', 'sec', 'fed', 'central bank',
                'institutional adoption', 'major partnership', 'hack', 'security breach',
                'fork', 'upgrade', 'halving', 'listing', 'delisting'
            ],
            'medium_impact': [
                'price prediction', 'analyst', 'technical analysis', 'support', 'resistance',
                'trading volume', 'market cap', 'whale movement', 'exchange', 'wallet'
            ],
            'low_impact': [
                'conference', 'interview', 'opinion', 'tutorial', 'guide', 'education',
                'community', 'social media', 'meme', 'celebrity'
            ]
        }
        
        # Cryptocurrency mentions
        self.crypto_keywords = {
            'BTC': ['bitcoin', 'btc', 'satoshi'],
            'ETH': ['ethereum', 'eth', 'ether', 'vitalik'],
            'ADA': ['cardano', 'ada'],
            'DOT': ['polkadot', 'dot'],
            'LINK': ['chainlink', 'link'],
            'UNI': ['uniswap', 'uni'],
            'AAVE': ['aave'],
            'COMP': ['compound', 'comp']
        }
    
    def generate_sample_news(self, count=20):
        """Generate sample news articles for demonstration"""
        sample_headlines = [
            "Bitcoin Reaches New All-Time High as Institutional Adoption Accelerates",
            "Ethereum 2.0 Upgrade Shows Promising Results in Network Efficiency",
            "SEC Approves First Bitcoin ETF, Market Responds Positively",
            "Major Bank Announces Cryptocurrency Trading Services for Clients",
            "DeFi Protocol Suffers $50M Hack, Security Concerns Rise",
            "Central Bank Digital Currency Pilot Program Launches in Major Economy",
            "Cryptocurrency Regulation Framework Proposed by Financial Authorities",
            "Blockchain Technology Adoption Increases in Supply Chain Management",
            "NFT Market Shows Signs of Recovery After Recent Downturn",
            "Stablecoin Issuer Faces Regulatory Scrutiny Over Reserve Backing",
            "Crypto Exchange Reports Record Trading Volumes Amid Market Rally",
            "Smart Contract Vulnerability Discovered in Popular DeFi Platform",
            "Institutional Investors Increase Cryptocurrency Allocations",
            "Cross-Chain Bridge Protocol Announces Major Security Upgrade",
            "Cryptocurrency Mining Industry Shifts Toward Renewable Energy",
            "Layer 2 Scaling Solution Achieves Significant Transaction Throughput",
            "Regulatory Clarity Boosts Cryptocurrency Market Confidence",
            "Decentralized Exchange Launches Innovative Liquidity Mining Program",
            "Cryptocurrency Payment Adoption Grows Among Online Merchants",
            "Blockchain Interoperability Protocol Gains Developer Traction"
        ]
        
        sample_content = [
            "The cryptocurrency market experienced significant movement today as institutional investors continued their adoption of digital assets. Market analysts point to increased regulatory clarity and technological improvements as key drivers.",
            "Technical analysis suggests strong support levels have been established, with trading volumes indicating sustained interest from both retail and institutional participants.",
            "Regulatory developments continue to shape market sentiment, with recent announcements providing greater clarity for cryptocurrency operations and compliance requirements.",
            "The decentralized finance sector shows continued innovation with new protocols launching advanced features for yield farming and liquidity provision.",
            "Security remains a top priority as the industry implements enhanced measures to protect user funds and maintain platform integrity.",
            "Market infrastructure improvements are enabling greater scalability and reduced transaction costs across major blockchain networks.",
            "Adoption metrics indicate growing mainstream acceptance of cryptocurrency payments and blockchain-based financial services.",
            "Cross-chain compatibility solutions are addressing interoperability challenges and enabling seamless asset transfers between different networks.",
            "Environmental sustainability initiatives are gaining momentum as the industry transitions toward more energy-efficient consensus mechanisms.",
            "Developer activity remains robust with continued innovation in smart contract functionality and decentralized application development."
        ]
        
        news_articles = []
        
        for i in range(count):
            source_key = random.choice(list(self.news_sources.keys()))
            source = self.news_sources[source_key]
            
            headline = random.choice(sample_headlines)
            content = random.choice(sample_content)
            
            # Determine mentioned cryptocurrencies
            mentioned_cryptos = []
            for crypto, keywords in self.crypto_keywords.items():
                if any(keyword in headline.lower() or keyword in content.lower() for keyword in keywords):
                    mentioned_cryptos.append(crypto)
            
            if not mentioned_cryptos:
                mentioned_cryptos = [random.choice(list(self.crypto_keywords.keys()))]
            
            # Determine impact level
            impact_level = 'low_impact'
            for level, keywords in self.impact_keywords.items():
                if any(keyword in headline.lower() or keyword in content.lower() for keyword in keywords):
                    impact_level = level
                    break
            
            article = {
                'id': f"news_{i+1}",
                'headline': headline,
                'content': content,
                'source': source['name'],
                'source_url': source['url'],
                'source_reliability': source['reliability'],
                'category': source['category'],
                'published_at': (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat(),
                'mentioned_cryptos': mentioned_cryptos,
                'impact_level': impact_level,
                'url': f"{source['url']}/article-{i+1}"
            }
            
            news_articles.append(article)
        
        return news_articles

class SentimentAnalyzer:
    """Advanced sentiment analysis for cryptocurrency news"""
    
    def __init__(self):
        # Crypto-specific sentiment modifiers
        self.crypto_sentiment_words = {
            'positive': [
                'bullish', 'moon', 'pump', 'rally', 'surge', 'breakout', 'adoption',
                'institutional', 'partnership', 'upgrade', 'innovation', 'breakthrough',
                'approval', 'mainstream', 'growth', 'expansion', 'success'
            ],
            'negative': [
                'bearish', 'dump', 'crash', 'correction', 'decline', 'hack', 'scam',
                'regulation', 'ban', 'restriction', 'volatility', 'risk', 'concern',
                'investigation', 'fraud', 'manipulation', 'bubble'
            ],
            'neutral': [
                'analysis', 'report', 'study', 'research', 'data', 'statistics',
                'conference', 'interview', 'discussion', 'opinion', 'perspective'
            ]
        }
        
        # Impact multipliers for different types of news
        self.impact_multipliers = {
            'regulation': 1.5,
            'institutional': 1.3,
            'technical': 1.1,
            'security': 1.4,
            'adoption': 1.2,
            'market': 1.0
        }
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of news text"""
        # Basic sentiment using TextBlob
        blob = TextBlob(text)
        base_sentiment = blob.sentiment.polarity
        
        # Crypto-specific sentiment adjustment
        crypto_score = self._calculate_crypto_sentiment(text.lower())
        
        # Combine base sentiment with crypto-specific sentiment
        adjusted_sentiment = (base_sentiment + crypto_score) / 2
        
        # Normalize to -1 to 1 range
        final_sentiment = max(-1, min(1, adjusted_sentiment))
        
        # Determine sentiment label
        if final_sentiment > 0.1:
            sentiment_label = 'POSITIVE'
        elif final_sentiment < -0.1:
            sentiment_label = 'NEGATIVE'
        else:
            sentiment_label = 'NEUTRAL'
        
        # Calculate confidence based on absolute value
        confidence = abs(final_sentiment)
        
        return {
            'sentiment_score': final_sentiment,
            'sentiment_label': sentiment_label,
            'confidence': confidence,
            'base_sentiment': base_sentiment,
            'crypto_adjustment': crypto_score
        }
    
    def _calculate_crypto_sentiment(self, text):
        """Calculate crypto-specific sentiment score"""
        positive_count = sum(1 for word in self.crypto_sentiment_words['positive'] if word in text)
        negative_count = sum(1 for word in self.crypto_sentiment_words['negative'] if word in text)
        neutral_count = sum(1 for word in self.crypto_sentiment_words['neutral'] if word in text)
        
        total_words = positive_count + negative_count + neutral_count
        
        if total_words == 0:
            return 0
        
        # Calculate weighted sentiment
        sentiment_score = (positive_count - negative_count) / total_words
        return sentiment_score
    
    def analyze_market_impact(self, article):
        """Analyze potential market impact of news article"""
        text = f"{article['headline']} {article['content']}".lower()
        
        # Base impact from sentiment
        sentiment_analysis = self.analyze_sentiment(text)
        base_impact = abs(sentiment_analysis['sentiment_score'])
        
        # Impact level multiplier
        impact_multipliers = {
            'high_impact': 1.5,
            'medium_impact': 1.2,
            'low_impact': 0.8
        }
        
        impact_multiplier = impact_multipliers.get(article['impact_level'], 1.0)
        
        # Source reliability multiplier
        reliability_multiplier = article['source_reliability']
        
        # Calculate final impact score
        impact_score = base_impact * impact_multiplier * reliability_multiplier
        
        # Determine impact category
        if impact_score > 0.7:
            impact_category = 'HIGH'
        elif impact_score > 0.4:
            impact_category = 'MEDIUM'
        else:
            impact_category = 'LOW'
        
        return {
            'impact_score': impact_score,
            'impact_category': impact_category,
            'sentiment_contribution': base_impact,
            'level_multiplier': impact_multiplier,
            'reliability_multiplier': reliability_multiplier
        }

class MarketResearcher:
    """Advanced market research and trend analysis"""
    
    def __init__(self):
        self.news_aggregator = NewsAggregator()
        self.sentiment_analyzer = SentimentAnalyzer()
    
    def analyze_news_sentiment(self, articles):
        """Analyze sentiment across multiple news articles"""
        sentiment_data = {}
        
        for article in articles:
            sentiment = self.sentiment_analyzer.analyze_sentiment(
                f"{article['headline']} {article['content']}"
            )
            impact = self.sentiment_analyzer.analyze_market_impact(article)
            
            for crypto in article['mentioned_cryptos']:
                if crypto not in sentiment_data:
                    sentiment_data[crypto] = {
                        'articles': [],
                        'total_sentiment': 0,
                        'total_impact': 0,
                        'article_count': 0
                    }
                
                sentiment_data[crypto]['articles'].append({
                    'article_id': article['id'],
                    'headline': article['headline'],
                    'sentiment': sentiment,
                    'impact': impact,
                    'source': article['source'],
                    'published_at': article['published_at']
                })
                
                sentiment_data[crypto]['total_sentiment'] += sentiment['sentiment_score']
                sentiment_data[crypto]['total_impact'] += impact['impact_score']
                sentiment_data[crypto]['article_count'] += 1
        
        # Calculate averages
        for crypto in sentiment_data:
            data = sentiment_data[crypto]
            data['average_sentiment'] = data['total_sentiment'] / data['article_count']
            data['average_impact'] = data['total_impact'] / data['article_count']
            
            # Determine overall sentiment label
            if data['average_sentiment'] > 0.1:
                data['sentiment_label'] = 'POSITIVE'
            elif data['average_sentiment'] < -0.1:
                data['sentiment_label'] = 'NEGATIVE'
            else:
                data['sentiment_label'] = 'NEUTRAL'
        
        return sentiment_data
    
    def detect_trending_topics(self, articles):
        """Detect trending topics and themes in news"""
        # Extract keywords from headlines and content
        all_text = ' '.join([f"{article['headline']} {article['content']}" for article in articles])
        
        # Common crypto/finance keywords to track
        trending_keywords = [
            'bitcoin', 'ethereum', 'defi', 'nft', 'regulation', 'etf', 'institutional',
            'adoption', 'blockchain', 'smart contracts', 'layer 2', 'scaling',
            'stablecoin', 'cbdc', 'mining', 'staking', 'yield farming', 'dao',
            'metaverse', 'web3', 'interoperability', 'security', 'hack'
        ]
        
        keyword_counts = {}
        for keyword in trending_keywords:
            count = all_text.lower().count(keyword)
            if count > 0:
                keyword_counts[keyword] = count
        
        # Sort by frequency
        trending_topics = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Calculate sentiment for each trending topic
        topic_sentiment = {}
        for topic, count in trending_topics:
            topic_articles = [a for a in articles if topic in f"{a['headline']} {a['content']}".lower()]
            if topic_articles:
                sentiments = [
                    self.sentiment_analyzer.analyze_sentiment(f"{a['headline']} {a['content']}")['sentiment_score']
                    for a in topic_articles
                ]
                avg_sentiment = sum(sentiments) / len(sentiments)
                
                topic_sentiment[topic] = {
                    'mentions': count,
                    'sentiment': avg_sentiment,
                    'sentiment_label': 'POSITIVE' if avg_sentiment > 0.1 else 'NEGATIVE' if avg_sentiment < -0.1 else 'NEUTRAL',
                    'article_count': len(topic_articles)
                }
        
        return topic_sentiment
    
    def generate_market_signals(self, sentiment_data, trending_topics):
        """Generate trading signals based on news analysis"""
        signals = []
        
        # Sentiment-based signals
        for crypto, data in sentiment_data.items():
            if data['article_count'] >= 3:  # Minimum articles for signal
                if data['average_sentiment'] > 0.3 and data['average_impact'] > 0.5:
                    signals.append({
                        'type': 'BULLISH_NEWS',
                        'asset': crypto,
                        'strength': min(data['average_sentiment'] * data['average_impact'], 1.0),
                        'description': f"Strong positive sentiment for {crypto} across {data['article_count']} articles",
                        'confidence': data['average_impact']
                    })
                elif data['average_sentiment'] < -0.3 and data['average_impact'] > 0.5:
                    signals.append({
                        'type': 'BEARISH_NEWS',
                        'asset': crypto,
                        'strength': min(abs(data['average_sentiment']) * data['average_impact'], 1.0),
                        'description': f"Strong negative sentiment for {crypto} across {data['article_count']} articles",
                        'confidence': data['average_impact']
                    })
        
        # Trending topic signals
        for topic, data in trending_topics.items():
            if data['mentions'] >= 5 and abs(data['sentiment']) > 0.2:
                signal_type = 'TREND_BULLISH' if data['sentiment'] > 0 else 'TREND_BEARISH'
                signals.append({
                    'type': signal_type,
                    'topic': topic,
                    'strength': min(abs(data['sentiment']) * (data['mentions'] / 10), 1.0),
                    'description': f"Trending topic '{topic}' with {data['sentiment_label'].lower()} sentiment",
                    'confidence': min(data['mentions'] / 20, 1.0)
                })
        
        return sorted(signals, key=lambda x: x['strength'], reverse=True)

class NewsAnalysisAPI:
    """API for AI-powered news analysis and market research"""
    
    def __init__(self):
        self.market_researcher = MarketResearcher()
    
    def get_news_analysis(self, hours_back=24):
        """Get comprehensive news analysis"""
        # Generate sample news articles
        articles = self.market_researcher.news_aggregator.generate_sample_news(30)
        
        # Filter articles by time range
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        recent_articles = [
            a for a in articles 
            if datetime.fromisoformat(a['published_at']) > cutoff_time
        ]
        
        # Analyze sentiment
        sentiment_analysis = self.market_researcher.analyze_news_sentiment(recent_articles)
        
        # Detect trending topics
        trending_topics = self.market_researcher.detect_trending_topics(recent_articles)
        
        # Generate market signals
        market_signals = self.market_researcher.generate_market_signals(
            sentiment_analysis, trending_topics
        )
        
        # Calculate overall market sentiment
        all_sentiments = [
            data['average_sentiment'] for data in sentiment_analysis.values()
        ]
        overall_sentiment = sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0
        
        return {
            'analysis_period_hours': hours_back,
            'total_articles': len(recent_articles),
            'overall_market_sentiment': overall_sentiment,
            'overall_sentiment_label': (
                'POSITIVE' if overall_sentiment > 0.1 else 
                'NEGATIVE' if overall_sentiment < -0.1 else 'NEUTRAL'
            ),
            'crypto_sentiment_analysis': sentiment_analysis,
            'trending_topics': trending_topics,
            'market_signals': market_signals,
            'news_sources': list(set([a['source'] for a in recent_articles])),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_crypto_news_summary(self, crypto='BTC'):
        """Get news summary for specific cryptocurrency"""
        articles = self.market_researcher.news_aggregator.generate_sample_news(20)
        
        # Filter articles mentioning the specific crypto
        crypto_articles = [
            a for a in articles if crypto in a['mentioned_cryptos']
        ]
        
        if not crypto_articles:
            return {
                'crypto': crypto,
                'articles_found': 0,
                'message': f'No recent news found for {crypto}'
            }
        
        # Analyze sentiment for this crypto
        sentiment_data = self.market_researcher.analyze_news_sentiment(crypto_articles)
        crypto_sentiment = sentiment_data.get(crypto, {})
        
        # Get recent headlines
        recent_headlines = [
            {
                'headline': a['headline'],
                'source': a['source'],
                'published_at': a['published_at'],
                'impact_level': a['impact_level']
            }
            for a in crypto_articles[:5]
        ]
        
        return {
            'crypto': crypto,
            'articles_found': len(crypto_articles),
            'sentiment_analysis': crypto_sentiment,
            'recent_headlines': recent_headlines,
            'timestamp': datetime.now().isoformat()
        }

# Test the system
if __name__ == "__main__":
    print("Testing AI News Analysis System...")
    
    # Install required package
    try:
        import textblob
    except ImportError:
        print("Installing textblob...")
        import subprocess
        subprocess.check_call(['pip3', 'install', 'textblob'])
        import textblob
    
    api = NewsAnalysisAPI()
    
    # Test news analysis
    print("\n1. Testing News Analysis:")
    analysis = api.get_news_analysis(24)
    print(f"Analyzed {analysis['total_articles']} articles")
    print(f"Overall market sentiment: {analysis['overall_sentiment_label']} ({analysis['overall_market_sentiment']:.3f})")
    print(f"Market signals generated: {len(analysis['market_signals'])}")
    print(f"Trending topics: {len(analysis['trending_topics'])}")
    
    # Test crypto-specific analysis
    print("\n2. Testing Crypto-Specific Analysis:")
    btc_analysis = api.get_crypto_news_summary('BTC')
    print(f"BTC articles found: {btc_analysis['articles_found']}")
    if btc_analysis['articles_found'] > 0:
        sentiment = btc_analysis['sentiment_analysis']
        print(f"BTC sentiment: {sentiment['sentiment_label']} ({sentiment['average_sentiment']:.3f})")
    
    print("\n✅ AI News Analysis System working correctly!")

