<template>
  <div class="ticker-view">
    <div class="app-container">

      <section class="ticker-header mb-6">
        <div v-if="tickerInfo || (!isLoading && routeSymbol)" class="ticker-header__left">
          <div class="ticker-header__symbol">{{ routeSymbol }}</div>
          <h1 class="ticker-header__name">{{ tickerInfo?.data?.shortName || routeSymbol }}</h1>
          <p class="ticker-header__meta" v-if="tickerInfo?.data">
              {{ tickerInfo.data.exchangeName }} | {{ tickerInfo.data.sector || $t('ticker.sector') }} | {{ tickerInfo.data.industry || $t('ticker.industry') }}
          </p>
           <p class="ticker-header__meta" v-else>&nbsp;</p>
        </div>
      </section>

      <div class="ticker-nav">
        <router-link
           v-for="navItem in tickerNavigation" :key="navItem.name"
           :to="{ name: navItem.routeName, params: { symbol: routeSymbol } }"
           class="ticker-nav__link"
           exact-active-class="active">
           {{ $t(navItem.label) }}
         </router-link>
      </div>

      <div class="loading-container" v-if="isLoading">
        <ProgressSpinner style="width: 50px; height: 50px" strokeWidth="4" animationDuration=".8s"/>
        <p>{{ $t('common.loading') }}</p>
      </div>

      <div class="error-container" v-else-if="error">
         <Message severity="error" :closable="false">{{ error }}</Message>
         <div class="text-center mt-4">
            <Button @click="retryLoad" :label="$t('common.tryAgain')" icon="pi pi-refresh" />
         </div>
       </div>

       <div class="ticker-content" v-else-if="tickerInfo">

          <div class="key-metrics-block card-like" v-if="tickerInfo.data">
             <div v-if="latestPrice !== null">
               <strong>{{ $t('ticker.price') }}:</strong> {{ formatCurrency(latestPrice, tickerInfo.data?.currency) }}
             </div>
             <div v-if="priceChangeValue !== null">
               <strong>{{ $t('ticker.change') }}:</strong>
               <span :class="priceChangeValue >= 0 ? 'positive' : 'negative'">
                 {{ formatCurrency(priceChangeValue, tickerInfo.data?.currency, 2) }}
                 ({{ formatPercentage(priceChangePercent, 2) }})
               </span>
             </div>
             <div><strong>{{ $t('ticker.marketCap') }}:</strong> {{ formatLargeNumber(tickerInfo.data?.marketCap, 2) }} {{ tickerInfo.data?.currency }}</div>
             <div><strong>{{ $t('ticker.peRatio') }}:</strong> {{ tickerInfo.data?.trailingPE ? tickerInfo.data.trailingPE.toFixed(2) : 'N/A' }}</div>
             <div><strong>{{ $t('ticker.volume') }}:</strong> {{ formatLargeNumber(tickerInfo.data?.volume) }}</div>
             <div><strong>{{ $t('ticker.dividendYield') }}:</strong> {{ tickerInfo.data?.dividendYield ? formatPercentage(tickerInfo.data.dividendYield * 100, 2) : 'N/A' }}</div>
          </div>
          <div v-else class="no-data-message card-like">
            <i class="pi pi-info-circle"></i>
            <p>Detailed data not available for {{ routeSymbol }}.</p>
          </div>


          <div class="chart-section mb-6">
            <h2 class="section-title">Chart</h2>
            <TradingViewWidget
              :symbol="tickerSymbolForTradingView"
              widgetHeight="600px"
              v-if="tickerSymbolForTradingView" />
          </div>

          <Card class="about-section mb-6" v-if="tickerInfo.data">
            <template #title>
              <h2 class="section-title-in-card">{{ $t('ticker.about', { companyName: tickerInfo.data?.shortName || routeSymbol }) }}</h2>
            </template>
            <template #content>
              <p class="about-text">{{ tickerInfo.data?.longBusinessSummary || $t('common.noData') }}</p>
              <div v-if="tickerInfo.data?.website" class="mt-4">
                <a :href="tickerInfo.data.website" target="_blank" rel="noopener noreferrer" class="p-button p-button-link px-0 text-sm">
                  {{ $t('ticker.visitWebsite') }} <i class="pi pi-external-link ml-1"></i>
                </a>
              </div>
            </template>
          </Card>

          <Card class="news-section mb-6" v-if="news && news.length > 0">
            <template #title>
              <div class="flex justify-between items-center">
                <h2 class="section-title-in-card mb-0">{{ $t('ticker.recentNews') }}</h2>
                <router-link :to="{ name: 'news', params: { symbol: routeSymbol } }" class="view-all-link p-button p-button-text p-button-sm">
                  {{ $t('ticker.viewAll') }}
                </router-link>
              </div>
            </template>
            <template #content>
              <ul class="news-list">
                <li v-for="(item, index) in news.slice(0, 5)" :key="item.uuid || index">
                  <a :href="item.link" target="_blank" rel="noopener noreferrer">{{ item.title }}</a>
                  <p class="news-meta">{{ item.publisher }} - {{ formatDate(item.providerPublishTime * 1000, { dateStyle: 'medium', timeStyle: 'short' }) }}</p>
                </li>
              </ul>
            </template>
          </Card>

      </div>

      <div class="no-data-message" v-else>
        <i class="pi pi-info-circle"></i>
        <p>{{ $t('common.noData') }}</p>
      </div>

    </div>
  </div>
