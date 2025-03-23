<template>
  <header class="app-header">
    <div class="app-header__container">
      <!-- Logo and App Name -->
      <router-link to="/" class="app-header__logo">
        <div class="app-header__logo-icon">
          <img src="@/assets/icons/bitmap-transparent.png" alt="UStock Logo" class="logo-image">
        </div>
        <h1 class="app-header__title">StockTic</h1>
      </router-link>

      <!-- Search Bar -->
      <div class="app-header__search">
        <span class="p-input-icon-left">
          <i class="pi pi-search"></i>
          <input 
            type="text" 
            v-model="searchQuery" 
            @keyup.enter="searchTicker"
            :placeholder="$t('ticker.search')" 
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

      <!-- Navigation and Theme Toggle -->
      <div class="app-header__actions">
        <!-- Navigation Menu -->
        <nav class="app-header__nav">
          <router-link 
            to="/finance" 
            class="app-header__nav-link"
            :class="{ 'app-header__nav-link--active': isFinanceActive }"
          >
            <i class="pi pi-wallet"></i>
            <span>{{ $t('navigation.personalFinance') }}</span>
          </router-link>
        </nav>

        <!-- Language Switcher -->
        <language-switcher class="language-switcher" />
        
        <!-- Theme Toggle -->
        <button 
          class="p-button p-button-text p-button-rounded"
          @click="toggleTheme"
        >
          <i :class="isDarkTheme ? 'pi pi-sun' : 'pi pi-moon'"></i>
        </button>

        <!-- User Menu with Authentication -->
        <div class="user-menu" v-if="isAuthenticated">
          <div class="user-menu__avatar" @click="toggleDropdown">
            <i class="pi pi-user"></i>
            <span>{{ username }}</span>
            <i class="pi pi-chevron-down" style="margin-left: 5px; font-size: 0.8rem;"></i>
          </div>
          <div class="user-menu__dropdown" :class="{ 'user-menu__dropdown--active': isDropdownOpen }">
            <button class="user-menu__item" @click="logout">
              <i class="pi pi-sign-out"></i>
              <span>{{ $t('auth.logout') }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useStore } from 'vuex';
import LanguageSwitcher from '@/components/common/LanguageSwitcher.vue';

export default {
  name: 'AppHeader',
  components: {
    LanguageSwitcher
  },
  
  setup() {
    const router = useRouter();
    const route = useRoute();
    const store = useStore();
    const searchQuery = ref('');
    const isDropdownOpen = ref(false);
    
    // Check if current route is under the finance section
    const isFinanceActive = computed(() => 
      route.path.startsWith('/finance')
    );
    
    const isDarkTheme = computed(() => store.getters.isDarkTheme);
    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated']);
    const user = computed(() => store.getters['auth/user']);
    const username = computed(() => user.value?.username || '');
    
    // Handle ticker search
    const searchTicker = () => {
      if (!searchQuery.value) return;
      
      // Normalize the ticker symbol (uppercase, trim whitespace)
      const ticker = searchQuery.value.trim().toUpperCase();
      
      // Navigate to the ticker page
      router.push({ name: 'ticker', params: { symbol: ticker } });
      
      // Clear the search query
      searchQuery.value = '';
    };
    
    // Toggle theme between light and dark
    const toggleTheme = () => {
      const newTheme = isDarkTheme.value ? 'light' : 'dark';
      store.dispatch('setTheme', newTheme);
    };
    
    // Toggle dropdown menu
    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value;
    };
    
    // Close dropdown when clicking outside
    const closeDropdown = (event) => {
      if (isDropdownOpen.value) {
        const userMenu = document.querySelector('.user-menu');
        if (userMenu && !userMenu.contains(event.target)) {
          isDropdownOpen.value = false;
        }
      }
    };
    
    // Logout with a slight delay to ensure the click event completes
    const logout = () => {
      // Close dropdown first
      isDropdownOpen.value = false;
      
      // Delay logout to ensure UI interactions complete
      setTimeout(() => {
        store.dispatch('auth/logout');
      }, 100);
    };
    
    // Add/remove global click handler
    onMounted(() => {
      document.addEventListener('click', closeDropdown);
    });
    
    onUnmounted(() => {
      document.removeEventListener('click', closeDropdown);
    });
    
    return {
      searchQuery,
      searchTicker,
      isDarkTheme,
      toggleTheme,
      isAuthenticated,
      username,
      isDropdownOpen,
      toggleDropdown,
      logout,
      isFinanceActive
    };
  }
};
</script>

