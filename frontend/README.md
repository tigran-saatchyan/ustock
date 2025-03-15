# UStock Frontend

A Vue.js frontend for the UStock financial data API.

## Overview

UStock Frontend provides a modern user interface for accessing comprehensive stock market data, including:

- Stock price data and charts
- Financial statements (Income Statement, Balance Sheet, Cash Flow)
- Options chains with detailed data
- News and analyst recommendations
- Company information and key metrics

## Project Setup

```bash
# Install dependencies
npm install

# Serve with hot-reload for development
npm run serve

# Compile and minify for production
npm run build

# Lint and fix files
npm run lint
```

## Features

1. **Ticker Search & Dashboard**
   - Search for any stock ticker
   - View comprehensive dashboard with key data points
   - Interactive price chart with multiple timeframes

2. **Financial Statements**
   - View annual and quarterly financial data
   - Toggle between Income Statement, Balance Sheet, and Cash Flow
   - Key financial metrics visualization

3. **Options Analysis**
   - View options chains for different expiration dates
   - Filter by calls, puts, or both
   - Highlight in-the-money and out-of-the-money options

4. **News Aggregation**
   - Latest news for selected ticker
   - Search and filter news articles
   - Sort by date

5. **Modern UI/UX**
   - Responsive design for all devices
   - Light/dark theme support
   - Interactive data visualizations

## Architecture

The frontend uses the following technologies:

- **Vue 3** with Composition API
- **Vuex** for state management
- **Vue Router** for navigation
- **Chart.js** for data visualization
- **Axios** for API requests
- **PrimeVue** for UI components
- **SCSS** for styling

## API Integration

The frontend integrates with the UStock API to fetch financial data. The API endpoints are defined in the API services.