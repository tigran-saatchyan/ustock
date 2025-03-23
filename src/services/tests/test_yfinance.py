import yfinance as yf
import json
import pandas as pd
import numpy as np

def convert_datetime(obj):
    if isinstance(obj, pd.Timestamp):
        return obj.strftime('%Y-%m-%d')
    raise TypeError(f'Type {type(obj)} not serializable')

def test_yfinance():
    ticker = yf.Ticker('AAPL')
    history = ticker.history(start='2023-01-01', end='2023-01-10', interval='1d')
    
    # Convert to records and handle NaN values
    history = history.reset_index()
    history_dict = history.replace({np.nan: None}).to_dict(orient='records')
    
    # Print sample data
    print("Sample history data format:")
    print(json.dumps(history_dict[0] if history_dict else {}, indent=2, default=convert_datetime))
    
    # Print all column names
    print("\nColumn names:", list(history.columns))
    
    # Print data types
    print("\nData types:")
    for col in history.columns:
        print(f"{col}: {history[col].dtype}")
        
    return history_dict

if __name__ == "__main__":
    test_yfinance()