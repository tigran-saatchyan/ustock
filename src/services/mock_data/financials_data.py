"""
This module provides mock data for financial statements when real data is unavailable or for testing purposes.
"""

import datetime
import random
import numpy as np


def generate_mock_financials(ticker_symbol, quarterly=False):
    """Generate mock financial statement data.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        quarterly (bool): Whether to generate quarterly data instead of annual.
        
    Returns:
        dict: Mock financials data.
    """
    current_date = datetime.datetime.now()
    periods = 4 if quarterly else 3
    period_length = 3 if quarterly else 12  # months
    
    # Create a base revenue value for the company
    base_revenue = random.uniform(1000000000, 50000000000)
    
    # Define common income statement items and their relationships to revenue
    income_items = {
        'Total Revenue': 1.0,  # 100% of base_revenue
        'Cost of Revenue': random.uniform(0.55, 0.75),  # 55-75% of revenue
        'Gross Profit': 0,  # Will be calculated
        'Research Development': random.uniform(0.08, 0.2),  # 8-20% of revenue
        'Selling General Administrative': random.uniform(0.1, 0.3),  # 10-30% of revenue
        'Operating Expenses': 0,  # Will be calculated
        'Operating Income': 0,  # Will be calculated
        'Interest Expense': random.uniform(0.01, 0.05),  # 1-5% of revenue
        'Total Other Income Expense Net': random.uniform(-0.05, 0.05),  # +/- 5% of revenue
        'Income Before Tax': 0,  # Will be calculated
        'Income Tax Expense': random.uniform(0.15, 0.35),  # 15-35% of income before tax (effective tax rate)
        'Net Income': 0,  # Will be calculated
        'EBITDA': 0,  # Will be calculated
    }
    
    # Create a random growth trend for revenue
    # Normal companies grow ~5-20% annually, with some variance
    annual_growth_rate = random.uniform(0.05, 0.2)
    if quarterly:
        period_growth_rate = (1 + annual_growth_rate) ** (1/4) - 1  # Convert annual to quarterly rate
    else:
        period_growth_rate = annual_growth_rate
    
    # Add some randomness to the growth rate
    growth_rates = [period_growth_rate * (1 + random.uniform(-0.3, 0.3)) for _ in range(periods)]
    
    # Create the dates for the periods
    period_dates = []
    for i in range(periods):
        if quarterly:
            # Go back i quarters
            date = current_date - datetime.timedelta(days=90 * i)
            period_dates.append(date.replace(day=1).strftime('%Y-%m-%d'))
        else:
            # Go back i years, set to fiscal year end (Dec 31)
            year = current_date.year - i
            period_dates.append(f"{year}-12-31")
    
    # Sort dates chronologically
    period_dates.sort()
    
    # Generate the data for each period
    financial_data = {}
    for i, date in enumerate(period_dates):
        # Revenue grows according to our growth model
        # We're working backwards chronologically, so growth is applied in reverse
        revenue = base_revenue * (1 + sum(growth_rates[:i]))
        
        # Calculate all the financial metrics based on ratios
        period_data = {}
        
        # First pass: set the basic items directly from ratios
        for item, ratio in income_items.items():
            if item == 'Total Revenue':
                period_data[item] = revenue
            elif item not in ['Gross Profit', 'Operating Expenses', 'Operating Income', 
                             'Income Before Tax', 'Income Tax Expense', 'Net Income', 'EBITDA']:
                period_data[item] = revenue * ratio
        
        # Second pass: calculate the derived metrics in proper order
        period_data['Gross Profit'] = period_data['Total Revenue'] - period_data['Cost of Revenue']
        
        period_data['Operating Expenses'] = period_data['Research Development'] + period_data['Selling General Administrative']
        
        period_data['Operating Income'] = period_data['Gross Profit'] - period_data['Operating Expenses']
        
        period_data['Income Before Tax'] = (
            period_data['Operating Income'] - 
            period_data['Interest Expense'] + 
            period_data['Total Other Income Expense Net']
        )
        
        period_data['Income Tax Expense'] = period_data['Income Before Tax'] * income_items['Income Tax Expense']
        
        period_data['Net Income'] = period_data['Income Before Tax'] - period_data['Income Tax Expense']
        
        # Simple approximation for EBITDA
        period_data['EBITDA'] = period_data['Operating Income'] + (revenue * 0.1)  # Add back depreciation & amortization
        
        financial_data[date] = period_data
    
    return financial_data


