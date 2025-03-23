<template>
  <div class="financials-view">
    <div class="app-container">
      <!-- Ticker Header -->
      <section class="ticker-header">
        <div class="ticker-header__left">
          <div class="ticker-header__symbol">{{ symbol }}</div>
          <h1 class="ticker-header__name">{{ companyName }} Financial Statements</h1>
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
          exact-active-class="active"
        >
          Financials
        </router-link>
        <router-link 
          :to="{ name: 'options', params: { symbol } }" 
          class="ticker-nav__link"
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
        <p>Loading financial data...</p>
      </div>
      
      <!-- Error Message -->
      <div class="error-message" v-if="hasError">
        <i class="pi pi-exclamation-triangle"></i>
        <p>{{ errorMessage }}</p>
      </div>
      
      <!-- Financial Statements Content -->
      <div class="financials-content" v-if="!loading && !hasError">
        <!-- Period Toggle -->
        <div class="statement-controls">
          <div class="statement-controls__period">
            <button 
              class="period-button" 
              :class="{ active: isAnnualView }"
              @click="setActiveView('annual')"
            >
              Annual
            </button>
            <button 
              class="period-button" 
              :class="{ active: !isAnnualView }"
              @click="setActiveView('quarterly')"
            >
              Quarterly
            </button>
          </div>
          
          <div class="statement-controls__statement">
            <button 
              class="statement-button" 
              :class="{ active: activeStatement === 'income' }"
              @click="setActiveStatement('income')"
            >
              Income Statement
            </button>
            <button 
              class="statement-button" 
              :class="{ active: activeStatement === 'balance' }"
              @click="setActiveStatement('balance')"
            >
              Balance Sheet
            </button>
            <button 
              class="statement-button" 
              :class="{ active: activeStatement === 'cashflow' }"
              @click="setActiveStatement('cashflow')"
            >
              Cash Flow
            </button>
          </div>
        </div>
        
        <!-- Key Metrics Card -->
        <div class="key-metrics" v-if="hasFinancials">
          <h3 class="key-metrics__title">Key Financial Metrics</h3>
          <div class="key-metrics__grid">
            <div class="metric-card">
              <div class="metric-card__label">Revenue</div>
              <div class="metric-card__value">
                {{ formatLargeNumber(keyMetrics?.revenue, 2) }}
              </div>
            </div>
            
            <div class="metric-card">
              <div class="metric-card__label">Net Income</div>
              <div class="metric-card__value" :class="getValueColorClass(keyMetrics?.netIncome)">
                {{ formatLargeNumber(keyMetrics?.netIncome, 2) }}
              </div>
            </div>
            
            <div class="metric-card">
              <div class="metric-card__label">EPS</div>
              <div class="metric-card__value" :class="getValueColorClass(keyMetrics?.eps)">
                {{ formatCurrency(keyMetrics?.eps) }}
              </div>
            </div>
            
            <div class="metric-card">
              <div class="metric-card__label">Total Assets</div>
              <div class="metric-card__value">
                {{ formatLargeNumber(keyMetrics?.totalAssets, 2) }}
              </div>
            </div>
            
            <div class="metric-card">
              <div class="metric-card__label">Total Liabilities</div>
              <div class="metric-card__value">
                {{ formatLargeNumber(keyMetrics?.totalLiabilities, 2) }}
              </div>
            </div>
            
            <div class="metric-card">
              <div class="metric-card__label">Equity</div>
              <div class="metric-card__value" :class="getValueColorClass(keyMetrics?.shareholderEquity)">
                {{ formatLargeNumber(keyMetrics?.shareholderEquity, 2) }}
              </div>
            </div>
          </div>
        </div>
        
        <!-- Financial Statement Table -->
        <div class="statement-container" v-if="hasFinancials">
          <h3 class="statement-title">{{ statementTitle }}</h3>
          
          <div class="statement-table-wrapper">
            <table class="financial-table">
              <thead>
                <tr>
                  <th class="label-column">Item</th>
                  <th v-for="period in financialPeriods" :key="period">
                    {{ formatDate(period, 'MMM DD, YYYY') }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in statementItems" :key="index">
                  <td class="label-column">{{ formatStatementLabel(item) }}</td>
                  <td 
                    v-for="period in financialPeriods" 
                    :key="period"
                    :class="getValueColorClass(currentStatementData[item]?.[period])"
                  >
                    {{ formatValue(currentStatementData[item]?.[period]) }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <!-- No Data Message -->
        <div class="no-data-message" v-if="!hasFinancials">
          <i class="pi pi-info-circle"></i>
          <p>No financial data available for {{ symbol }}</p>
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
  formatLargeNumber, 
  formatDate,
  getValueColorClass
} from '@/utils/formatters';

export default {
  name: 'FinancialsView',
  
  props: {
    symbol: {
      type: String,
      required: true
    }
  },
  
  setup(props) {
    const store = useStore();
    const activeStatement = ref('income');
    
    // Get state from store
    const companyName = computed(() => store.getters['ticker/companyName']);
    const loading = computed(() => store.getters.isLoading);
    const hasError = computed(() => store.getters.hasError);
    const errorMessage = computed(() => store.getters.errorMessage);
    
    // Financial data
    const financialPeriods = computed(() => store.getters['financials/financialPeriods']);
    const keyMetrics = computed(() => store.getters['financials/keyMetrics']);
    const isAnnualView = computed(() => store.getters['financials/isAnnualView']);
    
    // Determine which financial statement data to show
    const earnings = computed(() => store.getters['financials/activeEarnings']?.data || {});
    const balanceSheet = computed(() => store.getters['financials/activeBalanceSheet']?.data || {});
    const cashflow = computed(() => store.getters['financials/activeCashflow']?.data || {});
    
    // Current statement data based on the active statement
    const currentStatementData = computed(() => {
      switch (activeStatement.value) {
        case 'income':
          return earnings.value;
        case 'balance':
          return balanceSheet.value;
        case 'cashflow':
          return cashflow.value;
        default:
          return {};
      }
    });
    
    // Get items to display for the current statement
    const statementItems = computed(() => {
      return Object.keys(currentStatementData.value)
        .filter(key => key !== 'ticker' && key !== 'data');
    });
    
    // Determine if we have any financial data
    const hasFinancials = computed(() => {
      return (
        Object.keys(earnings.value).length > 0 ||
        Object.keys(balanceSheet.value).length > 0 ||
        Object.keys(cashflow.value).length > 0
      );
    });
    
    // Statement title based on the active statement and view
    const statementTitle = computed(() => {
      const viewText = isAnnualView.value ? 'Annual' : 'Quarterly';
      
      switch (activeStatement.value) {
        case 'income':
          return `${viewText} Income Statement`;
        case 'balance':
          return `${viewText} Balance Sheet`;
        case 'cashflow':
          return `${viewText} Cash Flow Statement`;
        default:
          return 'Financial Statement';
      }
    });
    
    // Methods
    const loadFinancialData = () => {
      // Set the ticker first
      store.dispatch('ticker/setTicker', props.symbol);
      
      // Load financial data based on the active view
      if (isAnnualView.value) {
        store.dispatch('financials/loadAnnualFinancials');
      } else {
        store.dispatch('financials/loadQuarterlyFinancials');
      }
    };
    
    const setActiveView = (view) => {
      store.dispatch('financials/setActiveView', view);
      
      // Reload data for the new view
      if (view === 'annual') {
        store.dispatch('financials/loadAnnualFinancials');
      } else {
        store.dispatch('financials/loadQuarterlyFinancials');
      }
    };
    
    const setActiveStatement = (statement) => {
      activeStatement.value = statement;
    };
    
    // Format statement label to make it more readable
    const formatStatementLabel = (label) => {
      if (!label) return '';
      
      // Replace camelCase with spaces
      return label
        .replace(/([A-Z])/g, ' $1')
        .replace(/^./, str => str.toUpperCase())
        .trim();
    };
    
    // Format financial values appropriately
    const formatValue = (value) => {
      if (value === null || value === undefined) return 'N/A';
      
      // Format as large number
      return formatLargeNumber(value, 2);
    };
    
    // Lifecycle hooks
    onMounted(() => {
      loadFinancialData();
    });
    
    // Watch for changes in the symbol prop
    watch(() => props.symbol, (newSymbol) => {
      if (newSymbol) {
        loadFinancialData();
      }
    });
    
    return {
      companyName,
      loading,
      hasError,
      errorMessage,
      financialPeriods,
      keyMetrics,
      isAnnualView,
      activeStatement,
      currentStatementData,
      statementItems,
      hasFinancials,
      statementTitle,
      setActiveView,
      setActiveStatement,
      formatStatementLabel,
      formatValue,
      // Utility functions
      formatCurrency,
      formatLargeNumber,
      formatDate,
      getValueColorClass
    };
  }
};
</script>

<style lang="scss" scoped>
.financials-view {
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

// Financial Statements Controls
.statement-controls {
  display: flex;
  justify-content: space-between;
  margin-bottom: $spacing-lg;
  
  @media (max-width: $breakpoint-sm) {
    flex-direction: column;
    gap: $spacing-md;
  }
  
  &__period,
  &__statement {
    display: flex;
    
    .period-button,
    .statement-button {
      background: transparent;
      border: 1px solid $text-disabled;
      color: $text-secondary;
      font-size: $font-size-sm;
      padding: $spacing-sm $spacing-lg;
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
        border-top-left-radius: $spacing-xs;
        border-bottom-left-radius: $spacing-xs;
      }
      
      &:last-child {
        border-top-right-radius: $spacing-xs;
        border-bottom-right-radius: $spacing-xs;
      }
    }
  }
}

// Key Metrics
.key-metrics {
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  margin-bottom: $spacing-lg;
  overflow: hidden;
  
  &__title {
    font-size: $font-size-lg;
    font-weight: 600;
    margin: 0;
    padding: $spacing-md;
    background-color: rgba($bg-secondary, 0.5);
    color: $secondary-color;
  }
  
  &__grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    padding: $spacing-md;
    gap: $spacing-md;
    
    @media (max-width: $breakpoint-md) {
      grid-template-columns: repeat(2, 1fr);
    }
    
    @media (max-width: $breakpoint-sm) {
      grid-template-columns: 1fr;
    }
  }
}

