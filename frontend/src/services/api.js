import axios from 'axios';

// Create an Axios instance with default configuration
const api = axios.create({
  baseURL: '/api/v1', // This matches the proxy configuration in vue.config.js
  timeout: 30000, // Increased timeout to 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true // Enable sending cookies with cross-origin requests
});

// Add request interceptor for authentication
api.interceptors.request.use(config => {
  // Get token from localStorage (set by auth module)
  const token = localStorage.getItem('auth_token');
  
  if (token) {
    config.headers.Authorization = token;
  }
  
  return config;
});

// Add a method to set auth header
const setAuthHeader = (token) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = token;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

// Ticker endpoints
const tickerService = {
  /**
   * Get general information about a ticker
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The ticker information
   */
  getTickerInfo(ticker) {
    return api.get(`/tickers/${ticker}/`);
  },

  /**
   * Get historical price data for a ticker
   * @param {string} ticker - The ticker symbol
   * @param {string} start - The start date in YYYY-MM-DD format
   * @param {string} end - The end date in YYYY-MM-DD format
   * @param {string} interval - The data interval (1d, 1wk, 1mo)
   * @returns {Promise} - The historical price data
   */
  getTickerHistory(ticker, start, end, interval = '1d') {
    return api.get(`/tickers/${ticker}/history/`, {
      params: { start, end, interval }
    });
  },

  /**
   * Get dividend data for a ticker
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The dividend data
   */
  getTickerDividends(ticker) {
    return api.get(`/tickers/${ticker}/dividends/`);
  },

  /**
   * Get stock splits data for a ticker
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The stock splits data
   */
  getTickerSplits(ticker) {
    return api.get(`/tickers/${ticker}/splits/`);
  },

  /**
   * Get analyst recommendations for a ticker
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The analyst recommendations
   */
  getTickerRecommendations(ticker) {
    return api.get(`/tickers/${ticker}/recommendations/`);
  },

  /**
   * Get event calendar data for a ticker
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The event calendar data
   */
  getTickerCalendar(ticker) {
    return api.get(`/tickers/${ticker}/calendar/`);
  },

  /**
   * Get sustainability (ESG) data for a ticker
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The sustainability data
   */
  getTickerSustainability(ticker) {
    return api.get(`/tickers/${ticker}/sustainability/`);
  },

  /**
   * Get holders information for a ticker
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The holders information
   */
  getTickerHolders(ticker) {
    return api.get(`/tickers/${ticker}/holders/`);
  },

  /**
   * Get news related to a ticker
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The news data
   */
  getTickerNews(ticker) {
    return api.get(`/tickers/${ticker}/news/`);
  }
};

// Financial data endpoints
const financialsService = {
  /**
   * Get annual financial statements
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The annual financial data
   */
  getFinancials(ticker) {
    return api.get(`/financials/${ticker}/financials/`);
  },

  /**
   * Get quarterly financial statements
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The quarterly financial data
   */
  getQuarterlyFinancials(ticker) {
    return api.get(`/financials/${ticker}/quarterly_financials/`);
  },

  /**
   * Get annual balance sheet
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The annual balance sheet data
   */
  getBalanceSheet(ticker) {
    return api.get(`/financials/${ticker}/balance_sheet/`);
  },

  /**
   * Get quarterly balance sheet
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The quarterly balance sheet data
   */
  getQuarterlyBalanceSheet(ticker) {
    return api.get(`/financials/${ticker}/quarterly_balance_sheet/`);
  },

  /**
   * Get annual cashflow statement
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The annual cashflow data
   */
  getCashflow(ticker) {
    return api.get(`/financials/${ticker}/cashflow/`);
  },

  /**
   * Get quarterly cashflow statement
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The quarterly cashflow data
   */
  getQuarterlyCashflow(ticker) {
    return api.get(`/financials/${ticker}/quarterly_cashflow/`);
  },

  /**
   * Get annual income statement
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The annual income statement data
   */
  getEarnings(ticker) {
    return api.get(`/financials/${ticker}/earnings/`);
  },

  /**
   * Get quarterly income statement
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The quarterly income statement data
   */
  getQuarterlyEarnings(ticker) {
    return api.get(`/financials/${ticker}/quarterly_earnings/`);
  }
};

// Options endpoints
const optionsService = {
  /**
   * Get available options expiration dates
   * @param {string} ticker - The ticker symbol
   * @returns {Promise} - The available expiration dates
   */
  getOptionsDates(ticker) {
    return api.get(`/options/${ticker}/dates/`);
  },

  /**
   * Get options chain for a given date
   * @param {string} ticker - The ticker symbol
   * @param {string} date - The expiration date in YYYY-MM-DD format
   * @returns {Promise} - The options chain data
   */
  getOptionsChain(ticker, date) {
    return api.get(`/options/${ticker}/chain/`, {
      params: { date }
    });
  }
};

// Auth service
const authService = {
  /**
   * Get current user information
   * @returns {Promise} - The user information
   */
  getCurrentUser() {
    return api.get('/auth/user/');
  },
  
  /**
   * Login with username and password
   * @param {string} username - The username
   * @param {string} password - The password
   * @returns {Promise} - The login response
   */
  login(username, password) {
    // Create Basic Auth token
    const auth = 'Basic ' + btoa(`${username}:${password}`);
    
    // Set the authorization header for this request
    return api.post('/auth/login/', { username, password }, {
      headers: {
        'Authorization': auth
      }
    });
  }
};

export { tickerService, financialsService, optionsService, authService, setAuthHeader };