def generate_mock_balance_sheet(ticker_symbol, quarterly=False):
    """Generate mock balance sheet data.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        quarterly (bool): Whether to generate quarterly data instead of annual.
        
    Returns:
        dict: Mock balance sheet data.
    """
    current_date = datetime.datetime.now()
    periods = 4 if quarterly else 3
    
    # Create a base assets value for the company
    base_assets = random.uniform(2000000000, 100000000000)
    
    # Define balance sheet items and their relationships to base assets
    balance_sheet_items = {
        # Assets
        'Cash And Cash Equivalents': random.uniform(0.05, 0.2),  # 5-20% of assets
        'Short Term Investments': random.uniform(0.03, 0.15),  # 3-15% of assets
        'Net Receivables': random.uniform(0.08, 0.25),  # 8-25% of assets
        'Inventory': random.uniform(0.05, 0.2),  # 5-20% of assets
        'Other Current Assets': random.uniform(0.02, 0.1),  # 2-10% of assets
        'Total Current Assets': 0,  # Will be calculated
        'Property Plant Equipment': random.uniform(0.15, 0.4),  # 15-40% of assets
        'Long Term Investments': random.uniform(0.05, 0.25),  # 5-25% of assets
        'Goodwill': random.uniform(0.05, 0.2),  # 5-20% of assets
        'Intangible Assets': random.uniform(0.03, 0.15),  # 3-15% of assets
        'Other Assets': random.uniform(0.01, 0.1),  # 1-10% of assets
        'Total Assets': 0,  # Will be calculated
        
        # Liabilities
        'Accounts Payable': random.uniform(0.05, 0.15),  # 5-15% of assets
        'Short Term Debt': random.uniform(0.03, 0.1),  # 3-10% of assets
        'Other Current Liabilities': random.uniform(0.05, 0.15),  # 5-15% of assets
        'Total Current Liabilities': 0,  # Will be calculated
        'Long Term Debt': random.uniform(0.1, 0.4),  # 10-40% of assets
        'Other Liabilities': random.uniform(0.05, 0.2),  # 5-20% of assets
        'Total Liabilities': 0,  # Will be calculated
        
        # Equity
        'Common Stock': random.uniform(0.01, 0.1),  # 1-10% of assets
        'Retained Earnings': 0,  # Will be a balancing item
        'Treasury Stock': -random.uniform(0, 0.05),  # 0-5% of assets (negative)
        'Other Stockholder Equity': random.uniform(-0.05, 0.05),  # +/- 5% of assets
        'Total Stockholder Equity': 0  # Will be calculated
    }
    
    # Create a random growth trend for assets
    annual_growth_rate = random.uniform(0.05, 0.15)
    if quarterly:
        period_growth_rate = (1 + annual_growth_rate) ** (1/4) - 1  # Convert annual to quarterly rate
    else:
        period_growth_rate = annual_growth_rate
    
    # Add some randomness to the growth rate
    growth_rates = [period_growth_rate * (1 + random.uniform(-0.3, 0.3)) for _ in range(periods)]
    
    # Create the dates for the periods
    period_dates = []
    for i in range(periods):
        if quarterly:
            # Go back i quarters
            date = current_date - datetime.timedelta(days=90 * i)
            period_dates.append(date.replace(day=1).strftime('%Y-%m-%d'))
        else:
            # Go back i years, set to fiscal year end (Dec 31)
            year = current_date.year - i
            period_dates.append(f"{year}-12-31")
    
    # Sort dates chronologically
    period_dates.sort()
    
    # Generate the data for each period
    balance_sheet_data = {}
    for i, date in enumerate(period_dates):
        # Assets grow according to our growth model
        assets = base_assets * (1 + sum(growth_rates[:i]))
        
        # First, calculate all the basic items based on ratios
        period_data = {}
        for item, ratio in balance_sheet_items.items():
            if item not in ['Total Current Assets', 'Total Assets', 'Total Current Liabilities', 
                           'Total Liabilities', 'Retained Earnings', 'Total Stockholder Equity']:
                period_data[item] = assets * ratio
        
        # Now calculate the composite items in the correct order
        # Current Assets total
        period_data['Total Current Assets'] = (
            period_data['Cash And Cash Equivalents'] +
            period_data['Short Term Investments'] +
            period_data['Net Receivables'] +
            period_data['Inventory'] +
            period_data['Other Current Assets']
        )
        
        # Total Assets
        period_data['Total Assets'] = (
            period_data['Total Current Assets'] +
            period_data['Property Plant Equipment'] +
            period_data['Long Term Investments'] +
            period_data['Goodwill'] +
            period_data['Intangible Assets'] +
            period_data['Other Assets']
        )
        
        # Current Liabilities total
        period_data['Total Current Liabilities'] = (
            period_data['Accounts Payable'] +
            period_data['Short Term Debt'] +
            period_data['Other Current Liabilities']
        )
        
        # Total Liabilities
        period_data['Total Liabilities'] = (
            period_data['Total Current Liabilities'] +
            period_data['Long Term Debt'] +
            period_data['Other Liabilities']
        )
        
        # Calculate Retained Earnings as balancing item
        total_equity_without_retained = (
            period_data['Common Stock'] +
            period_data['Treasury Stock'] +
            period_data['Other Stockholder Equity']
        )
        period_data['Retained Earnings'] = assets - period_data['Total Liabilities'] - total_equity_without_retained
        
        # Total Stockholder Equity
        period_data['Total Stockholder Equity'] = (
            period_data['Common Stock'] +
            period_data['Retained Earnings'] +
            period_data['Treasury Stock'] +
            period_data['Other Stockholder Equity']
        )
        
        balance_sheet_data[date] = period_data
    
    return balance_sheet_data


