import { personalFinanceService, currencyService } from '@/services/api';

const state = {
  // Data
  categories: [],
  accounts: [],
  transactions: [],
  budgets: [],
  savingsGoals: [],
  financialSummary: null,

  // UI state
  selectedMonth: new Date().getMonth() + 1, // 1-12
  selectedYear: new Date().getFullYear(),

  // Currency settings
  currencySettings: {
    primaryCurrency: 'USD', // Default primary currency
    secondaryCurrency: 'GEL', // Default secondary currency
    showSecondaryCurrency: true, // Show amounts in secondary currency
    useApiExchangeRates: true, // Use API for exchange rates instead of manual values
    manualExchangeRates: {}, // Manual exchange rates relative to USD
    exchangeRates: {}, // API exchange rates
    historicalRates: {}, // Historical exchange rates by date
    lastRatesUpdate: null, // Timestamp of last rates update
  },

  // Loading & error states
  loadingCategories: false,
  loadingAccounts: false,
  loadingTransactions: false,
  loadingBudgets: false,
  loadingSavingsGoals: false,
  loadingSummary: false,
  loadingExchangeRates: false,
  error: null
};

const getters = {
  // Categories
  categories: state => state.categories,
  expenseCategories: state => state.categories.filter(cat => cat.is_expense),
  incomeCategories: state => state.categories.filter(cat => cat.is_income),

  // Accounts
  accounts: state => state.accounts,
  activeAccounts: state => state.accounts.filter(acc => acc.is_active),
  totalBalance: state => state.accounts.reduce((sum, acc) => sum + parseFloat(acc.balance), 0),

  // Currency settings
  currencySettings: state => state.currencySettings,
  primaryCurrency: state => state.currencySettings.primaryCurrency,
  secondaryCurrency: state => state.currencySettings.secondaryCurrency,
  showSecondaryCurrency: state => state.currencySettings.showSecondaryCurrency,
  useApiExchangeRates: state => state.currencySettings.useApiExchangeRates,
  manualExchangeRates: state => state.currencySettings.manualExchangeRates,
  exchangeRates: state => state.currencySettings.exchangeRates,

  // Get exchange rate for a specific currency
  getExchangeRate: (state) => (currency, date) => {
    if (currency === 'USD') return 1; // Base currency is USD, rate is 1

    // If a specific date is requested, try to use historical rates
    if (date && state.currencySettings.historicalRates[date]) {
      const historicalRate = state.currencySettings.historicalRates[date][currency];
      if (historicalRate) return historicalRate;
    }

    // Use either API or manual exchange rates based on settings
    const rates = state.currencySettings.useApiExchangeRates
      ? state.currencySettings.exchangeRates
      : state.currencySettings.manualExchangeRates;

    return rates[currency] || 1; // Default to 1 if rate not found
  },
  
  // Get historical rates for a specific date
  historicalRates: (state) => (date) => {
    return state.currencySettings.historicalRates[date] || {};
  },

  // Transactions
  transactions: state => state.transactions,
  expenses: state => state.transactions.filter(t => t.is_expense),
  incomes: state => state.transactions.filter(t => t.is_income),
  transfers: state => state.transactions.filter(t => t.is_transfer),

  // Budgets
  budgets: state => state.budgets,

  // Savings Goals
  savingsGoals: state => state.savingsGoals,

  // Summary
  financialSummary: state => state.financialSummary,

  // UI and Date selections
  selectedMonth: state => state.selectedMonth,
  selectedYear: state => state.selectedYear,

  // Current month's totals
  currentMonthExpenses: (state) => {
    if (state.financialSummary) return state.financialSummary.current_month_expenses;
    return 0;
  },

  currentMonthIncome: (state) => {
    if (state.financialSummary) return state.financialSummary.current_month_income;
    return 0;
  },

  // Loading states
  isLoading: state => (
    state.loadingCategories ||
    state.loadingAccounts ||
    state.loadingTransactions ||
    state.loadingBudgets ||
    state.loadingSavingsGoals ||
    state.loadingSummary
  ),

  hasError: state => !!state.error,
  error: state => state.error
};

