<template>
  <div class="transactions-view">
    <finance-navigation />
    
    <div class="transactions-container">
      <div class="transactions-header">
        <h2 class="transactions-title">{{ $t('finance.transactions.title') }}</h2>
        
        <button @click="showTransactionForm = true" class="add-button">
          <i class="pi pi-plus"></i>
          <span>{{ $t('finance.transactions.add') }}</span>
        </button>
      </div>
      
      <div class="filters-row">
        <month-year-picker />
        
        <div class="filter-controls">
          <select v-model="filterType" class="filter-select">
            <option value="all">{{ $t('finance.transactions.types.all') }}</option>
            <option value="expense">{{ $t('finance.transactions.types.expense') }}</option>
            <option value="income">{{ $t('finance.transactions.types.income') }}</option>
            <option value="transfer">{{ $t('finance.transactions.types.transfer') }}</option>
          </select>
          
          <select v-model="filterAccount" class="filter-select">
            <option value="">{{ $t('finance.transactions.filters.allAccounts') }}</option>
            <option v-for="account in accounts" :key="account.id" :value="account.id">
              {{ account.name }}
            </option>
          </select>
          
          <select v-model="filterCategory" class="filter-select">
            <option value="">{{ $t('finance.transactions.filters.allCategories') }}</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>
      </div>
      
      <div v-if="isLoading" class="loading-spinner">
        <div class="spinner"></div>
        <p>{{ $t('finance.transactions.loading') }}</p>
      </div>
      
      <div v-else-if="filteredTransactions.length" class="transactions-list">
        <div class="transaction-row header">
          <div class="transaction-date">{{ $t('finance.transactions.fields.date') }}</div>
          <div class="transaction-description">{{ $t('finance.transactions.fields.description') }}</div>
          <div class="transaction-category">{{ $t('finance.transactions.fields.category') }}</div>
          <div class="transaction-account">{{ $t('finance.transactions.fields.account') }}</div>
          <div class="transaction-amount">{{ $t('finance.transactions.fields.amount') }}</div>
          <div class="transaction-actions">{{ $t('finance.transactions.fields.actions') }}</div>
        </div>
        
        <div 
          v-for="transaction in filteredTransactions" 
          :key="transaction.id"
          class="transaction-row"
        >
          <div class="transaction-date">{{ formatDate(transaction.date) }}</div>
          
          <div class="transaction-description">
            <div class="transaction-icon"
                :style="{ backgroundColor: transaction.category_color || '#e08200' }"
            >
              <i :class="getTransactionIcon(transaction)"></i>
            </div>
            {{ transaction.description }}
          </div>
          
          <div class="transaction-category">
            {{ transaction.category_name || 'Uncategorized' }}
          </div>
          
          <div class="transaction-account">
            {{ transaction.account_name }}
            <span v-if="transaction.is_transfer">
              → {{ transaction.to_account_name }}
            </span>
          </div>
          
          <div class="transaction-amount"
              :class="{
                'amount--negative': transaction.is_expense && !transaction.is_transfer,
                'amount--positive': transaction.is_income && !transaction.is_transfer,
                'amount--transfer': transaction.is_transfer
              }"
          >
            {{ formatCurrency(transaction.amount, transaction.account_currency) }}
          </div>
          
          <div class="transaction-actions">
            <button @click="editTransaction(transaction)" class="action-button">
              <i class="pi pi-pencil"></i>
            </button>
            <button @click="deleteTransactionConfirm(transaction)" class="action-button delete">
              <i class="pi pi-trash"></i>
            </button>
          </div>
        </div>
      </div>
      
      <div v-else class="empty-state">
        <p>{{ $t('finance.transactions.noTransactionsFound') }}</p>
        <button @click="showTransactionForm = true" class="button button--primary">
          {{ $t('finance.transactions.addFirst') }}
        </button>
      </div>
      
      <!-- Transaction Form Modal -->
      <div class="modal" v-if="showTransactionForm">
        <div class="modal-overlay" @click="showTransactionForm = false"></div>
        <div class="modal-container">
          <div class="modal-header">
            <h3>{{ editMode ? $t('finance.transactions.edit') : $t('finance.transactions.add') }}</h3>
            <button @click="showTransactionForm = false" class="close-button">
              <i class="pi pi-times"></i>
            </button>
          </div>
          
          <div class="modal-body">
            <form @submit.prevent="saveTransaction" class="transaction-form">
              <!-- Transaction Type -->
              <div class="form-group transaction-type-selector">
                <label>{{ $t('finance.transactions.form.transactionType') }}</label>
                <div class="transaction-types">
                  <button 
                    type="button"
                    class="type-button" 
                    :class="{ active: transactionForm.is_expense && !transactionForm.is_transfer }"
                    @click="selectTransactionType('expense')"
                  >
                    <i class="pi pi-arrow-down"></i>
                    <span>{{ $t('finance.transactions.types.expense') }}</span>
                  </button>
                  
                  <button 
                    type="button"
                    class="type-button" 
                    :class="{ active: transactionForm.is_income && !transactionForm.is_transfer }"
                    @click="selectTransactionType('income')"
                  >
                    <i class="pi pi-arrow-up"></i>
                    <span>{{ $t('finance.transactions.types.income') }}</span>
                  </button>
                  
                  <button 
                    type="button"
                    class="type-button" 
                    :class="{ active: transactionForm.is_transfer }"
                    @click="selectTransactionType('transfer')"
                  >
                    <i class="pi pi-sync"></i>
                    <span>{{ $t('finance.transactions.types.transfer') }}</span>
                  </button>
                </div>
              </div>
              
              <!-- Amount and Date -->
              <div class="form-row">
                <div class="form-group">
                  <label for="amount">{{ $t('finance.transactions.form.amount') }}</label>
                  <input type="number" id="amount" v-model="transactionForm.amount" step="0.01" min="0.01" required>
                </div>
                
                <div class="form-group">
                  <label for="date">{{ $t('finance.transactions.form.date') }}</label>
                  <input type="date" id="date" v-model="transactionForm.date" required>
                </div>
              </div>
              
              <!-- Description -->
              <div class="form-group">
                <label for="description">{{ $t('finance.transactions.form.description') }}</label>
                <input type="text" id="description" v-model="transactionForm.description" required>
              </div>
              
              <!-- Account Selection -->
              <div class="form-row" v-if="!transactionForm.is_transfer">
                <div class="form-group">
                  <label for="account">{{ $t('finance.transactions.form.account') }}</label>
                  <select id="account" v-model="transactionForm.account" required>
                    <option value="" disabled>{{ $t('finance.transactions.form.selectAccount') }}</option>
                    <option v-for="account in accounts" :key="account.id" :value="account.id">
                      {{ account.name }}
                    </option>
                  </select>
                </div>
                
                <div class="form-group" v-if="!transactionForm.is_transfer">
                  <label for="category">{{ $t('finance.transactions.form.category') }}</label>
                  <select id="category" v-model="transactionForm.category">
                    <option value="" disabled>{{ $t('finance.transactions.form.selectCategory') }}</option>
                    <option v-for="category in filteredCategories" :key="category.id" :value="category.id">
                      {{ category.name }}
                    </option>
                  </select>
                </div>
              </div>
              
              <!-- Transfer Accounts -->
              <div class="form-row" v-if="transactionForm.is_transfer">
                <div class="form-group">
                  <label for="from-account">{{ $t('finance.transactions.form.fromAccount') }}</label>
                  <select id="from-account" v-model="transactionForm.account" required>
                    <option value="" disabled>{{ $t('finance.transactions.form.selectAccount') }}</option>
                    <option v-for="account in accounts" :key="account.id" :value="account.id">
                      {{ account.name }}
                    </option>
                  </select>
                </div>
                
                <div class="form-group">
                  <label for="to-account">{{ $t('finance.transactions.form.toAccount') }}</label>
                  <select id="to-account" v-model="transactionForm.to_account" required>
                    <option value="" disabled>{{ $t('finance.transactions.form.selectAccount') }}</option>
                    <option v-for="account in toAccounts" :key="account.id" :value="account.id">
                      {{ account.name }}
                    </option>
                  </select>
                </div>
              </div>
              
              <!-- Form Actions -->
              <div class="form-actions">
                <button type="button" @click="showTransactionForm = false" class="button button--secondary">
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
            <p>{{ $t('finance.transactions.confirmDelete') }}</p>
            <p v-if="transactionToDelete" class="delete-details">
              <strong>{{ transactionToDelete.description }}</strong>
              <span>{{ formatCurrency(transactionToDelete.amount, transactionToDelete.account_currency) }}</span>
            </p>
            
            <div class="form-actions">
              <button @click="showDeleteConfirm = false" class="button button--secondary">
                {{ $t('common.cancel') }}
              </button>
              <button @click="deleteTransaction" class="button button--delete">
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
import { ref, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';
import FinanceNavigation from '@/components/finance/FinanceNavigation.vue';
import MonthYearPicker from '@/components/finance/MonthYearPicker.vue';
import { useDualCurrencyFormatter } from '@/utils/currencyUtils';

export default {
  name: 'TransactionsView',
  
  components: {
    FinanceNavigation,
    MonthYearPicker
  },
  
  setup() {
    const store = useStore();
    const { locale } = useI18n();
    
    // State
    const showTransactionForm = ref(false);
    const showDeleteConfirm = ref(false);
    const editMode = ref(false);
    const transactionToDelete = ref(null);
    const filterType = ref('all');
    const filterAccount = ref('');
    const filterCategory = ref('');
    
    // Default form values
    const defaultForm = {
      amount: '',
      date: new Date().toISOString().split('T')[0],
      description: '',
      category: '',
      account: '',
      to_account: '',
      is_expense: true,
      is_income: false,
      is_transfer: false
    };
    
    // Form model
    const transactionForm = ref({ ...defaultForm });
    
    // Store getters
    const isLoading = computed(() => store.getters['personalFinance/isLoading']);
    const transactions = computed(() => store.getters['personalFinance/transactions']);
    const categories = computed(() => store.getters['personalFinance/categories']);
    const accounts = computed(() => store.getters['personalFinance/accounts']);
    
    // Computed properties
    const filteredTransactions = computed(() => {
      let result = [...transactions.value];
      
      // Filter by type
      if (filterType.value !== 'all') {
        if (filterType.value === 'expense') {
          result = result.filter(t => t.is_expense && !t.is_transfer);
        } else if (filterType.value === 'income') {
          result = result.filter(t => t.is_income && !t.is_transfer);
        } else if (filterType.value === 'transfer') {
          result = result.filter(t => t.is_transfer);
        }
      }
      
      // Filter by account
      if (filterAccount.value) {
        result = result.filter(t => t.account === parseInt(filterAccount.value));
      }
      
      // Filter by category
      if (filterCategory.value) {
        result = result.filter(t => t.category === parseInt(filterCategory.value));
      }
      
      return result;
    });
    
    // Get categories filtered by transaction type
    const filteredCategories = computed(() => {
      if (transactionForm.value.is_expense) {
        return categories.value.filter(cat => cat.is_expense);
      } else if (transactionForm.value.is_income) {
        return categories.value.filter(cat => cat.is_income);
      }
      return [];
    });
    
    // Get available "to" accounts for transfers (excluding the "from" account)
    const toAccounts = computed(() => {
      return accounts.value.filter(acc => acc.id !== transactionForm.value.account);
    });
    
    // Initialize data
    onMounted(async () => {
      if (categories.value.length === 0) {
        await store.dispatch('personalFinance/fetchCategories');
      }
      
      if (accounts.value.length === 0) {
        await store.dispatch('personalFinance/fetchAccounts');
      }
      
      await store.dispatch('personalFinance/fetchTransactions');
    });
    
    // Watch for account changes in transfer mode to reset to_account if it's the same
    watch(() => transactionForm.value.account, (newAccount) => {
      if (transactionForm.value.is_transfer && transactionForm.value.to_account === newAccount) {
        transactionForm.value.to_account = '';
      }
    });
    
    // Transaction type selection
    const selectTransactionType = (type) => {
      if (type === 'expense') {
        transactionForm.value.is_expense = true;
        transactionForm.value.is_income = false;
        transactionForm.value.is_transfer = false;
      } else if (type === 'income') {
        transactionForm.value.is_expense = false;
        transactionForm.value.is_income = true;
        transactionForm.value.is_transfer = false;
      } else if (type === 'transfer') {
        transactionForm.value.is_expense = false;
        transactionForm.value.is_income = false;
        transactionForm.value.is_transfer = true;
        transactionForm.value.to_account = '';
      }
      
      // Reset category when changing type
      transactionForm.value.category = '';
    };
    
    // Edit transaction
    const editTransaction = (transaction) => {
      editMode.value = true;
      
      transactionForm.value = {
        id: transaction.id,
        amount: transaction.amount,
        date: transaction.date,
        description: transaction.description,
        category: transaction.category || '',
        account: transaction.account,
        to_account: transaction.to_account || '',
        is_expense: transaction.is_expense,
        is_income: transaction.is_income,
        is_transfer: transaction.is_transfer
      };
      
      showTransactionForm.value = true;
    };
    
    // Save transaction (create or update)
    const saveTransaction = async () => {
      try {
        if (editMode.value) {
          // Update existing transaction
          await store.dispatch('personalFinance/updateTransaction', {
            id: transactionForm.value.id,
            data: { ...transactionForm.value }
          });
        } else {
          // Create new transaction
          await store.dispatch('personalFinance/createTransaction', { ...transactionForm.value });
        }
        
        // Reset form and close modal
        resetForm();
        showTransactionForm.value = false;
      } catch (error) {
        console.error('Error saving transaction:', error);
        // Error handling would go here
      }
    };
    
    // Confirm transaction delete
    const deleteTransactionConfirm = (transaction) => {
      transactionToDelete.value = transaction;
      showDeleteConfirm.value = true;
    };
    
    // Delete transaction
    const deleteTransaction = async () => {
      if (!transactionToDelete.value) return;
      
      try {
        await store.dispatch('personalFinance/deleteTransaction', transactionToDelete.value.id);
        showDeleteConfirm.value = false;
        transactionToDelete.value = null;
      } catch (error) {
        console.error('Error deleting transaction:', error);
        // Error handling would go here
      }
    };
    
    // Reset form to defaults
    const resetForm = () => {
      editMode.value = false;
      transactionForm.value = { ...defaultForm };
      transactionForm.value.date = new Date().toISOString().split('T')[0];
    };
    
    // Use the dual currency formatter
    const { formatDualCurrency } = useDualCurrencyFormatter();
    
    // Helper function to format currency
    const formatCurrency = (amount, currency) => {
      if (currency) {
        return formatDualCurrency(amount, currency);
      }
      return formatDualCurrency(amount);
    };
    
    // Helper function to format dates
    const formatDate = (dateString) => {
      const dateLocale = locale.value === 'ru' ? 'ru-RU' : 'en-US';
      const date = new Date(dateString);
      
      return new Intl.DateTimeFormat(dateLocale, {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      }).format(date);
    };
    
    // Helper function to get transaction icon
    const getTransactionIcon = (transaction) => {
      if (transaction.is_transfer) return 'pi pi-sync';
      if (transaction.is_income) return 'pi pi-arrow-up';
      return 'pi pi-arrow-down';
    };
    
    return {
      showTransactionForm,
      showDeleteConfirm,
      editMode,
      transactionToDelete,
      transactionForm,
      filterType,
      filterAccount,
      filterCategory,
      isLoading,
      transactions,
      filteredTransactions,
      categories,
      filteredCategories,
      accounts,
      toAccounts,
      selectTransactionType,
      editTransaction,
      saveTransaction,
      deleteTransactionConfirm,
      deleteTransaction,
      formatCurrency,
      formatDate,
      getTransactionIcon
    };
  }
};
</script>

<style lang="scss" scoped>
.transactions-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: $spacing-lg;
}

