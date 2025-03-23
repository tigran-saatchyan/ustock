<template>
  <div class="budgets-view">
    <finance-navigation/>

    <div class="budgets-container">
      <div class="budgets-header">
        <h2 class="budgets-title">{{ $t('finance.budgets.title') }}</h2>

        <button @click="openNewBudgetForm" class="add-button">
          <i class="pi pi-plus"></i>
          <span>{{ $t('finance.budgets.add') }}</span>
        </button>
      </div>

      <!-- Header Controls Row -->
      <div class="controls-row">
        <month-year-picker/>
        <currency-display-selector
            v-model:currency="displayCurrency"
            @update:currency="updateDisplayCurrency"
        />
      </div>

      <div v-if="isLoading" class="loading-spinner">
        <div class="spinner"></div>
        <p>{{ $t('finance.budgets.loading') }}</p>
      </div>

      <!-- Budget Overview -->
      <div v-else-if="budgets.length" class="budgets-overview">
        <div class="overview-card total">
          <h3 class="overview-card__title">{{ $t('finance.budgets.totalBudget') }}</h3>
          <div class="overview-card__value">
            {{ formatCurrency(convertedTotalBudget, displayCurrency) }}
          </div>
          <div class="overview-card__progress">
            <div class="progress-bar">
              <div class="progress-bar__fill"
                  :style="{ 
                    width: `${totalSpentPercentage}%`,
                    backgroundColor: getBudgetColor(totalSpentPercentage) 
                  }"
              ></div>
            </div>
            <div class="overview-meta">
              <div class="overview-meta__spent">
                {{ $t('finance.budgets.spent') }}: {{ formatCurrency(convertedTotalSpent, displayCurrency) }}
              </div>
              <div class="overview-meta__remaining">
                {{ $t('finance.budgets.remaining') }}: {{ formatCurrency(convertedTotalRemaining, displayCurrency) }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Budget Cards -->
      <div v-if="budgets.length" class="budgets-grid">
        <div
            v-for="budget in budgets"
            :key="budget.id"
            class="budget-card"
        >
          <div class="budget-card__header">
            <h3 class="budget-card__title">{{ budget.category_name }}</h3>
            <div class="budget-card__amount">{{ formatCurrency(budget.amount, budget.currency) }}</div>
          </div>

          <div class="budget-card__progress">
            <div class="progress-bar">
              <div class="progress-bar__fill"
                  :style="{ 
                    width: `${getSpentPercentage(budget)}%`,
                    backgroundColor: getBudgetColor(getSpentPercentage(budget)) 
                  }"
              ></div>
            </div>
            <div class="progress-bar__percentage">{{ getSpentPercentage(budget) }}%</div>
          </div>

          <div class="budget-card__info">
            <div class="budget-card__spent">
              <span>{{ $t('finance.budgets.spent') }}: {{ formatCurrency(budget.spent, budget.currency) }}</span>
            </div>
            <div class="budget-card__remaining">
              <span>{{ $t('finance.budgets.remaining') }}:
                {{ formatCurrency(budget.amount - budget.spent, budget.currency) }}</span>
            </div>
          </div>

          <!-- Subcategory budgets -->
          <div v-if="budget.is_parent_budget && budget.subcategory_budgets && budget.subcategory_budgets.length > 0"
              class="subcategories-preview">
            <div class="subcategories-label">
              {{ $t('finance.categories.subcategories') || 'Subcategories' }}:
              <span class="subcategory-count">({{ budget.subcategory_budgets.length }})</span>
            </div>
            <div v-for="subcategoryBudget in budget.subcategory_budgets" :key="subcategoryBudget.id"
                class="subcategory-preview-item">
              <div class="subcategory-preview-name">
                <div class="subcategory-icon-mini">
                  <div class="icon-container-mini"
                      :style="{ backgroundColor: subcategoryBudget.category_color + '15' }">
                    <i v-if="subcategoryBudget.category_icon" :class="subcategoryBudget.category_icon"
                        :style="{ color: subcategoryBudget.category_color }"></i>
                    <div v-else class="fallback-mini"
                        :style="{ backgroundColor: subcategoryBudget.category_color }"></div>
                  </div>
                </div>
                {{ subcategoryBudget.category_name }}
              </div>
              <div class="subcategory-preview-amount">
                {{ formatCurrency(subcategoryBudget.amount, subcategoryBudget.currency) }}
              </div>
            </div>
          </div>

          <div class="budget-card__actions">
            <button @click="editBudget(budget)" class="action-button">
              <i class="pi pi-pencil"></i>
            </button>
            <button @click="deleteBudgetConfirm(budget)" class="action-button delete">
              <i class="pi pi-trash"></i>
            </button>
          </div>
        </div>
      </div>

      <div v-if="budgets.length" class="budget-section">
        <h2>{{ $t('finance.budgets.allocationChartTitle') }}</h2>
        <BudgetAllocationChart
            :budget="selectedBudget"
            :loading="chartLoading"
            :no-data-message="$t('finance.budgets.chartNoData')"
        />
        <div class="copy-budget-section">
          <h3>{{ $t('finance.budgets.copyLastMonthTitle') }}</h3>
          <button @click="copyLastMonthBudget" class="button button--primary">
            {{ $t('finance.budgets.copyButton') }}
          </button>
        </div>
      </div>


      <div v-else-if="!isLoading" class="empty-state">
        <p>{{ $t('finance.budgets.noBudgetsFound') }}</p>
        <button @click="openNewBudgetForm" class="button button--primary">
          {{ $t('finance.budgets.addFirst') }}
        </button>
      </div>

      <!-- Budget Form Modal -->
      <div class="modal" v-if="showBudgetForm">
        <div class="modal-overlay" @click="closeForm"></div>
        <div class="modal-container">
          <div class="modal-header">
            <h3>
              <span v-if="editMode">{{ $t('finance.budgets.edit') }}</span>
              <span v-else-if="isUsingTemplate">{{
                  $t('finance.budgets.createFromTemplate') || 'Create Budget from Template'
                }}</span>
              <span v-else>{{ $t('finance.budgets.add') }}</span>
            </h3>
            <div class="modal-actions">
              <button
                  v-if="!editMode && !isUsingTemplate && budgetFormStep === 1"
                  @click="toggleBudgetTemplates"
                  class="template-button"
                  title="Use Template"
              >
                <i class="pi pi-copy"></i>
                <span>{{ $t('finance.budgets.templates.useTemplate') || 'Use Template' }}</span>
              </button>
              <button @click="closeForm" class="close-button">
                <i class="pi pi-times"></i>
              </button>
            </div>
          </div>

          <div class="modal-body">
            <!-- Budget Templates Section -->
            <div v-if="showBudgetTemplates && !editMode" class="templates-section">
              <budget-templates
                  :current-month="selectedMonth"
                  :current-year="selectedYear"
                  @select-template="handleTemplateSelection"
              />
            </div>

            <form v-else @submit.prevent="saveBudget" class="budget-form">
              <!-- Step 1: Category Selection -->
              <div class="budget-step" v-if="budgetFormStep === 1">
                <h4 class="step-title">{{ $t('finance.budgets.form.selectCategory') || 'Select Category' }}</h4>

                <div class="form-group" :class="{ 'has-error': formSubmitted && formValidationErrors.category }">
                  <label for="category">{{ $t('finance.budgets.form.category') }}</label>
                  <div class="select-with-button">
                    <select
                        id="category"
                        v-model="budgetForm.category"
                        @change="onCategoryChange"
                        required
                        :class="{ 'input-error': formSubmitted && formValidationErrors.category }"
                    >
                      <option value="" disabled>{{
                          $t('finance.budgets.form.selectCategory') || 'Select category'
                        }}
                      </option>
                      <option v-for="category in mainExpenseCategories" :key="category.id" :value="category.id">
                        {{ category.name }}
                      </option>
                    </select>
                    <button
                        type="button"
                        @click="showAddCategoryModal"
                        class="add-category-button"
                        title="Add new category"
                    >
                      <i class="pi pi-plus"></i>
                    </button>
                  </div>
                  <div v-if="formSubmitted && formValidationErrors.category" class="field-error-message">
                    <i class="pi pi-exclamation-circle"></i>
                    <span>{{ formValidationErrors.category }}</span>
                  </div>
                  <div v-else-if="expenseCategories.length === 0" class="no-categories-warning">
                    <i class="pi pi-exclamation-circle"></i>
                    <span>{{
                        $t('finance.budgets.form.noCategories') || 'No expense categories available. Please create one.'
                      }}</span>
                  </div>
                </div>

                <!-- Month & Year Selection -->
                <div class="form-row">
                  <div class="form-group">
                    <label for="month">{{ $t('finance.budgets.form.month') }}</label>
                    <select id="month" v-model="budgetForm.month" required>
                      <option v-for="(month, index) in months" :key="index" :value="index + 1">
                        {{ month }}
                      </option>
                    </select>
                  </div>

                  <div class="form-group">
                    <label for="year">{{ $t('finance.budgets.form.year') }}</label>
                    <select id="year" v-model="budgetForm.year" required>
                      <option v-for="year in availableYears" :key="year" :value="year">
                        {{ year }}
                      </option>
                    </select>
                  </div>
                </div>

                <!-- Currency Selection -->
                <div class="form-group">
                  <label for="currency">{{ $t('finance.budgets.form.currency') }}</label>
                  <select id="currency" v-model="budgetForm.currency" required>
                    <option value="USD">USD</option>
                    <option value="EUR">EUR</option>
                    <option value="GEL">GEL</option>
                    <option value="RUB">RUB</option>
                  </select>
                </div>

                <!-- Total Budget Amount -->
                <div class="form-group" :class="{ 'has-error': formSubmitted && formValidationErrors.amount }">
                  <label for="amount">{{ $t('finance.budgets.form.totalBudget') || 'Total Budget Amount' }}</label>
                  <div class="input-with-icon">
                    <i class="pi pi-dollar"></i>
                    <input
                        type="number"
                        id="amount"
                        v-model="budgetForm.amount"
                        @input="updateSubcategoryBudgets"
                        step="0.01"
                        min="0.01"
                        required
                        :class="{ 'input-error': formSubmitted && formValidationErrors.amount }"
                        placeholder="Enter budget amount"
                    >
                  </div>
                  <div v-if="formSubmitted && formValidationErrors.amount" class="field-error-message">
                    <i class="pi pi-exclamation-circle"></i>
                    <span>{{ formValidationErrors.amount }}</span>
                  </div>
                </div>


                <div class="form-actions">
                  <button type="button" @click="closeForm" class="button button--secondary">
                    {{ $t('common.cancel') }}
                  </button>
                  <button
                      type="button"
                      @click="checkAndGoToSubcategories"
                      class="button button--primary"
                  >
                    {{ $t('finance.budgets.form.nextStep') || 'Next: Allocate Budget' }}
                  </button>
                </div>
              </div>

              <!-- Step 2: Subcategory Budget Allocation -->
              <div class="budget-step" v-if="budgetFormStep === 2">
                <h4 class="step-title">
                  {{ $t('finance.budgets.form.allocateBudget') || 'Allocate Budget for' }}:
                  <span class="category-name">{{ selectedCategoryName }}</span>
                </h4>

                <div class="budget-summary">
                  <div class="budget-info">
                    <div class="total-amount">{{ formatCurrency(budgetForm.amount, budgetForm.currency) }}</div>
                    <div class="budget-details">
                      <div class="allocated">
                        {{ $t('finance.budgets.form.allocated') || 'Allocated' }}:
                        <span class="amount">{{ formatCurrency(allocatedAmount, budgetForm.currency) }}</span>
                      </div>
                      <div class="remaining">
                        {{ $t('finance.budgets.form.remaining') || 'Remaining' }}:
                        <span class="amount" :class="{ 'negative': remainingAmount < 0 }">
                          {{ formatCurrency(remainingAmount, budgetForm.currency) }}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div class="allocation-bar">
                    <div class="allocation-bar__fill" :style="{ width: `${getAllocationPercentage()}%` }"></div>
                  </div>
                </div>

                <!-- Subcategory allocation -->
                <div class="subcategories-list">
                  <div
                      v-for="subcategory in subcategories"
                      :key="subcategory.id"
                      class="subcategory-item"
                  >
                    <div class="subcategory-info">
                      <div class="subcategory-icon">
                        <div class="icon-container" :style="{ backgroundColor: subcategory.color + '15' }">
                          <i v-if="subcategory.icon" :class="subcategory.icon"
                              :style="{ color: subcategory.color }"></i>
                          <div v-else class="fallback" :style="{ backgroundColor: subcategory.color }"></div>
                        </div>
                      </div>
                      <div class="subcategory-name">{{ subcategory.name }}</div>
                    </div>
                    <div class="subcategory-allocation">
                      <input
                          type="number"
                          v-model="subcategoryBudgets[subcategory.id]"
                          @input="updateRemainingBudget"
                          step="0.01"
                          min="0"
                          :placeholder="$t('finance.budgets.form.amount') || 'Amount'"
                      >
                    </div>
                  </div>

                  <!-- Button to add new subcategory -->
                  <div class="add-subcategory">
                    <button
                        type="button"
                        @click="showAddSubcategoryModal"
                        class="add-button"
                    >
                      <i class="pi pi-plus-circle"></i>
                      <span>{{ $t('finance.budgets.form.addSubcategory') || 'Add Subcategory' }}</span>
                    </button>
                  </div>
                </div>

