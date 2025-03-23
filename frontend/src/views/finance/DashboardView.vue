<template>
  <div class="finance-dashboard">
    <finance-navigation />
    
    <template v-if="isLoading">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>{{ $t('dashboard.loadingData') }}</p>
      </div>
    </template>
    
    <template v-else>
      <!-- Account Summary -->
      <section class="dashboard-section">
        <h2 class="section-title">{{ $t('dashboard.accountsSummary') }}</h2>
        <div class="account-cards">
          <div class="summary-card total-balance">
            <div class="summary-card__header">
              <i class="pi pi-wallet"></i>
              <h3>{{ $t('dashboard.totalBalance') }}</h3>
            </div>
            <div class="summary-card__value">{{ formatCurrency(totalBalance) }}</div>
            <div class="summary-card__footer">
              <router-link to="/finance/accounts" class="view-all-link">{{ $t('dashboard.viewAllAccounts') }}</router-link>
            </div>
          </div>
          
          <div class="summary-card income">
            <div class="summary-card__header">
              <i class="pi pi-arrow-up"></i>
              <h3>{{ $t('dashboard.monthIncome') }}</h3>
            </div>
            <div class="summary-card__value">{{ formatCurrency(currentMonthIncome) }}</div>
          </div>
          
          <div class="summary-card expenses">
            <div class="summary-card__header">
              <i class="pi pi-arrow-down"></i>
              <h3>{{ $t('dashboard.monthExpenses') }}</h3>
            </div>
            <div class="summary-card__value">{{ formatCurrency(currentMonthExpenses) }}</div>
          </div>
        </div>
      </section>
      
      <div class="dashboard-grid">
        <!-- Monthly Overview -->
        <section class="dashboard-section">
          <h2 class="section-title">{{ $t('dashboard.monthlyOverview') }}</h2>
          <month-year-picker />
          
          <div v-if="hasFinancialSummary && financialSummary.monthly_summary" class="chart-container">
            <canvas ref="monthlyChart" height="250"></canvas>
          </div>
          <div v-else class="empty-state">
            <p>{{ $t('dashboard.noMonthlyData') }}</p>
          </div>
        </section>
        
        <!-- Expense by Category -->
        <section class="dashboard-section">
          <h2 class="section-title">{{ $t('dashboard.expensesByCategory') }}</h2>
          
          <div v-if="hasFinancialSummary && financialSummary.expense_by_category?.length" class="chart-container">
            <canvas ref="categoryChart" height="250"></canvas>
          </div>
          <div v-else class="empty-state">
            <p>{{ $t('dashboard.noCategoryData') }}</p>
          </div>
        </section>
      </div>
      
      <!-- Recent Transactions -->
      <section class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">{{ $t('dashboard.recentTransactions') }}</h2>
          <router-link to="/finance/transactions" class="view-all-link">{{ $t('dashboard.viewAll') }}</router-link>
        </div>
        
        <div v-if="transactions.length" class="transactions-list">
          <div 
            v-for="transaction in recentTransactions" 
            :key="transaction.id" 
            class="transaction-item"
          >
            <div class="transaction-item__icon"
                :style="{ backgroundColor: transaction.category_color || '#e08200' }"
            >
              <i :class="getTransactionIcon(transaction)"></i>
            </div>
            
            <div class="transaction-item__details">
              <div class="transaction-item__title">{{ transaction.description }}</div>
              <div class="transaction-item__meta">
                <span>{{ formatDate(transaction.date) }}</span>
                <span>{{ transaction.category_name || 'Uncategorized' }}</span>
              </div>
            </div>
            
            <div class="transaction-item__amount" 
                :class="{
                  'amount--negative': transaction.is_expense && !transaction.is_transfer,
                  'amount--positive': transaction.is_income && !transaction.is_transfer,
                  'amount--transfer': transaction.is_transfer
                }"
            >
              {{ transaction.is_transfer ? $t('finance.transactions.types.transfer') : formatCurrency(transaction.amount) }}
            </div>
          </div>
        </div>
        
        <div v-else class="empty-state">
          <p>{{ $t('dashboard.noTransactionsYet') }}</p>
          <router-link to="/finance/transactions" class="button button--primary">
            {{ $t('dashboard.addFirstTransaction') }}
          </router-link>
        </div>
      </section>
      
      <!-- Savings Goals -->
      <section class="dashboard-section">
        <div class="section-header">
          <h2 class="section-title">{{ $t('dashboard.savingsGoals') }}</h2>
          <router-link to="/finance/goals" class="view-all-link">{{ $t('dashboard.viewAll') }}</router-link>
        </div>
        
        <div v-if="savingsGoals.length" class="savings-goals">
          <div 
            v-for="goal in savingsGoals" 
            :key="goal.id" 
            class="goal-card"
            :style="{ borderColor: goal.color }"
          >
            <h3 class="goal-card__title">{{ goal.name }}</h3>
            <div class="goal-card__amounts">
              <span>{{ formatCurrency(goal.current_amount) }}</span>
              <span>{{ $t('common.of') }} {{ formatCurrency(goal.target_amount) }}</span>
            </div>
            
            <div class="goal-card__progress">
              <div class="progress-bar">
                <div class="progress-bar__fill" 
                    :style="{ 
                      width: `${goal.progress_percentage}%`,
                      backgroundColor: goal.color 
                    }"
                ></div>
              </div>
              <div class="progress-bar__percentage">{{ goal.progress_percentage }}%</div>
            </div>
            
            <div v-if="goal.deadline" class="goal-card__deadline">
              {{ $t('dashboard.target') }}: {{ formatDate(goal.deadline) }}
            </div>
          </div>
        </div>
        
        <div v-else class="empty-state">
          <p>{{ $t('dashboard.noSavingsGoalsYet') }}</p>
          <router-link to="/finance/goals" class="button button--primary">
            {{ $t('dashboard.createFirstGoal') }}
          </router-link>
        </div>
      </section>
    </template>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';
