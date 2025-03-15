<template>
  <div class="options-view">
    <div class="app-container">
      <!-- Ticker Header -->
      <section class="ticker-header">
        <div class="ticker-header__left">
          <div class="ticker-header__symbol">{{ symbol }}</div>
          <h1 class="ticker-header__name">{{ companyName }} Options Chain</h1>
        </div>
      </section>
      
      <!-- Ticker Navigation -->
      <div class="ticker-nav">
        <router-link 
          :to="{ name: 'ticker', params: { symbol } }" 
          class="ticker-nav__link"
        >
          Overview
        </router-link>
        <router-link 
          :to="{ name: 'financials', params: { symbol } }" 
          class="ticker-nav__link"
        >
          Financials
        </router-link>
        <router-link 
          :to="{ name: 'options', params: { symbol } }" 
          class="ticker-nav__link"
          exact-active-class="active"
        >
          Options
        </router-link>
        <router-link 
          :to="{ name: 'news', params: { symbol } }" 
          class="ticker-nav__link"
        >
          News
        </router-link>
      </div>
      
      <!-- Loading Indicator -->
      <div class="loading-container" v-if="loading">
        <div class="loader"></div>
        <p>Loading options data...</p>
      </div>
      
      <!-- Error Message -->
      <div class="error-message" v-if="hasError">
        <i class="pi pi-exclamation-triangle"></i>
        <p>{{ errorMessage }}</p>
      </div>
      
      <!-- Options Content -->
      <div class="options-content" v-if="!loading && !hasError">
        <!-- Date and View Controls -->
        <div class="options-controls">
          <!-- Expiration Date Selector -->
          <div class="options-controls__dates">
            <label for="expiration-date">Expiration Date:</label>
            <select 
              id="expiration-date" 
              v-model="selectedDate"
              @change="onDateChange"
              class="date-select"
            >
              <option 
                v-for="date in optionsDates" 
                :key="date" 
                :value="date"
              >
                {{ formatDate(date, 'MMMM D, YYYY') }}
              </option>
            </select>
          </div>
          
          <!-- View Selector -->
          <div class="options-controls__view">
            <label for="options-view">View:</label>
            <div class="view-buttons">
              <button 
                class="view-button" 
                :class="{ active: optionsView === 'both' }"
                @click="setOptionsView('both')"
              >
                All
              </button>
              <button 
                class="view-button" 
                :class="{ active: optionsView === 'calls' }"
                @click="setOptionsView('calls')"
              >
                Calls
              </button>
              <button 
                class="view-button" 
                :class="{ active: optionsView === 'puts' }"
                @click="setOptionsView('puts')"
              >
                Puts
              </button>
            </div>
          </div>
          
          <!-- Filter Controls (Optional) -->
          <div class="options-controls__filter">
            <label for="options-filter">Filter:</label>
            <select 
              id="options-filter" 
              v-model="moneyFilter"
              class="filter-select"
            >
              <option value="all">All Options</option>
              <option value="in-the-money">In The Money</option>
              <option value="out-of-the-money">Out Of The Money</option>
            </select>
          </div>
        </div>
        
        <!-- Options Chain Table -->
        <div class="options-table-container" v-if="hasOptionsData">
          <table class="options-table">
            <thead>
              <tr>
                <th v-if="optionsView !== 'puts'" colspan="6" class="table-header calls-header">CALLS</th>
                <th v-if="optionsView === 'both'" class="strike-header">Strike</th>
                <th v-if="optionsView !== 'calls'" colspan="6" class="table-header puts-header">PUTS</th>
              </tr>
              <tr>
                <!-- Calls Headers -->
                <template v-if="optionsView !== 'puts'">
                  <th>Last Price</th>
                  <th>Change</th>
                  <th>Bid</th>
                  <th>Ask</th>
                  <th>Volume</th>
                  <th>Open Int</th>
                </template>
                
                <!-- Strike Price Column -->
                <th v-if="optionsView === 'both'" class="strike-column">Strike</th>
                
                <!-- Puts Headers -->
                <template v-if="optionsView !== 'calls'">
                  <th>Last Price</th>
                  <th>Change</th>
                  <th>Bid</th>
                  <th>Ask</th>
                  <th>Volume</th>
                  <th>Open Int</th>
                </template>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="strike in filteredStrikes" 
                :key="strike"
                :class="getStrikeRowClass(strike)"
              >
                <!-- Calls Data -->
                <template v-if="optionsView !== 'puts'">
                  <td 
                    v-for="(field, index) in callFields" 
                    :key="`call-${index}`"
                    :class="[
                      getCallFieldClass(field, getCallForStrike(strike)),
                      formatOptionValue(field, getCallForStrike(strike)) === 'N/A' ? 'na-value' : ''
                    ]"
                  >
                    {{ formatOptionValue(field, getCallForStrike(strike)) }}
                  </td>
                </template>
                
                <!-- Strike Price Column -->
                <td v-if="optionsView === 'both'" class="strike-column">
                  {{ formatCurrency(strike) }}
                </td>
                
                <!-- Puts Data -->
                <template v-if="optionsView !== 'calls'">
                  <td 
                    v-for="(field, index) in putFields" 
                    :key="`put-${index}`"
                    :class="[
                      getPutFieldClass(field, getPutForStrike(strike)),
                      formatOptionValue(field, getPutForStrike(strike)) === 'N/A' ? 'na-value' : ''
                    ]"
                  >
                    {{ formatOptionValue(field, getPutForStrike(strike)) }}
                  </td>
                </template>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- No Options Data Message -->
        <div class="no-data-message" v-else>
          <i class="pi pi-info-circle"></i>
          <p>No options data available for {{ symbol }} on {{ formatDate(selectedDate) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { 
  formatCurrency, 
  formatNumber, 
  formatPercent, 
  formatDate,
  getValueColorClass,
  formatWithSign
} from '@/utils/formatters';

export default {
  name: 'OptionsView',
  
  props: {
    symbol: {
      type: String,
      required: true
    }
  },
  
  setup(props) {
    const store = useStore();
    const selectedDate = ref('');
    const optionsView = ref('both');
    const moneyFilter = ref('all');
    
    // Get state from store
    const companyName = computed(() => store.getters['ticker/companyName']);
    const optionsDates = computed(() => store.getters['options/optionsDates']?.data || []);
    const callOptions = computed(() => store.getters['options/callOptions'] || []);
    const putOptions = computed(() => store.getters['options/putOptions'] || []);
    const loading = computed(() => store.getters.isLoading);
    const hasError = computed(() => store.getters.hasError);
    const errorMessage = computed(() => store.getters.errorMessage);
    
    // Fields to display for calls and puts
    const callFields = ['lastPrice', 'change', 'bid', 'ask', 'volume', 'openInterest'];
    const putFields = ['lastPrice', 'change', 'bid', 'ask', 'volume', 'openInterest'];
    
    // Determine if we have options data
    const hasOptionsData = computed(() => {
      return (callOptions.value.length > 0 || putOptions.value.length > 0) && selectedDate.value;
    });
    
    // Get list of all strike prices
    const strikes = computed(() => {
      return store.getters['options/strikeList'];
    });
    
    // Filter strikes based on moneyFilter
    const filteredStrikes = computed(() => {
      if (moneyFilter.value === 'in-the-money') {
        if (optionsView.value === 'calls') {
          return strikes.value.filter(strike => {
            const call = getCallForStrike(strike);
            return call && call.inTheMoney;
          });
        } else if (optionsView.value === 'puts') {
          return strikes.value.filter(strike => {
            const put = getPutForStrike(strike);
            return put && put.inTheMoney;
          });
        } else {
          return strikes.value.filter(strike => {
            const call = getCallForStrike(strike);
            const put = getPutForStrike(strike);
            return (call && call.inTheMoney) || (put && put.inTheMoney);
          });
        }
      } else if (moneyFilter.value === 'out-of-the-money') {
        if (optionsView.value === 'calls') {
          return strikes.value.filter(strike => {
            const call = getCallForStrike(strike);
            return call && !call.inTheMoney;
          });
        } else if (optionsView.value === 'puts') {
          return strikes.value.filter(strike => {
            const put = getPutForStrike(strike);
            return put && !put.inTheMoney;
          });
        } else {
          return strikes.value.filter(strike => {
            const call = getCallForStrike(strike);
            const put = getPutForStrike(strike);
            return (call && !call.inTheMoney) || (put && !put.inTheMoney);
          });
        }
      }
      
      return strikes.value;
    });
    
    // Methods
    const loadOptionsData = () => {
      // Set the ticker first
      store.dispatch('ticker/setTicker', props.symbol);
      
      // Load options data
      store.dispatch('options/loadOptionsData');
    };
    
    // Get the call option for a specific strike price
    const getCallForStrike = (strike) => {
      return callOptions.value.find(call => call.strike === strike);
    };
    
    // Get the put option for a specific strike price
    const getPutForStrike = (strike) => {
      return putOptions.value.find(put => put.strike === strike);
    };
    
    // Set options view (calls, puts, or both)
    const setOptionsView = (view) => {
      optionsView.value = view;
      store.dispatch('options/setView', view);
    };
    
    // Handle date change
    const onDateChange = () => {
      store.dispatch('options/selectExpirationDate', selectedDate.value);
    };
    
    // Format option values based on the field
    const formatOptionValue = (field, option) => {
      if (!option) return 'N/A';
      
      const value = option[field];
      if (value === undefined || value === null) return 'N/A';
      
      // Convert displayable values to correct formats
      try {
        switch (field) {
          case 'lastPrice':
          case 'bid':
          case 'ask':
            return formatCurrency(value);
            
          case 'change':
            return formatWithSign(formatCurrency(value));
            
          case 'percentChange':
            return formatWithSign(formatPercent(value / 100));
            
          case 'volume':
          case 'openInterest':
            return formatNumber(value, 0);
            
          default:
            return value.toString();
        }
      } catch (error) {
        // If there's any error formatting, just show N/A
        console.warn(`Error formatting ${field}:`, error);
        return 'N/A';
      }
    };
    
    // Get CSS class for call field
    const getCallFieldClass = (field, call) => {
      if (!call) return '';
      
      if (field === 'change' || field === 'percentChange') {
        const value = call[field];
        // Only apply color class if there's an actual value (not null/undefined/NaN)
        if (value !== null && value !== undefined && !isNaN(value)) {
          return getValueColorClass(value);
        }
      }
      
      return '';
    };
    
    // Get CSS class for put field
    const getPutFieldClass = (field, put) => {
      if (!put) return '';
      
      if (field === 'change' || field === 'percentChange') {
        const value = put[field];
        // Only apply color class if there's an actual value (not null/undefined/NaN)
        if (value !== null && value !== undefined && !isNaN(value)) {
          return getValueColorClass(value);
        }
      }
      
      return '';
    };
    
    // Get CSS class for strike row
    const getStrikeRowClass = (strike) => {
      const call = getCallForStrike(strike);
      const put = getPutForStrike(strike);
      
      if ((call && call.inTheMoney) || (put && put.inTheMoney)) {
        return 'in-the-money';
      }
      
      return '';
    };
    
    // Lifecycle hooks
    onMounted(() => {
      loadOptionsData();
      
      // Initialize selectedDate when optionsDates are loaded
      watch(optionsDates, (newDates) => {
        if (newDates && newDates.length > 0 && !selectedDate.value) {
          selectedDate.value = newDates[0];
          store.dispatch('options/selectExpirationDate', selectedDate.value);
        }
      });
    });
    
    // Watch for changes in the symbol prop
    watch(() => props.symbol, (newSymbol) => {
      if (newSymbol) {
        // Reset selected date when symbol changes
        selectedDate.value = '';
        
        // Load options data for the new symbol
        loadOptionsData();
      }
    });
    
    return {
      companyName,
      optionsDates,
      selectedDate,
      optionsView,
      moneyFilter,
      callFields,
      putFields,
      loading,
      hasError,
      errorMessage,
      hasOptionsData,
      filteredStrikes,
      getCallForStrike,
      getPutForStrike,
      setOptionsView,
      onDateChange,
      formatOptionValue,
      getCallFieldClass,
      getPutFieldClass,
      getStrikeRowClass,
      // Utility functions
      formatCurrency,
      formatNumber,
      formatPercent,
      formatDate,
      getValueColorClass,
      formatWithSign
    };
  }
};
</script>

<style lang="scss" scoped>
.options-view {
  min-height: 100vh;
}

// Ticker Header
.ticker-header {
  margin-bottom: $spacing-lg;
  
  &__symbol {
    font-size: $font-size-xl;
    font-weight: 700;
    color: $primary-color;
  }
  
  &__name {
    font-size: $font-size-xxl;
    font-weight: 600;
    margin: 0;
    color: $text-primary;
  }
}

// Navigation
.ticker-nav {
  display: flex;
  margin-bottom: $spacing-lg;
  border-bottom: 1px solid rgba($text-disabled, 0.3);
  
  &__link {
    padding: $spacing-md $spacing-lg;
    color: $text-secondary;
    text-decoration: none;
    font-weight: 500;
    position: relative;
    transition: $transition-quick;
    
    &:hover {
      color: $primary-color;
    }
    
    &.active {
      color: $primary-color;
      font-weight: 600;
      
      &:after {
        content: '';
        position: absolute;
        bottom: -1px;
        left: 0;
        right: 0;
        height: 3px;
        background-color: $primary-color;
      }
    }
  }
}

// Loading and Error States
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-xl;
  
  p {
    margin-top: $spacing-md;
    color: $text-secondary;
  }
}

.error-message {
  background-color: rgba($negative, 0.1);
  color: $negative;
  padding: $spacing-md;
  border-radius: $border-radius;
  margin-bottom: $spacing-lg;
  display: flex;
  align-items: center;
  
  i {
    margin-right: $spacing-md;
    font-size: $font-size-lg;
  }
  
  p {
    margin: 0;
  }
}

.no-data-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-xl;
  color: $text-secondary;
  
  i {
    font-size: 3rem;
    margin-bottom: $spacing-md;
    opacity: 0.5;
  }
  
  p {
    font-size: $font-size-lg;
  }
}

