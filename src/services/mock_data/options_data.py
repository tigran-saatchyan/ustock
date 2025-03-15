"""
This module provides mock data for options when real data is unavailable or for testing purposes.
"""

import datetime
import random


def generate_expiration_dates(ticker_symbol):
    """Generate mock option expiration dates.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        
    Returns:
        list: A list of expiration dates.
    """
    # Generate expiration dates for the next 12 months (monthly)
    expiration_dates = []
    current_date = datetime.datetime.now()
    
    # Options typically expire on the third Friday of each month
    for i in range(12):
        # Move to next month
        month = current_date.month + i
        year = current_date.year
        
        # Adjust year if we wrap around
        while month > 12:
            month -= 12
            year += 1
        
        # Find the third Friday of this month
        day = 1
        first_date = datetime.datetime(year, month, day)
        
        # Find the first Friday (weekday 4) of the month
        while first_date.weekday() != 4:  # 4 is Friday
            day += 1
            first_date = datetime.datetime(year, month, day)
        
        # Move to the third Friday
        third_friday = first_date + datetime.timedelta(days=14)
        
        # Format the date
        expiration_dates.append(third_friday.strftime('%Y-%m-%d'))
    
    # Add some weekly options (next 4 Fridays)
    friday_count = 0
    for i in range(28):  # Check the next 4 weeks
        check_date = current_date + datetime.timedelta(days=i)
        if check_date.weekday() == 4:  # Friday
            if check_date.strftime('%Y-%m-%d') not in expiration_dates:  # Don't duplicate monthly dates
                expiration_dates.append(check_date.strftime('%Y-%m-%d'))
                friday_count += 1
                if friday_count >= 4:
                    break
    
    # Sort the dates
    expiration_dates.sort()
    
    return expiration_dates


