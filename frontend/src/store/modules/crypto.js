import cryptoApi from '@/api/crypto';

export default {
  namespaced: true,

  state: {
    accountBalance: null,
    apiKeys: [],
    openOrders: [],
    exchangeInfo: null,
    allTickers: [],
    loading: false,
    error: null
  },

  getters: {
    accountBalance: state => state.accountBalance,
    apiKeys: state => state.apiKeys,
    openOrders: state => state.openOrders,
    exchangeInfo: state => state.exchangeInfo,
    allTickers: state => state.allTickers,
    loading: state => state.loading,
    error: state => state.error,
    
    // Get total balance in USDT
    totalBalance: state => {
      if (!state.accountBalance || !state.accountBalance.total_value_usdt) {
        return 0;
      }
      return state.accountBalance.total_value_usdt;
    },
    
    // Get balances sorted by value
    sortedBalances: state => {
      if (!state.accountBalance || !state.accountBalance.balances) {
        return [];
      }
      return [...state.accountBalance.balances].sort((a, b) => b.value_usdt - a.value_usdt);
    },
    
    // Check if user has API keys for a specific exchange
    hasApiKeys: state => exchange => {
      return state.apiKeys.some(key => key.exchange === exchange && key.is_active);
    }
  },

  mutations: {
    SET_ACCOUNT_BALANCE(state, balance) {
      state.accountBalance = balance;
    },
    
    SET_API_KEYS(state, keys) {
      state.apiKeys = keys;
    },
    
    SET_OPEN_ORDERS(state, orders) {
      state.openOrders = orders;
    },
    
    SET_EXCHANGE_INFO(state, info) {
      state.exchangeInfo = info;
    },
    
    SET_ALL_TICKERS(state, tickers) {
      state.allTickers = tickers;
    },
    
    SET_LOADING(state, loading) {
      state.loading = loading;
    },
    
    SET_ERROR(state, error) {
      state.error = error;
    }
  },

  actions: {
    /**
     * Set loading state
     */
    setLoading({ commit }, loading) {
      commit('SET_LOADING', loading);
    },
    
    /**
     * Set error state
     */
    setError({ commit }, error) {
      commit('SET_ERROR', error);
    },
    
    /**
     * Fetch account balance
     */
    async fetchAccountBalance({ commit, dispatch }, exchange = 'binance') {
      dispatch('setLoading', true);
      
      try {
        const response = await cryptoApi.getAccountBalance(exchange);
        commit('SET_ACCOUNT_BALANCE', response.data);
      } catch (error) {
        console.error('Error fetching account balance:', error);
        dispatch('setError', `Failed to load account balance: ${error.message}`);
      } finally {
        dispatch('setLoading', false);
      }
    },
    
    /**
     * Fetch API keys
     */
    async fetchApiKeys({ commit, dispatch }) {
      dispatch('setLoading', true);
      
      try {
        const response = await cryptoApi.getApiKeys();
        commit('SET_API_KEYS', response.data);
      } catch (error) {
        console.error('Error fetching API keys:', error);
        dispatch('setError', `Failed to load API keys: ${error.message}`);
      } finally {
        dispatch('setLoading', false);
      }
    },
    
    /**
     * Create or update API key
     */
    async createApiKey({ dispatch }, apiKeyData) {
      dispatch('setLoading', true);
      
      try {
        await cryptoApi.createApiKey(apiKeyData);
        // Refresh API keys after creating/updating
        dispatch('fetchApiKeys');
      } catch (error) {
        console.error('Error creating API key:', error);
        dispatch('setError', `Failed to create API key: ${error.message}`);
      } finally {
        dispatch('setLoading', false);
      }
    },
    
    /**
     * Delete API key
     */
    async deleteApiKey({ dispatch }, exchange) {
      dispatch('setLoading', true);
      
      try {
        await cryptoApi.deleteApiKey(exchange);
        // Refresh API keys after deleting
        dispatch('fetchApiKeys');
      } catch (error) {
        console.error('Error deleting API key:', error);
        dispatch('setError', `Failed to delete API key: ${error.message}`);
      } finally {
        dispatch('setLoading', false);
      }
    },
    
    /**
     * Fetch open orders
     */
    async fetchOpenOrders({ commit, dispatch }, { symbol = null, exchange = 'binance' } = {}) {
      dispatch('setLoading', true);
      
      try {
        const response = await cryptoApi.getOpenOrders(symbol, exchange);
        commit('SET_OPEN_ORDERS', response.data);
      } catch (error) {
        console.error('Error fetching open orders:', error);
        dispatch('setError', `Failed to load open orders: ${error.message}`);
      } finally {
        dispatch('setLoading', false);
      }
    },
    
    /**
     * Create order
     */
    async createOrder({ dispatch }, { orderData, exchange = 'binance' }) {
      dispatch('setLoading', true);
      
      try {
        const response = await cryptoApi.createOrder(orderData, exchange);
        // Refresh open orders and account balance after creating order
        dispatch('fetchOpenOrders', { exchange });
        dispatch('fetchAccountBalance', exchange);
        return response.data;
      } catch (error) {
        console.error('Error creating order:', error);
        dispatch('setError', `Failed to create order: ${error.message}`);
        throw error;
      } finally {
        dispatch('setLoading', false);
      }
    },
    
    /**
     * Cancel order
     */
    async cancelOrder({ dispatch }, { symbol, orderId, exchange = 'binance' }) {
      dispatch('setLoading', true);
      
      try {
        await cryptoApi.cancelOrder(symbol, orderId, exchange);
        // Refresh open orders and account balance after canceling order
        dispatch('fetchOpenOrders', { exchange });
        dispatch('fetchAccountBalance', exchange);
      } catch (error) {
        console.error('Error canceling order:', error);
        dispatch('setError', `Failed to cancel order: ${error.message}`);
      } finally {
        dispatch('setLoading', false);
      }
    },
    
    /**
     * Fetch exchange info
     */
    async fetchExchangeInfo({ commit, dispatch }, exchange = 'binance') {
      dispatch('setLoading', true);
      
      try {
        const response = await cryptoApi.getExchangeInfo(exchange);
        commit('SET_EXCHANGE_INFO', response.data);
      } catch (error) {
        console.error('Error fetching exchange info:', error);
        dispatch('setError', `Failed to load exchange info: ${error.message}`);
      } finally {
        dispatch('setLoading', false);
      }
    },
    
    /**
     * Fetch all tickers
     */
    async fetchAllTickers({ commit, dispatch }, exchange = 'binance') {
      dispatch('setLoading', true);
      
      try {
        const response = await cryptoApi.getAllTickers(exchange);
        commit('SET_ALL_TICKERS', response.data);
      } catch (error) {
        console.error('Error fetching all tickers:', error);
        dispatch('setError', `Failed to load tickers: ${error.message}`);
      } finally {
        dispatch('setLoading', false);
      }
    },
    
    /**
     * Initialize crypto data
     */
    async initialize({ dispatch }) {
      try {
        // Fetch API keys first to check if user has configured any exchanges
        await dispatch('fetchApiKeys');
        
        // Fetch account balance and other data
        await dispatch('fetchAccountBalance');
        await dispatch('fetchExchangeInfo');
        await dispatch('fetchAllTickers');
        await dispatch('fetchOpenOrders');
      } catch (error) {
        console.error('Error initializing crypto data:', error);
      }
    }
  }
};