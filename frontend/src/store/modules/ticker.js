import { tickerService } from '@/services/api';

export default {
  namespaced: true,
  
  state: {
    tickerInfo: null,
    historyData: [],
    dividends: null,
    splits: null,
    recommendations: [],
    calendar: null,
    sustainability: null,
    holders: null,
    news: [],
    currentTicker: null,
    historyParams: {
      start: null,
      end: null,
      interval: '1d'
    }
  },
  
  getters: {
    ticker: state => state.currentTicker,
    tickerInfo: state => state.tickerInfo,
    historyData: state => state.historyData,
    dividends: state => state.dividends,
    splits: state => state.splits,
    recommendations: state => state.recommendations,
    calendar: state => state.calendar,
    sustainability: state => state.sustainability,
    holders: state => state.holders,
    news: state => state.news,
    historyParams: state => state.historyParams,
    
    // Computed data
    latestPrice: state => {
      if (!state.historyData || state.historyData.length === 0) return null;
      return state.historyData[state.historyData.length - 1].close;
    },
    
    priceChange: state => {
      if (!state.historyData || state.historyData.length < 2) return null;
      const latest = state.historyData[state.historyData.length - 1].close;
      const previous = state.historyData[state.historyData.length - 2].close;
      return {
        value: latest - previous,
        percent: previous ? (latest - previous) / previous : 0
      };
    },
    
    priceData: state => {
      if (!state.historyData) return [];
      return state.historyData.map(item => ({
        date: item.date,
        open: item.open,
        high: item.high,
        low: item.low,
        close: item.close,
        volume: item.volume
      }));
    },
    
    hasTickerData: state => !!state.tickerInfo,
    
    companyName: state => state.tickerInfo?.data?.shortName || state.currentTicker
  },
  
  mutations: {
    SET_CURRENT_TICKER(state, ticker) {
      state.currentTicker = ticker;
    },
    
    SET_TICKER_INFO(state, info) {
      state.tickerInfo = info;
    },
    
    SET_HISTORY_DATA(state, data) {
      state.historyData = data;
    },
    
    SET_HISTORY_PARAMS(state, params) {
      state.historyParams = { ...state.historyParams, ...params };
    },
    
    SET_DIVIDENDS(state, dividends) {
      state.dividends = dividends;
    },
    
    SET_SPLITS(state, splits) {
      state.splits = splits;
    },
    
    SET_RECOMMENDATIONS(state, recommendations) {
      state.recommendations = recommendations;
    },
    
    SET_CALENDAR(state, calendar) {
      state.calendar = calendar;
    },
    
    SET_SUSTAINABILITY(state, sustainability) {
      state.sustainability = sustainability;
    },
    
    SET_HOLDERS(state, holders) {
      state.holders = holders;
    },
    
    SET_NEWS(state, news) {
      state.news = news;
    },
    
    CLEAR_TICKER_DATA(state) {
      state.tickerInfo = null;
      state.historyData = [];
      state.dividends = null;
      state.splits = null;
      state.recommendations = [];
      state.calendar = null;
      state.sustainability = null;
      state.holders = null;
      state.news = [];
    }
  },
  
  actions: {
    /**
     * Set the current ticker and load basic info
     */
    async setTicker({ commit, dispatch }, ticker) {
      if (!ticker) return;
      
      commit('SET_CURRENT_TICKER', ticker.toUpperCase());
      commit('CLEAR_TICKER_DATA');
      
      try {
        // Load basic ticker info
        await dispatch('fetchTickerInfo');
        
        // Add to recent tickers
        dispatch('addRecentTicker', ticker.toUpperCase(), { root: true });
      } catch (error) {
        dispatch('setError', `Failed to load ticker data: ${error.message}`, { root: true });
      }
    },
    
    /**
     * Fetch general ticker information
     */
    async fetchTickerInfo({ commit, state, dispatch }) {
      if (!state.currentTicker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await tickerService.getTickerInfo(state.currentTicker);
        commit('SET_TICKER_INFO', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load ticker info: ${error.message}`, { root: true });
        throw error;
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch historical price data
     */
    async fetchHistoryData({ commit, state, dispatch }, params = {}) {
      if (!state.currentTicker) return;
      
      // Default to last 6 months if no date range provided
      const today = new Date();
      const sixMonthsAgo = new Date();
      sixMonthsAgo.setMonth(today.getMonth() - 6);
      
      const start = params.start || sixMonthsAgo.toISOString().split('T')[0];
      const end = params.end || today.toISOString().split('T')[0];
      const interval = params.interval || state.historyParams.interval;
      
      // Check if the parameters are the same as the last request (avoid duplicate calls)
      if (
        state.historyParams.start === start &&
        state.historyParams.end === end &&
        state.historyParams.interval === interval &&
        state.historyData && 
        state.historyData.length > 0
      ) {
        console.log('Skipping duplicate history data request');
        return;
      }
      
      // Update history parameters
      commit('SET_HISTORY_PARAMS', { start, end, interval });
      dispatch('setLoading', true, { root: true });
      
      // Track the current request
      const requestId = `${state.currentTicker}_${start}_${end}_${interval}_${Date.now()}`;
      this.lastHistoryRequestId = requestId;
      
      try {
        // Make the API call directly - we've already increased the timeout in the API service
        const response = await tickerService.getTickerHistory(
          state.currentTicker, 
          start,
          end,
          interval
        );
        
        // Only update state if this is still the most recent request
        if (this.lastHistoryRequestId === requestId) {
          commit('SET_HISTORY_DATA', response.data.data || []);
        } else {
          console.log('Ignoring outdated history data response');
        }
      } catch (error) {
        console.error('History data fetch error:', error);
        
        // If there's no data yet, set an empty array to prevent UI issues
        if (!state.historyData || state.historyData.length === 0) {
          commit('SET_HISTORY_DATA', []);
        }
        
        // Show a more user-friendly error message
        let errorMessage = 'Failed to load history data';
        if (error.message.includes('timeout')) {
          errorMessage = 'Request timed out. The server is taking too long to respond. Please try again later or try a shorter date range.';
        } else if (error.response && error.response.status) {
          errorMessage = `Server error (${error.response.status}). Please try again later.`;
        } else {
          errorMessage = `${errorMessage}: ${error.message}`;
        }
        
        dispatch('setError', errorMessage, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch dividend data
     */
    async fetchDividends({ commit, state, dispatch }) {
      if (!state.currentTicker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await tickerService.getTickerDividends(state.currentTicker);
        commit('SET_DIVIDENDS', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load dividend data: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch stock splits data
     */
    async fetchSplits({ commit, state, dispatch }) {
      if (!state.currentTicker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await tickerService.getTickerSplits(state.currentTicker);
        commit('SET_SPLITS', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load splits data: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch analyst recommendations
     */
    async fetchRecommendations({ commit, state, dispatch }) {
      if (!state.currentTicker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await tickerService.getTickerRecommendations(state.currentTicker);
        commit('SET_RECOMMENDATIONS', response.data.data || []);
      } catch (error) {
        dispatch('setError', `Failed to load recommendations: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch event calendar data
     */
    async fetchCalendar({ commit, state, dispatch }) {
      if (!state.currentTicker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await tickerService.getTickerCalendar(state.currentTicker);
        commit('SET_CALENDAR', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load calendar data: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch sustainability (ESG) data
     */
    async fetchSustainability({ commit, state, dispatch }) {
      if (!state.currentTicker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await tickerService.getTickerSustainability(state.currentTicker);
        commit('SET_SUSTAINABILITY', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load sustainability data: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch holders information
     */
    async fetchHolders({ commit, state, dispatch }) {
      if (!state.currentTicker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await tickerService.getTickerHolders(state.currentTicker);
        commit('SET_HOLDERS', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load holders data: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch news related to the ticker
     */
    async fetchNews({ commit, state, dispatch }) {
      if (!state.currentTicker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await tickerService.getTickerNews(state.currentTicker);
        // Process news data - it might come in different formats from the backend or mock data
        let newsData = [];
        
        if (response && response.data) {
          if (Array.isArray(response.data)) {
            // Direct array of news items (typical yfinance format)
            newsData = response.data;
          } else if (response.data.data && Array.isArray(response.data.data)) {
            // Nested in data property (our API wrapper format)
            newsData = response.data.data;
          }
        }
        
        // Process each news item to ensure it has the expected properties
        const processedNews = newsData.map(item => {
          // If the item has a content property (yfinance structure), extract relevant info
          if (item.content) {
            return {
              title: item.title || item.content.title,
              publisher: item.publisher || (item.content.provider ? item.content.provider.displayName : ''),
              link: item.link || (item.content.clickThroughUrl ? item.content.clickThroughUrl.url : ''),
              providerPublishTime: item.providerPublishTime || new Date(item.content.pubDate).getTime() / 1000,
              type: item.type || item.content.contentType,
              summary: item.summary || item.content.summary,
              thumbnail: item.thumbnail || item.content.thumbnail
            };
          }
          
          // Item already has expected structure
          return item;
        });
        
        commit('SET_NEWS', processedNews);
      } catch (error) {
        console.error('News fetch error:', error);
        dispatch('setError', `Failed to load news: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Load all ticker data (for dashboard view)
     */
    async loadTickerDashboard({ dispatch }) {
      await dispatch('fetchTickerInfo');
      await dispatch('fetchHistoryData');
      await dispatch('fetchNews');
      
      // Load these in parallel
      Promise.all([
        dispatch('fetchDividends'),
        dispatch('fetchRecommendations'),
        dispatch('fetchCalendar')
      ]);
    },
    
    /**
     * Clear all ticker data
     */
    clearTickerData({ commit }) {
      commit('CLEAR_TICKER_DATA');
      commit('SET_CURRENT_TICKER', null);
    }
  }
};