def generate_mock_cashflow(ticker_symbol, quarterly=False):
    """Generate mock cash flow statement data.
    
    Args:
        ticker_symbol (str): The ticker symbol.
        quarterly (bool): Whether to generate quarterly data instead of annual.
        
    Returns:
        dict: Mock cash flow data.
    """
    current_date = datetime.datetime.now()
    periods = 4 if quarterly else 3
    
    # Get mock financials to use the net income figure
    financials = generate_mock_financials(ticker_symbol, quarterly)
    
    # Create cash flow statement items
    cashflow_items = {
        # Operating activities
        'Net Income': 0,  # Will be taken from income statement
        'Depreciation': random.uniform(0.05, 0.15),  # 5-15% of net income
        'Amortization': random.uniform(0.01, 0.05),  # 1-5% of net income
        'Changes In Receivables': lambda: random.uniform(-0.2, 0.2),  # +/- 20% of net income
        'Changes In Inventories': lambda: random.uniform(-0.15, 0.15),  # +/- 15% of net income
        'Changes In Accounts Payable': lambda: random.uniform(-0.1, 0.1),  # +/- 10% of net income
        'Other Operating Activities': lambda: random.uniform(-0.2, 0.2),  # +/- 20% of net income
        'Total Cash From Operating Activities': 0,  # Will be calculated
        
        # Investing activities
        'Capital Expenditures': lambda: -random.uniform(0.2, 0.5),  # 20-50% of net income (negative)
        'Investments': lambda: -random.uniform(0, 0.3),  # 0-30% of net income (negative)
        'Other Investing Activities': lambda: random.uniform(-0.2, 0.1),  # -20% to +10% of net income
        'Total Cash From Investing Activities': 0,  # Will be calculated
        
        # Financing activities
        'Dividends Paid': lambda: -random.uniform(0, 0.3),  # 0-30% of net income (negative)
        'Net Borrowings': lambda: random.uniform(-0.2, 0.3),  # -20% to +30% of net income
        'Stock Issuance (Repurchase)': lambda: random.uniform(-0.25, 0.1),  # -25% to +10% of net income
        'Other Financing Activities': lambda: random.uniform(-0.1, 0.1),  # +/- 10% of net income
        'Total Cash From Financing Activities': 0,  # Will be calculated
        
        # Summary
        'Change In Cash': 0,  # Will be calculated
        'Beginning Cash': 0,  # Will be based on previous period
        'Ending Cash': 0,  # Will be calculated
    }
    
    # Create the dates for the periods
    period_dates = []
    for i in range(periods):
        if quarterly:
            # Go back i quarters
            date = current_date - datetime.timedelta(days=90 * i)
            period_dates.append(date.replace(day=1).strftime('%Y-%m-%d'))
        else:
            # Go back i years, set to fiscal year end (Dec 31)
            year = current_date.year - i
            period_dates.append(f"{year}-12-31")
    
    # Sort dates chronologically
    period_dates.sort()
    
    # Generate the data for each period
    cashflow_data = {}
    beginning_cash = random.uniform(1000000000, 5000000000)  # Starting cash balance
    
    for i, date in enumerate(period_dates):
        # Get net income from our mock financials
        net_income = financials[date]['Net Income']
        
        # Calculate all the basic cash flow items first
        period_data = {}
        
        # First pass: set all the basic items
        for item, value in cashflow_items.items():
            if item == 'Net Income':
                period_data[item] = net_income
            elif item not in ['Total Cash From Operating Activities', 'Total Cash From Investing Activities', 
                            'Total Cash From Financing Activities', 'Change In Cash', 'Beginning Cash', 'Ending Cash']:
                if callable(value):
                    # For items with dynamic ratios
                    period_data[item] = net_income * value()
                else:
                    # For items with fixed ratios
                    period_data[item] = net_income * value
        
        # Second pass: calculate the composite items in proper order
        # Operating activities total
        period_data['Total Cash From Operating Activities'] = (
            period_data['Net Income'] +
            period_data['Depreciation'] +
            period_data['Amortization'] +
            period_data['Changes In Receivables'] +
            period_data['Changes In Inventories'] +
            period_data['Changes In Accounts Payable'] +
            period_data['Other Operating Activities']
        )
        
        # Investing activities total
        period_data['Total Cash From Investing Activities'] = (
            period_data['Capital Expenditures'] +
            period_data['Investments'] +
            period_data['Other Investing Activities']
        )
        
        # Financing activities total
        period_data['Total Cash From Financing Activities'] = (
            period_data['Dividends Paid'] +
            period_data['Net Borrowings'] +
            period_data['Stock Issuance (Repurchase)'] +
            period_data['Other Financing Activities']
        )
        
        # Total change in cash
        period_data['Change In Cash'] = (
            period_data['Total Cash From Operating Activities'] +
            period_data['Total Cash From Investing Activities'] +
            period_data['Total Cash From Financing Activities']
        )
        
        # Beginning and ending cash
        if i == 0:
            period_data['Beginning Cash'] = beginning_cash
        else:
            period_data['Beginning Cash'] = cashflow_data[period_dates[i-1]]['Ending Cash']
            
        period_data['Ending Cash'] = period_data['Beginning Cash'] + period_data['Change In Cash']
        
        cashflow_data[date] = period_data
    
    return cashflow_data


# Main mock data generator function
def get_mock_data(endpoint_type, ticker_symbol, quarterly=False):
    """Generate appropriate mock financial data based on the endpoint type.
    
    Args:
        endpoint_type (str): The type of data to generate.
        ticker_symbol (str): The ticker symbol.
        quarterly (bool): Whether to generate quarterly data.
        
    Returns:
        The appropriate mock data for the requested endpoint.
    """
    if endpoint_type == 'financials':
        return generate_mock_financials(ticker_symbol, quarterly=quarterly)
    elif endpoint_type == 'balance_sheet':
        return generate_mock_balance_sheet(ticker_symbol, quarterly=quarterly)
    elif endpoint_type == 'cashflow':
        return generate_mock_cashflow(ticker_symbol, quarterly=quarterly)
    elif endpoint_type == 'earnings':
        # Reuse the financials function for earnings since they're similar
        return generate_mock_financials(ticker_symbol, quarterly=quarterly)
    else:
        # Default empty response
        return {}