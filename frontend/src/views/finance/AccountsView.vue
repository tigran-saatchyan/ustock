<template>
  <div class="accounts-view">
    <finance-navigation />
    
    <div class="accounts-container">
      <div class="accounts-header">
        <h2 class="accounts-title">{{ $t('navigation.accounts') }}</h2>
        
        <button @click="showAccountForm = true" class="add-button">
          <i class="pi pi-plus"></i>
          <span>{{ $t('finance.addAccount') }}</span>
        </button>
      </div>
      
      <div v-if="isLoading" class="loading-spinner">
        <div class="spinner"></div>
        <p>{{ $t('common.loading') }}</p>
      </div>
      
      <!-- Accounts Overview -->
      <div v-else-if="accounts.length" class="accounts-overview">
        <div class="overview-card">
          <h3 class="overview-card__title">{{ $t('finance.totalBalance') }}</h3>
          <div class="overview-card__value">{{ formatCurrency(totalBalance) }}</div>
          <div class="overview-card__meta">{{ $t('finance.acrossAllAccounts') }}</div>
        </div>
        
        <div class="overview-card">
          <h3 class="overview-card__title">{{ $t('finance.activeAccounts') }}</h3>
          <div class="overview-card__value">{{ activeAccounts.length }}</div>
          <div class="overview-card__meta">{{ $t('common.of') }} {{ accounts.length }} {{ $t('common.total') }}</div>
        </div>
      </div>
      
      <!-- Assets, Liabilities, and Income Sources Sections -->
      <div v-if="accounts.length" class="accounts-sections">
        <!-- Assets Section -->
        <div class="accounts-section">
          <div class="accounts-section__header">
            <div class="accounts-section__title">
              <i class="pi pi-arrow-up" style="color: #4CAF50;"></i>
              <h2 style="color: #333333;">
                {{ $t('finance.assets') }}
                <info-tooltip>
                  {{ $t('finance.assetsTooltip') }}
                </info-tooltip>
              </h2>
            </div>
            <div class="accounts-section__total">{{ formatCurrency(assetsTotal, null, true) }}</div>
          </div>
          
          <div class="accounts-grid">
            <div 
              v-for="account in assetAccounts" 
              :key="account.id"
              class="account-card"
              :class="{ 'inactive': !account.is_active }"
              :data-inactive-text="$t('common.inactive')"
            >
              <div class="account-card__header" :style="{ backgroundColor: account.color || '#4CAF50' }">
                <i :class="getAccountIcon(account)"></i>
                <div class="account-card__type">{{ getAccountTypeLabel(account.account_type) }}</div>
              </div>
              
              <div class="account-card__content">
                <h3 class="account-card__name">{{ account.name }}</h3>
                <div class="account-card__balance">{{ formatCurrency(account.balance, account.currency) }}</div>
                <div class="account-card__currency">{{ $t(`finance.currencies.${account.currency.toLowerCase()}`) }}</div>
                <div v-if="account.is_cash_flow_generating" class="account-card__cashflow">
                  <i class="pi pi-arrow-circle-right" style="color: #4CAF50;"></i>
                  {{ formatCurrency(account.monthly_cash_flow, account.currency) }}/{{ $t('finance.month') || 'mo' }}
                </div>
              </div>
              
              <div class="account-card__actions">
                <button @click="editAccount(account)" class="action-button">
                  <i class="pi pi-pencil"></i>
                </button>
                <button @click="deleteAccountConfirm(account)" class="action-button delete">
                  <i class="pi pi-trash"></i>
                </button>
              </div>
            </div>
            
            <div v-if="assetAccounts.length === 0" class="empty-category">
              <p>{{ $t('finance.noAssetsFound') }}</p>
            </div>
          </div>
        </div>
        
        <!-- Income Sources Section -->
        <div class="accounts-section income-section">
          <div class="accounts-section__header">
            <div class="accounts-section__title">
              <i class="pi pi-dollar" style="color: #42A5F5;"></i>
              <h2 style="color: #333333;">
                {{ $t('finance.incomeSources') || 'Income Sources' }}
                <info-tooltip>
                  {{ $t('finance.incomeTooltip') || 'Income sources like salary, wages, freelance work, or commissions - money in exchange for your time.' }}
                </info-tooltip>
              </h2>
            </div>
            <div class="accounts-section__total">{{ formatCurrency(incomeSourceTotal, null, true) }}</div>
          </div>
          
          <div class="accounts-grid">
            <div 
              v-for="account in incomeSourceAccounts" 
              :key="account.id"
              class="account-card"
              :class="{ 'inactive': !account.is_active }"
              :data-inactive-text="$t('common.inactive')"
            >
              <div class="account-card__header" :style="{ backgroundColor: account.color || '#42A5F5' }">
                <i :class="getAccountIcon(account)"></i>
                <div class="account-card__type">{{ getAccountTypeLabel(account.account_type) }}</div>
              </div>
              
              <div class="account-card__content">
                <h3 class="account-card__name">{{ account.name }}</h3>
                <div class="account-card__balance">{{ formatCurrency(account.balance, account.currency) }}</div>
                <div class="account-card__currency">{{ $t(`finance.currencies.${account.currency.toLowerCase()}`) }}</div>
              </div>
              
              <div class="account-card__actions">
                <button @click="editAccount(account)" class="action-button">
                  <i class="pi pi-pencil"></i>
                </button>
                <button @click="deleteAccountConfirm(account)" class="action-button delete">
                  <i class="pi pi-trash"></i>
                </button>
              </div>
            </div>
            
            <div v-if="incomeSourceAccounts.length === 0" class="empty-category">
              <p>{{ $t('finance.noIncomeSourcesFound') || 'No income sources found' }}</p>
            </div>
          </div>
        </div>
        
        <!-- Liabilities Section -->
        <div class="accounts-section">
          <div class="accounts-section__header">
            <div class="accounts-section__title">
              <i class="pi pi-arrow-down" style="color: #F44336;"></i>
              <h2 style="color: #333333;">
                {{ $t('finance.liabilities') }}
                <info-tooltip>
                  {{ $t('finance.liabilitiesTooltip') }}
                </info-tooltip>
              </h2>
            </div>
            <div class="accounts-section__total">{{ formatCurrency(liabilitiesTotal, null, true) }}</div>
          </div>
          
          <div class="accounts-grid">
            <div 
              v-for="account in liabilityAccounts" 
              :key="account.id"
              class="account-card"
              :class="{ 'inactive': !account.is_active }"
              :data-inactive-text="$t('common.inactive')"
            >
              <div class="account-card__header" :style="{ backgroundColor: account.color || '#F44336' }">
                <i :class="getAccountIcon(account)"></i>
                <div class="account-card__type">{{ getAccountTypeLabel(account.account_type) }}</div>
              </div>
              
              <div class="account-card__content">
                <h3 class="account-card__name">{{ account.name }}</h3>
                <div class="account-card__balance">{{ formatCurrency(Math.abs(account.balance), account.currency) }}</div>
                <div class="account-card__currency">{{ $t(`finance.currencies.${account.currency.toLowerCase()}`) }}</div>
              </div>
              
              <div class="account-card__actions">
                <button @click="editAccount(account)" class="action-button">
                  <i class="pi pi-pencil"></i>
                </button>
                <button @click="deleteAccountConfirm(account)" class="action-button delete">
                  <i class="pi pi-trash"></i>
                </button>
              </div>
            </div>
            
            <div v-if="liabilityAccounts.length === 0" class="empty-category">
              <p>{{ $t('finance.noLiabilitiesFound') }}</p>
            </div>
          </div>
        </div>
        
        <!-- Net Worth Section -->
        <div class="net-worth-section">
          <div class="net-worth-card">
            <h3 class="net-worth-card__title">{{ $t('finance.netWorth') }}</h3>
            <div class="net-worth-card__value" :class="{'positive': netWorth >= 0, 'negative': netWorth < 0}">
              {{ formatCurrency(netWorth, null, true) }}
            </div>
            <div class="net-worth-card__formula">{{ $t('finance.assetsMinusLiabilities') }}</div>
          </div>
        </div>
      </div>
      
      <div v-else-if="!isLoading" class="empty-state">
        <p>{{ $t('finance.noAccountsFound') }}</p>
        <button @click="showAccountForm = true" class="button button--primary">
          {{ $t('finance.addFirstAccount') }}
        </button>
      </div>
      
      <!-- Account Form Modal -->
      <div class="modal" v-if="showAccountForm">
        <div class="modal-overlay" @click="showAccountForm = false"></div>
        <div class="modal-container">
          <div class="modal-header">
            <h3>{{ editMode ? $t('finance.editAccount') : $t('finance.addAccount') }}</h3>
            <button @click="showAccountForm = false" class="close-button">
              <i class="pi pi-times"></i>
            </button>
          </div>
          
          <div class="modal-body">
            <div v-if="formError" class="form-error-message">
              <i class="pi pi-exclamation-circle"></i>
              <span>{{ formError }}</span>
            </div>
            <form @submit.prevent="saveAccount" class="account-form">
              <!-- Account Name and Type -->
              <div class="form-row">
                <div class="form-group">
                  <label for="name">{{ $t('finance.accountName') }}</label>
                  <input type="text" id="name" v-model="accountForm.name" required>
                </div>
                
                <div class="form-group">
                  <label for="account-type">{{ $t('finance.accountType') }}</label>
                  <select 
                    id="account-type" 
                    v-model="accountForm.account_type" 
                    @change="handleAccountTypeChange"
                    required
                  >
                    <option value="" disabled>{{ $t('finance.accountType') }}</option>
                    <option value="cash">{{ $t('finance.accountTypes.cash') }}</option>
                    <option value="bank">{{ $t('finance.accountTypes.bank') }}</option>
                    <option value="credit_card">{{ $t('finance.accountTypes.credit_card') }}</option>
                    <option value="investment">{{ $t('finance.accountTypes.investment') }}</option>
                    <option value="real_estate">{{ $t('finance.accountTypes.real_estate') }}</option>
                    <option value="business">{{ $t('finance.accountTypes.business') }}</option>
                    <option value="stocks">{{ $t('finance.accountTypes.stocks') }}</option>
                    <option value="bonds">{{ $t('finance.accountTypes.bonds') }}</option>
                    <option value="intellectual">{{ $t('finance.accountTypes.intellectual') }}</option>
                    <option value="cash_flow">{{ $t('finance.accountTypes.cash_flow') }}</option>
                    <option value="mortgage">{{ $t('finance.accountTypes.mortgage') }}</option>
                    <option value="consumer_loan">{{ $t('finance.accountTypes.consumer_loan') }}</option>
                    <option value="auto_loan">{{ $t('finance.accountTypes.auto_loan') }}</option>
                    <option value="lease">{{ $t('finance.accountTypes.lease') }}</option>
                    <option value="other_debt">{{ $t('finance.accountTypes.other_debt') }}</option>
                    <option value="other">{{ $t('finance.accountTypes.other') }}</option>
                  </select>
                </div>
              </div>
              
              <!-- Balance and Currency -->
              <div class="form-row">
                <div class="form-group">
                  <label for="balance">{{ $t('finance.currentBalance') }}</label>
                  <input type="number" id="balance" v-model="accountForm.balance" step="0.01">
                </div>
                
                <div class="form-group">
                  <label for="currency">{{ $t('finance.currency') }}</label>
                  <select id="currency" v-model="accountForm.currency" required>
                    <option value="USD">USD - {{ $t('finance.currencies.usd') }}</option>
                    <option value="EUR">EUR - {{ $t('finance.currencies.eur') }}</option>
                    <option value="GBP">GBP - {{ $t('finance.currencies.gbp') }}</option>
                    <option value="CAD">CAD - {{ $t('finance.currencies.cad') }}</option>
                    <option value="AUD">AUD - {{ $t('finance.currencies.aud') }}</option>
                    <option value="JPY">JPY - {{ $t('finance.currencies.jpy') }}</option>
                    <option value="CNY">CNY - {{ $t('finance.currencies.cny') }}</option>
                    <option value="INR">INR - {{ $t('finance.currencies.inr') }}</option>
                    <option value="GEL">GEL - {{ $t('finance.currencies.gel') }}</option>
                  </select>
                </div>
              </div>
              
              <!-- Color and Icon -->
              <div class="form-row">
                <div class="form-group">
                  <label for="color">{{ $t('finance.accountColor') }}</label>
                  <input type="color" id="color" v-model="accountForm.color">
                </div>
                
                <div class="form-group">
                  <label for="icon">{{ $t('finance.accountIcon') }}</label>
                  <select id="icon" v-model="accountForm.icon">
                    <option value="pi pi-wallet">{{ $t('finance.icons.wallet') }}</option>
                    <option value="pi pi-credit-card">{{ $t('finance.icons.creditCard') }}</option>
                    <option value="pi pi-money-bill">{{ $t('finance.icons.cash') }}</option>
                    <option value="pi pi-building">{{ $t('finance.icons.bank') }}</option>
                    <option value="pi pi-chart-line">{{ $t('finance.icons.investment') }}</option>
                    <option value="pi pi-briefcase">{{ $t('finance.icons.business') }}</option>
                    <option value="pi pi-box">{{ $t('finance.icons.other') }}</option>
                  </select>
                </div>
              </div>
              
              <!-- Financial Definitions -->
              <div class="financial-tips">
                <h4>
                  <i class="pi pi-book"></i>
                  {{ $t('finance.kiyosakiTip') }}
                </h4>
                <div class="tip-item asset">
                  <div class="tip-header">
                    <span>{{ $t('finance.assets') }}</span>
                  </div>
                  <p v-html="$t('finance.assetsTooltip')"></p>
                </div>
                <div class="tip-item liability">
                  <div class="tip-header">
                    <span>{{ $t('finance.liabilities') }}</span>
                  </div>
                  <p v-html="$t('finance.liabilitiesTooltip')"></p>
                </div>
              </div>
              
              <!-- Active Status and Account Classification -->
              <div class="form-group checkbox-group">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="accountForm.is_active">
                  <span class="checkbox-text">{{ $t('finance.isActive') }}</span>
                </label>
                
                <div class="classification-grid">
                  <label class="checkbox-label">
                    <input 
                      type="radio" 
                      name="account-classification" 
                      :value="false" 
                      v-model="accountForm.is_liability"
                      @change="accountForm.is_income_source = false"
                      :checked="!accountForm.is_liability && !accountForm.is_income_source"
                    >
                    <span class="checkbox-text">{{ $t('finance.isAsset') || 'Asset' }}</span>
                    <info-tooltip>
                      {{ $t('finance.assetsTooltip') }}
                    </info-tooltip>
                  </label>
                  
                  <label class="checkbox-label">
                    <input 
                      type="radio" 
                      name="account-classification" 
                      :value="true" 
                      v-model="accountForm.is_liability"
                      @change="accountForm.is_income_source = false"
                    >
                    <span class="checkbox-text">{{ $t('finance.isLiability') }}</span>
                    <info-tooltip>
                      {{ $t('finance.liabilitiesTooltip') }}
                    </info-tooltip>
                  </label>
                  
                  <label class="checkbox-label">
                    <input 
                      type="radio" 
                      name="account-classification" 
                      :value="true" 
                      v-model="accountForm.is_income_source"
                      @change="accountForm.is_liability = false"
                    >
                    <span class="checkbox-text">{{ $t('finance.isIncomeSource') || 'Income Source' }}</span>
                    <info-tooltip>
                      {{ $t('finance.incomeTooltip') || 'Income sources like salary, wages, freelance work, or commissions - money in exchange for your time.' }}
                    </info-tooltip>
                  </label>
                </div>
                
                <label class="checkbox-label" v-if="!accountForm.is_liability && !accountForm.is_income_source">
                  <input type="checkbox" v-model="accountForm.is_cash_flow_generating">
                  <span class="checkbox-text">{{ $t('finance.isCashFlowGenerating') || 'Generates Cash Flow' }}</span>
                  <info-tooltip>
                    {{ $t('finance.cashFlowTooltip') || 'Assets that generate monthly cash flow increase your passive income.' }}
                  </info-tooltip>
                </label>
              </div>
              
              <!-- Monthly Cash Flow -->
              <div class="form-group" v-if="accountForm.is_cash_flow_generating">
                <label for="monthly-cash-flow">{{ $t('finance.monthlyCashFlow') || 'Monthly Cash Flow' }}</label>
                <input type="number" id="monthly-cash-flow" v-model="accountForm.monthly_cash_flow" step="0.01">
              </div>
              
              <!-- Form Actions -->
              <div class="form-actions">
                <button type="button" @click="showAccountForm = false" class="button button--secondary">
                  {{ $t('common.cancel') }}
                </button>
                <button type="submit" class="button button--primary">
                  {{ editMode ? $t('common.update') : $t('common.save') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
      
      <!-- Delete Confirmation Modal -->
      <div class="modal" v-if="showDeleteConfirm">
        <div class="modal-overlay" @click="showDeleteConfirm = false"></div>
        <div class="modal-container confirm-dialog">
          <div class="modal-header">
            <h3>{{ $t('finance.confirmDelete') }}</h3>
            <button @click="showDeleteConfirm = false" class="close-button">
              <i class="pi pi-times"></i>
            </button>
          </div>
          
          <div class="modal-body">
            <p>{{ $t('finance.deleteAccountConfirm') }}</p>
            <p v-if="accountToDelete" class="delete-details">
              <strong>{{ accountToDelete.name }}</strong>
              <span>{{ formatCurrency(accountToDelete.balance) }}</span>
            </p>
            
            <div class="warning-box" v-if="accountHasTransactions">
              <i class="pi pi-exclamation-triangle"></i>
              <p>{{ $t('finance.deleteTransactionsWarning') }}</p>
            </div>
            
            <div class="form-actions">
              <button @click="showDeleteConfirm = false" class="button button--secondary">
                {{ $t('common.cancel') }}
              </button>
              <button @click="deleteAccount" class="button button--delete">
                {{ $t('common.delete') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';
import FinanceNavigation from '@/components/finance/FinanceNavigation.vue';
import InfoTooltip from '@/components/finance/InfoTooltip.vue';
import { useDualCurrencyFormatter } from '@/utils/currencyUtils';

export default {
  name: 'AccountsView',
  
  components: {
    FinanceNavigation,
    InfoTooltip
  },
  
  setup() {
    const store = useStore();
    
    // State
    const showAccountForm = ref(false);
    const showDeleteConfirm = ref(false);
    const editMode = ref(false);
    const accountToDelete = ref(null);
    const accountHasTransactions = ref(false);
    const formError = ref(''); // For displaying form validation errors
    
    // Default form values
    const defaultForm = {
      name: '',
      balance: 0,
      currency: 'USD',
      account_type: 'bank',
      color: '#1f2937',
      icon: 'pi pi-wallet',
      is_active: true,
      is_liability: false,
      is_income_source: false,
      is_cash_flow_generating: false,
      monthly_cash_flow: 0
    };
    
    // Form model
    const accountForm = ref({ ...defaultForm });
    
    // Store getters
    const isLoading = computed(() => store.getters['personalFinance/isLoading']);
    const accounts = computed(() => store.getters['personalFinance/accounts']);
    const activeAccounts = computed(() => store.getters['personalFinance/activeAccounts']);
    const totalBalance = computed(() => store.getters['personalFinance/totalBalance']);
    const transactions = computed(() => store.getters['personalFinance/transactions']);
    
    // Computed properties for Assets, Liabilities, and Income sources
    const assetAccounts = computed(() => {
      return accounts.value.filter(account => 
        !account.is_liability && !account.is_income_source
      );
    });
    
    const liabilityAccounts = computed(() => {
      return accounts.value.filter(account => 
        account.is_liability || account.account_type === 'credit'
      );
    });
    
    const incomeSourceAccounts = computed(() => {
      return accounts.value.filter(account => account.is_income_source);
    });
    
    const assetsTotal = computed(() => {
      // Add debug logging
      console.log('Asset accounts:', assetAccounts.value);
      
      if (!assetAccounts.value || assetAccounts.value.length === 0) {
        return 0;
      }
      
      const result = assetAccounts.value.reduce((total, account) => {
        // Debug log individual account
        console.log('Processing asset account:', account.name, account.balance, account.currency);
        
        // Convert to USD if in different currency
        if (account.currency !== store.getters['personalFinance/primaryCurrency']) {
          const exchangeRate = store.getters['personalFinance/getExchangeRate'](account.currency);
          const primaryRate = store.getters['personalFinance/getExchangeRate'](
            store.getters['personalFinance/primaryCurrency']
          );
          
          console.log('Exchange rates:', account.currency, exchangeRate, 
                      store.getters['personalFinance/primaryCurrency'], primaryRate);
          
          // Convert to USD first, then to primary currency
          const valueInUSD = account.balance / exchangeRate;
          const convertedValue = valueInUSD * primaryRate;
          
          console.log('Converted values:', 'USD:', valueInUSD, 
                      store.getters['personalFinance/primaryCurrency'], convertedValue);
          
          return total + convertedValue;
        }
        return total + Number(account.balance);
      }, 0);
      
      console.log('Total assets value:', result);
      return result;
    });
    
    const liabilitiesTotal = computed(() => {
      // Add debug logging
      console.log('Liability accounts:', liabilityAccounts.value);
      
      if (!liabilityAccounts.value || liabilityAccounts.value.length === 0) {
        return 0;
      }
      
      const result = liabilityAccounts.value.reduce((total, account) => {
        // Debug log individual account
        console.log('Processing liability account:', account.name, account.balance, account.currency);
        
        // Convert to USD if in different currency
        if (account.currency !== store.getters['personalFinance/primaryCurrency']) {
          const exchangeRate = store.getters['personalFinance/getExchangeRate'](account.currency);
          const primaryRate = store.getters['personalFinance/getExchangeRate'](
            store.getters['personalFinance/primaryCurrency']
          );
          
          console.log('Exchange rates:', account.currency, exchangeRate, 
                      store.getters['personalFinance/primaryCurrency'], primaryRate);
          
          // Convert to USD first, then to primary currency
          const valueInUSD = Math.abs(Number(account.balance)) / exchangeRate;
          const convertedValue = valueInUSD * primaryRate;
          
          console.log('Converted values:', 'USD:', valueInUSD, 
                      store.getters['personalFinance/primaryCurrency'], convertedValue);
          
          return total + convertedValue;
        }
        return total + Math.abs(Number(account.balance));
      }, 0);
      
      console.log('Total liabilities value:', result);
      return result;
    });
    
    const incomeSourceTotal = computed(() => {
      console.log('Income source accounts:', incomeSourceAccounts.value);
      
      if (!incomeSourceAccounts.value || incomeSourceAccounts.value.length === 0) {
        return 0;
      }
      
      const result = incomeSourceAccounts.value.reduce((total, account) => {
        console.log('Processing income source account:', account.name, account.balance, account.currency);
        
        // Convert to USD if in different currency
        if (account.currency !== store.getters['personalFinance/primaryCurrency']) {
          const exchangeRate = store.getters['personalFinance/getExchangeRate'](account.currency);
          const primaryRate = store.getters['personalFinance/getExchangeRate'](
            store.getters['personalFinance/primaryCurrency']
          );
          
          // Convert to USD first, then to primary currency
          const valueInUSD = Number(account.balance) / exchangeRate;
          const convertedValue = valueInUSD * primaryRate;
          
          return total + convertedValue;
        }
        return total + Number(account.balance);
      }, 0);
      
      console.log('Total income sources value:', result);
      return result;
    });
    
    const netWorth = computed(() => {
      return assetsTotal.value - liabilitiesTotal.value;
    });
    
    // Initialize data
    onMounted(async () => {
      await store.dispatch('personalFinance/fetchAccounts');
    });
    
    // Edit account
    const editAccount = (account) => {
      editMode.value = true;
      
      accountForm.value = {
        id: account.id,
        name: account.name,
        balance: account.balance,
        currency: account.currency,
        account_type: account.account_type,
        color: account.color,
        icon: account.icon,
        is_active: account.is_active,
        is_liability: account.is_liability || false,
        is_income_source: account.is_income_source || false,
        is_cash_flow_generating: account.is_cash_flow_generating || false,
        monthly_cash_flow: account.monthly_cash_flow || 0
      };
      
      showAccountForm.value = true;
    };
    
    // Save account (create or update)
    const saveAccount = async () => {
      try {
        // Clear any previous errors
        formError.value = '';
        
        // Log form values for debugging
        console.log('Saving account with form data:', accountForm.value);
        
        // Validate form client-side
        if (accountForm.value.is_liability && accountForm.value.is_income_source) {
          formError.value = 'An account cannot be both a liability and an income source.';
          return;
        }
        
        if (accountForm.value.is_cash_flow_generating && 
            (accountForm.value.is_liability || accountForm.value.is_income_source)) {
          formError.value = 'Only assets can generate cash flow, not liabilities or income sources.';
          return;
        }
        
        // Process the form submission
        if (editMode.value) {
          // Update existing account
          await store.dispatch('personalFinance/updateAccount', {
            id: accountForm.value.id,
            data: { ...accountForm.value }
          });
        } else {
          // Create new account
          await store.dispatch('personalFinance/createAccount', { ...accountForm.value });
        }
        
        // Reset form and close modal
        resetForm();
        showAccountForm.value = false;
      } catch (error) {
        console.error('Error saving account:', error);
        
        // Enhanced error handling
        if (error.response && error.response.data) {
          // Check for field-specific errors (which come as field names with arrays of errors)
          const errorData = error.response.data;
          
          if (errorData.error) {
            // Non-field error with 'error' key
            formError.value = `Validation error: ${errorData.error}`;
          } else if (errorData.detail) {
            // Detail error
            formError.value = `Error: ${errorData.detail}`;
          } else if (errorData.non_field_errors) {
            // Non-field errors array
            formError.value = `Error: ${errorData.non_field_errors.join(', ')}`;
          } else {
            // Check for field-specific errors
            const fieldErrors = [];
            
            // Loop through response data to find field errors
            for (const [field, errors] of Object.entries(errorData)) {
              if (Array.isArray(errors)) {
                fieldErrors.push(`${field}: ${errors.join(', ')}`);
              }
            }
            
            if (fieldErrors.length > 0) {
              formError.value = `Validation errors: ${fieldErrors.join('; ')}`;
            } else {
              // Generic error message if we couldn't parse the error
              formError.value = 'An error occurred while saving the account. Please check the console for details.';
            }
          }
        } else {
          formError.value = 'An unexpected error occurred. Please try again.';
        }
      }
    };
    
    // Confirm account delete
    const deleteAccountConfirm = (account) => {
      accountToDelete.value = account;
      
      // Check if account has transactions
      accountHasTransactions.value = transactions.value.some(t => 
        t.account === account.id || t.to_account === account.id
      );
      
      showDeleteConfirm.value = true;
    };
    
    // Delete account
    const deleteAccount = async () => {
      if (!accountToDelete.value) return;
      
      try {
        await store.dispatch('personalFinance/deleteAccount', accountToDelete.value.id);
        showDeleteConfirm.value = false;
        accountToDelete.value = null;
      } catch (error) {
        console.error('Error deleting account:', error);
        // Error handling would go here
      }
    };
    
    // Reset form to defaults
    const resetForm = () => {
      editMode.value = false;
      accountForm.value = { ...defaultForm };
      formError.value = ''; // Clear any form errors
    };
    
    // Handle account type change to update form properties based on selected type
    const handleAccountTypeChange = () => {
      const type = accountForm.value.account_type;
      
      // Clear the form error when type changes
      formError.value = '';
      
      // Credit card accounts are always liabilities
      if (type === 'credit_card') {
        accountForm.value.is_liability = true;
        accountForm.value.is_income_source = false;
        accountForm.value.is_cash_flow_generating = false;
      }
      
      // Mortgage, consumer loan, auto loan, lease, other debt are always liabilities
      if (['mortgage', 'consumer_loan', 'auto_loan', 'lease', 'other_debt'].includes(type)) {
        accountForm.value.is_liability = true;
        accountForm.value.is_income_source = false;
        accountForm.value.is_cash_flow_generating = false;
      }
      
      // Salary, freelance, commission, consulting are always income sources
      if (['salary', 'freelance', 'commission', 'consulting'].includes(type)) {
        accountForm.value.is_liability = false;
        accountForm.value.is_income_source = true;
        accountForm.value.is_cash_flow_generating = false;
      }
    };
    
    // Import i18n
    // eslint-disable-next-line no-unused-vars
    const { t } = useI18n(); // Used for template translations
    
    // Use the dual currency formatter
    const { formatDualCurrency } = useDualCurrencyFormatter();
    
    // Helper function to format currency
    const formatCurrency = (amount, accountCurrency, forcePrimary = false) => {
      try {
        if (accountCurrency && !forcePrimary) {
          // If account currency is provided and we're not forcing primary currency, use it to format
          return formatDualCurrency(amount, accountCurrency);
        }
        
        if (forcePrimary) {
          // When forcing primary currency, use the primary currency from store
          const primaryCurrency = store.getters['personalFinance/primaryCurrency'];
          // Handle cases where multiple accounts might lead to NaN or undefined
          if (isNaN(amount) || amount === undefined) {
            console.log('Invalid amount for formatting:', amount);
            return formatDualCurrency(0, primaryCurrency);
          }
          return formatDualCurrency(amount, primaryCurrency);
        }
        
        return formatDualCurrency(amount);
      } catch (error) {
        console.error('Error in formatCurrency:', error);
        return formatDualCurrency(0);
      }
    };
    
    // Get account type label
    const getAccountTypeLabel = (type) => {
      return store.getters.getTranslation(`finance.accountTypes.${type}`) || store.getters.getTranslation('common.account');
    };
    
    // Get account icon based on account type if none is set
    const getAccountIcon = (account) => {
      if (account.icon) return account.icon;
      
      const defaultIcons = {
        'cash': 'pi pi-money-bill',
        'bank': 'pi pi-building',
        'credit_card': 'pi pi-credit-card',
        'investment': 'pi pi-chart-line',
        'other': 'pi pi-wallet'
      };
      
      return defaultIcons[account.account_type] || 'pi pi-wallet';
    };
    
    return {
      showAccountForm,
      showDeleteConfirm,
      editMode,
      accountToDelete,
      accountHasTransactions,
      accountForm,
      formError, // Add formError to the returned properties
      isLoading,
      accounts,
      activeAccounts,
      totalBalance,
      assetAccounts,
      liabilityAccounts,
      incomeSourceAccounts,
      assetsTotal,
      liabilitiesTotal,
      incomeSourceTotal,
      netWorth,
      editAccount,
      saveAccount,
      deleteAccountConfirm,
      deleteAccount,
      handleAccountTypeChange, // Add the account type change handler
      formatCurrency,
      getAccountTypeLabel,
      getAccountIcon
    };
  }
};
</script>

<style lang="scss" scoped>
.accounts-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: $spacing-lg;
}

.accounts-container {
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  padding: $spacing-lg;
}

.accounts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
}

.accounts-title {
  margin: 0;
  color: $text-primary;
  font-size: $font-size-xl;
  font-weight: 600;
}

.add-button {
  display: flex;
  align-items: center;
  padding: $spacing-sm $spacing-md;
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
  
  i {
    margin-right: $spacing-xs;
  }
}

.accounts-overview {
  display: flex;
  gap: $spacing-lg;
  margin-bottom: $spacing-lg;
  
  @media (max-width: $breakpoint-sm) {
    flex-direction: column;
    gap: $spacing-md;
  }
}

.overview-card {
  background-color: $bg-secondary;
  border-radius: $border-radius;
  padding: $spacing-lg;
  flex: 1;
  
  &__title {
    margin-top: 0;
    margin-bottom: $spacing-sm;
    font-size: $font-size-md;
    color: $text-secondary;
  }
  
  &__value {
    font-size: 1.75rem;
    font-weight: 700;
    color: $primary-color;
    margin-bottom: $spacing-xs;
  }
  
  &__meta {
    font-size: $font-size-sm;
    color: $text-secondary;
  }
}

.accounts-sections {
  display: flex;
  flex-direction: column;
  gap: $spacing-xl;
}

.accounts-section {
  background-color: $bg-primary;
  border-radius: $border-radius;
  padding: $spacing-lg;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  
  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $spacing-md;
    padding-bottom: $spacing-sm;
    border-bottom: 1px solid $chart-grid;
  }
  
  &__title {
    display: flex;
    align-items: center;
    
    i {
      font-size: $font-size-lg;
      margin-right: $spacing-sm;
    }
    
    h2 {
      margin: 0;
      font-size: $font-size-lg;
      font-weight: 600;
      color: $text-primary;
      display: flex;
      align-items: center;
    }
    
  }
  
  &__total {
    font-size: $font-size-lg;
    font-weight: 700;
    color: $primary-color;
  }
}

.accounts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: $spacing-md;
}