.transactions-container {
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  padding: $spacing-lg;
}

.transactions-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-md;
}

.transactions-title {
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

.filters-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
  flex-wrap: wrap;
  gap: $spacing-md;
}

.filter-controls {
  display: flex;
  gap: $spacing-sm;
  flex-wrap: wrap;
}

.filter-select {
  padding: $spacing-xs $spacing-sm;
  border: 1px solid $chart-grid;
  border-radius: $border-radius;
  background-color: $bg-primary;
  color: $text-primary;
  font-size: $font-size-sm;
  outline: none;
  transition: $transition-quick;
  
  &:focus {
    border-color: $primary-color;
  }
}

.transactions-list {
  border: 1px solid $chart-grid;
  border-radius: $border-radius;
  overflow: hidden;
}

.transaction-row {
  display: grid;
  grid-template-columns: 100px 2fr 1fr 1fr 1fr 80px;
  padding: $spacing-sm $spacing-md;
  border-bottom: 1px solid $chart-grid;
  align-items: center;
  
  &:last-child {
    border-bottom: none;
  }
  
  &.header {
    background-color: $bg-secondary;
    font-weight: 600;
    color: $text-primary;
  }
  
  &:not(.header):hover {
    background-color: rgba($primary-color, 0.05);
  }
}

.transaction-date,
.transaction-description,
.transaction-category,
.transaction-account,
.transaction-amount,
.transaction-actions {
  padding: $spacing-xs;
}