</template>

<script setup>
// --- Компоненты PrimeVue ---
import Button from 'primevue/button';
import Message from 'primevue/message';
import ProgressSpinner from 'primevue/progressspinner';
import Card from 'primevue/card'; // <-- Добавили импорт Card

// --- Остальные импорты ---
import { computed, onMounted, watch } from 'vue';
import { useRoute, onBeforeRouteUpdate } from 'vue-router';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';
import TradingViewWidget from '@/components/TradingViewWidget.vue';
import { formatCurrency, formatPercentage, formatLargeNumber, formatDate } from '@/utils/formatters';

const route = useRoute();
const store = useStore();
useI18n(); // Using for translations in template with $t

// --- Состояние из Vuex ---
const tickerInfo = computed(() => store.getters['ticker/tickerInfo']);
const news = computed(() => store.getters['ticker/news']);
const isLoading = computed(() => store.getters.isLoading);
const error = computed(() => store.state.error);

// --- Локальное состояние и вычисляемые свойства ---
const routeSymbol = computed(() => {
  return route.params.symbol ? String(route.params.symbol).toUpperCase() : null;
});

// Навигация
const tickerNavigation = [
  { name: 'Overview', routeName: 'ticker', label: 'ticker.navigation.overview' },
  { name: 'Financials', routeName: 'financials', label: 'ticker.navigation.financials' },
  { name: 'Options', routeName: 'options', label: 'ticker.navigation.options' },
  { name: 'News', routeName: 'news', label: 'ticker.navigation.news' },
];

// Вычисляемые свойства для цены и т.д.
const latestPrice = computed(() => {
  if (!tickerInfo.value || !tickerInfo.value.data) return null;
  return tickerInfo.value.data.regularMarketPrice || tickerInfo.value.data.currentPrice || null;
});

const priceChangeValue = computed(() => {
  if (!tickerInfo.value || !tickerInfo.value.data) return null;
  return tickerInfo.value.data.regularMarketChange || 0;
});

const priceChangePercent = computed(() => {
  if (!tickerInfo.value || !tickerInfo.value.data) return null;
  return tickerInfo.value.data.regularMarketChangePercent || 0;
});
const tickerSymbolForTradingView = computed(() => {
  // --- !!! ДОБАВЛЕНО ЛОГИРОВАНИЕ !!! ---
  const symbolValue = routeSymbol.value;
  if (!symbolValue) return null;

  const exchange = tickerInfo.value?.data?.exchange;
  let prefix = '';
  if (exchange) {
    const upperExchange = exchange.toUpperCase();
    if (['NMS', 'NASDAQ', 'NAS', 'NASDAQGS'].includes(upperExchange)) { prefix = 'NASDAQ'; }
    else if (['NYQ', 'NYSE'].includes(upperExchange)) { prefix = 'NYSE'; }
    else if (['PCX', 'ARCX', 'AMEX'].includes(upperExchange)) { prefix = 'AMEX'; }
    else if (upperExchange === 'LSE') { prefix = 'LSE'; }
    else if (upperExchange === 'TSX') { prefix = 'TSX'; }
    else if (upperExchange === 'FWB' || upperExchange === 'F') { prefix = 'FWB'; }
    else if (upperExchange === 'XETRA' || upperExchange === 'ETR') { prefix = 'XETRA'; }
    // ... другие биржи
  }
  const finalSymbol = prefix ? `${prefix}:${symbolValue}` : symbolValue;
  console.log('Symbol for TradingView:', finalSymbol); // <-- Вывод в консоль
  return finalSymbol;
});

// --- Методы ---
const loadData = () => {
  if (!routeSymbol.value) return;

  // Clear any previous errors
  store.dispatch('clearError');

  // Set the current ticker and load basic info
  store.dispatch('ticker/setTicker', routeSymbol.value)
    .then(() => {
      // Load additional data
      return Promise.all([
        store.dispatch('ticker/fetchNews'),
        store.dispatch('ticker/fetchHistoryData')
      ]);
    })
    .catch(error => {
      console.error('Error loading ticker data:', error);
    });
};

