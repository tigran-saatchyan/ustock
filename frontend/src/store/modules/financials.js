import { financialsService } from '@/services/api';

export default {
  namespaced: true,
  
  state: {
    financials: null,
    quarterlyFinancials: null,
    balanceSheet: null,
    quarterlyBalanceSheet: null,
    cashflow: null,
    quarterlyCashflow: null,
    earnings: null,
    quarterlyEarnings: null,
    activeView: 'annual' // 'annual' or 'quarterly'
  },
  
  getters: {
    financials: state => state.financials,
    quarterlyFinancials: state => state.quarterlyFinancials,
    balanceSheet: state => state.balanceSheet,
    quarterlyBalanceSheet: state => state.quarterlyBalanceSheet,
    cashflow: state => state.cashflow,
    quarterlyCashflow: state => state.quarterlyCashflow,
    earnings: state => state.earnings,
    quarterlyEarnings: state => state.quarterlyEarnings,
    
    // Get the active view state
    activeView: state => state.activeView,
    isAnnualView: state => state.activeView === 'annual',
    
    // Get financial data based on active view
    activeFinancials: (state, getters) => 
      getters.isAnnualView ? state.financials : state.quarterlyFinancials,
    
    activeBalanceSheet: (state, getters) => 
      getters.isAnnualView ? state.balanceSheet : state.quarterlyBalanceSheet,
    
    activeCashflow: (state, getters) => 
      getters.isAnnualView ? state.cashflow : state.quarterlyCashflow,
    
    activeEarnings: (state, getters) => 
      getters.isAnnualView ? state.earnings : state.quarterlyEarnings,
    
    // Helper for getting column headers (dates) from financial data
    financialPeriods: (state, getters) => {
      const financials = getters.activeFinancials;
      if (!financials || !financials.data) return [];
      
      return Object.keys(financials.data)
        .filter(key => key !== 'ticker' && key !== 'data')
        .sort((a, b) => new Date(b) - new Date(a));
    },
    
    // Extract common key metrics
    keyMetrics: (state, getters) => {
      const earnings = getters.activeEarnings;
      const balanceSheet = getters.activeBalanceSheet;
      
      if (!earnings || !earnings.data || !balanceSheet || !balanceSheet.data) {
        return null;
      }
      
      try {
        // Find the latest period
        const periods = getters.financialPeriods;
        if (periods.length === 0) return null;
        
        const latestPeriod = periods[0];
        
        // Extract key metrics from earnings and balance sheet
        const earningsData = earnings.data;
        const balanceSheetData = balanceSheet.data;
        
        return {
          period: latestPeriod,
          revenue: earningsData.TotalRevenue?.[latestPeriod],
          netIncome: earningsData.NetIncome?.[latestPeriod],
          eps: earningsData.BasicEPS?.[latestPeriod],
          totalAssets: balanceSheetData.TotalAssets?.[latestPeriod],
          totalLiabilities: balanceSheetData.TotalLiabilitiesNetMinorityInterest?.[latestPeriod],
          shareholderEquity: balanceSheetData.StockholdersEquity?.[latestPeriod]
        };
      } catch (error) {
        console.error('Error extracting key metrics:', error);
        return null;
      }
    }
  },
  
  mutations: {
    SET_FINANCIALS(state, data) {
      state.financials = data;
    },
    
    SET_QUARTERLY_FINANCIALS(state, data) {
      state.quarterlyFinancials = data;
    },
    
    SET_BALANCE_SHEET(state, data) {
      state.balanceSheet = data;
    },
    
    SET_QUARTERLY_BALANCE_SHEET(state, data) {
      state.quarterlyBalanceSheet = data;
    },
    
    SET_CASHFLOW(state, data) {
      state.cashflow = data;
    },
    
    SET_QUARTERLY_CASHFLOW(state, data) {
      state.quarterlyCashflow = data;
    },
    
    SET_EARNINGS(state, data) {
      state.earnings = data;
    },
    
    SET_QUARTERLY_EARNINGS(state, data) {
      state.quarterlyEarnings = data;
    },
    
    SET_ACTIVE_VIEW(state, view) {
      state.activeView = view;
    },
    
    CLEAR_FINANCIALS(state) {
      state.financials = null;
      state.quarterlyFinancials = null;
      state.balanceSheet = null;
      state.quarterlyBalanceSheet = null;
      state.cashflow = null;
      state.quarterlyCashflow = null;
      state.earnings = null;
      state.quarterlyEarnings = null;
    }
  },
  
  actions: {
    /**
     * Set active view (annual or quarterly)
     */
    setActiveView({ commit }, view) {
      commit('SET_ACTIVE_VIEW', view);
    },
    
    /**
     * Fetch annual financial statements
     */
    async fetchFinancials({ commit, rootState, dispatch }) {
      const ticker = rootState.ticker.currentTicker;
      if (!ticker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await financialsService.getFinancials(ticker);
        commit('SET_FINANCIALS', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load financial data: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch quarterly financial statements
     */
    async fetchQuarterlyFinancials({ commit, rootState, dispatch }) {
      const ticker = rootState.ticker.currentTicker;
      if (!ticker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await financialsService.getQuarterlyFinancials(ticker);
        commit('SET_QUARTERLY_FINANCIALS', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load quarterly financial data: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch annual balance sheet
     */
    async fetchBalanceSheet({ commit, rootState, dispatch }) {
      const ticker = rootState.ticker.currentTicker;
      if (!ticker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await financialsService.getBalanceSheet(ticker);
        commit('SET_BALANCE_SHEET', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load balance sheet: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch quarterly balance sheet
     */
    async fetchQuarterlyBalanceSheet({ commit, rootState, dispatch }) {
      const ticker = rootState.ticker.currentTicker;
      if (!ticker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await financialsService.getQuarterlyBalanceSheet(ticker);
        commit('SET_QUARTERLY_BALANCE_SHEET', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load quarterly balance sheet: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch annual cashflow statement
     */
    async fetchCashflow({ commit, rootState, dispatch }) {
      const ticker = rootState.ticker.currentTicker;
      if (!ticker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await financialsService.getCashflow(ticker);
        commit('SET_CASHFLOW', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load cashflow statement: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch quarterly cashflow statement
     */
    async fetchQuarterlyCashflow({ commit, rootState, dispatch }) {
      const ticker = rootState.ticker.currentTicker;
      if (!ticker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await financialsService.getQuarterlyCashflow(ticker);
        commit('SET_QUARTERLY_CASHFLOW', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load quarterly cashflow statement: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch annual income statement (earnings)
     */
    async fetchEarnings({ commit, rootState, dispatch }) {
      const ticker = rootState.ticker.currentTicker;
      if (!ticker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await financialsService.getEarnings(ticker);
        commit('SET_EARNINGS', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load income statement: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch quarterly income statement (earnings)
     */
    async fetchQuarterlyEarnings({ commit, rootState, dispatch }) {
      const ticker = rootState.ticker.currentTicker;
      if (!ticker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await financialsService.getQuarterlyEarnings(ticker);
        commit('SET_QUARTERLY_EARNINGS', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load quarterly income statement: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Load all annual financial data
     */
    async loadAnnualFinancials({ dispatch }) {
      await Promise.all([
        dispatch('fetchFinancials'),
        dispatch('fetchBalanceSheet'),
        dispatch('fetchCashflow'),
        dispatch('fetchEarnings')
      ]);
    },
    
    /**
     * Load all quarterly financial data
     */
    async loadQuarterlyFinancials({ dispatch }) {
      await Promise.all([
        dispatch('fetchQuarterlyFinancials'),
        dispatch('fetchQuarterlyBalanceSheet'),
        dispatch('fetchQuarterlyCashflow'),
        dispatch('fetchQuarterlyEarnings')
      ]);
    },
    
    /**
     * Load both annual and quarterly financial data
     */
    async loadAllFinancials({ dispatch }) {
      await Promise.all([
        dispatch('loadAnnualFinancials'),
        dispatch('loadQuarterlyFinancials')
      ]);
    },
    
    /**
     * Clear all financial data
     */
    clearFinancials({ commit }) {
      commit('CLEAR_FINANCIALS');
    }
  }
};