<template>
  <div class="crypto-api-key-settings">
    <h3>{{ $t('crypto.apiKeySettings') }}</h3>
    
    <div v-if="loading" class="text-center py-4">
      <div class="spinner"></div>
      <p class="mt-2">{{ $t('crypto.loading') }}</p>
    </div>
    
    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    
    <div v-else>
      <!-- API Keys List -->
      <div v-if="apiKeys.length > 0" class="api-keys-list mb-4">
        <h4>{{ $t('crypto.configuredExchanges') }}</h4>
        <div class="table-responsive">
          <table class="table">
            <thead>
              <tr>
                <th>{{ $t('crypto.exchange') }}</th>
                <th>{{ $t('crypto.status') }}</th>
                <th>{{ $t('crypto.lastUpdated') }}</th>
                <th>{{ $t('crypto.actions') }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="key in apiKeys" :key="key.exchange">
                <td>{{ getExchangeName(key.exchange) }}</td>
                <td>
                  <span :class="key.is_active ? 'badge badge-success' : 'badge badge-danger'">
                    {{ key.is_active ? $t('crypto.active') : $t('crypto.inactive') }}
                  </span>
                </td>
                <td>{{ formatDate(key.updated_at) }}</td>
                <td>
                  <button class="btn btn-sm btn-danger" @click="confirmDelete(key.exchange)">
                    {{ $t('crypto.delete') }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Add/Update API Key Form -->
      <div class="api-key-form">
        <h4>{{ formTitle }}</h4>
        <form @submit.prevent="saveApiKey">
          <div class="form-group">
            <label for="exchange">{{ $t('crypto.exchange') }}</label>
            <select id="exchange" v-model="form.exchange" class="form-control" required>
              <option value="">{{ $t('crypto.selectExchange') }}</option>
              <option v-for="exchange in availableExchanges" :key="exchange.value" :value="exchange.value">
                {{ exchange.label }}
              </option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="api_key">{{ $t('crypto.apiKey') }}</label>
            <input 
              id="api_key" 
              v-model="form.api_key" 
              type="text" 
              class="form-control" 
              required
              :placeholder="$t('crypto.apiKeyPlaceholder')"
            />
            <small class="form-text text-muted">{{ $t('crypto.apiKeyHelp') }}</small>
          </div>
          
          <div class="form-group">
            <label for="api_secret">{{ $t('crypto.apiSecret') }}</label>
            <input 
              id="api_secret" 
              v-model="form.api_secret" 
              type="password" 
              class="form-control" 
              required
              :placeholder="$t('crypto.apiSecretPlaceholder')"
            />
            <small class="form-text text-muted">{{ $t('crypto.apiSecretHelp') }}</small>
          </div>
          
          <div class="form-group">
            <div class="form-check">
              <input id="is_active" v-model="form.is_active" type="checkbox" class="form-check-input" />
              <label for="is_active" class="form-check-label">{{ $t('crypto.isActive') }}</label>
            </div>
          </div>
          
          <div class="form-group">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              {{ $t('crypto.save') }}
            </button>
          </div>
        </form>
      </div>
      
      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteModal" class="modal-backdrop">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">{{ $t('crypto.confirmDelete') }}</h5>
              <button type="button" class="close" @click="showDeleteModal = false">
                <span>&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <p>{{ $t('crypto.deleteConfirmation', { exchange: getExchangeName(exchangeToDelete) }) }}</p>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="showDeleteModal = false">
                {{ $t('crypto.cancel') }}
              </button>
              <button type="button" class="btn btn-danger" @click="deleteApiKey">
                {{ $t('crypto.delete') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import { formatDate } from '@/utils/formatters';

export default {
  name: 'CryptoApiKeySettings',
  
  data() {
    return {
      form: {
        exchange: '',
        api_key: '',
        api_secret: '',
        is_active: true
      },
      showDeleteModal: false,
      exchangeToDelete: null,
      availableExchanges: [
        { value: 'binance', label: 'Binance' },
        { value: 'coinbase', label: 'Coinbase' },
        { value: 'kraken', label: 'Kraken' },
        { value: 'kucoin', label: 'KuCoin' }
      ]
    };
  },
  
  computed: {
    ...mapState('crypto', ['apiKeys', 'loading', 'error']),
    
    formTitle() {
      const existingKey = this.apiKeys.find(key => key.exchange === this.form.exchange);
      return existingKey ? this.$t('crypto.updateApiKey') : this.$t('crypto.addApiKey');
    }
  },
  
  methods: {
    ...mapActions('crypto', ['fetchApiKeys', 'createApiKey', 'deleteApiKey']),
    
    formatDate,
    
    getExchangeName(exchangeCode) {
      const exchange = this.availableExchanges.find(e => e.value === exchangeCode);
      return exchange ? exchange.label : exchangeCode;
    },
    
    async saveApiKey() {
      try {
        await this.createApiKey(this.form);
        this.$toast.success(this.$t('crypto.apiKeySaved'));
        this.resetForm();
      } catch (error) {
        console.error('Error saving API key:', error);
        this.$toast.error(this.$t('crypto.errorSavingApiKey'));
      }
    },
    
    confirmDelete(exchange) {
      this.exchangeToDelete = exchange;
      this.showDeleteModal = true;
    },
    
    async deleteApiKey() {
      try {
        await this.deleteApiKey(this.exchangeToDelete);
        this.showDeleteModal = false;
        this.exchangeToDelete = null;
        this.$toast.success(this.$t('crypto.apiKeyDeleted'));
      } catch (error) {
        console.error('Error deleting API key:', error);
        this.$toast.error(this.$t('crypto.errorDeletingApiKey'));
      }
    },
    
    resetForm() {
      this.form = {
        exchange: '',
        api_key: '',
        api_secret: '',
        is_active: true
      };
    }
  },
  
  mounted() {
    this.fetchApiKeys();
  }
};
</script>

<style scoped>
.crypto-api-key-settings {
  padding: 1rem;
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

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-dialog {
  max-width: 500px;
  margin: 1.75rem auto;
}

.modal-content {
  position: relative;
  display: flex;
  flex-direction: column;
  width: 100%;
  background-color: var(--card-bg);
  border-radius: 0.3rem;
  outline: 0;
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-body {
  position: relative;
  flex: 1 1 auto;
  padding: 1rem;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 1rem;
  border-top: 1px solid var(--border-color);
}

.badge {
  padding: 0.25em 0.4em;
  font-size: 75%;
  font-weight: 700;
  border-radius: 0.25rem;
}

.badge-success {
  color: #fff;
  background-color: #28a745;
}

.badge-danger {
  color: #fff;
  background-color: #dc3545;
}
</style>