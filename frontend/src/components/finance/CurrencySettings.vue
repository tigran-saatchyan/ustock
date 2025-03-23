<template>
  <div class="currency-settings">
    <h2 class="settings-title">{{ $t('finance.currencySettings') }}</h2>

    <div class="settings-section">
      <div class="form-group">
        <label for="primary-currency">{{ $t('finance.primaryCurrency') }}</label>
        <select id="primary-currency" v-model="primaryCurrency" @change="updatePrimaryCurrency">
          <option v-for="currency in availableCurrencies" :key="currency.code" :value="currency.code">
            {{ currency.code }} - {{ $t(`finance.currencies.${currency.code.toLowerCase()}`) }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="secondary-currency">{{ $t('finance.secondaryCurrency') }}</label>
        <select id="secondary-currency" v-model="secondaryCurrency" @change="updateSecondaryCurrency">
          <option v-for="currency in availableCurrencies" :key="currency.code" :value="currency.code">
            {{ currency.code }} - {{ $t(`finance.currencies.${currency.code.toLowerCase()}`) }}
          </option>
        </select>
      </div>

      <div class="form-group-checkbox">
        <input type="checkbox" id="show-secondary" v-model="showSecondaryCurrency" @change="updateShowSecondaryCurrency">
        <label for="show-secondary">{{ $t('finance.showSecondaryCurrency') }}</label>
      </div>
    </div>

    <div class="settings-section exchange-rates-section">
      <h3>{{ $t('finance.exchangeRates') }}</h3>

      <div class="form-group-checkbox">
        <input type="checkbox" id="use-api-rates" v-model="useApiExchangeRates" @change="updateUseApiExchangeRates">
        <label for="use-api-rates">{{ $t('finance.useApiExchangeRates') }}</label>
      </div>

      <template v-if="!useApiExchangeRates">
        <div class="manual-rates">
          <h4>{{ $t('finance.manualExchangeRates') }}</h4>
          <p class="rate-info">{{ $t('finance.exchangeRateInfo') }}</p>

          <div v-for="currency in currenciesToShow" :key="currency.code" class="rate-input">
            <label>{{ currency.code }}</label>
            <input
              type="number"
              :value="getManualRate(currency.code)"
              @input="updateManualRate(currency.code, $event.target.value)"
              step="0.0001"
              min="0.0001"
            />
          </div>
        </div>
      </template>

      <template v-else>
        <div v-if="exchangeRates && Object.keys(exchangeRates).length > 0" class="api-rates">
          <div class="rates-table">
            <div v-for="currency in currenciesToShow" :key="currency.code" class="rate-row">
              <span class="rate-code">{{ currency.code }}</span>
              <span class="rate-value">{{ exchangeRates[currency.code] ? exchangeRates[currency.code].toFixed(2) : '-' }}</span>
            </div>
          </div>

          <div class="last-updated">
            <div v-if="storeLastUpdated">
              {{ $t('finance.lastUpdated') }}: {{ formatDate(storeLastUpdated) }}
            </div>
            <div class="update-frequency">
              {{ $t('finance.updates.daily') || 'Rates are updated once per day' }}
            </div>
          </div>

          <button @click="refreshExchangeRates" class="refresh-button" :disabled="isLoading">
            <i class="pi pi-refresh" :class="{ 'pi-spin': isLoading }"></i>
            {{ isLoading ? $t('common.loading') : $t('common.update') }}
          </button>
        </div>
        <div v-else class="loading-rates">
          <div v-if="isLoading" class="loading-spinner">
            <div class="spinner"></div>
            <p>{{ $t('common.loading') }}</p>
          </div>
          <div v-else class="no-rates">
            <p>{{ $t('common.noData') }}</p>
            <button @click="refreshExchangeRates" class="refresh-button">
              <i class="pi pi-refresh"></i>
              {{ $t('common.update') }}
            </button>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';
import { formatDate } from '@/utils/formatters';

export default {
  name: 'CurrencySettings',

  setup() {
    const store = useStore();
    const { t } = useI18n();

    // Define available currencies
    const availableCurrencies = [
      { code: 'USD' },
      { code: 'EUR' },
      { code: 'GBP' },
      { code: 'CAD' },
      { code: 'AUD' },
      { code: 'JPY' },
      { code: 'CNY' },
      { code: 'INR' },
      { code: 'GEL' }
    ];

    // Initialize currency settings with default values
    // In case the store doesn't have them yet

    // Currency settings from store
    const primaryCurrency = ref('USD');
    const secondaryCurrency = ref('GEL');
    const showSecondaryCurrency = ref(true);
    const useApiExchangeRates = ref(true);

    // Try to get values from store or use defaults
    try {
      primaryCurrency.value = store.getters['personalFinance/primaryCurrency'] || 'USD';
      secondaryCurrency.value = store.getters['personalFinance/secondaryCurrency'] || 'GEL';
      showSecondaryCurrency.value = store.getters['personalFinance/showSecondaryCurrency'] !== undefined ?
                                 store.getters['personalFinance/showSecondaryCurrency'] : true;
      useApiExchangeRates.value = store.getters['personalFinance/useApiExchangeRates'] !== undefined ?
                               store.getters['personalFinance/useApiExchangeRates'] : true;
    } catch (e) {
      console.error('Error getting currency settings from store:', e);
    }

    // Exchange rates
    const exchangeRates = computed(() => {
      try {
        return store.getters['personalFinance/exchangeRates'] || {};
      } catch (e) {
        console.error('Error accessing exchangeRates:', e);
        return {};
      }
    });

    const manualExchangeRates = computed(() => {
      try {
        return store.getters['personalFinance/manualExchangeRates'] || {};
      } catch (e) {
        console.error('Error accessing manualExchangeRates:', e);
        return {};
      }
    });

    const isLoading = computed(() => {
      try {
        return store.state.personalFinance.loadingExchangeRates;
      } catch (e) {
        console.error('Error accessing loadingExchangeRates:', e);
        return false;
      }
    });

    // Last updated timestamp from store
    const storeLastUpdated = computed(() => {
      try {
        return store.state.personalFinance.currencySettings.lastRatesUpdate;
      } catch (e) {
        console.error('Error accessing lastRatesUpdate:', e);
        return null;
      }
    });

    // Only show non-USD currencies for exchange rates
    const currenciesToShow = computed(() =>
      availableCurrencies.filter(currency => currency.code !== 'USD')
    );

    // Load settings and rates on component mount
    onMounted(async () => {
      store.dispatch('personalFinance/loadCurrencySettings');

      // Update local refs after loading from localStorage
      primaryCurrency.value = store.getters['personalFinance/primaryCurrency'];
      secondaryCurrency.value = store.getters['personalFinance/secondaryCurrency'];
      showSecondaryCurrency.value = store.getters['personalFinance/showSecondaryCurrency'];
      useApiExchangeRates.value = store.getters['personalFinance/useApiExchangeRates'];

      // Fetch exchange rates if needed
      if (useApiExchangeRates.value) {
        if (Object.keys(exchangeRates.value).length === 0) {
          await refreshExchangeRates();
        }
        
        // Also fetch historical rates for the current month if not already loaded
        const currentDate = new Date();
        const currentYearMonth = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-01`;
        
        if (useApiExchangeRates.value && 
            (!store.state.personalFinance.currencySettings.historicalRates || 
             !store.state.personalFinance.currencySettings.historicalRates[currentYearMonth])) {
          try {
            store.dispatch('personalFinance/fetchHistoricalRates', currentYearMonth);
          } catch (error) {
            console.error('Error fetching historical rates for current month:', error);
          }
        }
      }
    });

    // Update currency settings
    const updatePrimaryCurrency = () => {
      try {
        store.dispatch('personalFinance/setPrimaryCurrency', primaryCurrency.value);
      } catch (e) {
        console.error('Error updating primary currency:', e);
      }
    };

    const updateSecondaryCurrency = () => {
      try {
        store.dispatch('personalFinance/setSecondaryCurrency', secondaryCurrency.value);
      } catch (e) {
        console.error('Error updating secondary currency:', e);
      }
    };

    const updateShowSecondaryCurrency = () => {
      try {
        store.dispatch('personalFinance/setShowSecondaryCurrency', showSecondaryCurrency.value);
      } catch (e) {
        console.error('Error updating show secondary currency setting:', e);
      }
    };

    const updateUseApiExchangeRates = () => {
      try {
        store.dispatch('personalFinance/setUseApiExchangeRates', useApiExchangeRates.value);

        if (useApiExchangeRates.value && Object.keys(exchangeRates.value).length === 0) {
          refreshExchangeRates();
        }
      } catch (e) {
        console.error('Error updating API exchange rates setting:', e);
      }
    };

    // Get manual exchange rate for a currency
    const getManualRate = (currency) => {
      try {
        if (manualExchangeRates.value && typeof manualExchangeRates.value === 'object') {
          return manualExchangeRates.value[currency] || '';
        }
        return '';
      } catch (e) {
        console.error('Error getting manual rate for', currency, e);
        return '';
      }
    };

    // Update manual exchange rate
    const updateManualRate = (currency, rate) => {
      try {
        const numericRate = parseFloat(rate);
        if (!isNaN(numericRate) && numericRate > 0) {
          store.dispatch('personalFinance/setManualExchangeRate', {
            currency,
            rate: numericRate
          });
        }
      } catch (e) {
        console.error('Error updating manual exchange rate for', currency, e);
      }
    };

    // Refresh exchange rates from API
    const refreshExchangeRates = async () => {
      try {
        await store.dispatch('personalFinance/fetchExchangeRates');
        
        // Also refresh historical rates for current month
        const currentDate = new Date();
        const currentYearMonth = `${currentDate.getFullYear()}-${String(currentDate.getMonth() + 1).padStart(2, '0')}-01`;
        await store.dispatch('personalFinance/fetchHistoricalRates', currentYearMonth);
      } catch (error) {
        console.error('Error refreshing exchange rates:', error);
        // If API fetch fails, use mock data as fallback
        const { MOCK_EXCHANGE_RATES } = await import('@/api/mockCurrencyRates');
        store.commit('personalFinance/SET_EXCHANGE_RATES', MOCK_EXCHANGE_RATES);
      }
    };

    return {
      primaryCurrency,
      secondaryCurrency,
      showSecondaryCurrency,
      useApiExchangeRates,
      availableCurrencies,
      exchangeRates,
      manualExchangeRates,
      currenciesToShow,
      isLoading,
      storeLastUpdated,
      updatePrimaryCurrency,
      updateSecondaryCurrency,
      updateShowSecondaryCurrency,
      updateUseApiExchangeRates,
      getManualRate,
      updateManualRate,
      refreshExchangeRates,
      formatDate,
      t
    };
  }
};
</script>

<style lang="scss" scoped>
.currency-settings {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.settings-title {
  color: #f7941d; /* Changed to orange */
  font-size: 20px;
  margin-top: 0;
  margin-bottom: 16px;
  font-weight: 600;
}

.settings-section {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e0e0e0;

  &:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
  }

  h3 {
    font-size: 18px;
    margin-top: 0;
    margin-bottom: 16px;
    color: #333333;
  }

  h4 {
    font-size: 16px;
    margin-top: 16px;
    margin-bottom: 8px;
    color: #333333;
  }
}

.form-group {
  margin-bottom: 16px;

  label {
    display: block;
    margin-bottom: 4px;
    color: #666666;
    font-weight: 500;
  }

  select, input[type="number"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    background-color: #f5f5f5;
    color: #333333;
    font-size: 16px;

    &:focus {
      outline: none;
      border-color: #f7941d; /* Changed to orange */
    }
  }
}

.form-group-checkbox {
  display: flex;
  align-items: center;
  margin-bottom: 16px;

  input[type="checkbox"] {
    margin-right: 8px;
  }

  label {
    color: #333333;
    font-weight: 500;
  }
}

.manual-rates {
  .rate-info {
    color: #666666;
    font-size: 14px;
    margin-bottom: 16px;
  }

  .rate-input {
    display: flex;
    align-items: center;
    margin-bottom: 8px;

    label {
      width: 80px;
      font-weight: 500;
      color: #333333;
    }

    input {
      flex: 1;
      padding: 4px 8px;
      border: 1px solid #e0e0e0;
      border-radius: 4px;
      background-color: #f5f5f5;
      color: #333333;

      &:focus {
        outline: none;
        border-color: #f7941d; /* Changed to orange */
      }
    }
  }
}

.api-rates {
  .rates-table {
    margin-bottom: 16px;
  }

  .rate-row {
    display: flex;
    justify-content: space-between;
    padding: 4px 0;
    border-bottom: 1px solid rgba(#e0e0e0, 0.5);

    &:last-child {
      border-bottom: none;
    }
  }

  .rate-code {
    font-weight: 600;
    color: #f7941d; /* Changed to orange */
  }

  .rate-value {
    color: #666666;
  }

  .last-updated {
    color: #666666;
    font-size: 14px;
    margin-bottom: 16px;
    
    .update-frequency {
      font-style: italic;
      margin-top: 4px;
      font-size: 12px;
    }
  }
}

.refresh-button {
  display: inline-flex;
  align-items: center;
  padding: 4px 16px;
  background-color: #f7941d; /* Changed to orange */
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;

  i {
    margin-right: 4px;
  }

  &:hover {
    background-color: #e58714; /* Darker orange */
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;

  .spinner {
    width: 24px;
    height: 24px;
    border: 3px solid rgba(#f7941d, 0.2);
    border-radius: 50%;
    border-top-color: #f7941d; /* Changed to orange */
    animation: spin 1s ease-in-out infinite;
    margin-bottom: 8px;
  }

  p {
    color: #666666;
  }
}

.no-rates {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 16px;

  p {
    color: #666666;
    margin-bottom: 16px;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>