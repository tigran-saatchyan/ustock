<template>
  <div class="month-year-picker">
    <div class="month-year-picker__selectors">
      <select v-model="selectedMonth" class="month-year-picker__select">
        <option v-for="(month, index) in months" :key="index" :value="index + 1">
          {{ month }}
        </option>
      </select>
      
      <select v-model="selectedYear" class="month-year-picker__select">
        <option v-for="year in availableYears" :key="year" :value="year">
          {{ year }}
        </option>
      </select>
    </div>
    
    <div class="month-year-picker__navigation">
      <button @click="previousMonth" class="month-year-picker__button">
        <i class="pi pi-chevron-left"></i>
      </button>
      
      <button @click="currentMonth" class="month-year-picker__button">
        Today
      </button>
      
      <button @click="nextMonth" class="month-year-picker__button">
        <i class="pi pi-chevron-right"></i>
      </button>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue';
import { useStore } from 'vuex';

export default {
  name: 'MonthYearPicker',
  
  setup() {
    const store = useStore();
    
    // Get current date
    const today = new Date();
    const currentMonthNum = today.getMonth() + 1; // JavaScript months are 0-indexed
    const currentYear = today.getFullYear();
    
    // List of months
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    
    // Generate available years (5 years back and 2 years forward)
    const availableYears = [];
    for (let year = currentYear - 5; year <= currentYear + 2; year++) {
      availableYears.push(year);
    }
    
    // Helper function to fetch historical rates for a month
    const fetchHistoricalRatesForMonth = (month, year) => {
      if (store.getters['personalFinance/useApiExchangeRates']) {
        // Format date as YYYY-MM-01
        const dateStr = `${year}-${String(month).padStart(2, '0')}-01`;
        
        // Check if we already have rates for this date
        const historicalRates = store.state.personalFinance.currencySettings.historicalRates || {};
        if (!historicalRates[dateStr]) {
          // Fetch historical rates for this month
          store.dispatch('personalFinance/fetchHistoricalRates', dateStr)
            .catch(error => {
              console.error('Error fetching historical rates:', error);
            });
        }
      }
    };

    // Get selected month and year from store with custom setters
    const selectedMonth = computed({
      get: () => store.getters['personalFinance/selectedMonth'],
      set: (value) => {
        store.dispatch('personalFinance/setSelectedMonth', value);
        fetchHistoricalRatesForMonth(value, selectedYear.value);
      }
    });
    
    const selectedYear = computed({
      get: () => store.getters['personalFinance/selectedYear'],
      set: (value) => {
        store.dispatch('personalFinance/setSelectedYear', value);
        fetchHistoricalRatesForMonth(selectedMonth.value, value);
      }
    });
    
    // Navigate to previous month
    const previousMonth = () => {
      if (selectedMonth.value === 1) {
        // If January, go to December of previous year
        selectedMonth.value = 12;
        selectedYear.value = selectedYear.value - 1;
      } else {
        // Otherwise, go to previous month
        selectedMonth.value = selectedMonth.value - 1;
      }
    };
    
    // Navigate to next month
    const nextMonth = () => {
      if (selectedMonth.value === 12) {
        // If December, go to January of next year
        selectedMonth.value = 1;
        selectedYear.value = selectedYear.value + 1;
      } else {
        // Otherwise, go to next month
        selectedMonth.value = selectedMonth.value + 1;
      }
    };
    
    // Navigate to current month
    const currentMonth = () => {
      selectedMonth.value = currentMonthNum;
      selectedYear.value = currentYear;
    };
    
    // Initialize with current month/year on component mount
    onMounted(() => {
      if (!selectedMonth.value) selectedMonth.value = currentMonthNum;
      if (!selectedYear.value) selectedYear.value = currentYear;
      
      // Fetch historical rates for the current month
      fetchHistoricalRatesForMonth(selectedMonth.value, selectedYear.value);
    });
    
    return {
      months,
      availableYears,
      selectedMonth,
      selectedYear,
      previousMonth,
      nextMonth,
      currentMonth
    };
  }
};
</script>

<style lang="scss" scoped>
.month-year-picker {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: $spacing-md;
  
  &__selectors {
    display: flex;
    gap: $spacing-sm;
  }
  
  &__select {
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
  
  &__navigation {
    display: flex;
    gap: $spacing-xs;
  }
  
  &__button {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: $spacing-xs $spacing-sm;
    border: 1px solid $chart-grid;
    border-radius: $border-radius;
    background-color: $bg-primary;
    color: $text-primary;
    cursor: pointer;
    transition: $transition-quick;
    
    &:hover {
      background-color: rgba($primary-color, 0.1);
    }
  }
}

// Responsive adjustments
@media (max-width: $breakpoint-sm) {
  .month-year-picker {
    flex-direction: column;
    gap: $spacing-sm;
    
    &__selectors,
    &__navigation {
      width: 100%;
      justify-content: space-between;
    }
  }
}
</style>