"""
This module provides mock data for tickers when real data is unavailable or for testing purposes.
"""

import datetime
import random
import uuid
import numpy as np


def generate_mock_ticker_info(ticker_symbol):
    """Generate mock ticker info data for a given symbol.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        
    Returns:
        dict: Mock ticker information.
    """
    # Dictionary of well-known tickers with actual company information
    known_tickers = {
        'T': {
            'shortName': 'AT&T Inc.',
            'longName': 'AT&T Inc.',
            'sector': 'Communication Services',
            'industry': 'Telecom Services',
            'country': 'United States',
            'website': 'https://www.att.com',
            'longBusinessSummary': 'AT&T Inc. provides telecommunications, media, and technology services worldwide. Its Communications segment offers wireless voice and data communications services; and sells handsets, wireless data cards, wireless computing devices, and carrying cases and hands-free devices through its own company-owned stores, agents, and third-party retail stores.',
        },
        'AAPL': {
            'shortName': 'Apple Inc.',
            'longName': 'Apple Inc.',
            'sector': 'Technology',
            'industry': 'Consumer Electronics',
            'country': 'United States',
            'website': 'https://www.apple.com',
            'longBusinessSummary': 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells various related services. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, and HomePod.',
        },
        'MSFT': {
            'shortName': 'Microsoft Corporation',
            'longName': 'Microsoft Corporation',
            'sector': 'Technology',
            'industry': 'Software - Infrastructure',
            'country': 'United States',
            'website': 'https://www.microsoft.com',
            'longBusinessSummary': 'Microsoft Corporation develops, licenses, and supports software, services, devices, and solutions worldwide. The company operates in three segments: Productivity and Business Processes, Intelligent Cloud, and More Personal Computing.',
        },
        'AMZN': {
            'shortName': 'Amazon.com, Inc.',
            'longName': 'Amazon.com, Inc.',
            'sector': 'Consumer Cyclical',
            'industry': 'Internet Retail',
            'country': 'United States',
            'website': 'https://www.amazon.com',
            'longBusinessSummary': 'Amazon.com, Inc. engages in the retail sale of consumer products and subscriptions through online and physical stores in North America and internationally. It operates through three segments: North America, International, and Amazon Web Services (AWS).',
        },
        'GOOGL': {
            'shortName': 'Alphabet Inc.',
            'longName': 'Alphabet Inc.',
            'sector': 'Communication Services',
            'industry': 'Internet Content & Information',
            'country': 'United States',
            'website': 'https://www.abc.xyz',
            'longBusinessSummary': 'Alphabet Inc. provides various products and platforms in the United States, Europe, the Middle East, Africa, the Asia-Pacific, Canada, and Latin America. It operates through Google Services, Google Cloud, and Other Bets segments.',
        },
        'META': {
            'shortName': 'Meta Platforms, Inc.',
            'longName': 'Meta Platforms, Inc.',
            'sector': 'Communication Services',
            'industry': 'Internet Content & Information',
            'country': 'United States',
            'website': 'https://www.meta.com',
            'longBusinessSummary': 'Meta Platforms, Inc. develops products that enable people to connect and share with friends and family through mobile devices, personal computers, virtual reality headsets, and wearables worldwide. It operates in two segments, Family of Apps and Reality Labs.',
        },
        'TSLA': {
            'shortName': 'Tesla, Inc.',
            'longName': 'Tesla, Inc.',
            'sector': 'Consumer Cyclical',
            'industry': 'Auto Manufacturers',
            'country': 'United States',
            'website': 'https://www.tesla.com',
            'longBusinessSummary': 'Tesla, Inc. designs, develops, manufactures, leases, and sells electric vehicles, and energy generation and storage systems in the United States, China, and internationally. The company operates in two segments, Automotive, and Energy Generation and Storage.',
        }
    }
    
    price = round(random.uniform(50, 500), 2)
    market_cap = random.randint(1000000000, 2000000000000)
    
    # Check if it's a known ticker
    if ticker_symbol in known_tickers:
        company_info = known_tickers[ticker_symbol]
        
        # For known tickers, use more appropriate prices
        if ticker_symbol == 'T':
            price = round(random.uniform(15, 25), 2)  # AT&T typically trades in this range
            market_cap = random.randint(100000000000, 200000000000)
        elif ticker_symbol == 'AAPL':
            price = round(random.uniform(150, 200), 2)
            market_cap = random.randint(2000000000000, 3000000000000)
        elif ticker_symbol == 'MSFT':
            price = round(random.uniform(300, 350), 2)
            market_cap = random.randint(2000000000000, 3000000000000)
            
        # Create info for known ticker
        mock_info = {
            'ticker': ticker_symbol,
            'data': {
                'symbol': ticker_symbol,
                'shortName': company_info['shortName'],
                'longName': company_info['longName'],
                'sector': company_info['sector'],
                'industry': company_info['industry'],
                'fullTimeEmployees': random.randint(10000, 150000),
                'country': company_info['country'],
                'website': company_info['website'],
                'longBusinessSummary': company_info['longBusinessSummary'],
                'marketCap': market_cap,
                'trailingPE': round(random.uniform(10, 40), 2),
                'forwardPE': round(random.uniform(8, 35), 2),
                'trailingEps': round(random.uniform(1, 15), 2),
                'forwardEps': round(random.uniform(1, 20), 2),
                'dividendYield': round(random.uniform(0, 0.05), 4),
                'dividendRate': round(random.uniform(0, 5), 2),
                'fiveYearAvgDividendYield': round(random.uniform(0, 0.06), 4),
                'fiftyTwoWeekHigh': round(price * 1.3, 2),
                'fiftyTwoWeekLow': round(price * 0.7, 2),
                'previousClose': round(price * (1 - random.uniform(-0.05, 0.05)), 2),
                'open': round(price * (1 - random.uniform(-0.02, 0.02)), 2),
                'dayHigh': round(price * (1 + random.uniform(0, 0.05)), 2),
                'dayLow': round(price * (1 - random.uniform(0, 0.05)), 2),
                'volume': random.randint(1000000, 20000000),
                'averageVolume': random.randint(2000000, 15000000),
                'averageVolume10days': random.randint(2000000, 15000000),
                'beta': round(random.uniform(0.5, 2.0), 2),
                'priceToBook': round(random.uniform(1, 10), 2),
                'targetHighPrice': round(price * 1.5, 2),
                'targetLowPrice': round(price * 0.8, 2),
                'targetMeanPrice': round(price * 1.2, 2),
                'targetMedianPrice': round(price * 1.15, 2),
            }
        }
    else:
        # Generate generic mock data for unknown ticker
        mock_info = {
            'ticker': ticker_symbol,
            'data': {
                'symbol': ticker_symbol,
                'shortName': f"{ticker_symbol} Corporation",
                'longName': f"{ticker_symbol} Technology Corporation",
                'sector': random.choice(['Technology', 'Healthcare', 'Consumer Cyclical', 'Financial Services']),
                'industry': random.choice(['Software', 'Semiconductors', 'Biotechnology', 'Banks']),
                'fullTimeEmployees': random.randint(1000, 100000),
                'country': random.choice(['United States', 'China', 'Japan', 'Germany', 'United Kingdom']),
                'website': f"https://www.{ticker_symbol.lower()}.com",
                'longBusinessSummary': f"A leading company in the {random.choice(['technology', 'healthcare', 'finance', 'entertainment'])} sector, {ticker_symbol} Corporation develops innovative solutions for businesses and consumers worldwide. With a strong focus on R&D, the company continues to expand its market presence through strategic partnerships and acquisitions.",
                'marketCap': market_cap,
                'trailingPE': round(random.uniform(10, 40), 2),
                'forwardPE': round(random.uniform(8, 35), 2),
                'trailingEps': round(random.uniform(1, 15), 2),
                'forwardEps': round(random.uniform(1, 20), 2),
                'dividendYield': round(random.uniform(0, 0.05), 4),
                'dividendRate': round(random.uniform(0, 5), 2),
                'fiveYearAvgDividendYield': round(random.uniform(0, 0.06), 4),
                'fiftyTwoWeekHigh': round(price * 1.3, 2),
                'fiftyTwoWeekLow': round(price * 0.7, 2),
                'previousClose': round(price * (1 - random.uniform(-0.05, 0.05)), 2),
                'open': round(price * (1 - random.uniform(-0.02, 0.02)), 2),
                'dayHigh': round(price * (1 + random.uniform(0, 0.05)), 2),
                'dayLow': round(price * (1 - random.uniform(0, 0.05)), 2),
                'volume': random.randint(1000000, 20000000),
                'averageVolume': random.randint(2000000, 15000000),
                'averageVolume10days': random.randint(2000000, 15000000),
                'beta': round(random.uniform(0.5, 2.0), 2),
                'priceToBook': round(random.uniform(1, 10), 2),
                'targetHighPrice': round(price * 1.5, 2),
                'targetLowPrice': round(price * 0.8, 2),
                'targetMeanPrice': round(price * 1.2, 2),
                'targetMedianPrice': round(price * 1.15, 2),
            }
        }
    
    return mock_info