import Chart from 'chart.js/auto';
import FinanceNavigation from '@/components/finance/FinanceNavigation.vue';
import MonthYearPicker from '@/components/finance/MonthYearPicker.vue';
import { useDualCurrencyFormatter } from '@/utils/currencyUtils';

export default {
  name: 'FinanceDashboardView',
  
  components: {
    FinanceNavigation,
    MonthYearPicker
  },
  
  setup() {
    const store = useStore();
    const monthlyChart = ref(null);
    const categoryChart = ref(null);
    let monthlyChartInstance = null;
    let categoryChartInstance = null;
    
    // Computed properties from store
    const isLoading = computed(() => store.getters['personalFinance/isLoading']);
    const totalBalance = computed(() => store.getters['personalFinance/totalBalance']);
    const currentMonthIncome = computed(() => store.getters['personalFinance/currentMonthIncome']);
    const currentMonthExpenses = computed(() => store.getters['personalFinance/currentMonthExpenses']);
    const transactions = computed(() => store.getters['personalFinance/transactions']);
    const recentTransactions = computed(() => transactions.value.slice(0, 5));
    const savingsGoals = computed(() => store.getters['personalFinance/savingsGoals']);
    const financialSummary = computed(() => store.getters['personalFinance/financialSummary']);
    const hasFinancialSummary = computed(() => !!financialSummary.value);
    
    // Initialize data
    onMounted(async () => {
      await store.dispatch('personalFinance/initPersonalFinance');
      await store.dispatch('personalFinance/fetchTransactions');
      await store.dispatch('personalFinance/fetchSavingsGoals');
      
      renderCharts();
    });
    
    // Watch for changes in financial summary to update charts
    watch(financialSummary, () => {
      renderCharts();
    });
    
    // Render charts
    const renderCharts = () => {
      if (hasFinancialSummary.value) {
        renderMonthlyChart();
        renderCategoryChart();
      }
    };
    
    // Render monthly income/expense chart
    const renderMonthlyChart = () => {
      if (!financialSummary.value?.monthly_summary || !monthlyChart.value) return;
      
      // Destroy existing chart instance if it exists
      if (monthlyChartInstance) {
        monthlyChartInstance.destroy();
      }
      
      const ctx = monthlyChart.value.getContext('2d');
      const monthlyData = financialSummary.value.monthly_summary;
      
      // Prepare data for chart
      const labels = monthlyData.map(data => {
        const date = new Date(data.year, data.month - 1);
        return date.toLocaleString(locale.value, { month: 'short' }) + ' ' + data.year;
      });
      
      const incomeData = monthlyData.map(data => data.income);
      const expenseData = monthlyData.map(data => data.expenses);
      
      // Create chart
      monthlyChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
              label: t('finance.transactions.types.income'),
              data: incomeData,
              backgroundColor: '#00c853',
              borderColor: '#00c853',
              borderWidth: 1
            },
            {
              label: t('finance.transactions.types.expense'),
              data: expenseData,
              backgroundColor: '#ff5252',
              borderColor: '#ff5252',
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: '#e0e0e0'
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          }
        }
      });
    };
    
    // Render expense by category chart
    const renderCategoryChart = () => {
      if (!financialSummary.value?.expense_by_category || !categoryChart.value) return;
      
      // Destroy existing chart instance if it exists
      if (categoryChartInstance) {
        categoryChartInstance.destroy();
      }
      
      const ctx = categoryChart.value.getContext('2d');
      const categoryData = financialSummary.value.expense_by_category;
      
      // Prepare data for chart
      const labels = categoryData.map(cat => cat.name);
      const data = categoryData.map(cat => cat.amount);
      const backgroundColors = categoryData.map(cat => cat.color || '#e08200');
      
      // Create chart
      categoryChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [
            {
              data: data,
              backgroundColor: backgroundColors,
              borderWidth: 1
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right'
            }
          }
        }
      });
    };
    
    // Import i18n
    const { t, locale } = useI18n();
    
    // Use the dual currency formatter
    const { formatDualCurrency } = useDualCurrencyFormatter();
    
    // Helper function to format currency
    const formatCurrency = (amount) => {
      return formatDualCurrency(amount);
    };
    
    // Helper function to format dates
    const formatDate = (dateString) => {
      const date = new Date(dateString);
      const dateLocale = locale.value === 'ru' ? 'ru-RU' : 'en-US';
      return new Intl.DateTimeFormat(dateLocale, {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      }).format(date);
    };
    
    // Helper function to get appropriate icon for transaction
    const getTransactionIcon = (transaction) => {
      if (transaction.is_transfer) return 'pi pi-sync';
      if (transaction.is_income) return 'pi pi-arrow-up';
      return 'pi pi-arrow-down';
    };
    
    return {
      isLoading,
      totalBalance,
      currentMonthIncome,
      currentMonthExpenses,
      transactions,
      recentTransactions,
      savingsGoals,
      financialSummary,
      hasFinancialSummary,
      monthlyChart,
      categoryChart,
      formatCurrency,
      formatDate,
      getTransactionIcon
    };
  }
};
</script>

