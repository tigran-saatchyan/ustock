<template>
  <div class="crypto-balance">
    <div v-if="loading" class="text-center py-4">
      <div class="spinner"></div>
      <p class="mt-2">{{ $t('crypto.loading') }}</p>
    </div>
    
    <div v-else-if="error" class="text-center py-4">
      <div class="alert alert-danger">
        {{ error }}
      </div>
    </div>
    
    <div v-else-if="!hasApiKeys" class="text-center py-4">
      <div class="alert alert-info">
        {{ $t('crypto.noApiKeys') }}
      </div>
      <router-link to="/settings/crypto" class="btn btn-primary mt-2">
        {{ $t('crypto.configureApiKeys') }}
      </router-link>
    </div>
    
    <div v-else-if="!accountBalance || !accountBalance.balances || accountBalance.balances.length === 0" class="text-center py-4">
      <div class="alert alert-info">
        {{ $t('crypto.noBalance') }}
      </div>
    </div>
    
    <div v-else>
      <div class="total-balance mb-4">
        <h3>{{ $t('crypto.totalBalance') }}</h3>
        <div class="total-value">{{ formatCurrency(totalBalance, 'USD') }}</div>
      </div>
      
      <div class="balances">
        <h4>{{ $t('crypto.assets') }}</h4>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>{{ $t('crypto.asset') }}</th>
                <th>{{ $t('crypto.amount') }}</th>
                <th>{{ $t('crypto.price') }}</th>
                <th>{{ $t('crypto.value') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="balance in sortedBalances" :key="balance.asset">
                <td>{{ balance.asset }}</td>
                <td>{{ formatNumber(balance.total) }}</td>
                <td>{{ formatCurrency(balance.price_usdt, 'USD') }}</td>
                <td>{{ formatCurrency(balance.value_usdt, 'USD') }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex';
import { formatCurrency, formatNumber } from '@/utils/formatters';

export default {
  name: 'CryptoBalance',
  
  props: {
    exchange: {
      type: String,
      default: 'binance'
    }
  },
  
  computed: {
    ...mapState('crypto', ['accountBalance', 'loading', 'error']),
    ...mapGetters('crypto', ['totalBalance', 'sortedBalances', 'hasApiKeys']),
    
    hasApiKeys() {
      return this.$store.getters['crypto/hasApiKeys'](this.exchange);
    }
  },
  
  methods: {
    ...mapActions('crypto', ['fetchAccountBalance']),
    
    formatCurrency,
    formatNumber,
    
    async refreshBalance() {
      try {
        await this.fetchAccountBalance(this.exchange);
      } catch (error) {
        console.error('Error refreshing balance:', error);
      }
    }
  },
  
  mounted() {
    this.refreshBalance();
  }
};
</script>

<style scoped>
.crypto-balance {
  padding: 1rem;
  background-color: var(--card-bg);
  border-radius: 0.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.total-balance {
  text-align: center;
  padding: 1rem;
  background-color: var(--card-bg-accent);
  border-radius: 0.5rem;
}

.total-value {
  font-size: 2rem;
  font-weight: bold;
  color: var(--text-primary);
}

.spinner {
  display: inline-block;
  width: 2rem;
  height: 2rem;
  border: 0.25rem solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top-color: var(--primary);
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.table {
  margin-bottom: 0;
}

.table th {
  border-top: none;
  color: var(--text-secondary);
}

.table td, .table th {
  padding: 0.75rem;
  vertical-align: middle;
}
</style>