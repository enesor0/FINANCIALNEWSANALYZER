"""
In-Memory News Repository Implementation
For development and testing purposes
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

from ...domain.repositories.news_repository import INewsRepository
from ...domain.entities.financial_news import FinancialNews, NewsCategory, NewsSource

class InMemoryNewsRepository(INewsRepository):
    """
    In-memory implementation of news repository
    Useful for development, testing, and demos
    """
    
    def __init__(self):
        """Initialize with empty news storage"""
        self._news_storage: Dict[str, FinancialNews] = {}
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample news data for demo purposes"""
        sample_news = [
            FinancialNews(
                id=str(uuid.uuid4()),
                title="Tech Stocks Rally on Strong Earnings Reports",
                content="Major technology companies reported better-than-expected earnings, driving significant gains in tech stock prices. The positive momentum reflects strong demand for digital services and cloud computing solutions.",
                source=NewsSource.BLOOMBERG,
                category=NewsCategory.EARNINGS,
                published_at=datetime.now() - timedelta(hours=2),
                summary="Tech sector shows strong performance with positive earnings",
                keywords=["tech", "earnings", "rally", "stocks", "cloud"],
                mentioned_symbols=["AAPL", "MSFT", "GOOGL", "AMZN"],
                sentiment_score=0.75,
                confidence_score=0.85,
                impact_score=0.8
            ),
            FinancialNews(
                id=str(uuid.uuid4()),
                title="Federal Reserve Signals Potential Interest Rate Changes",
                content="The Federal Reserve indicated possible adjustments to interest rates in response to recent economic indicators. Market analysts are closely watching for signals about monetary policy direction.",
                source=NewsSource.REUTERS,
                category=NewsCategory.ECONOMIC_INDICATORS,
                published_at=datetime.now() - timedelta(hours=4),
                summary="Fed hints at interest rate policy adjustments",
                keywords=["federal reserve", "interest rates", "monetary policy", "economy"],
                mentioned_symbols=["SPY", "TLT", "DXY"],
                sentiment_score=-0.15,
                confidence_score=0.9,
                impact_score=0.95
            ),
            # Add more sample data...
        ]
        
        for news in sample_news:
            self._news_storage[news.id] = news
    
    def save(self, news: FinancialNews) -> bool:
        """Save a news article"""
        try:
            if not news.id:
                news.id = str(uuid.uuid4())
            self._news_storage[news.id] = news
            return True
        except Exception:
            return False
    
    def find_by_id(self, news_id: str) -> Optional[FinancialNews]:
        """Find news by ID"""
        return self._news_storage.get(news_id)
    
    def find_by_criteria(self, criteria) -> List[FinancialNews]:
        """Find news by search criteria"""
        results = list(self._news_storage.values())
        
        # Apply time filters
        if criteria.start_date:
            results = [n for n in results if n.published_at >= criteria.start_date]
        
        if criteria.end_date:
            results = [n for n in results if n.published_at <= criteria.end_date]
        
        # Apply content filters
        if criteria.categories:
            results = [n for n in results if n.category in criteria.categories]
        
        if criteria.sources:
            results = [n for n in results if n.source in criteria.sources]
        
        if criteria.symbols:
            results = [n for n in results 
                      if n.mentioned_symbols and 
                      any(symbol in n.mentioned_symbols for symbol in criteria.symbols)]
        
        if criteria.keywords:
            results = [n for n in results 
                      if n.keywords and 
                      any(keyword.lower() in [k.lower() for k in n.keywords] 
                          for keyword in criteria.keywords)]
        
        # Apply sentiment filters
        if criteria.min_sentiment_score is not None:
            results = [n for n in results 
                      if n.sentiment_score is not None and 
                      n.sentiment_score >= criteria.min_sentiment_score]
        
        if criteria.max_sentiment_score is not None:
            results = [n for n in results 
                      if n.sentiment_score is not None and 
                      n.sentiment_score <= criteria.max_sentiment_score]
        
        # Apply impact filters
        if criteria.min_impact_score is not None:
            results = [n for n in results 
                      if n.impact_score is not None and 
                      n.impact_score >= criteria.min_impact_score]
        
        return results
    
    def find_by_symbol(self, symbol: str, limit: int = 50) -> List[FinancialNews]:
        """Find news mentioning specific stock symbol"""
        results = []
        symbol_upper = symbol.upper()
        
        for news in self._news_storage.values():
            if (news.mentioned_symbols and 
                symbol_upper in [s.upper() for s in news.mentioned_symbols]):
                results.append(news)
        
        # Sort by published date (newest first)
        results.sort(key=lambda x: x.published_at, reverse=True)
        return results[:limit]
    
    def find_by_category(self, category: NewsCategory, limit: int = 50) -> List[FinancialNews]:
        """Find news by category"""
        results = [news for news in self._news_storage.values() 
                  if news.category == category]
        
        results.sort(key=lambda x: x.published_at, reverse=True)
        return results[:limit]
    
    def find_by_source(self, source: NewsSource, limit: int = 50) -> List[FinancialNews]:
        """Find news by source"""
        results = [news for news in self._news_storage.values() 
                  if news.source == source]
        
        results.sort(key=lambda x: x.published_at, reverse=True)
        return results[:limit]
    
    def find_recent(self, hours_back: int = 24, limit: int = 50) -> List[FinancialNews]:
        """Find recent news within specified time window"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        results = [news for news in self._news_storage.values() 
                  if news.published_at >= cutoff_time]
        
        results.sort(key=lambda x: x.published_at, reverse=True)
        return results[:limit]
    
    def find_by_sentiment_range(self, min_score: float, max_score: float, 
                               limit: int = 50) -> List[FinancialNews]:
        """Find news by sentiment score range"""
        results = []
        
        for news in self._news_storage.values():
            if (news.sentiment_score is not None and 
                min_score <= news.sentiment_score <= max_score):
                results.append(news)
        
        results.sort(key=lambda x: x.published_at, reverse=True)
        return results[:limit]
    
    def find_high_impact(self, min_impact: float = 0.7, limit: int = 50) -> List[FinancialNews]:
        """Find high-impact news articles"""
        results = []
        
        for news in self._news_storage.values():
            if news.impact_score is not None and news.impact_score >= min_impact:
                results.append(news)
        
        results.sort(key=lambda x: x.impact_score or 0, reverse=True)
        return results[:limit]
    
    def update(self, news: FinancialNews) -> bool:
        """Update existing news article"""
        try:
            if news.id in self._news_storage:
                self._news_storage[news.id] = news
                return True
            return False
        except Exception:
            return False
    
    def delete(self, news_id: str) -> bool:
        """Delete news article by ID"""
        try:
            if news_id in self._news_storage:
                del self._news_storage[news_id]
                return True
            return False
        except Exception:
            return False
    
    def count_by_criteria(self, criteria) -> int:
        """Count news articles matching criteria"""
        results = self.find_by_criteria(criteria)
        return len(results)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get repository statistics"""
        total_count = len(self._news_storage)
        
        if total_count == 0:
            return {"total_articles": 0}
        
        # Calculate category distribution
        category_counts = {}
        source_counts = {}
        sentiment_scores = []
        impact_scores = []
        
        for news in self._news_storage.values():
            # Categories
            category = news.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
            
            # Sources
            source = news.source.value
            source_counts[source] = source_counts.get(source, 0) + 1
            
            # Sentiment scores
            if news.sentiment_score is not None:
                sentiment_scores.append(news.sentiment_score)
            
            # Impact scores
            if news.impact_score is not None:
                impact_scores.append(news.impact_score)
        
        return {
            "total_articles": total_count,
            "category_distribution": category_counts,
            "source_distribution": source_counts,
            "sentiment_stats": {
                "count": len(sentiment_scores),
                "average": sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0,
                "min": min(sentiment_scores) if sentiment_scores else None,
                "max": max(sentiment_scores) if sentiment_scores else None
            },
            "impact_stats": {
                "count": len(impact_scores),
                "average": sum(impact_scores) / len(impact_scores) if impact_scores else 0,
                "min": min(impact_scores) if impact_scores else None,
                "max": max(impact_scores) if impact_scores else None
            }
        }