.metric-card {
  background-color: rgba($bg-secondary, 0.3);
  padding: $spacing-md;
  border-radius: $spacing-xs;
  
  &__label {
    font-size: $font-size-sm;
    color: $text-secondary;
    margin-bottom: $spacing-xs;
  }
  
  &__value {
    font-size: $font-size-lg;
    font-weight: 600;
    color: $text-primary;
  }
}

// Statement Table
.statement-container {
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  margin-bottom: $spacing-lg;
  overflow: hidden;
}

.statement-title {
  font-size: $font-size-lg;
  font-weight: 600;
  margin: 0;
  padding: $spacing-md;
  background-color: rgba($bg-secondary, 0.5);
  color: $secondary-color;
}

.statement-table-wrapper {
  overflow-x: auto;
  padding: $spacing-md;
}

.financial-table {
  width: 100%;
  border-collapse: collapse;
  
  th, td {
    padding: $spacing-sm;
    text-align: right;
    border-bottom: 1px solid rgba($text-disabled, 0.2);
    white-space: nowrap;
  }
  
  th {
    font-weight: 600;
    color: $text-secondary;
    background-color: rgba($bg-secondary, 0.3);
  }
  
  td {
    color: $text-primary;
  }
  
  th:first-child,
  td:first-child {
    position: sticky;
    left: 0;
    background-color: $bg-primary;
    z-index: 1;
    text-align: left;
  }
  
  .label-column {
    min-width: 220px;
    max-width: 300px;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: 500;
  }
  
  tr:hover td {
    background-color: rgba($bg-secondary, 0.2);
  }
  
  tr:hover td:first-child {
    background-color: rgba($bg-secondary, 0.4);
  }
}
</style>