<style lang="scss" scoped>
.finance-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: $spacing-lg;
}

.dashboard-section {
  margin-bottom: $spacing-xl;
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  padding: $spacing-lg;
}

.section-title {
  margin-top: 0;
  margin-bottom: $spacing-md;
  color: $text-primary;
  font-size: $font-size-lg;
  font-weight: 600;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-md;
}

.view-all-link {
  color: $primary-color;
  text-decoration: none;
  font-size: $font-size-sm;
  font-weight: 500;
  
  &:hover {
    text-decoration: underline;
  }
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-lg;
  margin-bottom: $spacing-lg;
  
  @media (max-width: $breakpoint-md) {
    grid-template-columns: 1fr;
  }
}

.account-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-md;
  
  @media (max-width: $breakpoint-md) {
    grid-template-columns: 1fr;
  }
}

.summary-card {
  background-color: $bg-secondary;
  border-radius: $border-radius;
  padding: $spacing-md;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: $transition-quick;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: $box-shadow-hover;
  }
  
  &__header {
    display: flex;
    align-items: center;
    margin-bottom: $spacing-sm;
    
    i {
      margin-right: $spacing-sm;
      font-size: $font-size-lg;
      color: $primary-color;
    }
    
    h3 {
      margin: 0;
      font-size: $font-size-md;
      font-weight: 500;
      color: $text-secondary;
    }
  }
  
  &__value {
    font-size: 1.5rem;
    font-weight: 700;
    color: $text-primary;
    margin-bottom: $spacing-sm;
  }
  
  &__footer {
    font-size: $font-size-sm;
    color: $text-secondary;
  }
  
  &.total-balance {
    border-left: 4px solid $primary-color;
  }
  
  &.income {
    border-left: 4px solid $positive;
    
    i {
      color: $positive;
    }
  }
  
  &.expenses {
    border-left: 4px solid $negative;
    
    i {
      color: $negative;
    }
  }
}