def generate_option_chain(ticker_symbol, expiration_date):
    """Generate mock options chain data for a specific expiration date.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        expiration_date (str): The expiration date in 'YYYY-MM-DD' format.
        
    Returns:
        dict: A dictionary containing calls and puts option chains.
    """
    try:
        expiry_date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d')
    except ValueError:
        # Handle invalid date formats
        expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)
    
    # Set a current price for the underlying stock
    underlying_price = round(random.uniform(50, 500), 2)
    
    # Generate strike prices around the current price (typically in $5 or $2.5 increments)
    increment = 5.0 if underlying_price > 100 else 2.5
    num_strikes = 15  # Generate 15 strikes above and below current price
    
    # Calculate the lowest and highest strikes
    lowest_strike = underlying_price - (increment * num_strikes)
    lowest_strike = max(5, round(lowest_strike / increment) * increment)  # Ensure it's positive and aligned to increment
    
    strikes = []
    for i in range(num_strikes * 2 + 1):
        strike = lowest_strike + (i * increment)
        strikes.append(round(strike, 2))
    
    # Calculate days to expiration
    days_to_expiry = (expiry_date - datetime.datetime.now()).days
    days_to_expiry = max(1, days_to_expiry)  # Ensure at least 1 day
    
    # Generate option chains
    calls = []
    puts = []
    
    for strike in strikes:
        # Calculate call and put prices based on strike and days to expiry
        call_itm = underlying_price > strike
        put_itm = underlying_price < strike
        
        # Simple model for intrinsic value
        call_intrinsic = max(0, underlying_price - strike)
        put_intrinsic = max(0, strike - underlying_price)
        
        # Time value decreases as we get closer to expiry
        time_factor = min(1.0, days_to_expiry / 365.0) * 0.2
        
        # Volatility factor - higher when further from current price
        price_distance = abs(underlying_price - strike) / underlying_price
        vol_factor = 0.3 + price_distance
        
        # Calculate option prices
        call_price = call_intrinsic + (underlying_price * time_factor * vol_factor)
        put_price = put_intrinsic + (underlying_price * time_factor * vol_factor)
        
        # Apply some randomness
        call_price *= (1 + random.uniform(-0.1, 0.1))
        put_price *= (1 + random.uniform(-0.1, 0.1))
        
        # Round to 2 decimal places
        call_price = round(max(0.01, call_price), 2)
        put_price = round(max(0.01, put_price), 2)
        
        # Calculate implied volatility (simplified)
        call_iv = vol_factor * (1 + random.uniform(-0.2, 0.2))
        put_iv = vol_factor * (1 + random.uniform(-0.2, 0.2))
        
        # Generate other columns
        call_volume = int(random.uniform(10, 1000)) if call_price > 0.1 else 0
        put_volume = int(random.uniform(10, 1000)) if put_price > 0.1 else 0
        
        call_open_interest = int(call_volume * random.uniform(1, 5))
        put_open_interest = int(put_volume * random.uniform(1, 5))
        
        # Generate bid/ask spread
        call_bid = call_price * 0.95
        call_ask = call_price * 1.05
        put_bid = put_price * 0.95
        put_ask = put_price * 1.05
        
        # Round bid/ask
        call_bid = round(max(0.01, call_bid), 2)
        call_ask = round(max(0.01, call_ask), 2)
        put_bid = round(max(0.01, put_bid), 2)
        put_ask = round(max(0.01, put_ask), 2)
        
        # Create call option
        call = {
            'contractSymbol': f"{ticker_symbol}{expiry_date.strftime('%y%m%d')}C{int(strike * 1000)}",
            'strike': strike,
            'currency': 'USD',
            'lastPrice': call_price,
            'change': round(random.uniform(-0.5, 0.5), 2),
            'percentChange': round(random.uniform(-10, 10), 2),
            'volume': call_volume,
            'openInterest': call_open_interest,
            'bid': call_bid,
            'ask': call_ask,
            'impliedVolatility': round(call_iv, 4),
            'inTheMoney': call_itm,
            'contractSize': '100',
            'expiration': expiry_date.strftime('%Y-%m-%d'),
            'lastTradeDate': (datetime.datetime.now() - datetime.timedelta(hours=random.randint(1, 24))).strftime('%Y-%m-%d %H:%M:%S'),
            'itm': call_itm
        }
        calls.append(call)
        
        # Create put option
        put = {
            'contractSymbol': f"{ticker_symbol}{expiry_date.strftime('%y%m%d')}P{int(strike * 1000)}",
            'strike': strike,
            'currency': 'USD',
            'lastPrice': put_price,
            'change': round(random.uniform(-0.5, 0.5), 2),
            'percentChange': round(random.uniform(-10, 10), 2),
            'volume': put_volume,
            'openInterest': put_open_interest,
            'bid': put_bid,
            'ask': put_ask,
            'impliedVolatility': round(put_iv, 4),
            'inTheMoney': put_itm,
            'contractSize': '100',
            'expiration': expiry_date.strftime('%Y-%m-%d'),
            'lastTradeDate': (datetime.datetime.now() - datetime.timedelta(hours=random.randint(1, 24))).strftime('%Y-%m-%d %H:%M:%S'),
            'itm': put_itm
        }
        puts.append(put)
    
    return {
        'calls': calls,
        'puts': puts
    }


# Main mock data generator function
def get_mock_data(endpoint_type, ticker_symbol, **kwargs):
    """Generate appropriate mock options data based on the endpoint type.
    
    Args:
        endpoint_type (str): The type of data to generate.
        ticker_symbol (str): The ticker symbol.
        **kwargs: Additional arguments specific to the endpoint type.
        
    Returns:
        The appropriate mock data for the requested endpoint.
    """
    if endpoint_type == 'options_dates':
        return generate_expiration_dates(ticker_symbol)
    elif endpoint_type == 'option_chain':
        date = kwargs.get('date')
        if not date:
            # Default to a date in the future
            future_date = datetime.datetime.now() + datetime.timedelta(days=30)
            date = future_date.strftime('%Y-%m-%d')
        return generate_option_chain(ticker_symbol, date)
    else:
        # Default empty response
        return []