<style lang="scss" scoped>
.app-header {
  background-color: $bg-primary;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 10;
  border-bottom: 3px solid $primary-color;
  
  &__container {
    max-width: 1440px;
    margin: 0 auto;
    padding: $spacing-md;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  
  &__logo {
    display: flex;
    align-items: center;
    text-decoration: none;
    color: $primary-color;
    
    &-icon {
      display: flex;
      align-items: center;
      margin-right: $spacing-sm;
      
      .logo-image {
        height: 40px;
        width: auto;
      }
    }
  }
  
  &__title {
    font-size: $font-size-lg;
    font-weight: 700;
    margin: 0;
  }
  
  &__search {
    flex: 1;
    max-width: 500px;
    margin: 0 $spacing-lg;
    display: flex;
    
    .p-inputtext {
      flex: 1;
      margin-right: $spacing-sm;
    }
  }
  
  &__actions {
    display: flex;
    align-items: center;
    
    .p-button {
      margin-left: $spacing-sm;
    }
    
    .language-switcher {
      margin-right: $spacing-sm;
      margin-left: $spacing-sm;
    }
  }
  
  &__nav {
    display: flex;
    align-items: center;
    margin-right: $spacing-md;
    
    &-link {
      display: flex;
      align-items: center;
      padding: $spacing-sm $spacing-md;
      border-radius: $border-radius;
      text-decoration: none;
      color: $text-primary;
      transition: $transition-quick;
      font-weight: 500;
      background-color: $bg-secondary;
      
      i {
        margin-right: $spacing-xs;
        color: $primary-color;
      }
      
      &:hover {
        background-color: rgba($primary-color, 0.1);
      }
      
      &--active {
        background-color: rgba($primary-color, 0.1);
        font-weight: 600;
        
        i, span {
          color: $primary-color;
        }
      }
    }
  }
}

.user-menu {
  position: relative;
  margin-left: $spacing-md;
  
  &__avatar {
    display: flex;
    align-items: center;
    cursor: pointer;
    padding: $spacing-xs $spacing-md;
    border-radius: $border-radius;
    transition: $transition-quick;
    background-color: $bg-secondary;
    
    &:hover {
      background-color: rgba($primary-color, 0.1);
    }
    
    i {
      font-size: $font-size-md;
      color: $primary-color;
      margin-right: $spacing-xs;
    }
    
    span {
      font-weight: 500;
      color: $text-primary;
      margin-right: $spacing-xs;
    }
  }
  
  &__dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    background-color: $bg-primary;
    border-radius: $border-radius;
    box-shadow: $box-shadow;
    min-width: 180px;
    z-index: 100;
    overflow: hidden;
    opacity: 0;
    transform: translateY(10px);
    pointer-events: none;
    transition: $transition-quick;
    margin-top: 5px;
    
    &--active {
      opacity: 1;
      transform: translateY(0);
      pointer-events: auto;
    }
  }
  
  &__item {
    display: flex;
    align-items: center;
    width: 100%;
    padding: $spacing-md;
    border: none;
    background: none;
    text-align: left;
    cursor: pointer;
    transition: $transition-quick;
    
    i {
      margin-right: $spacing-sm;
      color: $text-secondary;
    }
    
    &:hover {
      background-color: rgba($primary-color, 0.05);
      
      i, span {
        color: $primary-color;
      }
    }
  }
}

// Responsive adjustments
@media (max-width: $breakpoint-md) {
  .app-header {
    &__container {
      flex-wrap: wrap;
    }
    
    &__search {
      order: 3;
      margin: $spacing-md 0 0;
      max-width: 100%;
      width: 100%;
    }
  }
}
</style>