def generate_mock_history_data(ticker_symbol, start, end, interval='1d'):
    """Generate mock historical price data.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        start (str): Start date in YYYY-MM-DD format.
        end (str): End date in YYYY-MM-DD format.
        interval (str, optional): Data interval. Defaults to '1d'.
        
    Returns:
        list: A list of historical price data points.
    """
    try:
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d')
    except ValueError:
        # Handle invalid date formats
        start_date = datetime.datetime.now() - datetime.timedelta(days=365)
        end_date = datetime.datetime.now()
    
    if interval == '1d':
        days_delta = 1
    elif interval == '1wk':
        days_delta = 7
    elif interval == '1mo':
        days_delta = 30
    else:
        days_delta = 1
    
    # Calculate number of data points
    delta = end_date - start_date
    num_points = max(delta.days // days_delta, 1)
    
    # Dictionary of realistic price ranges for known tickers
    ticker_price_data = {
        'T': {
            'base_price': 17.0,              # AT&T price range $16-19
            'volatility': 0.01,              # Lower volatility
            'volume_base': 35000000,         # Higher volume for T
            'volume_std': 10000000
        },
        'AAPL': {
            'base_price': 170.0,             # Apple price range $165-190
            'volatility': 0.015,
            'volume_base': 60000000,
            'volume_std': 15000000
        },
        'MSFT': {
            'base_price': 330.0,             # Microsoft price range $310-350
            'volatility': 0.012,
            'volume_base': 25000000,
            'volume_std': 8000000
        },
        'AMZN': {
            'base_price': 180.0,             # Amazon price range $170-200
            'volatility': 0.018,
            'volume_base': 30000000,
            'volume_std': 10000000
        },
        'GOOGL': {
            'base_price': 140.0,             # Google price range $130-155
            'volatility': 0.014,
            'volume_base': 25000000,
            'volume_std': 8000000
        },
        'META': {
            'base_price': 420.0,             # Meta price range $390-480
            'volatility': 0.02,
            'volume_base': 20000000,
            'volume_std': 7000000
        },
        'TSLA': {
            'base_price': 175.0,             # Tesla price range $150-220
            'volatility': 0.025,             # Higher volatility
            'volume_base': 100000000,        # High volume
            'volume_std': 30000000
        }
    }
    
    # Default values for unknown tickers
    default_data = {
        'base_price': random.uniform(100, 300),
        'volatility': 0.02,                  # Standard volatility
        'volume_base': 5000000,
        'volume_std': 2000000
    }
    
    # Get price data for the ticker
    price_data = ticker_price_data.get(ticker_symbol, default_data)
    base_price = price_data['base_price']
    volatility = price_data['volatility']
    volume_base = price_data['volume_base']
    volume_std = price_data['volume_std']
    
    # Generate random walk for price movement with appropriate volatility
    np.random.seed(hash(ticker_symbol) % 2**32)  # Seed for reproducibility based on ticker
    changes = np.random.normal(0, volatility, num_points)  # Daily returns with ticker-specific volatility
    
    # For some tickers like T, add a slight positive or negative trend
    if ticker_symbol == 'T':
        # AT&T has had a slight downward trend recently
        trend = -0.0002  # Slight downward
        changes = changes + trend
    elif ticker_symbol in ['AAPL', 'MSFT', 'GOOGL']:
        # Tech companies often have slight upward trend
        trend = 0.0003  # Slight upward
        changes = changes + trend
    
    cumulative_returns = np.cumprod(1 + changes)
    prices = base_price * cumulative_returns
    
    data = []
    current_date = start_date
    
    for i in range(num_points):
        if current_date > end_date:
            break
            
        # Calculate daily price data
        close_price = prices[i]
        open_price = close_price * (1 + np.random.normal(0, volatility/4))  # Open price with small random difference
        high_price = max(close_price, open_price) * (1 + abs(np.random.normal(0, volatility/2)))  # High slightly above
        low_price = min(close_price, open_price) * (1 - abs(np.random.normal(0, volatility/2)))   # Low slightly below
        volume = int(np.random.normal(volume_base, volume_std))  # Random volume with ticker-specific parameters
        
        data_point = {
            'date': current_date.strftime('%Y-%m-%d'),
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2),
            'volume': max(volume, 100000),  # Ensure volume is positive and reasonable
            'dividends': 0.0,
            'stock_splits': 0.0
        }
        
        # Add dividend for AT&T quarterly (they pay around $0.28 per quarter)
        if ticker_symbol == 'T' and i > 0 and i % 60 == 0:  # Roughly quarterly
            data_point['dividends'] = 0.28
        
        data.append(data_point)
        current_date += datetime.timedelta(days=days_delta)
    
    return data


