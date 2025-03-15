import { optionsService } from '@/services/api';

export default {
  namespaced: true,
  
  state: {
    optionsDates: [],
    optionsChain: null,
    selectedExpirationDate: null,
    view: 'both' // 'calls', 'puts', or 'both'
  },
  
  getters: {
    optionsDates: state => state.optionsDates,
    optionsChain: state => state.optionsChain,
    selectedExpirationDate: state => state.selectedExpirationDate,
    view: state => state.view,
    
    // Get calls data with calculated values
    callOptions: state => {
      if (!state.optionsChain || !state.optionsChain.data || !state.optionsChain.data.calls) {
        return [];
      }
      
      return state.optionsChain.data.calls.map(call => ({
        ...call,
        type: 'call',
        inTheMoney: call.inTheMoney === undefined 
          ? (call.strike < call.lastPrice) 
          : call.inTheMoney
      }));
    },
    
    // Get puts data with calculated values
    putOptions: state => {
      if (!state.optionsChain || !state.optionsChain.data || !state.optionsChain.data.puts) {
        return [];
      }
      
      return state.optionsChain.data.puts.map(put => ({
        ...put,
        type: 'put',
        inTheMoney: put.inTheMoney === undefined 
          ? (put.strike > put.lastPrice) 
          : put.inTheMoney
      }));
    },
    
    // Get displayed options based on the selected view
    displayedOptions: (state, getters) => {
      if (state.view === 'calls') {
        return getters.callOptions;
      }
      if (state.view === 'puts') {
        return getters.putOptions;
      }
      
      // Both calls and puts (default)
      return [...getters.callOptions, ...getters.putOptions];
    },
    
    // Get the option chain ticker
    optionsTicker: state => state.optionsChain?.ticker,
    
    // Check if options data is available
    hasOptionsData: state => state.optionsChain !== null && 
      state.optionsChain.data !== null &&
      ((state.optionsChain.data.calls && state.optionsChain.data.calls.length > 0) ||
       (state.optionsChain.data.puts && state.optionsChain.data.puts.length > 0)),
    
    // Get a list of unique strike prices from both calls and puts
    strikeList: (state, getters) => {
      if (!getters.hasOptionsData) {
        return [];
      }
      
      // Collect all strike prices from calls and puts
      const strikes = new Set([
        ...(getters.callOptions.map(call => call.strike) || []),
        ...(getters.putOptions.map(put => put.strike) || [])
      ]);
      
      // Return sorted array of unique strike prices
      return Array.from(strikes).sort((a, b) => a - b);
    },
    
    // Determine if there's a loading state
    isLoading: state => {
      return !state.optionsChain && state.selectedExpirationDate !== null;
    }
  },
  
  mutations: {
    SET_OPTIONS_DATES(state, dates) {
      state.optionsDates = dates;
      
      // Initialize selectedExpirationDate if it's not set and we have dates
      if (!state.selectedExpirationDate && dates && dates.data && dates.data.length > 0) {
        state.selectedExpirationDate = dates.data[0];
      }
    },
    
    SET_OPTIONS_CHAIN(state, chain) {
      state.optionsChain = chain;
    },
    
    SET_SELECTED_EXPIRATION_DATE(state, date) {
      state.selectedExpirationDate = date;
    },
    
    SET_VIEW(state, view) {
      state.view = view;
    },
    
    CLEAR_OPTIONS_DATA(state) {
      state.optionsDates = [];
      state.optionsChain = null;
      state.selectedExpirationDate = null;
    }
  },
  
  actions: {
    /**
     * Set the options view (calls, puts, or both)
     */
    setView({ commit }, view) {
      commit('SET_VIEW', view);
    },
    
    /**
     * Set the selected expiration date and fetch the options chain
     */
    async selectExpirationDate({ commit, dispatch }, date) {
      commit('SET_SELECTED_EXPIRATION_DATE', date);
      commit('SET_OPTIONS_CHAIN', null); // Clear previous data
      
      // Fetch options chain for the selected date
      await dispatch('fetchOptionsChain');
    },
    
    /**
     * Fetch available options expiration dates
     */
    async fetchOptionsDates({ commit, rootState, dispatch }) {
      const ticker = rootState.ticker.currentTicker;
      if (!ticker) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await optionsService.getOptionsDates(ticker);
        commit('SET_OPTIONS_DATES', response.data);
        
        // If we have dates and no selected date yet, select the first one
        if (response.data.data && response.data.data.length > 0 && !rootState.options.selectedExpirationDate) {
          commit('SET_SELECTED_EXPIRATION_DATE', response.data.data[0]);
        }
      } catch (error) {
        dispatch('setError', `Failed to load options dates: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Fetch options chain for the selected expiration date
     */
    async fetchOptionsChain({ commit, state, rootState, dispatch }) {
      const ticker = rootState.ticker.currentTicker;
      const date = state.selectedExpirationDate;
      
      if (!ticker || !date) return;
      
      dispatch('setLoading', true, { root: true });
      
      try {
        const response = await optionsService.getOptionsChain(ticker, date);
        commit('SET_OPTIONS_CHAIN', response.data);
      } catch (error) {
        dispatch('setError', `Failed to load options chain: ${error.message}`, { root: true });
      } finally {
        dispatch('setLoading', false, { root: true });
      }
    },
    
    /**
     * Load initial options data
     */
    async loadOptionsData({ dispatch, commit }) {
      // Reset view to 'both'
      commit('SET_VIEW', 'both');
      
      // First fetch available expiration dates
      await dispatch('fetchOptionsDates');
      
      // Then fetch options chain for the selected date
      await dispatch('fetchOptionsChain');
    },
    
    /**
     * Clear all options data
     */
    clearOptionsData({ commit }) {
      commit('CLEAR_OPTIONS_DATA');
    }
  }
};