.empty-category {
  grid-column: 1 / -1;
  text-align: center;
  padding: $spacing-md;
  color: $text-secondary;
  background-color: rgba($chart-grid, 0.3);
  border-radius: $border-radius;
  font-style: italic;
}

.net-worth-section {
  margin-top: $spacing-md;
}

.net-worth-card {
  background-color: $bg-primary;
  border-radius: $border-radius;
  padding: $spacing-lg;
  border-left: 4px solid $primary-color;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  
  &__title {
    margin-top: 0;
    margin-bottom: $spacing-sm;
    font-size: $font-size-lg;
    font-weight: 600;
    color: $text-primary;
  }
  
  &__value {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: $spacing-xs;
    
    &.positive {
      color: #4CAF50;
    }
    
    &.negative {
      color: #F44336;
    }
  }
  
  &__formula {
    font-size: $font-size-sm;
    color: $text-secondary;
    font-style: italic;
  }
}

.account-card {
  background-color: $bg-primary;
  border-radius: $border-radius;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: $transition-quick;
  position: relative;
  border: 1px solid $chart-grid;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: $box-shadow-hover;
  }
  
  &__header {
    background-color: $primary-color;
    color: white;
    padding: $spacing-md;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    
    i {
      font-size: $font-size-xl;
      z-index: 1;
    }
    
    &::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(to bottom, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.1));
      pointer-events: none;
    }
  }
  
  &__type {
    font-size: $font-size-sm;
    opacity: 0.9;
    font-weight: 600;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
    position: relative;
    z-index: 1;
    margin-right: 70px; /* Make room for the action buttons */
  }
  
  &__content {
    padding: $spacing-md;
    background-color: $bg-secondary;
  }
  
  &__name {
    font-size: $font-size-md;
    font-weight: 600;
    margin: 0 0 $spacing-sm 0;
    color: $text-primary;
  }
  
  &__balance {
    font-size: $font-size-lg;
    font-weight: 700;
    margin-bottom: $spacing-xs;
    color: $text-primary;
  }
  
  &__currency {
    font-size: $font-size-sm;
    color: $text-primary;
    font-weight: 500;
  }
  
  &__cashflow {
    font-size: $font-size-sm;
    color: #4CAF50;
    margin-top: $spacing-xs;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  
  &__actions {
    position: absolute;
    top: $spacing-md;
    right: $spacing-md;
    display: flex;
    gap: $spacing-xs;
    z-index: 2;
    
    .action-button {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: rgba(0, 0, 0, 0.3);
      border: none;
      color: white;
      cursor: pointer;
      transition: $transition-quick;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
      
      &:hover {
        background-color: rgba(0, 0, 0, 0.5);
      }
      
      &.delete:hover {
        background-color: rgba(255, 0, 0, 0.5);
      }
    }
  }
  
  &.inactive {
    opacity: 0.6;
    
    &::after {
      content: attr(data-inactive-text);
      position: absolute;
      top: 10px;
      left: 10px;
      background-color: rgba(0, 0, 0, 0.7);
      color: white;
      font-size: $font-size-xs;
      padding: 3px 8px;
      border-radius: 4px;
      font-weight: 600;
      z-index: 3;
    }
  }
}

