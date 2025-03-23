<template>
  <div class="currency-display-selector">
    <div class="selector-label">{{ $t('finance.currency.displayIn') || 'Display in:' }}</div>
    <div class="selector-dropdown">
      <select v-model="selectedCurrency" @change="updateDisplayCurrency">
        <option v-for="currency in availableCurrencies" :key="currency" :value="currency">
          {{ currency }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'CurrencyDisplaySelector',
  
  emits: ['update:currency'],
  
  props: {
    currency: {
      type: String,
      default: 'USD'
    }
  },
  
  setup(props, { emit }) {
    const store = useStore();
    const selectedCurrency = ref(props.currency || 'USD');
    
    // Get available currencies from the store
    const availableCurrencies = computed(() => {
      const rates = store.getters['personalFinance/exchangeRates'];
      return ['USD', 'EUR', 'GEL', 'RUB'].filter(currency => 
        currency === 'USD' || rates[currency]
      );
    });
    
    // Watch for changes in props
    watch(() => props.currency, (newCurrency) => {
      if (newCurrency && newCurrency !== selectedCurrency.value) {
        selectedCurrency.value = newCurrency;
      }
    });
    
    // Update display currency when selection changes
    const updateDisplayCurrency = () => {
      emit('update:currency', selectedCurrency.value);
    };
    
    // Initialize
    onMounted(async () => {
      // Ensure we have exchange rates
      if (Object.keys(store.getters['personalFinance/exchangeRates']).length === 0) {
        await store.dispatch('personalFinance/fetchExchangeRates');
      }
    });
    
    return {
      selectedCurrency,
      availableCurrencies,
      updateDisplayCurrency
    };
  }
};
</script>

<style lang="scss" scoped>
.currency-display-selector {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  
  .selector-label {
    font-size: $font-size-sm;
    color: $text-secondary;
  }
  
  .selector-dropdown {
    select {
      padding: $spacing-xs $spacing-sm;
      border-radius: $border-radius;
      border: 1px solid $chart-grid;
      background-color: $bg-secondary;
      font-size: $font-size-sm;
      cursor: pointer;
      transition: $transition-quick;
      
      &:focus {
        outline: none;
        border-color: $primary-color;
      }
    }
  }
}
</style>