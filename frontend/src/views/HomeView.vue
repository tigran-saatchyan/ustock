<template>
  <div class="home-view">
    <div class="app-container">
      <!-- Hero Section -->
      <section class="hero">
        <div class="hero__content">
          <h1 class="hero__title" v-html="$t('home.title')"></h1>
          <p class="hero__subtitle">
            {{ $t('home.subtitle') }}
          </p>
          
          <div class="hero__search">
            <span class="p-input-icon-left">
              <i class="pi pi-search"></i>
              <input 
                type="text" 
                v-model="searchQuery" 
                @keyup.enter="searchTicker"
                :placeholder="$t('home.searchPlaceholder')" 
                class="p-inputtext" 
              />
            </span>
            <button 
              class="p-button p-button-primary" 
              @click="searchTicker"
            >
              <span class="p-button-label">{{ $t('common.search') }}</span>
            </button>
          </div>
          
          <!-- Popular Tickers -->
          <div class="hero__popular">
            <span class="hero__popular-label">{{ $t('home.popularTickers') }}:</span>
            <div class="hero__popular-tickers">
              <button 
                v-for="ticker in popularTickers" 
                :key="ticker"
                class="hero__popular-ticker"
                @click="goToTicker(ticker)"
              >
                {{ ticker }}
              </button>
            </div>
          </div>
        </div>
      </section>
      
      <!-- Features Section -->
      <section class="features">
        <h2 class="section-title">{{ $t('home.platformFeatures') }}</h2>
        
        <div class="features__grid">
          <div class="feature-card">
            <div class="feature-card__icon">
              <i class="pi pi-chart-line"></i>
            </div>
            <h3 class="feature-card__title">{{ $t('home.features.stockPrice.title') }}</h3>
            <p class="feature-card__description">
              {{ $t('home.features.stockPrice.description') }}
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-card__icon">
              <i class="pi pi-file-excel"></i>
            </div>
            <h3 class="feature-card__title">{{ $t('home.features.financialStatements.title') }}</h3>
            <p class="feature-card__description">
              {{ $t('home.features.financialStatements.description') }}
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-card__icon">
              <i class="pi pi-percentage"></i>
            </div>
            <h3 class="feature-card__title">{{ $t('home.features.optionsTrading.title') }}</h3>
            <p class="feature-card__description">
              {{ $t('home.features.optionsTrading.description') }}
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-card__icon">
              <i class="pi pi-megaphone"></i>
            </div>
            <h3 class="feature-card__title">{{ $t('home.features.newsIntegration.title') }}</h3>
            <p class="feature-card__description">
              {{ $t('home.features.newsIntegration.description') }}
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-card__icon">
              <i class="pi pi-chart-bar"></i>
            </div>
            <h3 class="feature-card__title">{{ $t('home.features.analystInsights.title') }}</h3>
            <p class="feature-card__description">
              {{ $t('home.features.analystInsights.description') }}
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-card__icon">
              <i class="pi pi-calendar"></i>
            </div>
            <h3 class="feature-card__title">{{ $t('home.features.eventCalendar.title') }}</h3>
            <p class="feature-card__description">
              {{ $t('home.features.eventCalendar.description') }}
            </p>
          </div>
          
          <div class="feature-card" @click="goToFinance">
            <div class="feature-card__icon">
              <i class="pi pi-wallet"></i>
            </div>
            <h3 class="feature-card__title">{{ $t('home.features.personalFinance.title') }}</h3>
            <p class="feature-card__description">
              {{ $t('home.features.personalFinance.description') }}
            </p>
            <button class="feature-card__button">{{ $t('home.getStarted') }}</button>
          </div>
        </div>
      </section>
      
      <!-- Recent Tickers Section -->
      <section class="recent-tickers" v-if="recentTickers.length > 0">
        <h2 class="section-title">{{ $t('home.recentSearches') }}</h2>
        
        <div class="recent-tickers__list">
          <transition-group name="ticker-list">
            <div 
              v-for="(ticker, index) in recentTickers" 
              :key="ticker"
              class="ticker-card"
              @click="goToTicker(ticker)"
              :style="{ animationDelay: index * 0.1 + 's' }"
              v-ripple
            >
              <div class="ticker-card__symbol">{{ ticker }}</div>
              <div class="ticker-card__action">
                <i class="pi pi-arrow-right"></i>
              </div>
            </div>
          </transition-group>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

export default {
  name: 'HomeView',
  
  setup() {
    const router = useRouter();
    const store = useStore();
    const searchQuery = ref('');
    
    // Popular tickers for quick access
    const popularTickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'];
    
    // Get recent tickers from store
    const recentTickers = computed(() => store.getters.recentTickers);
    
    // Initialize store data
    onMounted(() => {
      store.dispatch('init');
    });
    
    // Search for a ticker
    const searchTicker = () => {
      if (!searchQuery.value) return;
      
      const ticker = searchQuery.value.trim().toUpperCase();
      goToTicker(ticker);
      
      // Clear search query
      searchQuery.value = '';
    };
    
    // Navigate to ticker page
    const goToTicker = (ticker) => {
      router.push({ name: 'ticker', params: { symbol: ticker } });
    };
    
    // Navigate to personal finance
    const goToFinance = () => {
      router.push({ name: 'finance' });
    };
    
    return {
      searchQuery,
      popularTickers,
      recentTickers,
      searchTicker,
      goToTicker,
      goToFinance
    };
  }
};
</script>

<style lang="scss" scoped>
:deep(.title-highlight) {
  color: #f7941d;
  position: relative;
}
.home-view {
  min-height: 100vh;
}