// Modal styles
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-container {
  position: relative;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  z-index: 1001;
  
  &.confirm-dialog {
    max-width: 400px;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-md $spacing-lg;
  border-bottom: 1px solid $chart-grid;
  
  h3 {
    margin: 0;
    color: $text-primary;
    font-size: $font-size-lg;
  }
}

.close-button {
  background: none;
  border: none;
  font-size: $font-size-md;
  color: $text-secondary;
  cursor: pointer;
  transition: $transition-quick;
  
  &:hover {
    color: $text-primary;
  }
}

.modal-body {
  padding: $spacing-lg;
}

.form-error-message {
  background-color: rgba($negative, 0.1);
  border-left: 4px solid $negative;
  padding: $spacing-md;
  margin-bottom: $spacing-md;
  display: flex;
  align-items: center;
  border-radius: $border-radius;
  
  i {
    color: $negative;
    margin-right: $spacing-sm;
    font-size: $font-size-md;
  }
  
  span {
    color: $text-primary;
    font-size: $font-size-md;
  }
}

// Form styles
.account-form {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-md;
  
  @media (max-width: $breakpoint-sm) {
    grid-template-columns: 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  
  label {
    font-size: $font-size-sm;
    margin-bottom: $spacing-xs;
    color: $text-secondary;
    font-weight: 500;
  }
  
  input, select {
    padding: $spacing-sm;
    border: 1px solid $chart-grid;
    border-radius: $border-radius;
    font-size: $font-size-md;
    transition: $transition-quick;
    
    &:focus {
      border-color: $primary-color;
      outline: none;
    }
  }
  
  input[type="color"] {
    height: 40px;
    cursor: pointer;
  }
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  margin-bottom: $spacing-xs;
  
  input[type="checkbox"],
  input[type="radio"] {
    margin-right: $spacing-sm;
  }
  
  .checkbox-text {
    font-size: $font-size-md;
    color: $text-primary;
  }
}

.classification-grid {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
  padding: $spacing-md 0;
  border-top: 1px solid $chart-grid;
  border-bottom: 1px solid $chart-grid;
  margin: $spacing-sm 0;
}

.income-section .account-card__header {
  background-color: #42A5F5;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: $spacing-md;
  margin-top: $spacing-md;
}

.button {
  padding: $spacing-sm $spacing-lg;
  border-radius: $border-radius;
  font-weight: 500;
  cursor: pointer;
  transition: $transition-quick;
  border: none;
  
  &--primary {
    background-color: $primary-color;
    color: white;
    
    &:hover {
      background-color: $primary-dark;
    }
  }
  
  &--secondary {
    background-color: $bg-secondary;
    color: $text-primary;
    
    &:hover {
      background-color: darken($bg-secondary, 5%);
    }
  }
  
  &--delete {
    background-color: $negative;
    color: white;
    
    &:hover {
      background-color: darken($negative, 10%);
    }
  }
}

.delete-details {
  display: flex;
  justify-content: space-between;
  padding: $spacing-md;
  background-color: $bg-secondary;
  border-radius: $border-radius;
  margin: $spacing-md 0;
}

.warning-box {
  display: flex;
  align-items: flex-start;
  padding: $spacing-md;
  background-color: rgba($warning, 0.1);
  border-left: 4px solid $warning;
  border-radius: $border-radius;
  margin: $spacing-md 0;
  
  i {
    color: $warning;
    margin-right: $spacing-sm;
    font-size: $font-size-md;
  }
  
  p {
    margin: 0;
    font-size: $font-size-sm;
    color: $text-primary;
  }
}

.financial-tips {
  background-color: $bg-secondary;
  border-radius: $border-radius;
  padding: $spacing-md;
  margin-bottom: $spacing-md;
  border-left: 3px solid $primary-color;
  
  h4 {
    font-size: $font-size-md;
    margin-top: 0;
    margin-bottom: $spacing-sm;
    color: $text-primary;
    display: flex;
    align-items: center;
    
    i {
      margin-right: $spacing-xs;
      color: $primary-color;
    }
  }
  
  .tip-item {
    margin-bottom: $spacing-sm;
    padding: $spacing-sm;
    border-radius: $border-radius;
    
    &:last-child {
      margin-bottom: 0;
    }
    
    &.asset {
      background-color: rgba(#4CAF50, 0.05);
      border-left: 3px solid #4CAF50;
    }
    
    &.liability {
      background-color: rgba(#F44336, 0.05);
      border-left: 3px solid #F44336;
    }
    
    &.rule {
      background-color: rgba(#f7941d, 0.05);
      border-left: 3px solid #f7941d;
    }
    
    &.cash-flow {
      background-color: rgba(#42A5F5, 0.05);
      border-left: 3px solid #42A5F5;
    }
    
    .tip-header {
      font-weight: 600;
      margin-bottom: $spacing-xs;
      display: flex;
      align-items: center;
      
      i {
        margin-right: $spacing-xs;
      }
      
      span {
        color: $text-primary;
      }
    }
    
    p {
      margin: 0;
      font-size: $font-size-sm;
      color: $text-secondary;
      line-height: 1.4;
    }
  }
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: $spacing-xl;
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba($primary-color, 0.2);
    border-radius: 50%;
    border-top-color: $primary-color;
    animation: spin 1s ease-in-out infinite;
    margin-bottom: $spacing-md;
  }
  
  p {
    color: $text-secondary;
  }
}

.empty-state {
  text-align: center;
  padding: $spacing-xl;
  color: $text-secondary;
  
  p {
    margin-bottom: $spacing-md;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>