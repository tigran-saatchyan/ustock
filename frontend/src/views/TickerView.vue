<template>
  <div class="ticker-view">
    <div class="app-container">
      <!-- Ticker Header -->
      <section class="ticker-header">
        <div class="ticker-header__left">
          <div class="ticker-header__symbol">
            {{ symbol }}
            <button 
              @click="toggleFavorite" 
              class="ticker-header__favorite-btn"
              :class="{ 'is-favorite': isFavorite }"
            >
              <i class="pi pi-star-fill"></i>
            </button>
          </div>
          <h1 class="ticker-header__name">{{ companyName }}</h1>
        </div>
        
        <div class="ticker-header__right" v-if="tickerInfo">
          <div class="ticker-header__price-container">
            <div class="ticker-header__price">
              {{ formatCurrency(latestPrice) }}
            </div>
            <div 
              class="ticker-header__change"
              :class="priceChangeClass"
            >
              {{ formatWithSign(formatCurrency(priceChange?.value)) }}
              ({{ formatWithSign(formatPercent(priceChange?.percent)) }})
            </div>
          </div>
        </div>
      </section>
      
      <!-- Ticker Navigation -->
      <div class="ticker-nav">
        <router-link 
          :to="{ name: 'ticker', params: { symbol } }" 
          class="ticker-nav__link"
          exact-active-class="active"
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
        <p>Loading {{ symbol }} data...</p>
      </div>
      
      <!-- Error Message -->
      <div class="error-message" v-if="hasError">
        <i class="pi pi-exclamation-triangle"></i>
        <p>{{ errorMessage }}</p>
      </div>
      
      <!-- Main Content -->
      <div class="ticker-content" v-if="!loading && !hasError && tickerInfo">
        <!-- Price Chart -->
        <price-chart 
          :data="historyData" 
          :ticker="symbol"
          :loading="chartLoading"
          @period-change="updateChartPeriod"
        />
        
        <!-- Info Grid -->
        <div class="info-grid">
          <!-- Company Overview -->
          <div class="info-card">
            <h3 class="info-card__title">Company Overview</h3>
            <div class="info-card__content">
              <table class="data-table">
                <tr v-if="tickerInfo?.data?.sector">
                  <td>Sector</td>
                  <td>{{ tickerInfo.data.sector }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.industry">
                  <td>Industry</td>
                  <td>{{ tickerInfo.data.industry }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.fullTimeEmployees">
                  <td>Employees</td>
                  <td>{{ formatNumber(tickerInfo.data.fullTimeEmployees) }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.country">
                  <td>Country</td>
                  <td>{{ tickerInfo.data.country }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.website">
                  <td>Website</td>
                  <td>
                    <a :href="tickerInfo.data.website" target="_blank" rel="noopener">
                      {{ tickerInfo.data.website }}
                    </a>
                  </td>
                </tr>
              </table>
            </div>
          </div>
          
          <!-- Key Statistics -->
          <div class="info-card">
            <h3 class="info-card__title">Key Statistics</h3>
            <div class="info-card__content">
              <table class="data-table">
                <tr v-if="tickerInfo?.data?.marketCap">
                  <td>Market Cap</td>
                  <td>{{ formatLargeNumber(tickerInfo.data.marketCap, 2) }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.trailingPE">
                  <td>P/E Ratio</td>
                  <td>{{ formatNumber(tickerInfo.data.trailingPE, 2) }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.trailingEps">
                  <td>EPS (TTM)</td>
                  <td>{{ formatCurrency(tickerInfo.data.trailingEps) }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.dividendYield">
                  <td>Dividend Yield</td>
                  <td>{{ formatPercent(tickerInfo.data.dividendYield) }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.fiftyTwoWeekHigh">
                  <td>52 Week High</td>
                  <td>{{ formatCurrency(tickerInfo.data.fiftyTwoWeekHigh) }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.fiftyTwoWeekLow">
                  <td>52 Week Low</td>
                  <td>{{ formatCurrency(tickerInfo.data.fiftyTwoWeekLow) }}</td>
                </tr>
              </table>
            </div>
          </div>
          
          <!-- Volume and Trading -->
          <div class="info-card">
            <h3 class="info-card__title">Volume & Trading</h3>
            <div class="info-card__content">
              <table class="data-table">
                <tr v-if="tickerInfo?.data?.averageVolume">
                  <td>Average Volume</td>
                  <td>{{ formatLargeNumber(tickerInfo.data.averageVolume) }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.averageVolume10days">
                  <td>Average 10 Day Volume</td>
                  <td>{{ formatLargeNumber(tickerInfo.data.averageVolume10days) }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.previousClose">
                  <td>Previous Close</td>
                  <td>{{ formatCurrency(tickerInfo.data.previousClose) }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.open">
                  <td>Open</td>
                  <td>{{ formatCurrency(tickerInfo.data.open) }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.dayHigh">
                  <td>Day High</td>
                  <td>{{ formatCurrency(tickerInfo.data.dayHigh) }}</td>
                </tr>
                <tr v-if="tickerInfo?.data?.dayLow">
                  <td>Day Low</td>
                  <td>{{ formatCurrency(tickerInfo.data.dayLow) }}</td>
                </tr>
              </table>
            </div>
          </div>
        </div>
        
        <!-- Company Description -->
        <div class="info-card full-width" v-if="tickerInfo?.data?.longBusinessSummary">
          <h3 class="info-card__title">About {{ companyName }}</h3>
          <div class="info-card__content">
            <p>{{ tickerInfo.data.longBusinessSummary }}</p>
          </div>
        </div>
        
        <!-- News Highlights -->
        <div class="info-card full-width" v-if="news && news.length > 0">
          <h3 class="info-card__title">
            Recent News
            <router-link :to="{ name: 'news', params: { symbol } }" class="view-all-link">
              View All
            </router-link>
          </h3>
          <div class="info-card__content">
            <div class="news-grid">
              <div 
                v-for="(item, index) in news.slice(0, 3)" 
                :key="index"
                class="news-item"
              >
                <a :href="item.link" target="_blank" rel="noopener" class="news-item__link">
                  <div class="news-item__meta">
                    <span class="news-item__source">{{ item.publisher }}</span>
                    <span class="news-item__date">{{ formatDate(item.providerPublishTime * 1000) }}</span>
                  </div>
                  <h4 class="news-item__title">{{ item.title }}</h4>
                  <p class="news-item__summary">{{ item.summary }}</p>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import PriceChart from '@/components/charts/PriceChart.vue';
import { 
  formatCurrency, 
  formatNumber, 
  formatPercent, 
  formatLargeNumber, 
  formatWithSign,
  formatDate
} from '@/utils/formatters';

export default {
  name: 'TickerView',
  components: {
    PriceChart
  },
  
  props: {
    symbol: {
      type: String,
      required: true
    }
  },
  
  setup(props) {
    const store = useStore();
    const chartLoading = ref(false);
    
    // Get state from store
    const tickerInfo = computed(() => store.getters['ticker/tickerInfo']);
    const historyData = computed(() => store.getters['ticker/historyData']);
    const latestPrice = computed(() => store.getters['ticker/latestPrice']);
    const priceChange = computed(() => store.getters['ticker/priceChange']);
    const news = computed(() => store.getters['ticker/news']);
    const loading = computed(() => store.getters.isLoading);
    const hasError = computed(() => store.getters.hasError);
    const errorMessage = computed(() => store.getters.errorMessage);
    const companyName = computed(() => store.getters['ticker/companyName']);
    
    // Check if ticker is in favorites
    const isFavorite = computed(() => {
      return store.getters.favoriteTickers.includes(props.symbol);
    });
    
    // Computed class for price change
    const priceChangeClass = computed(() => {
      if (!priceChange.value) return '';
      return priceChange.value.value >= 0 ? 'positive' : 'negative';
    });
    
    // Methods
    const loadTickerData = () => {
      store.dispatch('ticker/setTicker', props.symbol);
      store.dispatch('ticker/loadTickerDashboard');
    };
    
    // Create a debounced version of the history data fetching
    let fetchHistoryTimeout = null;
    
    // Keep track of the last requested period to avoid duplicates
    const lastRequestedPeriod = ref(null);
    
    const updateChartPeriod = (period) => {
      console.log('Period change requested:', period);
      
      // Cancel any pending requests
      if (fetchHistoryTimeout) {
        clearTimeout(fetchHistoryTimeout);
      }
      
      // Set loading state
      chartLoading.value = true;
      
      // Convert period to comparable string for duplicate checking
      const periodString = JSON.stringify(period);
      
      // Debounce the request to prevent multiple calls
      fetchHistoryTimeout = setTimeout(() => {
        try {
          // Check if this is a duplicate request
          if (lastRequestedPeriod.value === periodString) {
            console.log('Duplicate period request detected, skipping:', period);
            chartLoading.value = false;
            fetchHistoryTimeout = null;
            return;
          }
          
          // Save this request as the last one we made
          lastRequestedPeriod.value = periodString;
          
          // Dispatch the action to fetch data
          console.log('Fetching history data for period:', period);
          store.dispatch('ticker/fetchHistoryData', period)
            .then(() => {
              console.log('History data fetched successfully, data points:', 
                store.getters['ticker/historyData']?.length || 0);
            })
            .catch(error => {
              console.error('History data fetch error:', error);
            })
            .finally(() => {
              chartLoading.value = false;
              fetchHistoryTimeout = null;
            });
        } catch (error) {
          console.error('Error in updateChartPeriod:', error);
          chartLoading.value = false;
          fetchHistoryTimeout = null;
        }
      }, 300); // 300ms debounce delay
    };
    
    const toggleFavorite = () => {
      store.dispatch('toggleFavoriteTicker', props.symbol);
    };
    
    // Watch for symbol changes (e.g., from route)
    watch(() => props.symbol, (newSymbol, oldSymbol) => {
      // Only reload if the symbol has actually changed
      if (newSymbol && newSymbol !== oldSymbol) {
        loadTickerData();
      }
    });
    
    // Lifecycle
    onMounted(() => {
      loadTickerData();
    });
    
    return {
      tickerInfo,
      historyData,
      latestPrice,
      priceChange,
      news,
      loading,
      hasError,
      errorMessage,
      companyName,
      isFavorite,
      priceChangeClass,
      chartLoading,
      updateChartPeriod,
      toggleFavorite,
      // Utility formatters
      formatCurrency,
      formatNumber,
      formatPercent,
      formatLargeNumber,
      formatWithSign,
      formatDate
    };
  }
};
</script>

<style lang="scss" scoped>
.ticker-view {
  min-height: 100vh;
}

// Ticker Header
.ticker-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: $spacing-lg;
  
  @media (max-width: $breakpoint-sm) {
    flex-direction: column;
  }
  
  &__left {
    display: flex;
    flex-direction: column;
  }
  
  &__symbol {
    font-size: $font-size-xl;
    font-weight: 700;
    color: $primary-color;
    display: flex;
    align-items: center;
  }
  
  &__favorite-btn {
    background: none;
    border: none;
    cursor: pointer;
    margin-left: $spacing-sm;
    padding: $spacing-xs;
    color: $text-disabled;
    transition: $transition-quick;
    
    &:hover {
      color: #FFD700;
    }
    
    &.is-favorite {
      color: #FFD700;
    }
  }
  
  &__name {
    font-size: $font-size-xxl;
    font-weight: 600;
    margin: 0;
    color: $text-primary;
  }
  
  &__right {
    text-align: right;
    
    @media (max-width: $breakpoint-sm) {
      margin-top: $spacing-md;
      text-align: left;
    }
  }
  
  &__price {
    font-size: 2rem;
    font-weight: 700;
    color: $text-primary;
  }
  
  &__change {
    font-size: $font-size-md;
    font-weight: 600;
    
    &.positive {
      color: $positive;
    }
    
    &.negative {
      color: $negative;
    }
  }
}

// Ticker Navigation
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

// Main Content
.ticker-content {
  margin-bottom: $spacing-xl;
}

// Info Grid
.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-md;
  margin-bottom: $spacing-lg;
  
  @media (max-width: $breakpoint-lg) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (max-width: $breakpoint-sm) {
    grid-template-columns: 1fr;
  }
}

// Info Card
.info-card {
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  overflow: hidden;
  
  &.full-width {
    grid-column: 1 / -1;
  }
  
  &__title {
    font-size: $font-size-lg;
    font-weight: 600;
    margin: 0;
    padding: $spacing-md;
    background-color: rgba($bg-secondary, 0.5);
    color: $secondary-color;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  &__content {
    padding: $spacing-md;
    color: $text-secondary;
    
    p {
      line-height: 1.6;
      margin: 0;
    }
  }
  
  .data-table {
    width: 100%;
    
    td {
      padding: $spacing-xs $spacing-sm;
      border-bottom: 1px solid rgba($text-disabled, 0.2);
    }
    
    td:first-child {
      font-weight: 500;
      color: $text-primary;
    }
    
    tr:last-child td {
      border-bottom: none;
    }
  }
}

// News Grid
.news-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-md;
  
  @media (max-width: $breakpoint-lg) {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (max-width: $breakpoint-sm) {
    grid-template-columns: 1fr;
  }
}

.news-item {
  border-radius: $border-radius;
  overflow: hidden;
  transition: $transition-default;
  background-color: $bg-primary;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  
  &:hover {
    transform: translateY(-3px);
    box-shadow: $box-shadow;
  }
  
  &__link {
    display: block;
    padding: $spacing-md;
    color: inherit;
    text-decoration: none;
  }
  
  &__meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: $spacing-sm;
    font-size: $font-size-xs;
  }
  
  &__source {
    font-weight: 600;
    color: $primary-color;
  }
  
  &__date {
    color: $text-disabled;
  }
  
  &__title {
    font-size: $font-size-md;
    font-weight: 600;
    margin: 0 0 $spacing-sm;
    color: $text-primary;
    line-height: 1.4;
  }
  
  &__summary {
    font-size: $font-size-sm;
    color: $text-secondary;
    margin: 0;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.view-all-link {
  font-size: $font-size-sm;
  color: $primary-color;
  text-decoration: none;
  font-weight: normal;
  
  &:hover {
    text-decoration: underline;
  }
}
</style>