<!--                &lt;!&ndash; Error message - only visible after submission attempt &ndash;&gt;-->
<!--                <div class="form-error-container" v-if="formSubmitted">-->
<!--                  <div-->
<!--                      :class="['form-error-message', {'form-error-visible': formError !== '', 'form-error-hidden': formError === ''}]">-->
<!--                    <i class="pi pi-exclamation-circle"></i>-->
<!--                    <span>{{ formError }}</span>-->
<!--                  </div>-->
<!--                </div>-->

                <div class="form-actions">
                  <button type="button" @click="backToStep1" class="button button--secondary">
                    {{ $t('finance.budgets.form.back') || 'Back' }}
                  </button>
                  <button type="submit" class="button button--primary">
                    {{ editMode ? $t('common.update') : $t('common.save') }}
                  </button>
                </div>
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
            <p>{{ $t('finance.budgets.confirmDelete') }}</p>
            <p v-if="budgetToDelete" class="delete-details">
              <strong>{{ budgetToDelete.category_name }}</strong>
              <span>{{ formatCurrency(budgetToDelete.amount, budgetToDelete.currency) }}</span>
            </p>

            <div class="form-actions">
              <button @click="showDeleteConfirm = false" class="button button--secondary">
                {{ $t('common.cancel') }}
              </button>
              <button @click="deleteBudget" class="button button--delete">
                {{ $t('common.delete') }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Category Manager Modal -->
      <div class="modal" v-if="showCategoryManager">
        <div class="modal-overlay" @click="showCategoryManager = false"></div>
        <div class="modal-container category-manager-modal">
          <div class="modal-header">
            <h3>{{ $t('finance.categories.manage') }}</h3>
            <button @click="closeCategoryManager" class="close-button">
              <i class="pi pi-times"></i>
            </button>
          </div>

          <div class="modal-body">
            <category-manager @updated="onCategoriesUpdated"/>
          </div>
        </div>
      </div>

      <!-- Collapsible Category Manager Section -->
      <div class="category-manager-section">
        <div class="section-header" @click="toggleCategoryManager">
          <h3>{{ $t('finance.categories.manage') || 'Manage Categories' }}</h3>
          <button class="toggle-button">
            <i :class="showInlineCategoryManager ? 'pi pi-chevron-up' : 'pi pi-chevron-down'"></i>
          </button>
        </div>

        <div v-if="showInlineCategoryManager" class="section-content">
          <category-manager @updated="onCategoriesUpdated"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {computed, onMounted, ref, watch} from 'vue';
import {useStore} from 'vuex';
import {useI18n} from 'vue-i18n';
import FinanceNavigation from '@/components/finance/FinanceNavigation.vue';
import MonthYearPicker from '@/components/finance/MonthYearPicker.vue';
import CategoryManager from '@/components/finance/CategoryManager.vue';
import CurrencyDisplaySelector from '@/components/finance/CurrencyDisplaySelector.vue';
import BudgetAllocationChart from '@/components/finance/BudgetAllocationChart.vue';
import BudgetTemplates from '@/components/finance/BudgetTemplates.vue';
import {convertCurrency} from '@/utils/currencyUtils';

export default {
  name: 'BudgetsView',

  components: {
    FinanceNavigation,
    MonthYearPicker,
    CategoryManager,
    CurrencyDisplaySelector,
    BudgetAllocationChart,
    BudgetTemplates
  },

  setup() {
    const store = useStore();
    // eslint-disable-next-line no-unused-vars
    const {locale, t: $t} = useI18n(); // Use a different variable name to avoid ESLint warning

    // State
    const showBudgetForm = ref(false);
    const showDeleteConfirm = ref(false);
    const showCategoryManager = ref(false);
    const showInlineCategoryManager = ref(false); // State for collapsible section
    const showBudgetTemplates = ref(false); // State for budget templates section
    const editMode = ref(false);
    const budgetToDelete = ref(null);
    const formError = ref('');  // Error message for form validation
    const formSubmitted = ref(false); // Flag to track if form was submitted
    const formValidationErrors = ref({}); // Field-specific validation errors
    const displayCurrency = ref('USD'); // Currency to display totals in
    const budgetFormStep = ref(1);      // Current step in budget form (1: Category selection, 2: Subcategory allocation)
    const subcategories = ref([]);      // Available subcategories for selected category
    const subcategoryBudgets = ref({}); // Budget amounts for each subcategory
    const allocatedAmount = ref(0);     // Total allocated to subcategories
    const otherSubcategoryId = ref(null); // ID of the "Other" subcategory
    const showSubcategoryChart = ref({}); // Track which budget cards show chart vs list view
    const isUsingTemplate = ref(false); // Flag to track if user is using a template

    // Months array - using the current locale
    const getLocalizedMonths = () => {
      const months = [];
      for (let i = 0; i < 12; i++) {
        const date = new Date(2000, i, 1);
        const monthName = date.toLocaleString(locale.value, {month: 'long'});
        months.push(monthName);
      }
      return months;
    };

    const months = computed(() => getLocalizedMonths());

    // Get current date
    const today = new Date();
    const currentYear = today.getFullYear();

    // Generate available years (3 years back and 2 years forward)
    const availableYears = [];
    for (let year = currentYear - 3; year <= currentYear + 2; year++) {
      availableYears.push(year);
    }

    // Store getters
    const isLoading = computed(() => store.getters['personalFinance/isLoading']);
    const budgets = computed(() => store.getters['personalFinance/budgets']);
    const categories = computed(() => store.getters['personalFinance/categories']);
    const expenseCategories = computed(() => store.getters['personalFinance/expenseCategories']);
    const selectedMonth = computed(() => store.getters['personalFinance/selectedMonth']);
    const selectedYear = computed(() => store.getters['personalFinance/selectedYear']);
    const exchangeRates = computed(() => store.getters['personalFinance/exchangeRates']);

    // Filter for main expense categories only (no subcategories)
    const mainExpenseCategories = computed(() =>
        expenseCategories.value.filter(cat => !cat.parent)
    );

    // Default form values
    const defaultForm = {
      category: '',
      amount: '',
      currency: 'USD',
      month: selectedMonth.value,
      year: selectedYear.value
    };

    // Form models
    const budgetForm = ref({...defaultForm});

    // Computed properties for multi-currency totals
    const currencyTotals = computed(() => {
      const totals = {};
      budgets.value.forEach(budget => {
        const currency = budget.currency || 'USD';
        if (!totals[currency]) totals[currency] = 0;
        totals[currency] += parseFloat(budget.amount);
      });
      return totals;
    });

    const currencySpent = computed(() => {
      const spent = {};
      budgets.value.forEach(budget => {
        const currency = budget.currency || 'USD';
        if (!spent[currency]) spent[currency] = 0;
        spent[currency] += parseFloat(budget.spent || 0);
      });
      return spent;
    });

    const currencyRemaining = computed(() => {
      const remaining = {};
      for (const currency in currencyTotals.value) {
        remaining[currency] = currencyTotals.value[currency] - (currencySpent.value[currency] || 0);
      }
      return remaining;
    });

    // Converted totals in the selected display currency
    const convertedTotalBudget = computed(() => {
      let total = 0;

      // Convert all currency totals to the display currency
      for (const [currency, amount] of Object.entries(currencyTotals.value)) {
        total += convertCurrency(amount, currency, displayCurrency.value, exchangeRates.value);
      }

      return total;
    });

    const convertedTotalSpent = computed(() => {
      let total = 0;

      // Convert all currency spent to the display currency
      for (const [currency, amount] of Object.entries(currencySpent.value)) {
        total += convertCurrency(amount, currency, displayCurrency.value, exchangeRates.value);
      }

      return total;
    });

    const convertedTotalRemaining = computed(() => {
      return convertedTotalBudget.value - convertedTotalSpent.value;
    });

    // Progress percentage based on converted amounts
    const totalSpentPercentage = computed(() => {
      if (convertedTotalBudget.value === 0) return 0;
      return Math.min(Math.round((convertedTotalSpent.value / convertedTotalBudget.value) * 100), 100);
    });

    // Update display currency
    const updateDisplayCurrency = (currency) => {
      displayCurrency.value = currency;
      // Save the preference to localStorage
      localStorage.setItem('budgetDisplayCurrency', currency);
    };

    // Watch for changes in selected month/year
    watch([selectedMonth, selectedYear], () => {
      fetchBudgets();
    });

    // Initialize data
    onMounted(async () => {
      // Load saved display currency preference
      const savedCurrency = localStorage.getItem('budgetDisplayCurrency');
      if (savedCurrency) {
        displayCurrency.value = savedCurrency;
      }

      // Load exchange rates if not already loaded
      if (Object.keys(exchangeRates.value).length === 0) {
        await store.dispatch('personalFinance/fetchExchangeRates');
      }

      fetchBudgets();
    });

    // Fetch budgets
    const fetchBudgets = async () => {
      await store.dispatch('personalFinance/fetchBudgets', {
        month: selectedMonth.value,
        year: selectedYear.value,
        only_parent: true // Only fetch parent budgets by default
      });
    };

    // Edit budget
    const editBudget = async (budget) => {
      editMode.value = true;

      budgetForm.value = {
        id: budget.id,
        category: budget.category,
        amount: budget.amount,
        currency: budget.currency || 'USD', // Default to USD if not set (for existing budgets before migration)
        month: budget.month,
        year: budget.year,
        is_parent_budget: budget.is_parent_budget
      };

      // Load subcategories for this category
      await loadSubcategories(budget.category);

      // If this is a parent budget with subcategories, load their allocations
      subcategoryBudgets.value = {};

      if (budget.is_parent_budget && budget.subcategory_budgets && budget.subcategory_budgets.length > 0) {
        // Initialize subcategory budgets from existing data
        let totalAllocated = 0;
        let otherCategoryFound = false;

        budget.subcategory_budgets.forEach(subBudget => {
          subcategoryBudgets.value[subBudget.category] = parseFloat(subBudget.amount);
          totalAllocated += parseFloat(subBudget.amount);

          // Check if this is the "Other" category
          const subCategory = subcategories.value.find(sc => sc.id === subBudget.category);
          if (subCategory && subCategory.name === 'Other') {
            otherCategoryFound = true;
            otherSubcategoryId.value = subBudget.category;
          }
        });

        // If no Other category was found in the existing budget, add it
        if (!otherCategoryFound && otherSubcategoryId.value) {
          // Calculate how much to allocate to Other (remaining amount)
          const remainingForOther = Math.max(0, parseFloat(budget.amount) - totalAllocated);
          subcategoryBudgets.value[otherSubcategoryId.value] = remainingForOther;
          totalAllocated += remainingForOther;
        }

        allocatedAmount.value = totalAllocated;

        // Now update the remaining amount, which should make sure "Other" gets any unallocated amount
        updateRemainingBudget();

        // Go directly to step 2 since we have subcategory data
        budgetFormStep.value = 2;
      } else {
        // Start at step 1 for new budgets or budgets without subcategories
        budgetFormStep.value = 1;
      }

      showBudgetForm.value = true;
    };

    // Save budget (create or update)
    const saveBudget = async () => {
      // Set form as submitted to show errors
      formSubmitted.value = true;

      try {
        // Ensure we're on step 2 with subcategory allocations
        if (budgetFormStep.value === 1) {
          checkAndGoToSubcategories();
          return;
        }

        // Validate the total allocation
        updateRemainingBudget();
        if (Math.abs(remainingAmount.value) > 0.01) {
          // Show an error or warning if the allocation doesn't match the total
          console.warn('Budget allocation does not match the total amount');
          formError.value = `Allocation doesn't match the total budget amount. Please adjust allocations.`;
          return;
        }

        // Before creating the array, make sure "Other" has the correct allocation
        // (any remaining unallocated amount)
        if (otherSubcategoryId.value) {
          // Calculate how much is allocated to non-Other categories
          let allocatedToRegularCategories = 0;

          Object.entries(subcategoryBudgets.value).forEach(([id, amount]) => {
            if (id !== otherSubcategoryId.value && !isNaN(parseFloat(amount))) {
              allocatedToRegularCategories += parseFloat(amount);
            }
          });

          // Calculate remaining amount for "Other"
          const totalBudget = parseFloat(budgetForm.value.amount);
          const remainingForOther = Math.max(0, totalBudget - allocatedToRegularCategories);

          // Set the "Other" category budget amount
          subcategoryBudgets.value[otherSubcategoryId.value] = remainingForOther;
        }

        // Create an array of subcategory budget objects
        const subcategoryBudgetsArray = [];

        // For each subcategory, add it to the array
        Object.entries(subcategoryBudgets.value).forEach(([subcategoryId, amount]) => {
          // Always include the subcategory, even if amount is 0
          // This ensures the "Other" category always gets included
          subcategoryBudgetsArray.push({
            category: subcategoryId,
            amount: parseFloat(amount) || 0, // Use 0 if NaN
            currency: budgetForm.value.currency
          });
        });

        if (editMode.value) {
          // In edit mode, update the existing budget (main category)
          await store.dispatch('personalFinance/updateBudget', {
            id: budgetForm.value.id,
            data: {...budgetForm.value}
          });

          // Update subcategory budgets if this is a parent budget with subcategories
          if (budgetForm.value.is_parent_budget && subcategoryBudgetsArray.length > 0) {
            await store.dispatch('personalFinance/updateSubcategoryBudgets', {
              parentBudgetId: budgetForm.value.id,
              subcategoryBudgets: subcategoryBudgetsArray
            });
          }
        } else {
          // Create parent budget with subcategory budgets in a single operation
          await store.dispatch('personalFinance/createBudget', {
            ...budgetForm.value,
            is_parent_budget: true,
            subcategory_budgets: subcategoryBudgetsArray
          });
        }

        // Reset form and close modal
        closeForm();

        // Refresh budgets
        fetchBudgets();
      } catch (error) {
        console.error('Error saving budget:', error);
        formError.value = error.response?.data?.detail || 'Failed to save budget. Please try again.';
      }
    };

    // Confirm budget delete
    const deleteBudgetConfirm = (budget) => {
      budgetToDelete.value = budget;
      showDeleteConfirm.value = true;
    };

    // Delete budget
    const deleteBudget = async () => {
      if (!budgetToDelete.value) return;

      try {
        await store.dispatch('personalFinance/deleteBudget', budgetToDelete.value.id);
        showDeleteConfirm.value = false;
        budgetToDelete.value = null;

        // Reset form state completely to avoid issues with new budget creation
        resetForm();
      } catch (error) {
        console.error('Error deleting budget:', error);
        // Error handling would go here
      }
    };

    // Reset form to defaults
    const resetForm = () => {
      editMode.value = false;
      isUsingTemplate.value = false;
      budgetForm.value = {...defaultForm};
      budgetForm.value.month = selectedMonth.value;
      budgetForm.value.year = selectedYear.value;
      budgetFormStep.value = 1;
      subcategories.value = [];
      subcategoryBudgets.value = {};
      allocatedAmount.value = 0;
      otherSubcategoryId.value = null;
      formError.value = ''; // Clear any error messages
      formSubmitted.value = false; // Reset submission flag
      formValidationErrors.value = {}; // Clear field-specific errors
    };

    // Open new budget form
    const openNewBudgetForm = () => {
      // Make sure we reset the form completely before opening
      resetForm();
      // Set the edit mode to false
      editMode.value = false;
      // Open the form modal
      showBudgetForm.value = true;
    };

    // Close budget form
    const closeForm = () => {
      // Reset the form state
      resetForm();
      // Close the modal
      showBudgetForm.value = false;
    };

    // Get selected category name
    const selectedCategoryName = computed(() => {
      if (!budgetForm.value.category) return '';
      const category = categories.value.find(c => c.id === budgetForm.value.category);
      return category ? category.name : '';
    });

    // Calculate remaining budget amount
    const remainingAmount = computed(() => {
      return parseFloat(budgetForm.value.amount || 0) - allocatedAmount.value;
    });

    // Check if budget form is valid to proceed to next step
    const isValidBudgetForm = computed(() => {
      return budgetForm.value.category &&
          budgetForm.value.currency &&
          budgetForm.value.amount > 0;
    });

    // Handle category change
    const onCategoryChange = async () => {
      if (!budgetForm.value.category) return;

      // Load subcategories for the selected category
      await loadSubcategories(budgetForm.value.category);

      // Reset subcategory budgets
      subcategoryBudgets.value = {};
      allocatedAmount.value = 0;
    };

    // Load subcategories for the selected category
    const loadSubcategories = async (categoryId) => {
      subcategories.value = [];

      // Find the category
      const category = categories.value.find(c => c.id === categoryId);
      if (!category) return;

      // Get subcategories
      if (category.subcategories && category.subcategories.length > 0) {
        subcategories.value = [...category.subcategories];
      }

      // Check if there's an "Other" subcategory, create it if not
      const otherSubcategory = subcategories.value.find(sc => sc.name === 'Other');
      if (otherSubcategory) {
        otherSubcategoryId.value = otherSubcategory.id;
      } else {
        try {
          // Create the "Other" subcategory in the database
          const otherSubData = {
            name: 'Other',
            parent: categoryId,
            color: category.color,
            icon: 'pi pi-folder',
            is_expense: category.is_expense,
            is_income: category.is_income
          };

          // Create the category using the store
          const newCategory = await store.dispatch('personalFinance/createCategory', otherSubData);

          // Add it to our local list of subcategories
          subcategories.value.push(newCategory);
          otherSubcategoryId.value = newCategory.id;

          // Also refresh categories to include the new one
          store.dispatch('personalFinance/fetchCategories');
        } catch (error) {
          console.error('Error creating Other subcategory:', error);

          // If creation fails, create a temporary placeholder
          const otherSub = {
            id: `other_${categoryId}`, // Temporary ID
            name: 'Other',
            parent: categoryId,
            color: category.color,
            icon: 'pi pi-folder',
            is_expense: category.is_expense,
            is_income: category.is_income
          };
          subcategories.value.push(otherSub);
          otherSubcategoryId.value = otherSub.id;
        }
      }
    };

    // Toggle between chart and list view for subcategory budgets
    const toggleSubcategoryChart = (budgetId) => {
      showSubcategoryChart.value[budgetId] = !showSubcategoryChart.value[budgetId];
    };

    // Duplicate an existing budget (create a copy with the same allocations)
    const duplicateBudget = (budget) => {
      // Reset form to default state
      resetForm();

      // Set form values from the budget to duplicate
      budgetForm.value = {
        category: budget.category,
        amount: budget.amount,
        currency: budget.currency,
        month: selectedMonth.value, // Use current selected month
        year: selectedYear.value,   // Use current selected year
        is_parent_budget: true      // Always create as parent budget
      };

      // Load subcategories for this category
      loadSubcategories(budget.category);

      // If this is a parent budget with subcategories, copy their allocations
      if (budget.is_parent_budget && budget.subcategory_budgets && budget.subcategory_budgets.length > 0) {
        budget.subcategory_budgets.forEach(subBudget => {
          subcategoryBudgets.value[subBudget.category] = subBudget.amount;
        });

        // Calculate total allocated amount
        allocatedAmount.value = budget.subcategory_budgets.reduce((total, sub) => {
          return total + parseFloat(sub.amount);
        }, 0);

        // Update "Other" subcategory with remaining amount
        updateRemainingBudget();

        // Go directly to step 2 (subcategory allocation)
        budgetFormStep.value = 2;
      } else {
        budgetFormStep.value = 1;
      }

      // Open the form in create mode (not edit mode)
      editMode.value = false;
      showBudgetForm.value = true;
    };

    // Handle template selection from BudgetTemplates component
    const handleTemplateSelection = (template) => {
      isUsingTemplate.value = true;

      // Close templates panel
      showBudgetTemplates.value = false;

      // Reset form and set it up for the selected template
      resetForm();

      // Set form values from the template
      budgetForm.value = {
        category: template.category,
        amount: template.amount,
        currency: template.currency,
        month: selectedMonth.value, // Use current selected month
        year: selectedYear.value,   // Use current selected year
        is_parent_budget: true      // Always create as parent budget
      };

      // Load subcategories for this category
      loadSubcategories(template.category);

      // If template has subcategories, copy their allocations
      if (template.subcategory_budgets && template.subcategory_budgets.length > 0) {
        template.subcategory_budgets.forEach(subBudget => {
          subcategoryBudgets.value[subBudget.category] = subBudget.amount;
        });

        // Calculate total allocated amount
        allocatedAmount.value = template.subcategory_budgets.reduce((total, sub) => {
          return total + parseFloat(sub.amount);
        }, 0);

        // Update "Other" subcategory with remaining amount
        updateRemainingBudget();

        // Go directly to step 2 (subcategory allocation)
        budgetFormStep.value = 2;
      } else {
        budgetFormStep.value = 1;
      }

      // Open the form in create mode (not edit mode)
      editMode.value = false;
      showBudgetForm.value = true;
    };

    // Toggle the budget templates section
    const toggleBudgetTemplates = () => {
      showBudgetTemplates.value = !showBudgetTemplates.value;
    };

    // Check form and show validation errors
    const checkAndGoToSubcategories = () => {
      // Set form as submitted to show errors
      formSubmitted.value = true;

      // Clear any previous error messages
      formError.value = '';
      formValidationErrors.value = {};

      // Validation checks
      let isValid = true;

      // Check for category
      if (!budgetForm.value.category) {
        formValidationErrors.value.category = 'Please select a category';
        isValid = false;
      }

      // Check for valid amount
      if (!budgetForm.value.amount) {
        formValidationErrors.value.amount = 'Please enter a budget amount';
        isValid = false;
      } else if (parseFloat(budgetForm.value.amount) <= 0) {
        formValidationErrors.value.amount = 'Budget amount must be greater than zero';
        isValid = false;
      }

      // Set generic error message if any validation failed
      if (!isValid) {
        formError.value = 'Please correct the errors in the form';
        return;
      }

      // If all checks pass, proceed to subcategories
      formError.value = ''; // Clear error message
      goToSubcategories();
    };

    // Go to subcategory allocation step
    const goToSubcategories = async () => {
      // Make sure subcategories are loaded
      if (subcategories.value.length === 0) {
        await loadSubcategories(budgetForm.value.category);
      }

      // Initialize "Other" with total budget amount
      if (otherSubcategoryId.value) {
        subcategoryBudgets.value[otherSubcategoryId.value] = parseFloat(budgetForm.value.amount);
        allocatedAmount.value = parseFloat(budgetForm.value.amount);
      }

      budgetFormStep.value = 2;
    };

    // Go back to step 1
    const backToStep1 = () => {
      formError.value = ''; // Clear any error messages
      budgetFormStep.value = 1;
    };

    // Update remaining budget when subcategory budgets change
    const updateRemainingBudget = () => {
      // Clear any previous error messages 
      formError.value = '';

      let total = 0;

      // Calculate total allocated (excluding "Other")
      Object.entries(subcategoryBudgets.value).forEach(([id, amount]) => {
        if (id !== otherSubcategoryId.value && !isNaN(parseFloat(amount))) {
          total += parseFloat(amount);
        }
      });

      // Update allocated amount
      allocatedAmount.value = total;

      // Update "Other" category with remaining amount
      if (otherSubcategoryId.value) {
        const remainingForOther = Math.max(0, parseFloat(budgetForm.value.amount) - total);
        subcategoryBudgets.value[otherSubcategoryId.value] = remainingForOther;

        // If other subcategories are allocated, include "Other" in the total
        if (remainingForOther > 0) {
          allocatedAmount.value = total + remainingForOther;
        }
      }
    };

    // Update subcategory budgets when total amount changes
    const updateSubcategoryBudgets = () => {
      // Clear any previous error messages
      formError.value = '';

      if (otherSubcategoryId.value && parseFloat(budgetForm.value.amount) > 0) {
        // Calculate current allocation excluding "Other"
        let allocatedToOthers = 0;
        Object.entries(subcategoryBudgets.value).forEach(([id, amount]) => {
          if (id !== otherSubcategoryId.value && !isNaN(parseFloat(amount))) {
            allocatedToOthers += parseFloat(amount);
          }
        });

        // Update "Other" with remaining amount
        const remainingForOther = Math.max(0, parseFloat(budgetForm.value.amount) - allocatedToOthers);
        subcategoryBudgets.value[otherSubcategoryId.value] = remainingForOther;

        // Update total allocation
        allocatedAmount.value = allocatedToOthers + remainingForOther;
      }
    };

    // Get allocation percentage for the progress bar
    const getAllocationPercentage = () => {
      if (parseFloat(budgetForm.value.amount) <= 0) return 0;
      const percentage = (allocatedAmount.value / parseFloat(budgetForm.value.amount)) * 100;
      return Math.min(percentage, 100); // Cap at 100%
    };

    // Show modal to add a new category
    const showAddCategoryModal = () => {
      showCategoryManager.value = true;
    };

    // Show modal to add a new subcategory
    const showAddSubcategoryModal = () => {
      // Pre-select the parent category in the category manager
      showCategoryManager.value = true;
    };

    // Handle closing the category manager modal
    const closeCategoryManager = () => {
      showCategoryManager.value = false;
    };

    // Toggle the visibility of the inline category manager
    const toggleCategoryManager = () => {
      showInlineCategoryManager.value = !showInlineCategoryManager.value;

      // If opening the manager and we need to load categories
      if (showInlineCategoryManager.value && categories.value.length === 0) {
        store.dispatch('personalFinance/fetchCategories');
      }
    };

    // Handle category updates from CategoryManager
    const onCategoriesUpdated = async () => {
      // Refresh categories from the store
      await store.dispatch('personalFinance/fetchCategories');

      // If we're in the budget form and a category is selected, reload subcategories
      if (showBudgetForm.value && budgetForm.value.category) {
        await loadSubcategories(budgetForm.value.category);
      }
    };

    // Helper function to get spent percentage
    const getSpentPercentage = (budget) => {
      if (parseFloat(budget.amount) === 0) return 0;
      return Math.min(Math.round((parseFloat(budget.spent) / parseFloat(budget.amount)) * 100), 100);
    };

    // Helper function to get color based on percentage
    const getBudgetColor = (percentage) => {
      if (percentage < 70) return '#00c853'; // Green
      if (percentage < 90) return '#ffc107'; // Yellow/Warning
      return '#ff5252'; // Red
    };

    // Helper function to format currency
    const formatCurrency = (amount, currencyCode = 'USD') => {
      const currencyLocale = locale.value === 'ru' ? 'ru-RU' : 'en-US';

      return new Intl.NumberFormat(currencyLocale, {
        style: 'currency',
        currency: currencyCode
      }).format(amount);
    };

    return {
      showBudgetForm,
      showDeleteConfirm,
      showCategoryManager,
      showInlineCategoryManager,
      showBudgetTemplates,
      editMode,
      isUsingTemplate,
      budgetToDelete,
      budgetForm,
      budgetFormStep,
      formSubmitted,
      formValidationErrors,
      openNewBudgetForm,
      closeForm,
      months,
      availableYears,
      isLoading,
      budgets,
      categories,
      expenseCategories,
      mainExpenseCategories,
      selectedMonth,
      selectedYear,
      displayCurrency,
      updateDisplayCurrency,
      convertedTotalBudget,
      convertedTotalSpent,
      convertedTotalRemaining,
      totalSpentPercentage,
      currencyTotals,
      currencySpent,
      currencyRemaining,
      editBudget,
      saveBudget,
      deleteBudgetConfirm,
      deleteBudget,
      duplicateBudget,
      getSpentPercentage,
      getBudgetColor,
      formatCurrency,
      selectedCategoryName,
      subcategories,
      subcategoryBudgets,
      allocatedAmount,
      remainingAmount,
      isValidBudgetForm,
      onCategoryChange,
      checkAndGoToSubcategories,
      goToSubcategories,
      backToStep1,
      updateRemainingBudget,
      updateSubcategoryBudgets,
      getAllocationPercentage,
      showAddCategoryModal,
      showAddSubcategoryModal,
      closeCategoryManager,
      toggleCategoryManager,
      onCategoriesUpdated,
      handleTemplateSelection,
      toggleBudgetTemplates,
      toggleSubcategoryChart,
      showSubcategoryChart
    };
  }
};
</script>

<style lang="scss" scoped>
.budgets-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: $spacing-lg;
}