// Options Controls
.options-controls {
  display: flex;
  flex-wrap: wrap;
  gap: $spacing-md;
  margin-bottom: $spacing-lg;
  
  &__dates,
  &__view,
  &__filter {
    display: flex;
    flex-direction: column;
    
    label {
      font-size: $font-size-sm;
      color: $text-secondary;
      margin-bottom: $spacing-xs;
    }
  }
  
  &__dates {
    flex: 1;
    min-width: 200px;
  }
  
  .date-select,
  .filter-select {
    height: 40px;
    border: 1px solid $text-disabled;
    border-radius: $spacing-xs;
    padding: 0 $spacing-sm;
    color: $text-primary;
    background-color: $bg-primary;
    
    &:focus {
      outline: none;
      border-color: $primary-color;
    }
  }
  
  .view-buttons {
    display: flex;
    height: 40px;
    
    .view-button {
      padding: 0 $spacing-md;
      background: transparent;
      border: 1px solid $text-disabled;
      color: $text-secondary;
      cursor: pointer;
      transition: $transition-quick;
      
      &:hover {
        background-color: rgba($primary-color, 0.05);
      }
      
      &.active {
        background-color: $primary-color;
        color: white;
        border-color: $primary-color;
      }
      
      &:first-child {
        border-radius: $spacing-xs 0 0 $spacing-xs;
      }
      
      &:last-child {
        border-radius: 0 $spacing-xs $spacing-xs 0;
      }
    }
  }
}

