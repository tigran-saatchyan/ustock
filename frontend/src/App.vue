<template>
  <div 
    id="app" 
    :class="{ 'theme-dark': isDarkTheme }"
  >
    <app-header />
    
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <app-footer />
    
    <!-- Global Error Toast -->
    <div class="error-toast" v-if="hasError">
      <div class="error-toast__content">
        <i class="pi pi-exclamation-circle"></i>
        <span>{{ errorMessage }}</span>
      </div>
      <button class="error-toast__close" @click="clearError">
        <i class="pi pi-times"></i>
      </button>
    </div>
    
    <!-- Global Loading Overlay -->
    <div class="loading-overlay" v-if="isGlobalLoading">
      <div class="loader"></div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue';
import { useStore } from 'vuex';
import AppHeader from '@/components/common/AppHeader.vue';
import AppFooter from '@/components/common/AppFooter.vue';

export default {
  name: 'App',
  
  components: {
    AppHeader,
    AppFooter
  },
  
  setup() {
    const store = useStore();
    
    // Get loading and error state from store
    const isLoading = computed(() => store.getters.isLoading);
    const hasError = computed(() => store.getters.hasError);
    const errorMessage = computed(() => store.getters.errorMessage);
    const isDarkTheme = computed(() => store.getters.isDarkTheme);
    
    // Only show loading overlay for global operations
    const isGlobalLoading = computed(() => {
      return isLoading.value && !store.state.ticker.currentTicker;
    });
    
    // Clear error message
    const clearError = () => {
      store.dispatch('clearError');
    };
    
    // Initialize store data
    store.dispatch('init');
    
    return {
      isLoading,
      hasError,
      errorMessage,
      isDarkTheme,
      isGlobalLoading,
      clearError
    };
  }
};
</script>

<style lang="scss">
@import '@/assets/styles/global.scss';

// Theme Support
.theme-dark {
  --bg-primary: #{$bg-dark};
  --bg-secondary: #{darken($bg-dark, 3%)};
  --text-primary: #f5f5f5;
  --text-secondary: #bdbdbd;
  --text-disabled: #757575;
  --chart-grid: #424242;
  --primary-accent: #{$primary-light};
  
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  
  .app-header,
  .app-footer,
  .card,
  .info-card,
  .feature-card,
  .ticker-card,
  .metric-card,
  .news-card,
  .options-table-container,
  .financial-table th:first-child,
  .financial-table td:first-child,
  .date-select,
  .filter-select,
  .sort-select {
    background-color: var(--bg-primary);
  }
  
  .card__title,
  .info-card__title,
  .feature-card__title,
  .ticker-card__symbol,
  .statement-title,
  .news-card__title a,
  .ticker-header__name {
    color: var(--text-primary);
  }
  
  .card__content,
  .news-card__summary,
  .news-card__title a:hover {
    color: var(--text-secondary);
  }
  
  .date-select,
  .filter-select,
  .sort-select {
    color: var(--text-primary);
    border-color: #616161;
  }
  
  .view-button,
  .period-button,
  .statement-button {
    background-color: var(--bg-primary);
    color: var(--text-secondary);
    
    &:hover {
      background-color: rgba($primary-color, 0.2);
    }
  }
  
  .data-table th {
    background-color: rgba(#000, 0.2);
  }
  
  .data-table td,
  .data-table th {
    border-color: rgba(#fff, 0.1);
  }
  
  .ticker-nav {
    border-color: rgba(#fff, 0.1);
  }
  
  .in-the-money td:not(.strike-column) {
    background-color: rgba($primary-color, 0.3);
  }
}

// Global Styles
.main-content {
  min-height: calc(100vh - 200px);
}

// Error Toast
.error-toast {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background-color: $negative;
  color: white;
  padding: $spacing-md $spacing-lg;
  border-radius: $border-radius;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  display: flex;
  align-items: center;
  max-width: 90%;
  animation: slideUp 0.3s ease-out forwards;
  
  &__content {
    display: flex;
    align-items: center;
    
    i {
      margin-right: $spacing-md;
    }
  }
  
  &__close {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    margin-left: $spacing-lg;
    opacity: 0.8;
    transition: $transition-quick;
    
    &:hover {
      opacity: 1;
    }
  }
}

@keyframes slideUp {
  from {
    transform: translate(-50%, 100px);
    opacity: 0;
  }
  to {
    transform: translate(-50%, 0);
    opacity: 1;
  }
}

// Page transition animations
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

// Add more animations for components
.animated-item {
  animation: fadeInUp 0.5s ease-out forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// Loading Overlay
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  display: flex;
  justify-content: center;
  align-items: center;
  
  .loader {
    width: 50px;
    height: 50px;
    border-width: 5px;
  }
}
</style>