.controls-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;

  @media (max-width: $breakpoint-sm) {
    flex-direction: column;
    align-items: stretch;
    gap: $spacing-md;
  }
}

.budgets-container {
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  padding: $spacing-lg;
}

.budgets-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
}

.budgets-title {
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

.budgets-overview {
  margin-bottom: $spacing-lg;
}

.overview-card {
  background-color: $bg-secondary;
  border-radius: $border-radius;
  padding: $spacing-lg;

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
    margin-bottom: $spacing-md;
    display: flex;
    flex-direction: column;

    .currency-total {
      margin-bottom: $spacing-xs;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }

  &__progress {
    margin-bottom: $spacing-sm;
  }
}

.progress-bar {
  height: 12px;
  background-color: $chart-grid;
  border-radius: 6px;
  margin-bottom: $spacing-sm;
  overflow: hidden;

  &__fill {
    height: 100%;
    background-color: $positive;
    border-radius: 6px;
    transition: width 0.3s ease;
  }

  &__percentage {
    font-size: $font-size-sm;
    text-align: right;
    color: $text-secondary;
    margin-bottom: $spacing-xs;
  }
}

.overview-meta {
  display: flex;
  justify-content: space-between;

  &__spent,
  &__remaining {
    font-size: $font-size-sm;
    display: flex;
    flex-direction: column;

    .currency-spent,
    .currency-remaining {
      margin-bottom: $spacing-xs;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }

  &__spent {
    color: $text-secondary;
  }

  &__remaining {
    font-weight: 500;
  }
}

.budgets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: $spacing-md;
}

.budget-card {
  background-color: $bg-secondary;
  border-radius: $border-radius;
  padding: $spacing-md;
  position: relative;
  transition: $transition-quick;

  &:hover {
    transform: translateY(-2px);
    box-shadow: $box-shadow;
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $spacing-md;
  }

  &__title {
    margin: 0;
    font-size: $font-size-md;
    font-weight: 600;
    color: $text-primary;
  }

  &__amount {
    font-weight: 700;
    color: $primary-color;
  }

  &__info {
    display: flex;
    justify-content: space-between;
    font-size: $font-size-sm;
    margin-top: $spacing-xs;
    margin-bottom: $spacing-sm;
  }

  &__spent {
    color: $text-secondary;
  }

  &__remaining {
    font-weight: 500;
  }

  &__actions {
    position: absolute;
    top: $spacing-sm;
    right: $spacing-sm;
    display: flex;
    gap: $spacing-xs;
    opacity: 0;
    transition: opacity 0.2s ease;
  }

  &:hover &__actions {
    opacity: 1;
  }
}

.budget-card__subcategories {
  background-color: rgba($chart-grid, 0.2);
  border-radius: $border-radius;
  padding: $spacing-xs $spacing-sm;
  margin-top: $spacing-xs;
  font-size: $font-size-xs;

  .subcategories-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $spacing-xs;

    .subcategories-label {
      color: $text-secondary;
      font-weight: 500;
      font-size: 0.75rem;
      display: flex;
      align-items: center;

      .subcategory-count {
        color: $text-secondary;
        font-size: 0.7rem;
        opacity: 0.8;
        margin-left: 4px;
      }
    }

    .subcategories-toggle {
      width: 24px;
      height: 24px;
      border-radius: 50%;
      background-color: rgba($primary-color, 0.1);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: $transition-quick;

      &:hover {
        background-color: rgba($primary-color, 0.2);
      }

      i {
        font-size: 0.7rem;
        color: $primary-color;
      }
    }
  }

  .subcategories-chart {
    margin: $spacing-sm 0;
    height: 200px;
  }

  .subcategories-list {
    max-height: 150px;
    overflow-y: auto;

    &::-webkit-scrollbar {
      width: 4px;
    }

    &::-webkit-scrollbar-track {
      background: rgba($chart-grid, 0.1);
      border-radius: 4px;
    }

    &::-webkit-scrollbar-thumb {
      background: rgba($text-secondary, 0.2);
      border-radius: 4px;

      &:hover {
        background: rgba($text-secondary, 0.4);
      }
    }
  }

  .subcategory-preview-item {
    display: flex;
    justify-content: space-between;
    padding: $spacing-xs 0;
    border-bottom: 1px dashed rgba($chart-grid, 0.6);

    &:last-child {
      border-bottom: none;
    }

    .subcategory-preview-name {
      display: flex;
      align-items: center;
      gap: $spacing-xs;
      color: $text-primary;
      font-size: 0.75rem;
    }

    .subcategory-preview-amount {
      color: $text-primary;
      font-weight: 500;
      font-size: 0.75rem;
    }

    .subcategory-icon-mini {
      display: flex;
      align-items: center;
      justify-content: center;

      .icon-container-mini {
        width: 20px;
        height: 20px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;

        i {
          font-size: 0.7rem;
        }

        .fallback-mini {
          width: 10px;
          height: 10px;
          border-radius: 2px;
        }
      }
    }
  }
}