// Options Table
.options-table-container {
  overflow-x: auto;
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  margin-bottom: $spacing-lg;
}

.options-table {
  width: 100%;
  border-collapse: collapse;
  
  th, td {
    padding: $spacing-sm;
    text-align: center;
    border-bottom: 1px solid rgba($text-disabled, 0.2);
    white-space: nowrap;
  }
  
  th {
    font-weight: 600;
    color: white;
    background-color: $secondary-color;
  }
  
  td {
    color: $text-primary;
  }
  
  .na-value {
    color: $text-disabled !important;
    font-style: italic;
  }
  
  .table-header {
    text-align: center;
    font-size: $font-size-md;
    font-weight: 700;
  }
  
  .calls-header {
    background-color: $chart-up;
  }
  
  .puts-header {
    background-color: $chart-down;
  }
  
  .strike-header,
  .strike-column {
    background-color: $secondary-color;
    color: white;
    font-weight: 600;
  }
  
  tr:hover td:not(.strike-column) {
    background-color: rgba($bg-secondary, 0.2);
  }
  
  .in-the-money td:not(.strike-column) {
    background-color: rgba($primary-color, 0.1);
  }
  
  .in-the-money:hover td:not(.strike-column) {
    background-color: rgba($primary-color, 0.15);
  }
  
  .financial-value--positive {
    color: $positive;
  }
  
  .financial-value--negative {
    color: $negative;
  }
}
</style>