def generate_mock_dividends(ticker_symbol):
    """Generate mock dividend data.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        
    Returns:
        dict: Mock dividend data.
    """
    # Decide if this stock pays dividends
    pays_dividends = random.random() > 0.3  # 70% chance of paying dividends
    
    if not pays_dividends:
        return {}
    
    # Generate quarterly dividends for the past 3 years
    dividends = {}
    current_date = datetime.datetime.now()
    
    # Some companies pay dividends, create a reasonable dividend amount
    dividend_amount = round(random.uniform(0.1, 3.0), 2)
    
    for i in range(12):  # 12 quarters (3 years)
        # Go back in time, one quarter at a time
        dividend_date = current_date - datetime.timedelta(days=90 * i)
        date_str = dividend_date.strftime('%Y-%m-%d')
        
        # Add small variations to dividend amount
        actual_dividend = dividend_amount * (1 + random.uniform(-0.05, 0.05))
        dividends[date_str] = round(actual_dividend, 2)
    
    return dividends


def generate_mock_splits(ticker_symbol):
    """Generate mock stock split data.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        
    Returns:
        dict: Mock stock split data.
    """
    # Stock splits are rare, so most stocks won't have any
    has_split = random.random() > 0.7  # 30% chance of having splits
    
    if not has_split:
        return {}
    
    splits = {}
    current_date = datetime.datetime.now()
    
    # Generate between 0 and 2 splits in the past 5 years
    num_splits = random.randint(1, 2)
    
    for i in range(num_splits):
        # Random date in the past 5 years
        days_ago = random.randint(180, 5 * 365)
        split_date = (current_date - datetime.timedelta(days=days_ago)).strftime('%Y-%m-%d')
        
        # Typically splits are 2:1, 3:1, 4:1, or reverse splits like 1:2
        common_splits = [2.0, 3.0, 4.0, 0.5]
        split_ratio = random.choice(common_splits)
        
        splits[split_date] = split_ratio
    
    return splits