.transaction-description {
  display: flex;
  align-items: center;
}

.transaction-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: $primary-color;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: $spacing-sm;
  
  i {
    color: white;
    font-size: 12px;
  }
}

.transaction-amount {
  font-weight: 600;
  
  &.amount--negative {
    color: $negative;
  }
  
  &.amount--positive {
    color: $positive;
  }
  
  &.amount--transfer {
    color: $primary-color;
  }
}

.transaction-actions {
  display: flex;
  gap: $spacing-xs;
}

.action-button {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  color: $text-secondary;
  cursor: pointer;
  transition: $transition-quick;
  
  &:hover {
    color: $primary-color;
    background-color: rgba($primary-color, 0.1);
  }
  
  &.delete:hover {
    color: $negative;
    background-color: rgba($negative, 0.1);
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

// Form styles
.transaction-form {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-md;
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
}

.transaction-type-selector {
  margin-bottom: $spacing-sm;
}

.transaction-types {
  display: flex;
  gap: $spacing-xs;
}

.type-button {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-md;
  border: 1px solid $chart-grid;
  border-radius: $border-radius;
  background-color: $bg-primary;
  cursor: pointer;
  transition: $transition-quick;
  
  i {
    font-size: $font-size-md;
    margin-bottom: $spacing-xs;
    color: $text-secondary;
  }
  
  span {
    font-size: $font-size-sm;
    color: $text-primary;
  }
  
  &:hover {
    background-color: rgba($primary-color, 0.05);
  }
  
  &.active {
    border-color: $primary-color;
    background-color: rgba($primary-color, 0.1);
    
    i, span {
      color: $primary-color;
    }
  }
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

// Responsive styles
@media (max-width: $breakpoint-md) {
  .transaction-row {
    grid-template-columns: 1fr 1fr 1fr;
    
    &.header {
      display: none;
    }
    
    &:not(.header) {
      padding: $spacing-md;
      display: grid;
      grid-template-areas:
        "desc desc amount"
        "date cat actions"
        "account account account";
      row-gap: $spacing-sm;
    }
  }
  
  .transaction-description {
    grid-area: desc;
    font-weight: 500;
  }
  
  .transaction-amount {
    grid-area: amount;
    text-align: right;
  }
  
  .transaction-date {
    grid-area: date;
    font-size: $font-size-sm;
    color: $text-secondary;
  }
  
  .transaction-category {
    grid-area: cat;
    font-size: $font-size-sm;
    color: $text-secondary;
  }
  
  .transaction-account {
    grid-area: account;
    font-size: $font-size-sm;
    color: $text-secondary;
    margin-top: $spacing-xs;
  }
  
  .transaction-actions {
    grid-area: actions;
    justify-content: flex-end;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>