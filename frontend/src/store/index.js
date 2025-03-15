import { createStore } from 'vuex';
import tickerModule from './modules/ticker';
import financialsModule from './modules/financials';
import optionsModule from './modules/options';
import authModule from './modules/auth';

export default createStore({
  state: {
    loading: false,
    error: null,
    recentTickers: [],
    favoriteTickers: [],
    theme: 'light',
  },
  
  getters: {
    isLoading: state => state.loading,
    hasError: state => !!state.error,
    errorMessage: state => state.error,
    recentTickers: state => state.recentTickers,
    favoriteTickers: state => state.favoriteTickers,
    isDarkTheme: state => state.theme === 'dark',
  },
  
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading;
    },
    
    SET_ERROR(state, error) {
      state.error = error;
    },
    
    CLEAR_ERROR(state) {
      state.error = null;
    },
    
    ADD_RECENT_TICKER(state, ticker) {
      // Remove if already exists
      const filtered = state.recentTickers.filter(t => t !== ticker);
      
      // Add to beginning and limit to 10 recent tickers
      state.recentTickers = [ticker, ...filtered].slice(0, 10);
      
      // Save to localStorage
      localStorage.setItem('recentTickers', JSON.stringify(state.recentTickers));
    },
    
    LOAD_RECENT_TICKERS(state) {
      const stored = localStorage.getItem('recentTickers');
      if (stored) {
        try {
          state.recentTickers = JSON.parse(stored);
        } catch (e) {
          console.error('Failed to parse recent tickers from localStorage', e);
        }
      }
    },
    
    TOGGLE_FAVORITE_TICKER(state, ticker) {
      const index = state.favoriteTickers.indexOf(ticker);
      
      if (index !== -1) {
        // Remove from favorites
        state.favoriteTickers.splice(index, 1);
      } else {
        // Add to favorites
        state.favoriteTickers.push(ticker);
      }
      
      // Save to localStorage
      localStorage.setItem('favoriteTickers', JSON.stringify(state.favoriteTickers));
    },
    
    LOAD_FAVORITE_TICKERS(state) {
      const stored = localStorage.getItem('favoriteTickers');
      if (stored) {
        try {
          state.favoriteTickers = JSON.parse(stored);
        } catch (e) {
          console.error('Failed to parse favorite tickers from localStorage', e);
        }
      }
    },
    
    SET_THEME(state, theme) {
      state.theme = theme;
      localStorage.setItem('theme', theme);
      document.documentElement.setAttribute('data-theme', theme);
    },
    
    LOAD_THEME(state) {
      const stored = localStorage.getItem('theme');
      if (stored) {
        state.theme = stored;
        document.documentElement.setAttribute('data-theme', stored);
      }
    }
  },
  
  actions: {
    /**
     * Initialize the application state
     */
    init({ commit, dispatch }) {
      commit('LOAD_RECENT_TICKERS');
      commit('LOAD_FAVORITE_TICKERS');
      commit('LOAD_THEME');
      
      // Initialize authentication from localStorage
      dispatch('auth/initAuth');
    },
    
    /**
     * Set the API auth header
     */
    setApiAuthHeader(context, token) {
      // Import done inside the action to avoid circular dependencies
      const { setAuthHeader } = require('@/services/api');
      setAuthHeader(token);
    },
    
    /**
     * Set the global loading state
     */
    setLoading({ commit }, loading) {
      commit('SET_LOADING', loading);
    },
    
    /**
     * Set a global error
     */
    setError({ commit }, error) {
      commit('SET_ERROR', error);
    },
    
    /**
     * Clear the global error
     */
    clearError({ commit }) {
      commit('CLEAR_ERROR');
    },
    
    /**
     * Add a ticker to the recent tickers list
     */
    addRecentTicker({ commit }, ticker) {
      commit('ADD_RECENT_TICKER', ticker);
    },
    
    /**
     * Toggle a ticker's favorite status
     */
    toggleFavoriteTicker({ commit }, ticker) {
      commit('TOGGLE_FAVORITE_TICKER', ticker);
    },
    
    /**
     * Set the application theme
     */
    setTheme({ commit }, theme) {
      commit('SET_THEME', theme);
    }
  },
  
  modules: {
    ticker: tickerModule,
    financials: financialsModule,
    options: optionsModule,
    auth: authModule
  }
});