def generate_mock_recommendations(ticker_symbol):
    """Generate mock analyst recommendations.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        
    Returns:
        list: Mock analyst recommendations.
    """
    recommendations = []
    current_date = datetime.datetime.now()
    
    firms = [
        "Morgan Stanley", "Goldman Sachs", "JP Morgan", "Bank of America", 
        "Citigroup", "Wells Fargo", "UBS", "Deutsche Bank", "Credit Suisse", 
        "Barclays", "HSBC", "RBC Capital", "Jefferies", "Piper Sandler"
    ]
    
    grades = ["Buy", "Sell", "Hold", "Underperform", "Outperform", "Neutral", "Overweight", "Equal-Weight"]
    
    # Create recommendations for the past year, approximately monthly
    for i in range(12):
        rec_date = current_date - datetime.timedelta(days=30 * i)
        
        rec = {
            'firm': random.choice(firms),
            'to_grade': random.choice(grades),
            'from_grade': random.choice(grades),
            'action': random.choice(["main", "init", "up", "down", "reit"]),
            'date': rec_date.strftime('%Y-%m-%d')
        }
        
        recommendations.append(rec)
    
    return recommendations


def generate_mock_calendar(ticker_symbol):
    """Generate mock calendar events data.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        
    Returns:
        dict: Mock calendar events.
    """
    current_date = datetime.datetime.now()
    next_quarter = current_date + datetime.timedelta(days=90)
    
    calendar = {
        'earnings_date': next_quarter.strftime('%Y-%m-%d'),
        'earnings_time': random.choice(['bmo', 'amc']),  # before market open or after market close
        'revenue_estimate': round(random.uniform(1000000000, 20000000000), 2),
        'earnings_estimate': round(random.uniform(0.5, 5.0), 2),
        'dividend_date': (current_date + datetime.timedelta(days=random.randint(10, 60))).strftime('%Y-%m-%d'),
        'ex_dividend_date': (current_date + datetime.timedelta(days=random.randint(5, 30))).strftime('%Y-%m-%d')
    }
    
    return calendar