.chart-container {
  width: 100%;
  height: 250px;
  position: relative;
}

.transactions-list {
  margin-top: $spacing-md;
}

.transaction-item {
  display: flex;
  align-items: center;
  padding: $spacing-md;
  border-bottom: 1px solid $chart-grid;
  transition: $transition-quick;
  
  &:hover {
    background-color: rgba($primary-color, 0.05);
  }
  
  &:last-child {
    border-bottom: none;
  }
  
  &__icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: $primary-color;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: $spacing-md;
    
    i {
      color: white;
      font-size: $font-size-md;
    }
  }
  
  &__details {
    flex: 1;
  }
  
  &__title {
    font-weight: 500;
    color: $text-primary;
    margin-bottom: 4px;
  }
  
  &__meta {
    font-size: $font-size-sm;
    color: $text-secondary;
    font-weight: 500;
    
    span {
      margin-right: $spacing-md;
      
      &:last-child {
        margin-right: 0;
      }
    }
  }
  
  &__amount {
    font-weight: 600;
    margin-left: $spacing-md;
    
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
}

.savings-goals {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: $spacing-md;
  margin-top: $spacing-md;
}

.goal-card {
  padding: $spacing-md;
  background-color: $bg-secondary;
  border-radius: $border-radius;
  border-left: 4px solid $primary-color;
  
  &__title {
    margin-top: 0;
    margin-bottom: $spacing-sm;
    font-size: $font-size-md;
    font-weight: 600;
    color: $text-primary;
  }
  
  &__amounts {
    display: flex;
    justify-content: space-between;
    margin-bottom: $spacing-sm;
    
    span:first-child {
      font-weight: 600;
      color: $primary-color;
    }
    
    span:last-child {
      color: $text-secondary;
      font-weight: 500;
    }
  }
  
  &__progress {
    margin-bottom: $spacing-sm;
  }
  
  &__deadline {
    font-size: $font-size-sm;
    color: $text-secondary;
  }
}

.progress-bar {
  height: 8px;
  background-color: $chart-grid;
  border-radius: 4px;
  margin-bottom: 4px;
  overflow: hidden;
  
  &__fill {
    height: 100%;
    background-color: $primary-color;
    border-radius: 4px;
  }
  
  &__percentage {
    font-size: $font-size-sm;
    text-align: right;
    color: $text-secondary;
  }
}

.empty-state {
  text-align: center;
  padding: $spacing-lg;
  color: $text-secondary;
  font-weight: 500;
  
  p {
    margin-bottom: $spacing-md;
  }
}

.button {
  display: inline-block;
  padding: $spacing-sm $spacing-md;
  border-radius: $border-radius;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: $transition-quick;
  
  &--primary {
    background-color: $primary-color;
    color: white;
    
    &:hover {
      background-color: $primary-dark;
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

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>