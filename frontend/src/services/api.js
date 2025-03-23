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

  // Log the request for debugging
  console.log('API Request:', config.method.toUpperCase(), config.url, config.data);

  return config;
});

// Add response interceptor for logging errors
api.interceptors.response.use(
  response => {
    console.log('API Response:', response.status, response.config.url, response.data);
    return response;
  },
  error => {
    console.error('API Error:',
      error.response?.status,
      error.response?.config?.url,
      error.response?.data || error.message
    );
    return Promise.reject(error);
  }
);

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

// Personal Finance service
const personalFinanceService = {
  // Categories
  getCategories() {
    return api.get('/personal-finance/categories/');
  },

  createCategory(data) {
    return api.post('/personal-finance/categories/', data);
  },

  updateCategory(id, data) {
    return api.put(`/personal-finance/categories/${id}/`, data);
  },

  deleteCategory(id) {
    return api.delete(`/personal-finance/categories/${id}/`);
  },

  // Accounts
  getAccounts() {
    return api.get('/personal-finance/accounts/');
  },

  createAccount(data) {
    return api.post('/personal-finance/accounts/', data);
  },

  updateAccount(id, data) {
    return api.put(`/personal-finance/accounts/${id}/`, data);
  },

  deleteAccount(id) {
    return api.delete(`/personal-finance/accounts/${id}/`);
  },

  // Transactions
  getTransactions(params = {}) {
    return api.get('/personal-finance/transactions/', { params });
  },

  createTransaction(data) {
    return api.post('/personal-finance/transactions/', data);
  },

  updateTransaction(id, data) {
    return api.put(`/personal-finance/transactions/${id}/`, data);
  },

  deleteTransaction(id) {
    return api.delete(`/personal-finance/transactions/${id}/`);
  },

  // Budgets
  getBudgets(params = {}) {
    return api.get('/personal-finance/budgets/', { params });
  },

  createBudget(data) {
    return api.post('/personal-finance/budgets/', data);
  },

  updateBudget(id, data) {
    return api.put(`/personal-finance/budgets/${id}/`, data);
  },

  deleteBudget(id) {
    return api.delete(`/personal-finance/budgets/${id}/`);
  },
  
  // Subcategory Budgets
  createSubcategoryBudgets(parentBudgetId, subcategoryBudgetsData) {
    return api.post(`/personal-finance/budgets/${parentBudgetId}/create_subcategory_budgets/`, {
      subcategory_budgets: subcategoryBudgetsData 
    });
  },
  
  updateSubcategoryBudgets(parentBudgetId, subcategoryBudgetsData) {
    return api.put(`/personal-finance/budgets/${parentBudgetId}/update_subcategory_budgets/`, {
      subcategory_budgets: subcategoryBudgetsData 
    });
  },

  // Savings Goals
  getSavingsGoals() {
    return api.get('/personal-finance/savings-goals/');
  },

  createSavingsGoal(data) {
    return api.post('/personal-finance/savings-goals/', data);
  },

  updateSavingsGoal(id, data) {
    return api.put(`/personal-finance/savings-goals/${id}/`, data);
  },

  deleteSavingsGoal(id) {
    return api.delete(`/personal-finance/savings-goals/${id}/`);
  },

  addToSavingsGoal(id, amount) {
    return api.post(`/personal-finance/savings-goals/${id}/add_savings/`, { amount });
  },

  // Summary and Reports
  getFinancialSummary() {
    return api.get('/personal-finance/summary/');
  }
};

// Currency service
const currencyService = {
  /**
   * Get exchange rates for currencies relative to USD
   * @returns {Promise} - The exchange rate data
   */
  async getExchangeRates() {
    // Use real CurrencyFreaks API instead of mock data
    try {
      const { getExchangeRates } = await import('@/api/currencyFreaksClient');
      const rates = await getExchangeRates();
      return { data: rates };
    } catch (error) {
      console.error('Error loading exchange rates from CurrencyFreaks:', error);
      // Fallback to mock data if API fails
      try {
        const { getMockExchangeRatesAsync } = await import('@/api/mockCurrencyRates');
        const mockRates = await getMockExchangeRatesAsync(0); // No delay needed for fallback
        console.warn('Using mock exchange rates as fallback');
        return { data: mockRates };
      } catch (fallbackError) {
        console.error('Error loading mock exchange rates fallback:', fallbackError);
        // Ultimate fallback to empty data with USD only
        return { data: { USD: 1 } };
      }
    }
  },

  /**
   * Get historical exchange rates for a specific date
   * @param {string} date - The date in YYYY-MM-DD format
   * @returns {Promise} - The historical exchange rate data
   */
  async getHistoricalRates(date) {
    try {
      const { getHistoricalRates } = await import('@/api/currencyFreaksClient');
      const rates = await getHistoricalRates(date);
      return { data: rates };
    } catch (error) {
      console.error(`Error loading historical rates for ${date}:`, error);
      // Fallback to current rates
      return this.getExchangeRates();
    }
  }
};

export {
  tickerService,
  financialsService,
  optionsService,
  authService,
  personalFinanceService,
  currencyService,
  setAuthHeader
};