def generate_mock_news(ticker_symbol):
    """Generate mock news articles that match the yfinance structure.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        
    Returns:
        list: Mock news articles formatted like yfinance responses.
    """
    news = []
    current_time = datetime.datetime.now()
    
    publishers = [
        "Reuters", "Bloomberg", "CNBC", "Wall Street Journal", "Financial Times",
        "Yahoo Finance", "MarketWatch", "Seeking Alpha", "The Motley Fool", "Business Insider"
    ]
    
    # Types of news headlines
    headline_templates = [
        f"{ticker_symbol} Reports Q{random.randint(1, 4)} Earnings, Beats Expectations",
        f"{ticker_symbol} Announces New Product Line",
        f"{ticker_symbol} CEO Discusses Future Growth Strategy",
        f"Analysts Upgrade {ticker_symbol} Stock Rating",
        f"{ticker_symbol} Expands into New Markets",
        f"Is {ticker_symbol} Stock a Buy Right Now?",
        f"{ticker_symbol} Completes Acquisition of Competitor",
        f"Why {ticker_symbol} Stock Jumped Today",
        f"{ticker_symbol} Faces Challenges in Current Market",
        f"Institutional Investors Increase Stakes in {ticker_symbol}"
    ]
    
    # Create 5-10 news articles
    for i in range(random.randint(5, 10)):
        # News from the past 30 days
        days_ago = random.randint(0, 30)
        news_time = current_time - datetime.timedelta(days=days_ago, hours=random.randint(0, 24))
        
        headline = random.choice(headline_templates)
        publisher = random.choice(publishers)
        
        # Create a slug from the headline
        slug = headline.lower().replace(" ", "-").replace(",", "").replace(".", "")
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        # Generate a Yahoo Finance style URL and ID
        yahoo_id = f"{random.randint(100000, 999999)}"
        uuid_id = str(uuid.uuid4())
        
        # Generate summary
        summary = f"This article discusses the latest developments at {ticker_symbol}. " + \
                 f"The company has been making strategic moves in the {random.choice(['technology', 'healthcare', 'finance', 'retail'])} sector. " + \
                 f"Analysts are {random.choice(['optimistic', 'cautious', 'divided'])} about the company's future prospects."
        
        # Format the publication date in ISO format
        pub_date = news_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # Decide if this article has a thumbnail (about 60% of articles do)
        has_thumbnail = random.random() < 0.6
        
        # Build the article structure matching yfinance
        article = {
            'id': uuid_id,
            'content': {
                'id': uuid_id,
                'contentType': random.choice(["STORY", "VIDEO", "BLOG"]),
                'title': headline,
                'summary': summary,
                'pubDate': pub_date,
                'isHosted': True,
                'provider': {
                    'displayName': publisher,
                    'url': f"https://{publisher.lower().replace(' ', '')}.com/"
                },
                'canonicalUrl': {
                    'url': f"https://finance.yahoo.com/news/{slug}-{yahoo_id}.html"
                },
                'clickThroughUrl': {
                    'url': f"https://finance.yahoo.com/news/{slug}-{yahoo_id}.html"
                }
            }
        }
        
        # Add thumbnail if applicable
        if has_thumbnail:
            img_id = random.randint(1000, 9999)
            article['content']['thumbnail'] = {
                'originalUrl': f"https://s.yimg.com/os/creatr-uploaded-images/2025-03/{img_id}-{ticker_symbol.lower()}.jpg",
                'originalWidth': random.choice([1280, 1920, 2740]),
                'originalHeight': random.choice([720, 1080, 1539]),
                'resolutions': [
                    {
                        'url': f"https://s.yimg.com/uu/api/res/1.2/img_{img_id}_{ticker_symbol.lower()}.jpg",
                        'width': 2740,
                        'height': 1539,
                        'tag': 'original'
                    },
                    {
                        'url': f"https://s.yimg.com/uu/api/res/1.2/thumb_{img_id}_{ticker_symbol.lower()}.jpg",
                        'width': 170,
                        'height': 128,
                        'tag': '170x128'
                    }
                ]
            }
        
        # Add frontend-expected fields directly at the top level for compatibility
        article['title'] = headline
        article['publisher'] = publisher
        article['link'] = f"https://finance.yahoo.com/news/{slug}-{yahoo_id}.html"
        article['providerPublishTime'] = int(news_time.timestamp())
        article['type'] = article['content']['contentType']
        article['summary'] = summary
        
        # If there's a thumbnail, make it accessible at the top level too
        if has_thumbnail:
            article['thumbnail'] = article['content']['thumbnail']
        
        news.append(article)
    
    return news


