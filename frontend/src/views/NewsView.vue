<template>
  <div class="news-view">
    <div class="app-container">
      <!-- Ticker Header -->
      <section class="ticker-header">
        <div class="ticker-header__left">
          <div class="ticker-header__symbol">{{ symbol }}</div>
          <h1 class="ticker-header__name">{{ companyName }} News</h1>
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
        >
          Options
        </router-link>
        <router-link 
          :to="{ name: 'news', params: { symbol } }" 
          class="ticker-nav__link"
          exact-active-class="active"
        >
          News
        </router-link>
      </div>
      
      <!-- Loading Indicator -->
      <div class="loading-container" v-if="loading">
        <div class="loader"></div>
        <p>Loading news for {{ symbol }}...</p>
      </div>
      
      <!-- Error Message -->
      <div class="error-message" v-if="hasError">
        <i class="pi pi-exclamation-triangle"></i>
        <p>{{ errorMessage }}</p>
      </div>
      
      <!-- News Content -->
      <div class="news-content" v-if="!loading && !hasError">
        <!-- Filter Bar (Optional) -->
        <div class="news-filter">
          <div class="news-filter__search">
            <span class="p-input-icon-left">
              <i class="pi pi-search"></i>
              <input 
                type="text" 
                v-model="searchTerm" 
                placeholder="Search news..." 
                class="p-inputtext"
              />
            </span>
          </div>
          
          <div class="news-filter__sort">
            <label for="sort-by">Sort by:</label>
            <select 
              id="sort-by" 
              v-model="sortOption"
              class="sort-select"
            >
              <option value="newest">Newest First</option>
              <option value="oldest">Oldest First</option>
            </select>
          </div>
        </div>
        
        <!-- News List -->
        <div class="news-list" v-if="filteredNews.length > 0">
          <div 
            v-for="(item, index) in filteredNews" 
            :key="index"
            class="news-card"
          >
            <div class="news-card__content">
              <div class="news-card__meta">
                <span class="news-card__publisher">{{ item.publisher }}</span>
                <span class="news-card__date">{{ formatDate(item.providerPublishTime * 1000) }}</span>
              </div>
              
              <h3 class="news-card__title">
                <a :href="item.link" target="_blank" rel="noopener">
                  {{ item.title }}
                </a>
              </h3>
              
              <p class="news-card__summary">{{ item.summary }}</p>
              
              <div class="news-card__footer">
                <a :href="item.link" target="_blank" rel="noopener" class="news-card__link">
                  Read Full Article
                  <i class="pi pi-external-link"></i>
                </a>
              </div>
            </div>
            
            <div class="news-card__thumbnail" v-if="item.thumbnail">
              <img :src="item.thumbnail.resolutions[0].url" :alt="item.title">
            </div>
          </div>
        </div>
        
        <!-- No News Message -->
        <div class="no-news-message" v-else>
          <i class="pi pi-info-circle"></i>
          <p v-if="searchTerm">No news matching "{{ searchTerm }}" found for {{ symbol }}</p>
          <p v-else>No news available for {{ symbol }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { formatDate } from '@/utils/formatters';

export default {
  name: 'NewsView',
  
  props: {
    symbol: {
      type: String,
      required: true
    }
  },
  
  setup(props) {
    const store = useStore();
    const searchTerm = ref('');
    const sortOption = ref('newest');
    
    // Get state from store
    const companyName = computed(() => store.getters['ticker/companyName']);
    const news = computed(() => store.getters['ticker/news'] || []);
    const loading = computed(() => store.getters.isLoading);
    const hasError = computed(() => store.getters.hasError);
    const errorMessage = computed(() => store.getters.errorMessage);
    
    // Filter and sort news
    const filteredNews = computed(() => {
      let result = [...news.value];
      
      // Filter by search term if provided
      if (searchTerm.value) {
        const term = searchTerm.value.toLowerCase();
        result = result.filter(item => 
          item.title?.toLowerCase().includes(term) || 
          item.summary?.toLowerCase().includes(term) ||
          item.publisher?.toLowerCase().includes(term)
        );
      }
      
      // Sort news articles
      if (sortOption.value === 'newest') {
        result.sort((a, b) => b.providerPublishTime - a.providerPublishTime);
      } else if (sortOption.value === 'oldest') {
        result.sort((a, b) => a.providerPublishTime - b.providerPublishTime);
      }
      
      return result;
    });
    
    // Methods
    const loadNewsData = () => {
      // Set the ticker first
      store.dispatch('ticker/setTicker', props.symbol);
      
      // Load news data
      store.dispatch('ticker/fetchNews');
    };
    
    // Lifecycle hooks
    onMounted(() => {
      loadNewsData();
    });
    
    // Watch for changes in the symbol prop
    watch(() => props.symbol, (newSymbol) => {
      if (newSymbol) {
        // Reset search term when symbol changes
        searchTerm.value = '';
        
        // Load news for the new symbol
        loadNewsData();
      }
    });
    
    return {
      companyName,
      news,
      loading,
      hasError,
      errorMessage,
      searchTerm,
      sortOption,
      filteredNews,
      formatDate
    };
  }
};
</script>

<style lang="scss" scoped>
.news-view {
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

.no-news-message {
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

// News Filter
.news-filter {
  display: flex;
  justify-content: space-between;
  margin-bottom: $spacing-lg;
  
  @media (max-width: $breakpoint-sm) {
    flex-direction: column;
    gap: $spacing-md;
  }
  
  &__search {
    flex: 1;
    max-width: 400px;
    
    @media (max-width: $breakpoint-sm) {
      max-width: 100%;
    }
    
    .p-inputtext {
      width: 100%;
    }
  }
  
  &__sort {
    display: flex;
    align-items: center;
    
    label {
      margin-right: $spacing-sm;
      color: $text-secondary;
    }
  }
  
  .sort-select {
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
}

// News List
.news-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.news-card {
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  overflow: hidden;
  transition: $transition-default;
  display: flex;
  
  @media (max-width: $breakpoint-sm) {
    flex-direction: column;
  }
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: $box-shadow-hover;
  }
  
  &__content {
    flex: 1;
    padding: $spacing-lg;
  }
  
  &__meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: $spacing-sm;
    flex-wrap: wrap;
  }
  
  &__publisher {
    font-weight: 600;
    color: $primary-color;
    font-size: $font-size-sm;
  }
  
  &__date {
    color: $text-disabled;
    font-size: $font-size-sm;
  }
  
  &__title {
    font-size: $font-size-lg;
    font-weight: 600;
    margin: 0 0 $spacing-md;
    line-height: 1.4;
    
    a {
      color: $text-primary;
      text-decoration: none;
      transition: $transition-quick;
      
      &:hover {
        color: $primary-color;
      }
    }
  }
  
  &__summary {
    color: $text-secondary;
    line-height: 1.6;
    margin: 0 0 $spacing-lg;
  }
  
  &__footer {
    display: flex;
    justify-content: flex-end;
  }
  
  &__link {
    color: $primary-color;
    text-decoration: none;
    font-weight: 500;
    display: flex;
    align-items: center;
    
    i {
      margin-left: $spacing-xs;
    }
    
    &:hover {
      text-decoration: underline;
    }
  }
  
  &__thumbnail {
    width: 200px;
    flex-shrink: 0;
    background-color: $bg-secondary;
    
    @media (max-width: $breakpoint-sm) {
      width: 100%;
      height: 200px;
    }
    
    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
  }
}
</style>