const mutations = {
  // Currency settings mutations
  SET_PRIMARY_CURRENCY(state, currency) {
    state.currencySettings.primaryCurrency = currency;
  },

  SET_SECONDARY_CURRENCY(state, currency) {
    state.currencySettings.secondaryCurrency = currency;
  },

  SET_SHOW_SECONDARY_CURRENCY(state, show) {
    state.currencySettings.showSecondaryCurrency = show;
  },

  SET_USE_API_EXCHANGE_RATES(state, useApi) {
    state.currencySettings.useApiExchangeRates = useApi;
  },

  SET_MANUAL_EXCHANGE_RATE(state, { currency, rate }) {
    state.currencySettings.manualExchangeRates = {
      ...state.currencySettings.manualExchangeRates,
      [currency]: rate
    };
  },

  SET_EXCHANGE_RATES(state, rates) {
    state.currencySettings.exchangeRates = rates;
    state.currencySettings.lastRatesUpdate = new Date().toISOString();
  },

  SET_HISTORICAL_RATES(state, { date, rates }) {
    state.currencySettings.historicalRates = {
      ...state.currencySettings.historicalRates,
      [date]: rates
    };
  },

  SET_LOADING_EXCHANGE_RATES(state, loading) {
    state.loadingExchangeRates = loading;
  },

  // Categories mutations
  SET_CATEGORIES(state, categories) {
    state.categories = categories;
  },

  ADD_CATEGORY(state, category) {
    state.categories.push(category);
  },

  UPDATE_CATEGORY(state, updatedCategory) {
    const index = state.categories.findIndex(cat => cat.id === updatedCategory.id);
    if (index !== -1) {
      state.categories.splice(index, 1, updatedCategory);
    }
  },

  REMOVE_CATEGORY(state, categoryId) {
    state.categories = state.categories.filter(cat => cat.id !== categoryId);
  },

  // Accounts mutations
  SET_ACCOUNTS(state, accounts) {
    state.accounts = accounts;
  },

  ADD_ACCOUNT(state, account) {
    state.accounts.push(account);
  },

  UPDATE_ACCOUNT(state, updatedAccount) {
    const index = state.accounts.findIndex(acc => acc.id === updatedAccount.id);
    if (index !== -1) {
      state.accounts.splice(index, 1, updatedAccount);
    }
  },

  REMOVE_ACCOUNT(state, accountId) {
    state.accounts = state.accounts.filter(acc => acc.id !== accountId);
  },

  // Transactions mutations
  SET_TRANSACTIONS(state, transactions) {
    state.transactions = transactions;
  },

  ADD_TRANSACTION(state, transaction) {
    state.transactions.unshift(transaction); // Add to beginning
  },

  UPDATE_TRANSACTION(state, updatedTransaction) {
    const index = state.transactions.findIndex(t => t.id === updatedTransaction.id);
    if (index !== -1) {
      state.transactions.splice(index, 1, updatedTransaction);
    }
  },

  REMOVE_TRANSACTION(state, transactionId) {
    state.transactions = state.transactions.filter(t => t.id !== transactionId);
  },

  // Budgets mutations
  SET_BUDGETS(state, budgets) {
    state.budgets = budgets;
  },

  ADD_BUDGET(state, budget) {
    state.budgets.push(budget);
  },

  UPDATE_BUDGET(state, updatedBudget) {
    const index = state.budgets.findIndex(b => b.id === updatedBudget.id);
    if (index !== -1) {
      state.budgets.splice(index, 1, updatedBudget);
    }
  },

  REMOVE_BUDGET(state, budgetId) {
    state.budgets = state.budgets.filter(b => b.id !== budgetId);
  },

  // Savings Goals mutations
  SET_SAVINGS_GOALS(state, goals) {
    state.savingsGoals = goals;
  },

  ADD_SAVINGS_GOAL(state, goal) {
    state.savingsGoals.push(goal);
  },

  UPDATE_SAVINGS_GOAL(state, updatedGoal) {
    const index = state.savingsGoals.findIndex(g => g.id === updatedGoal.id);
    if (index !== -1) {
      state.savingsGoals.splice(index, 1, updatedGoal);
    }
  },

  REMOVE_SAVINGS_GOAL(state, goalId) {
    state.savingsGoals = state.savingsGoals.filter(g => g.id !== goalId);
  },

  // Financial Summary mutations
  SET_FINANCIAL_SUMMARY(state, summary) {
    state.financialSummary = summary;
  },

  // Date selections
  SET_SELECTED_MONTH(state, month) {
    state.selectedMonth = month;
  },

  SET_SELECTED_YEAR(state, year) {
    state.selectedYear = year;
  },

  // Loading state mutations
  SET_LOADING_CATEGORIES(state, loading) {
    state.loadingCategories = loading;
  },

  SET_LOADING_ACCOUNTS(state, loading) {
    state.loadingAccounts = loading;
  },

  SET_LOADING_TRANSACTIONS(state, loading) {
    state.loadingTransactions = loading;
  },

  SET_LOADING_BUDGETS(state, loading) {
    state.loadingBudgets = loading;
  },

  SET_LOADING_SAVINGS_GOALS(state, loading) {
    state.loadingSavingsGoals = loading;
  },

  SET_LOADING_SUMMARY(state, loading) {
    state.loadingSummary = loading;
  },

  // Error handling
  SET_ERROR(state, error) {
    state.error = error;
  },

  CLEAR_ERROR(state) {
    state.error = null;
  }
};