def generate_mock_sustainability(ticker_symbol):
    """Generate mock sustainability (ESG) data.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        
    Returns:
        dict: Mock sustainability data.
    """
    sustainability = {
        'environmental_score': round(random.uniform(0, 100), 1),
        'social_score': round(random.uniform(0, 100), 1),
        'governance_score': round(random.uniform(0, 100), 1),
        'total_esg_score': round(random.uniform(0, 100), 1),
        'esg_performance': random.choice(['UNDERPERFORMER', 'AVERAGE', 'OUTPERFORMER']),
        'environment_percentile': round(random.uniform(0, 100), 1),
        'social_percentile': round(random.uniform(0, 100), 1),
        'governance_percentile': round(random.uniform(0, 100), 1),
        'controversy_level': random.randint(0, 5)
    }
    
    return sustainability


def generate_mock_holders(ticker_symbol):
    """Generate mock holders data.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        
    Returns:
        dict: Mock holders data with institutional and major holders.
    """
    institutional_holders = []
    
    institutions = [
        "Vanguard Group", "BlackRock", "State Street Corporation", "Fidelity",
        "T. Rowe Price", "Capital Group", "Berkshire Hathaway", "JP Morgan Chase",
        "Bank of America", "Goldman Sachs", "Morgan Stanley", "Wellington Management"
    ]
    
    # Generate 5-10 institutional holders
    for i in range(random.randint(5, 10)):
        holder = {
            'holder': random.choice(institutions),
            'shares': random.randint(1000000, 50000000),
            'date_reported': (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
            'pct_held': round(random.uniform(0.001, 0.1), 4),
            'value': random.randint(100000000, 5000000000)
        }
        institutional_holders.append(holder)
    
    # Major holders percentages
    major_holders = [
        {"category": "Insiders", "percentage": round(random.uniform(0.01, 0.2), 3)},
        {"category": "Institutions", "percentage": round(random.uniform(0.4, 0.9), 3)},
        {"category": "Public", "percentage": 0}  # Will be calculated
    ]
    
    # Calculate public percentage to make sum = 1
    public_pct = 1.0 - (major_holders[0]["percentage"] + major_holders[1]["percentage"])
    major_holders[2]["percentage"] = round(max(0, public_pct), 3)
    
    mutualfund_holders = []
    
    mutualfunds = [
        "Vanguard Total Stock Market Index Fund", "Vanguard 500 Index Fund",
        "SPDR S&P 500 ETF Trust", "Fidelity 500 Index Fund", "iShares Core S&P 500 ETF",
        "Vanguard Growth Index Fund", "Vanguard Value Index Fund", "Fidelity Contrafund",
        "American Funds Growth Fund of America", "T. Rowe Price Blue Chip Growth Fund"
    ]
    
    # Generate 3-7 mutual fund holders
    for i in range(random.randint(3, 7)):
        holder = {
            'holder': random.choice(mutualfunds),
            'shares': random.randint(500000, 20000000),
            'date_reported': (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d'),
            'pct_held': round(random.uniform(0.001, 0.05), 4),
            'value': random.randint(50000000, 2000000000)
        }
        mutualfund_holders.append(holder)
    
    return {
        'institutional_holders': institutional_holders,
        'major_holders': major_holders,
        'mutualfund_holders': mutualfund_holders
    }


# Main mock data generator function
def get_mock_data(endpoint_type, ticker_symbol, **kwargs):
    """Generate appropriate mock data based on the endpoint type.
    
    Args:
        endpoint_type (str): The type of data to generate (e.g., 'info', 'history').
        ticker_symbol (str): The ticker symbol.
        **kwargs: Additional arguments specific to the endpoint type.
        
    Returns:
        The appropriate mock data for the requested endpoint.
    """
    if endpoint_type == 'info':
        return generate_mock_ticker_info(ticker_symbol)
    elif endpoint_type == 'history':
        start = kwargs.get('start', (datetime.datetime.now() - datetime.timedelta(days=365)).strftime('%Y-%m-%d'))
        end = kwargs.get('end', datetime.datetime.now().strftime('%Y-%m-%d'))
        interval = kwargs.get('interval', '1d')
        return {'ticker': ticker_symbol, 'data': generate_mock_history_data(ticker_symbol, start, end, interval)}
    elif endpoint_type == 'dividends':
        return {'ticker': ticker_symbol, 'data': generate_mock_dividends(ticker_symbol)}
    elif endpoint_type == 'splits':
        return {'ticker': ticker_symbol, 'data': generate_mock_splits(ticker_symbol)}
    elif endpoint_type == 'recommendations':
        return {'ticker': ticker_symbol, 'data': generate_mock_recommendations(ticker_symbol)}
    elif endpoint_type == 'calendar':
        return {'ticker': ticker_symbol, 'data': generate_mock_calendar(ticker_symbol)}
    elif endpoint_type == 'sustainability':
        return {'ticker': ticker_symbol, 'data': generate_mock_sustainability(ticker_symbol)}
    elif endpoint_type == 'holders':
        return {'ticker': ticker_symbol, 'data': generate_mock_holders(ticker_symbol)}
    elif endpoint_type == 'news':
        # For news, yfinance returns the news items directly,
        # not wrapped in a data object. However, our API
        # wrapper adds the ticker field, so we need to match that
        return {'ticker': ticker_symbol, 'data': generate_mock_news(ticker_symbol)}
    else:
        # Default empty response
        return {'ticker': ticker_symbol, 'data': {}}