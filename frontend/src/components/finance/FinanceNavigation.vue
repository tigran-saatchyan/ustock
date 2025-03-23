<template>
  <div class="finance-navigation">
    <div class="finance-navigation__container">
      <h2 class="finance-navigation__title">{{ $t('navigation.personalFinance') }}</h2>
      
      <div class="finance-navigation__links">
        <router-link 
          to="/finance" 
          class="finance-navigation__link"
          exact-active-class="finance-navigation__link--active"
        >
          <i class="pi pi-chart-line"></i>
          <span>{{ $t('navigation.dashboard') }}</span>
        </router-link>
        
        <router-link 
          to="/finance/transactions" 
          class="finance-navigation__link"
          exact-active-class="finance-navigation__link--active"
        >
          <i class="pi pi-list"></i>
          <span>{{ $t('navigation.transactions') }}</span>
        </router-link>
        
        <router-link 
          to="/finance/accounts" 
          class="finance-navigation__link"
          exact-active-class="finance-navigation__link--active"
        >
          <i class="pi pi-wallet"></i>
          <span>{{ $t('navigation.accounts') }}</span>
        </router-link>
        
        <router-link 
          to="/finance/budgets" 
          class="finance-navigation__link"
          exact-active-class="finance-navigation__link--active"
        >
          <i class="pi pi-chart-pie"></i>
          <span>{{ $t('navigation.budgets') }}</span>
        </router-link>
        
        <router-link 
          to="/finance/goals" 
          class="finance-navigation__link"
          exact-active-class="finance-navigation__link--active"
        >
          <i class="pi pi-flag"></i>
          <span>{{ $t('navigation.goals') }}</span>
        </router-link>
        
        <router-link 
          :to="{name: 'finance-settings'}" 
          class="finance-navigation__link"
          exact-active-class="finance-navigation__link--active"
        >
          <i class="pi pi-cog"></i>
          <span>{{ $t('navigation.settings') }}</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { useI18n } from 'vue-i18n';

export default {
  name: 'FinanceNavigation',
  
  setup() {
    const { t } = useI18n();
    
    return {
      t
    };
  }
}
</script>

<style lang="scss" scoped>
.finance-navigation {
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
  
  &__container {
    padding: 16px;
  }
  
  &__title {
    color: #f7941d; /* Changed to orange */
    font-size: 20px;
    margin-top: 0;
    margin-bottom: 16px;
    font-weight: 600;
  }
  
  &__links {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  
  &__link {
    display: flex;
    align-items: center;
    padding: 8px 16px;
    border-radius: 8px;
    text-decoration: none;
    color: #333333;
    transition: all 0.2s ease;
    background-color: #ffffff;
    font-weight: 500;
    
    i {
      margin-right: 4px;
      color: #f7941d; /* Changed to orange */
    }
    
    &:hover {
      background-color: rgba(247, 148, 29, 0.1); /* Changed to orange */
    }
    
    &--active {
      background-color: #f7941d; /* Changed to orange */
      color: white;
      font-weight: 600;
      
      i {
        color: white;
      }
    }
  }
}

// Responsive adjustments
@media (max-width: 768px) {
  .finance-navigation {
    &__links {
      flex-direction: column;
    }
  }
}</style>