.section-title {
  font-size: $font-size-xxl;
  font-weight: 700;
  margin-bottom: $spacing-xl;
  color: $primary-color;
  text-align: center;
}

// Hero Section
.hero {
  padding: $spacing-xl 0 $spacing-xxl;
  background: linear-gradient(135deg, $secondary-color, darken($secondary-color, 15%));
  background-image: linear-gradient(135deg, rgba($secondary-color, 0.97), rgba(darken($secondary-color, 15%), 0.97)), url('@/assets/icons/bitmap.png');
  background-size: cover;
  background-position: center;
  color: white;
  border-radius: 0 0 50px 50px;
  margin-bottom: $spacing-xl;
  display: flex;
  align-items: center;
  min-height: 70vh;
  
  &__content {
    max-width: 800px;
    margin: 0 auto;
    padding: 0 $spacing-md;
    text-align: center;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  
  &__title {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: $spacing-md;
    line-height: 1.2;
    
    &-highlight {
      color: $primary-light;
      position: relative;
      
      &::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 100%;
        height: 3px;
        background: $primary-light;
        border-radius: 2px;
      }
    }
  }
  
  &__subtitle {
    font-size: $font-size-xl;
    margin-bottom: $spacing-xl;
    opacity: 0.9;
    max-width: 80%;
  }
  
  &__search {
    display: flex;
    max-width: 600px;
    margin: $spacing-xl auto;
    position: relative;
    z-index: 5;
    
    .p-inputtext {
      flex: 1;
      height: 56px;
      font-size: $font-size-md;
      border-radius: $border-radius 0 0 $border-radius;
      border: none;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      padding-left: 50px;
    }
    
    .p-button {
      height: 56px;
      border-radius: 0 $border-radius $border-radius 0;
      font-weight: 600;
      padding: 0 $spacing-lg;
      min-width: 120px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .p-input-icon-left {
      width: 100%;
      
      i {
        left: $spacing-md;
        top: 50%;
        transform: translateY(-50%);
        font-size: $font-size-lg;
      }
    }
  }
  
  &__popular {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    margin-top: $spacing-md;
    
    &-label {
      margin-right: $spacing-sm;
      opacity: 0.7;
      font-weight: 500;
    }
    
    &-tickers {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
    }
    
    &-ticker {
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba($primary-light, 0.3);
      color: white;
      padding: $spacing-xs $spacing-md;
      margin: $spacing-xs;
      border-radius: $spacing-sm;
      cursor: pointer;
      transition: $transition-quick;
      font-weight: 500;
      
      &:hover {
        background: rgba($primary-light, 0.2);
        border-color: $primary-light;
        transform: translateY(-2px);
      }
    }
  }
}

// Features Section
.features {
  padding: $spacing-xl 0;
  
  &__grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: $spacing-lg;
  }
}

.feature-card {
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  padding: $spacing-lg;
  transition: $transition-default;
  border-top: 3px solid $primary-color;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: $box-shadow-hover;
  }
  
  &__icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, $primary-color, $primary-light);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: $spacing-md;
    
    i {
      font-size: 1.5rem;
      color: white;
    }
  }
  
  &__title {
    font-size: $font-size-lg;
    font-weight: 600;
    margin-bottom: $spacing-sm;
    color: $secondary-color;
  }
  
  &__description {
    color: $text-secondary;
    line-height: 1.5;
  }
  
  &__button {
    margin-top: $spacing-md;
    padding: $spacing-xs $spacing-md;
    background-color: $primary-color;
    color: white;
    border: none;
    border-radius: $border-radius;
    font-weight: 500;
    cursor: pointer;
    transition: $transition-quick;
    
    &:hover {
      background-color: $primary-dark;
    }
  }
}

// Recent Tickers Section
.recent-tickers {
  padding: $spacing-xl 0;
  
  &__list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: $spacing-md;
  }
}

.ticker-card {
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  padding: $spacing-md;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
  animation: fadeInUp 0.5s backwards;
  position: relative;
  overflow: hidden;
  border-left: 3px solid transparent;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to right, rgba($primary-color, 0.05), transparent);
    transform: translateX(-100%);
    transition: transform 0.5s ease;
  }
  
  &:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: $box-shadow-hover;
    border-left: 3px solid $primary-color;
    
    &::before {
      transform: translateX(0);
    }
  }
  
  &__symbol {
    font-size: $font-size-lg;
    font-weight: 600;
    color: $secondary-color;
  }
  
  &__action {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: rgba($primary-color, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    
    i {
      color: $primary-color;
      font-size: 0.8rem;
    }
  }
}

// Responsive Adjustments
@media (max-width: $breakpoint-md) {
  .hero {
    &__title {
      font-size: 2rem;
    }
    
    &__subtitle {
      font-size: $font-size-md;
    }
  }
}

// Ticker list transitions
.ticker-list-enter-active,
.ticker-list-leave-active {
  transition: all 0.5s ease;
}

.ticker-list-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.ticker-list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

// Ensure items are positioned relative to their natural position
.ticker-list-move {
  transition: transform 0.5s ease;
}

@media (max-width: $breakpoint-sm) {
  .hero {
    min-height: auto;
    padding: $spacing-xl 0;
    
    &__title {
      font-size: 2rem;
    }
    
    &__subtitle {
      font-size: $font-size-md;
      max-width: 100%;
    }
    
    &__search {
      flex-direction: column;
      margin: $spacing-md auto;
      
      .p-inputtext {
        border-radius: $border-radius $border-radius 0 0;
        height: 50px;
      }
      
      .p-button {
        border-radius: 0 0 $border-radius $border-radius;
        height: 50px;
        min-width: 100%;
      }
    }
  }
}
</style>