.action-button {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: $bg-primary;
  border: none;
  color: $text-secondary;
  cursor: pointer;
  transition: $transition-quick;

  &:hover {
    background-color: rgba($primary-color, 0.1);
    color: $primary-color;
  }

  &.duplicate:hover {
    background-color: rgba($chart-grid, 0.3);
    color: darken($text-secondary, 10%);
  }

  &.delete:hover {
    background-color: rgba($negative, 0.1);
    color: $negative;
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
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  z-index: 1001;

  &.confirm-dialog {
    max-width: 400px;
  }

  &.category-manager-modal {
    max-width: 700px;
    width: 90%;
    max-height: 90vh;
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

.form-error-container {
  margin: $spacing-md 0;
  width: 100%;
}

.form-error-message {
  background-color: rgba($negative, 0.15);
  border: 2px solid $negative;
  padding: $spacing-md;
  display: flex;
  align-items: center;
  border-radius: $border-radius;
  width: 100%;
  box-shadow: 0 2px 8px rgba($negative, 0.2);

  &.form-error-visible {
    display: flex;
    animation: fadeInAndShake 0.5s ease;
    height: auto;
    opacity: 1;
    margin: $spacing-md 0;
  }

  &.form-error-hidden {
    height: 0;
    opacity: 0;
    padding: 0;
    margin: 0;
    border: none;
    overflow: hidden;
  }

  i {
    color: $negative;
    margin-right: $spacing-sm;
    font-size: $font-size-lg;
  }

  span {
    color: darken($negative, 10%);
    font-size: $font-size-md;
    font-weight: 600;
  }
}

.field-error-message {
  display: flex;
  align-items: center;
  padding-top: 5px;
  font-size: $font-size-xs;
  color: $negative;
  animation: fadeIn 0.3s ease;

  i {
    margin-right: 6px;
    font-size: 12px;
  }
}

.form-group {
  &.has-error {
    input, select {
      border-color: $negative;
      background-color: rgba($negative, 0.03);
    }
  }

  .input-with-icon {
    position: relative;

    i {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      color: $text-secondary;
    }

    input {
      padding-left: 35px;
    }
  }

  .input-error {
    border-color: $negative !important;
    box-shadow: 0 0 0 1px rgba($negative, 0.4) !important;
  }
}

.modal-header {
  .modal-actions {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
  }

  .template-button {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    background-color: transparent;
    border: 1px solid rgba($primary-color, 0.3);
    border-radius: $border-radius;
    color: $primary-color;
    font-size: $font-size-sm;
    cursor: pointer;
    transition: $transition-quick;

    &:hover {
      background-color: rgba($primary-color, 0.1);
    }

    i {
      font-size: 0.8rem;
    }
  }
}

.templates-section {
  margin-bottom: $spacing-md;
  background-color: $bg-secondary;
  border-radius: $border-radius;
  padding: $spacing-md;
}

@keyframes fadeInAndShake {
  0% {
    opacity: 0;
    transform: translateX(0);
  }
  20% {
    opacity: 1;
    transform: translateX(-5px);
  }
  40% {
    transform: translateX(5px);
  }
  60% {
    transform: translateX(-3px);
  }
  80% {
    transform: translateX(3px);
  }
  100% {
    transform: translateX(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

// Form styles
.budget-form {
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
      box-shadow: 0 0 0 2px rgba($primary-color, 0.15);
    }
  }

  &.currency-group {
    align-items: flex-start;
  }

  .select-with-button {
    display: flex;
    align-items: center;
    gap: $spacing-xs;

    select {
      flex: 1;
    }

    .add-category-button {
      width: 36px;
      height: 36px;
      border-radius: $border-radius;
      background-color: $bg-secondary;
      border: 1px solid $chart-grid;
      color: $text-secondary;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: $transition-quick;

      &:hover {
        background-color: rgba($primary-color, 0.1);
        color: $primary-color;
        border-color: $primary-color;
      }
    }
  }

  .no-categories-warning {
    margin-top: $spacing-xs;
    display: flex;
    align-items: center;
    gap: $spacing-xs;
    color: $warning;
    font-size: $font-size-sm;

    i {
      color: $warning;
    }
  }

  .radio-group {
    display: flex;
    gap: $spacing-md;
    margin-top: $spacing-xs;
  }

  .radio-label {
    display: flex;
    align-items: center;
    gap: $spacing-xs;
    cursor: pointer;

    input[type="radio"] {
      margin: 0;
    }

    span {
      font-size: $font-size-md;
    }
  }
}

.budget-step {
  margin-bottom: $spacing-lg;

  .step-title {
    font-size: 1.125rem;
    font-weight: 600;
    margin-bottom: $spacing-md;
    color: $text-primary;

    .category-name {
      color: $primary-color;
    }
  }
}

.budget-summary {
  background-color: $bg-secondary;
  border-radius: $border-radius;
  padding: $spacing-md;
  margin-bottom: $spacing-lg;

  .budget-info {
    display: flex;
    flex-direction: column;
    gap: $spacing-xs;
    margin-bottom: $spacing-sm;

    .total-amount {
      font-size: 1.5rem;
      font-weight: 700;
      color: $text-primary;
    }

    .budget-details {
      display: flex;
      justify-content: space-between;
      color: $text-secondary;
      font-size: $font-size-sm;

      .allocated, .remaining {
        display: flex;
        flex-direction: column;

        .amount {
          font-weight: 600;
          color: $text-primary;

          &.negative {
            color: $negative;
          }
        }
      }
    }
  }

  .allocation-bar {
    height: 8px;
    background-color: $chart-grid;
    border-radius: 4px;
    overflow: hidden;

    &__fill {
      height: 100%;
      background-color: $primary-color;
      border-radius: 4px;
      transition: width 0.3s ease;
    }
  }
}

.subcategories-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
  margin-bottom: $spacing-lg;

  .subcategory-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: $spacing-sm;
    background-color: $bg-secondary;
    border-radius: $border-radius;
    transition: $transition-quick;

    &:hover {
      background-color: darken($bg-secondary, 3%);
    }

    .subcategory-info {
      display: flex;
      align-items: center;
      gap: $spacing-sm;
      flex: 1;

      .subcategory-icon {
        .icon-container {
          width: 32px;
          height: 32px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          justify-content: center;

          i {
            font-size: 1.1rem;
          }

          .fallback {
            width: 16px;
            height: 16px;
            border-radius: 4px;
          }
        }
      }

      .subcategory-name {
        font-weight: 500;
        color: $text-primary;
      }
    }

    .subcategory-allocation {
      width: 120px;

      input {
        width: 100%;
        padding: 8px;
        border: 1px solid rgba($chart-grid, 0.8);
        border-radius: 6px;
        font-size: $font-size-sm;
        text-align: right;

        &:focus {
          border-color: $primary-color;
          outline: none;
          box-shadow: 0 0 0 2px rgba($primary-color, 0.15);
        }
      }
    }
  }

  .add-subcategory {
    display: flex;
    justify-content: center;
    margin-top: $spacing-sm;

    .add-button {
      display: flex;
      align-items: center;
      gap: $spacing-xs;
      padding: $spacing-xs $spacing-sm;
      background-color: transparent;
      color: $primary-color;
      border: 1px dashed $primary-color;
      border-radius: $border-radius;
      cursor: pointer;
      transition: $transition-quick;

      &:hover {
        background-color: rgba($primary-color, 0.05);
      }

      i {
        font-size: $font-size-sm;
      }

      span {
        font-size: $font-size-sm;
        font-weight: 500;
      }
    }
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: $spacing-md;
  margin-top: $spacing-lg;
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

.category-manager-section {
  margin-top: $spacing-xl;
  border-top: 1px solid $chart-grid;
  padding-top: $spacing-lg;

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    padding: $spacing-md 0;

    h3 {
      margin: 0;
      font-size: $font-size-lg;
      color: $text-primary;
    }

    .toggle-button {
      background: none;
      border: none;
      color: $text-secondary;
      cursor: pointer;
      transition: $transition-quick;

      &:hover {
        color: $primary-color;
      }

      i {
        font-size: $font-size-md;
      }
    }
  }

  .section-content {
    margin-top: $spacing-md;
    padding: $spacing-md;
    border-radius: $border-radius;
    background-color: $bg-secondary;
    animation: slideDown 0.3s ease;
  }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>