const retryLoad = () => { loadData(); };

// --- Хуки жизненного цикла ---
onMounted(() => { loadData(); });

// Watch for symbol changes
watch(() => route.params.symbol, (newSymbol, oldSymbol) => {
  if (newSymbol && newSymbol !== oldSymbol) { loadData(); }
});

// Add a navigation guard to reload data when navigating back to this component
onBeforeRouteUpdate((to, from) => {
  // If we're navigating to the ticker view from another tab (same symbol)
  if (to.name === 'ticker' && from.params.symbol === to.params.symbol) {
    console.log('Navigating back to ticker view, reloading data...');
    loadData();
  }
});

</script>

<style lang="scss" scoped>
@import '@/assets/styles/variables.scss';

.ticker-view {
  color: var(--text-color, $text-primary);
}

/* --- Header --- */
.ticker-header {
  margin-bottom: $spacing-lg;
  &__symbol {
    font-size: $font-size-xl;
    font-weight: 700;
    color: var(--primary-color, $primary-color);
    margin-bottom: $spacing-xs;
  }
  &__name {
    font-size: $font-size-xxl;
    font-weight: 600;
    margin: 0;
    color: var(--text-color, $text-primary);
    line-height: 1.3;
  }
   &__meta {
       font-size: 0.9rem;
       color: var(--text-color-secondary, $text-secondary);
       margin-top: $spacing-sm;
   }
}

/* --- Navigation --- */
.ticker-nav {
  display: flex;
  margin-bottom: $spacing-xl;
  border-bottom: 1px solid var(--surface-border, rgba($text-disabled, 0.3));

  &__link {
    padding: $spacing-md $spacing-lg;
    color: var(--text-color-secondary, $text-secondary);
    text-decoration: none;
    font-weight: 500;
    font-size: 0.95rem;
    position: relative;
    border-bottom: 3px solid transparent;
    transition: color $transition-quick;
    margin-bottom: -1px;

    &:hover { color: var(--primary-color, $primary-color); }
    &.active {
      color: var(--primary-color, $primary-color);
      font-weight: 600;
      border-bottom-color: var(--primary-color, $primary-color);
    }
  }
}