const actions = {
  // Initialization
  async initPersonalFinance({ dispatch }) {
    await Promise.all([
      dispatch('fetchCategories'),
      dispatch('fetchAccounts'),
      dispatch('fetchFinancialSummary'),
      dispatch('fetchExchangeRates')
    ]);
  },

  // Currency settings actions
  async fetchExchangeRates({ commit }) {
    commit('SET_LOADING_EXCHANGE_RATES', true);
    commit('CLEAR_ERROR');

    try {
      const response = await currencyService.getExchangeRates();
      commit('SET_EXCHANGE_RATES', response.data);
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to fetch exchange rates');
      console.error('Error fetching exchange rates:', error);
    } finally {
      commit('SET_LOADING_EXCHANGE_RATES', false);
    }
  },

  async fetchHistoricalRates({ commit }, date) {
    commit('SET_LOADING_EXCHANGE_RATES', true);
    commit('CLEAR_ERROR');

    try {
      const response = await currencyService.getHistoricalRates(date);
      commit('SET_HISTORICAL_RATES', { date, rates: response.data });
      return response.data;
    } catch (error) {
      commit('SET_ERROR', `Failed to fetch historical rates for ${date}`);
      console.error(`Error fetching historical rates for ${date}:`, error);
      return null;
    } finally {
      commit('SET_LOADING_EXCHANGE_RATES', false);
    }
  },

  setPrimaryCurrency({ commit }, currency) {
    commit('SET_PRIMARY_CURRENCY', currency);
    localStorage.setItem('primaryCurrency', currency);
  },

  setSecondaryCurrency({ commit }, currency) {
    commit('SET_SECONDARY_CURRENCY', currency);
    localStorage.setItem('secondaryCurrency', currency);
  },

  setShowSecondaryCurrency({ commit }, show) {
    commit('SET_SHOW_SECONDARY_CURRENCY', show);
    localStorage.setItem('showSecondaryCurrency', String(show));
  },

  setUseApiExchangeRates({ commit }, useApi) {
    commit('SET_USE_API_EXCHANGE_RATES', useApi);
    localStorage.setItem('useApiExchangeRates', String(useApi));
  },

  setManualExchangeRate({ commit }, { currency, rate }) {
    commit('SET_MANUAL_EXCHANGE_RATE', { currency, rate });

    // Update localStorage with all manual rates
    const currentRates = JSON.parse(localStorage.getItem('manualExchangeRates') || '{}');
    currentRates[currency] = rate;
    localStorage.setItem('manualExchangeRates', JSON.stringify(currentRates));
  },

  // Load currency settings from localStorage
  loadCurrencySettings({ commit }) {
    try {
      // Primary currency
      const primaryCurrency = localStorage.getItem('primaryCurrency');
      if (primaryCurrency) {
        commit('SET_PRIMARY_CURRENCY', primaryCurrency);
      }

      // Secondary currency
      const secondaryCurrency = localStorage.getItem('secondaryCurrency');
      if (secondaryCurrency) {
        commit('SET_SECONDARY_CURRENCY', secondaryCurrency);
      }

      // Show secondary currency
      const showSecondaryCurrency = localStorage.getItem('showSecondaryCurrency');
      if (showSecondaryCurrency !== null) {
        commit('SET_SHOW_SECONDARY_CURRENCY', showSecondaryCurrency === 'true');
      }

      // Use API exchange rates
      const useApiExchangeRates = localStorage.getItem('useApiExchangeRates');
      if (useApiExchangeRates !== null) {
        commit('SET_USE_API_EXCHANGE_RATES', useApiExchangeRates === 'true');
      }

      // Manual exchange rates
      const manualExchangeRates = localStorage.getItem('manualExchangeRates');
      if (manualExchangeRates) {
        try {
          const rates = JSON.parse(manualExchangeRates);
          Object.entries(rates).forEach(([currency, rate]) => {
            commit('SET_MANUAL_EXCHANGE_RATE', { currency, rate });
          });
        } catch (e) {
          console.error('Error parsing manual exchange rates from localStorage:', e);
        }
      }
    } catch (e) {
      console.error('Error loading currency settings from localStorage:', e);
    }
  },

  // Categories actions
  async fetchCategories({ commit }) {
    commit('SET_LOADING_CATEGORIES', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.getCategories();
      commit('SET_CATEGORIES', response.data);
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to fetch categories');
      console.error('Error fetching categories:', error);
    } finally {
      commit('SET_LOADING_CATEGORIES', false);
    }
  },

  async createCategory({ commit }, categoryData) {
    commit('SET_LOADING_CATEGORIES', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.createCategory(categoryData);
      commit('ADD_CATEGORY', response.data);
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to create category');
      console.error('Error creating category:', error);
      throw error;
    } finally {
      commit('SET_LOADING_CATEGORIES', false);
    }
  },

  async updateCategory({ commit }, { id, data }) {
    commit('SET_LOADING_CATEGORIES', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.updateCategory(id, data);
      commit('UPDATE_CATEGORY', response.data);
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to update category');
      console.error('Error updating category:', error);
      throw error;
    } finally {
      commit('SET_LOADING_CATEGORIES', false);
    }
  },

  async deleteCategory({ commit }, categoryId) {
    commit('SET_LOADING_CATEGORIES', true);
    commit('CLEAR_ERROR');

    try {
      await personalFinanceService.deleteCategory(categoryId);
      commit('REMOVE_CATEGORY', categoryId);
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to delete category');
      console.error('Error deleting category:', error);
      throw error;
    } finally {
      commit('SET_LOADING_CATEGORIES', false);
    }
  },

  // Accounts actions
  async fetchAccounts({ commit }) {
    commit('SET_LOADING_ACCOUNTS', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.getAccounts();
      commit('SET_ACCOUNTS', response.data);
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to fetch accounts');
      console.error('Error fetching accounts:', error);
    } finally {
      commit('SET_LOADING_ACCOUNTS', false);
    }
  },

  async createAccount({ commit }, accountData) {
    commit('SET_LOADING_ACCOUNTS', true);
    commit('CLEAR_ERROR');

    try {
      console.log('Store: Creating account with data:', accountData);
      const response = await personalFinanceService.createAccount(accountData);
      console.log('Store: Account created successfully:', response.data);
      commit('ADD_ACCOUNT', response.data);
      return response.data;
    } catch (error) {
      // Log the full error for debugging
      console.error('Store: Error creating account:', error);
      console.error('Response data:', error.response?.data);

      let errorMessage = 'Failed to create account';

      if (error.response?.data) {
        const errorData = error.response.data;

        // Check for validation errors
        if (errorData.error) {
          errorMessage = errorData.error;
        } else if (errorData.detail) {
          errorMessage = errorData.detail;
        } else if (errorData.non_field_errors) {
          errorMessage = errorData.non_field_errors.join(', ');
        } else {
          // Check for field-specific errors
          const fieldErrors = [];

          for (const [field, errors] of Object.entries(errorData)) {
            if (Array.isArray(errors)) {
              fieldErrors.push(`${field}: ${errors.join(', ')}`);
            }
          }

          if (fieldErrors.length > 0) {
            errorMessage = fieldErrors.join('; ');
          }
        }
      }

      commit('SET_ERROR', errorMessage);
      throw error;
    } finally {
      commit('SET_LOADING_ACCOUNTS', false);
    }
  },

  async updateAccount({ commit }, { id, data }) {
    commit('SET_LOADING_ACCOUNTS', true);
    commit('CLEAR_ERROR');

    try {
      console.log('Store: Updating account with ID:', id, 'and data:', data);
      const response = await personalFinanceService.updateAccount(id, data);
      console.log('Store: Account updated successfully:', response.data);
      commit('UPDATE_ACCOUNT', response.data);
      return response.data;
    } catch (error) {
      // Log the full error for debugging
      console.error('Store: Error updating account:', error);
      console.error('Response data:', error.response?.data);

      let errorMessage = 'Failed to update account';

      if (error.response?.data) {
        const errorData = error.response.data;

        // Check for validation errors
        if (errorData.error) {
          errorMessage = errorData.error;
        } else if (errorData.detail) {
          errorMessage = errorData.detail;
        } else if (errorData.non_field_errors) {
          errorMessage = errorData.non_field_errors.join(', ');
        } else {
          // Check for field-specific errors
          const fieldErrors = [];

          for (const [field, errors] of Object.entries(errorData)) {
            if (Array.isArray(errors)) {
              fieldErrors.push(`${field}: ${errors.join(', ')}`);
            }
          }

          if (fieldErrors.length > 0) {
            errorMessage = fieldErrors.join('; ');
          }
        }
      }

      commit('SET_ERROR', errorMessage);
      throw error;
    } finally {
      commit('SET_LOADING_ACCOUNTS', false);
    }
  },

  async deleteAccount({ commit }, accountId) {
    commit('SET_LOADING_ACCOUNTS', true);
    commit('CLEAR_ERROR');

    try {
      await personalFinanceService.deleteAccount(accountId);
      commit('REMOVE_ACCOUNT', accountId);
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to delete account');
      console.error('Error deleting account:', error);
      throw error;
    } finally {
      commit('SET_LOADING_ACCOUNTS', false);
    }
  },

  // Transactions actions
  async fetchTransactions({ commit, state }, params = {}) {
    commit('SET_LOADING_TRANSACTIONS', true);
    commit('CLEAR_ERROR');

    // If no specific month/year provided in params, use the selected ones
    if (!params.month && !params.year) {
      params.month = state.selectedMonth;
      params.year = state.selectedYear;
    }

    try {
      const response = await personalFinanceService.getTransactions(params);
      commit('SET_TRANSACTIONS', response.data);
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to fetch transactions');
      console.error('Error fetching transactions:', error);
    } finally {
      commit('SET_LOADING_TRANSACTIONS', false);
    }
  },

  async createTransaction({ commit, dispatch }, transactionData) {
    commit('SET_LOADING_TRANSACTIONS', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.createTransaction(transactionData);
      commit('ADD_TRANSACTION', response.data);

      // Refresh accounts to get updated balances
      dispatch('fetchAccounts');

      // Refresh financial summary
      dispatch('fetchFinancialSummary');

      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to create transaction');
      console.error('Error creating transaction:', error);
      throw error;
    } finally {
      commit('SET_LOADING_TRANSACTIONS', false);
    }
  },

  async updateTransaction({ commit, dispatch }, { id, data }) {
    commit('SET_LOADING_TRANSACTIONS', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.updateTransaction(id, data);
      commit('UPDATE_TRANSACTION', response.data);

      // Refresh accounts to get updated balances
      dispatch('fetchAccounts');

      // Refresh financial summary
      dispatch('fetchFinancialSummary');

      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to update transaction');
      console.error('Error updating transaction:', error);
      throw error;
    } finally {
      commit('SET_LOADING_TRANSACTIONS', false);
    }
  },

  async deleteTransaction({ commit, dispatch }, transactionId) {
    commit('SET_LOADING_TRANSACTIONS', true);
    commit('CLEAR_ERROR');

    try {
      await personalFinanceService.deleteTransaction(transactionId);
      commit('REMOVE_TRANSACTION', transactionId);

      // Refresh accounts to get updated balances
      dispatch('fetchAccounts');

      // Refresh financial summary
      dispatch('fetchFinancialSummary');
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to delete transaction');
      console.error('Error deleting transaction:', error);
      throw error;
    } finally {
      commit('SET_LOADING_TRANSACTIONS', false);
    }
  },

  // Budgets actions
  async fetchBudgets({ commit, state }, params = {}) {
    commit('SET_LOADING_BUDGETS', true);
    commit('CLEAR_ERROR');

    // If no specific month/year provided in params, use the selected ones
    if (!params.month && !params.year) {
      params.month = state.selectedMonth;
      params.year = state.selectedYear;
    }

    try {
      const response = await personalFinanceService.getBudgets(params);
      commit('SET_BUDGETS', response.data);
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to fetch budgets');
      console.error('Error fetching budgets:', error);
      return [];
    } finally {
      commit('SET_LOADING_BUDGETS', false);
    }
  },
  
  // Fetch previous budgets (for templates)
  async fetchPreviousBudgets({ dispatch }, { currentMonth, currentYear }) {
    try {
      // Create an array to hold previous budgets
      let previousBudgets = [];
      
      // Get budgets from the previous month
      const prevMonth = currentMonth === 1 ? 12 : currentMonth - 1;
      const prevYear = currentMonth === 1 ? currentYear - 1 : currentYear;
      
      const prevMonthBudgets = await dispatch('fetchBudgets', {
        month: prevMonth,
        year: prevYear,
        only_parent: true
      });
      
      if (prevMonthBudgets && prevMonthBudgets.length > 0) {
        previousBudgets = [...previousBudgets, ...prevMonthBudgets];
      }
      
      // Get budgets from two months ago
      const twoMonthsAgoMonth = prevMonth === 1 ? 12 : prevMonth - 1;
      const twoMonthsAgoYear = prevMonth === 1 ? prevYear - 1 : prevYear;
      
      const twoMonthsAgoBudgets = await dispatch('fetchBudgets', {
        month: twoMonthsAgoMonth,
        year: twoMonthsAgoYear,
        only_parent: true
      });
      
      if (twoMonthsAgoBudgets && twoMonthsAgoBudgets.length > 0) {
        previousBudgets = [...previousBudgets, ...twoMonthsAgoBudgets];
      }
      
      return previousBudgets;
    } catch (error) {
      console.error('Error fetching previous budgets:', error);
      return [];
    }
  },

  async createBudget({ commit, dispatch }, budgetData) {
    commit('SET_LOADING_BUDGETS', true);
    commit('CLEAR_ERROR');

    try {
      // Check if this is a parent budget with subcategory budgets
      const subcategoryBudgets = budgetData.subcategory_budgets;
      const isParentBudget = budgetData.is_parent_budget;
      
      // Remove subcategory_budgets from data before creating parent budget
      if (subcategoryBudgets) {
        delete budgetData.subcategory_budgets;
      }
      
      // Create the parent budget
      const response = await personalFinanceService.createBudget(budgetData);
      commit('ADD_BUDGET', response.data);
      
      // If this is a parent budget and we have subcategory budgets, create them too
      if (isParentBudget && subcategoryBudgets && subcategoryBudgets.length > 0) {
        await dispatch('createSubcategoryBudgets', {
          parentBudgetId: response.data.id,
          subcategoryBudgets: subcategoryBudgets
        });
      }
      
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to create budget');
      console.error('Error creating budget:', error);
      throw error;
    } finally {
      commit('SET_LOADING_BUDGETS', false);
    }
  },
  
  async createSubcategoryBudgets({ commit }, { parentBudgetId, subcategoryBudgets }) {
    commit('SET_LOADING_BUDGETS', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.createSubcategoryBudgets(
        parentBudgetId, subcategoryBudgets
      );
      
      // Add each subcategory budget to the store
      if (response.data.subcategory_budgets) {
        response.data.subcategory_budgets.forEach(budget => {
          commit('ADD_BUDGET', budget);
        });
      }
      
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to create subcategory budgets');
      console.error('Error creating subcategory budgets:', error);
      throw error;
    } finally {
      commit('SET_LOADING_BUDGETS', false);
    }
  },
  
  async updateSubcategoryBudgets({ commit, dispatch }, { parentBudgetId, subcategoryBudgets }) {
    commit('SET_LOADING_BUDGETS', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.updateSubcategoryBudgets(
        parentBudgetId, subcategoryBudgets
      );
      
      // Update each subcategory budget in the store
      if (response.data.subcategory_budgets) {
        response.data.subcategory_budgets.forEach(budget => {
          commit('UPDATE_BUDGET', budget);
        });
      }
      
      // Refresh budgets to ensure we have the latest data
      await dispatch('fetchBudgets');
      
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to update subcategory budgets');
      console.error('Error updating subcategory budgets:', error);
      throw error;
    } finally {
      commit('SET_LOADING_BUDGETS', false);
    }
  },

  async updateBudget({ commit }, { id, data }) {
    commit('SET_LOADING_BUDGETS', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.updateBudget(id, data);
      commit('UPDATE_BUDGET', response.data);
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to update budget');
      console.error('Error updating budget:', error);
      throw error;
    } finally {
      commit('SET_LOADING_BUDGETS', false);
    }
  },

  async deleteBudget({ commit }, budgetId) {
    commit('SET_LOADING_BUDGETS', true);
    commit('CLEAR_ERROR');

    try {
      await personalFinanceService.deleteBudget(budgetId);
      commit('REMOVE_BUDGET', budgetId);
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to delete budget');
      console.error('Error deleting budget:', error);
      throw error;
    } finally {
      commit('SET_LOADING_BUDGETS', false);
    }
  },

  // Savings Goals actions
  async fetchSavingsGoals({ commit }) {
    commit('SET_LOADING_SAVINGS_GOALS', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.getSavingsGoals();
      commit('SET_SAVINGS_GOALS', response.data);
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to fetch savings goals');
      console.error('Error fetching savings goals:', error);
    } finally {
      commit('SET_LOADING_SAVINGS_GOALS', false);
    }
  },

  async createSavingsGoal({ commit }, goalData) {
    commit('SET_LOADING_SAVINGS_GOALS', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.createSavingsGoal(goalData);
      commit('ADD_SAVINGS_GOAL', response.data);
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to create savings goal');
      console.error('Error creating savings goal:', error);
      throw error;
    } finally {
      commit('SET_LOADING_SAVINGS_GOALS', false);
    }
  },

  async updateSavingsGoal({ commit }, { id, data }) {
    commit('SET_LOADING_SAVINGS_GOALS', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.updateSavingsGoal(id, data);
      commit('UPDATE_SAVINGS_GOAL', response.data);
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to update savings goal');
      console.error('Error updating savings goal:', error);
      throw error;
    } finally {
      commit('SET_LOADING_SAVINGS_GOALS', false);
    }
  },

  async deleteSavingsGoal({ commit }, goalId) {
    commit('SET_LOADING_SAVINGS_GOALS', true);
    commit('CLEAR_ERROR');

    try {
      await personalFinanceService.deleteSavingsGoal(goalId);
      commit('REMOVE_SAVINGS_GOAL', goalId);
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to delete savings goal');
      console.error('Error deleting savings goal:', error);
      throw error;
    } finally {
      commit('SET_LOADING_SAVINGS_GOALS', false);
    }
  },

  async addToSavingsGoal({ commit }, { id, amount }) {
    commit('SET_LOADING_SAVINGS_GOALS', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.addToSavingsGoal(id, amount);
      commit('UPDATE_SAVINGS_GOAL', response.data);
      return response.data;
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to add to savings goal');
      console.error('Error adding to savings goal:', error);
      throw error;
    } finally {
      commit('SET_LOADING_SAVINGS_GOALS', false);
    }
  },

  // Financial Summary actions
  async fetchFinancialSummary({ commit }) {
    commit('SET_LOADING_SUMMARY', true);
    commit('CLEAR_ERROR');

    try {
      const response = await personalFinanceService.getFinancialSummary();
      commit('SET_FINANCIAL_SUMMARY', response.data);
    } catch (error) {
      commit('SET_ERROR', error.response?.data?.detail || 'Failed to fetch financial summary');
      console.error('Error fetching financial summary:', error);
    } finally {
      commit('SET_LOADING_SUMMARY', false);
    }
  },

  // Date selection actions
  setSelectedMonth({ commit, dispatch }, month) {
    commit('SET_SELECTED_MONTH', month);
    dispatch('fetchTransactions');
    dispatch('fetchBudgets');
  },

  setSelectedYear({ commit, dispatch }, year) {
    commit('SET_SELECTED_YEAR', year);
    dispatch('fetchTransactions');
    dispatch('fetchBudgets');
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};