/* --- Key metrics block --- */
.key-metrics-block {
    &.card-like {
        background-color: var(--surface-card, $bg-primary);
        color: var(--text-color, $text-primary);
        border-radius: var(--border-radius, $border-radius);
        box-shadow: $box-shadow;
        border: 1px solid var(--surface-border, #dee2e6);
        padding: $spacing-lg;
        margin-bottom: $spacing-xl;
    }
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: $spacing-md $spacing-lg;
    font-size: 0.9rem;

    div {
        strong {
            display: block;
            color: var(--text-color-secondary, $text-secondary);
            font-weight: 500;
            margin-bottom: $spacing-xs;
            font-size: 0.8rem;
        }
        span { font-weight: 500; color: var(--text-color, $text-primary); }
        .positive { color: var(--green-600, $positive); }
        .negative { color: var(--red-600, $negative); }
    }
}

/* --- Common styles for content sections --- */
.chart-section, .about-section, .news-section {
    margin-bottom: $spacing-xl; // Spacing between sections
}

/* Use this class inside p-card title slot or as a regular heading */
.section-title, .section-title-in-card {
    font-size: 1.3rem; // Reduced section heading size
    font-weight: 600;
    color: var(--text-color, $text-primary);
    margin: 0; // Remove default h2 margins
    padding: 0;
    border: none; // Remove border since Card has one
}
.section-title { // Add margins and border if used outside of card
     margin-bottom: $spacing-lg;
     padding-bottom: $spacing-sm;
     border-bottom: 1px solid var(--surface-border, rgba($text-disabled, 0.3));
}
.section-title-in-card {
    margin: $spacing-md $spacing-md $spacing-sm $spacing-md; // Add margins on all sides
    padding-bottom: $spacing-xs; // Add some padding at the bottom
    font-size: 1.25rem; // Slightly smaller than section-title for better hierarchy
}


/* Chart */
.chart-section {
  height: 600px;
  border-radius: $border-radius;
  overflow: hidden;
  position: relative; // For possible loading overlay
  background-color: var(--surface-card, #fff); // Add card background
  border: 1px solid var(--surface-border, #dee2e6); // Add card border
}

/* About company (inside p-card) */
.about-section { // Class for p-card
   // Add a subtle background to the card content
   :deep(.p-card-content) {
      background-color: var(--surface-ground, rgba($bg-secondary, 0.03));
      border-radius: 0 0 $border-radius $border-radius;
      padding: $spacing-md $spacing-lg;
   }

   .about-text {
      font-size: 0.95rem;
      line-height: 1.8;
      color: var(--text-color-secondary, $text-secondary);
      margin: 0 0 $spacing-lg 0; // Increased bottom margin for better spacing
      padding: $spacing-md;
      text-align: justify; // Better text readability for long paragraphs
      letter-spacing: 0.01em; // Slight letter spacing for readability
      background-color: var(--surface-section, rgba($bg-primary, 0.5));
      border-radius: $border-radius;
      border-left: 3px solid var(--primary-color-lighter, lighten($primary-color, 20%));

      // Add responsive font size
      @media (max-width: $breakpoint-sm) {
        font-size: 0.9rem;
        line-height: 1.7;
        padding: $spacing-sm;
      }

      // First paragraph styling
      &::first-letter {
        font-size: 1.2em;
        font-weight: 500;
        color: var(--primary-color, $primary-color);
      }
  }

   // Link is styled with p-button classes
   a.p-button-link {
      margin-top: $spacing-md;
      font-weight: 500;
      transition: $transition-quick;
      display: inline-flex;
      align-items: center;
      padding: $spacing-sm $spacing-md;
      background-color: rgba($primary-color, 0.05);
      border-radius: $border-radius;

      i {
        margin-left: $spacing-xs;
        transition: transform 0.2s ease;
      }

      &:hover {
        text-decoration: underline;
        background-color: rgba($primary-color, 0.1);

        i {
          transform: translateX(2px);
        }
      }
   }
}

/* News section (inside p-card) */
.news-section { // Class for p-card
   // Add a subtle background to the card content
   :deep(.p-card-content) {
      background-color: var(--surface-ground, rgba($bg-secondary, 0.03));
      border-radius: 0 0 $border-radius $border-radius;
      padding: $spacing-md;
   }

   .news-header { // For flex container in #title slot
      width: 100%;
   }

  .view-all-link { // "View all" link
        color: var(--primary-color, $primary-color);
        text-decoration: none;
        font-weight: 500;
        display: flex;
        align-items: center;
        padding: $spacing-xs $spacing-sm;
        border-radius: $border-radius;
        transition: background-color 0.2s ease, transform 0.2s ease;

        &:hover { 
          text-decoration: none;
          background-color: rgba($primary-color, 0.08);
        }

        &::after {
          content: '\2192'; // Right arrow
          margin-left: $spacing-xs;
          transition: transform 0.2s ease;
          font-size: 1.1em; // Slightly larger arrow
          line-height: 1;
        }

        &:hover::after {
          transform: translateX(3px);
        }
  }

  .news-list {
      list-style: none;
      padding: $spacing-md;
      margin: 0; // Remove list margins
      border-radius: $border-radius;
      background-color: var(--surface-card, $bg-primary);
  }

  li {
      padding: $spacing-md;
      margin-bottom: $spacing-md;
      border-bottom: 1px solid var(--surface-border, rgba($text-disabled, 0.2));
      transition: all 0.2s ease;
      border-radius: $border-radius;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);

      &:hover {
        background-color: var(--surface-hover, rgba($bg-secondary, 0.1));
        transform: translateY(-2px);
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.08);
      }

      &:last-child { 
        border-bottom: none; 
        margin-bottom: 0;
      }

      a {
          color: var(--primary-color, $primary-color);
          text-decoration: none;
          font-weight: 600;
          font-size: 1rem;
          display: block;
          margin-bottom: $spacing-sm;
          line-height: 1.4;
          position: relative;
          padding-left: $spacing-md;

          &::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0.5em;
            width: 4px;
            height: 4px;
            background-color: var(--primary-color, $primary-color);
            border-radius: 50%;
          }

          &:hover { 
            text-decoration: underline;
          }
      }

      .news-meta {
          font-size: 0.8rem;
          color: var(--text-color-secondary, $text-secondary);
          display: flex;
          align-items: center;
          padding-left: $spacing-md;

          &::before {
            content: '\1F4F0'; // Newspaper emoji
            font-size: 0.9em;
            margin-right: $spacing-xs;
            opacity: 0.7;
          }
      }
  }
}

/* --- Loading, error, and no data states --- */
.loading-container, .error-container, .no-data-message {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: $spacing-xl;
  color: var(--text-color-secondary, $text-secondary);
}
.loading-container p { margin-top: $spacing-md; }
.error-container {
    .p-message { margin-bottom: $spacing-lg; }
}
.no-data-message {
  i { font-size: 3rem; margin-bottom: $spacing-md; opacity: 0.6; }
  p { font-size: $font-size-lg; }
}

</style>
