<template>
  <div class="budget-templates">
    <div class="templates-header">
      <h4 class="templates-title">{{ $t('finance.budgets.templates.title') || 'Budget Templates' }}</h4>
      <div class="templates-description">
        {{ $t('finance.budgets.templates.description') || 'Save time by using an existing budget as a template' }}
      </div>
    </div>
    
    <div v-if="isLoading" class="templates-loading">
      <i class="pi pi-spin pi-spinner"></i>
      <span>{{ $t('finance.budgets.templates.loading') || 'Loading previous budgets...' }}</span>
    </div>
    
    <div v-else-if="previousBudgets.length === 0" class="no-templates">
      <i class="pi pi-info-circle"></i>
      <span>{{ $t('finance.budgets.templates.none') || 'No previous budgets available to use as templates' }}</span>
    </div>
    
    <div v-else class="templates-list">
      <div 
        v-for="budget in previousBudgets" 
        :key="budget.id" 
        class="template-item"
        @click="selectTemplate(budget)"
        :class="{ 'selected': selectedTemplateId === budget.id }"
      >
        <div class="template-icon">
          <div class="icon-container" :style="{ backgroundColor: budget.category_color + '15' }">
            <i v-if="budget.category_icon" :class="budget.category_icon" :style="{ color: budget.category_color }"></i>
            <div v-else class="icon-fallback" :style="{ backgroundColor: budget.category_color }"></div>
          </div>
        </div>
        
        <div class="template-info">
          <div class="template-category">{{ budget.category_name }}</div>
          <div class="template-details">
            <span class="template-date">{{ formatBudgetDate(budget) }}</span>
            <span class="template-amount">{{ formatCurrency(budget.amount, budget.currency) }}</span>
          </div>
          
          <div v-if="budget.subcategory_budgets && budget.subcategory_budgets.length > 0" class="template-subcategories">
            <div class="subcategory-label">
              {{ $t('finance.categories.subcategories') || 'Subcategories' }}:
              <span class="subcategory-count">({{ budget.subcategory_budgets.length }})</span>
            </div>
          </div>
        </div>
        
        <div class="template-select">
          <div class="select-indicator" :class="{ 'selected': selectedTemplateId === budget.id }">
            <i class="pi pi-check"></i>
          </div>
        </div>
      </div>
    </div>
    
    <div class="templates-actions" v-if="previousBudgets.length > 0">
      <button 
        type="button" 
        class="button button--primary use-template-btn" 
        :disabled="!selectedTemplateId" 
        @click="useSelectedTemplate"
      >
        <i class="pi pi-copy"></i>
        {{ $t('finance.budgets.templates.use') || 'Use Selected Template' }}
      </button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useStore } from 'vuex';
import { formatCurrency } from '@/utils/formatters';

export default {
  name: 'BudgetTemplates',
  
  props: {
    currentMonth: {
      type: Number,
      required: true
    },
    currentYear: {
      type: Number,
      required: true
    }
  },
  
  emits: ['select-template'],
  
  setup(props, { emit }) {
    const store = useStore();
    const isLoading = ref(false);
    const previousBudgets = ref([]);
    const selectedTemplateId = ref(null);
    
    // Month names
    const monthNames = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    
    // Format budget date (Month Year)
    const formatBudgetDate = (budget) => {
      return `${monthNames[budget.month - 1]} ${budget.year}`;
    };
    
    // Load previous budgets
    const loadPreviousBudgets = async () => {
      isLoading.value = true;
      try {
        // Fetch previous budgets (only parent budgets)
        const response = await store.dispatch('personalFinance/fetchPreviousBudgets', {
          currentMonth: props.currentMonth,
          currentYear: props.currentYear
        });
        
        // Set the previous budgets
        previousBudgets.value = response.filter(budget => budget.is_parent_budget);
      } catch (error) {
        console.error('Error loading previous budgets:', error);
      } finally {
        isLoading.value = false;
      }
    };
    
    // Select a template
    const selectTemplate = (budget) => {
      selectedTemplateId.value = budget.id;
    };
    
    // Use the selected template
    const useSelectedTemplate = () => {
      if (!selectedTemplateId.value) return;
      
      const template = previousBudgets.value.find(b => b.id === selectedTemplateId.value);
      if (template) {
        emit('select-template', template);
      }
    };
    
    onMounted(() => {
      loadPreviousBudgets();
    });
    
    return {
      isLoading,
      previousBudgets,
      selectedTemplateId,
      formatBudgetDate,
      formatCurrency,
      selectTemplate,
      useSelectedTemplate
    };
  }
};
</script>

<style lang="scss" scoped>
.budget-templates {
  margin-bottom: $spacing-lg;
}

.templates-header {
  margin-bottom: $spacing-md;
  
  .templates-title {
    font-size: $font-size-md;
    font-weight: 600;
    margin: 0 0 $spacing-xs 0;
    color: $text-primary;
  }
  
  .templates-description {
    font-size: $font-size-sm;
    color: $text-secondary;
  }
}

.templates-loading,
.no-templates {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-lg;
  background-color: $bg-secondary;
  border-radius: $border-radius;
  text-align: center;
  
  i {
    font-size: 1.5rem;
    color: $text-secondary;
    margin-bottom: $spacing-sm;
  }
  
  span {
    color: $text-secondary;
    font-size: $font-size-sm;
  }
}

.templates-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: $spacing-md;
  padding-right: $spacing-xs;
  
  &::-webkit-scrollbar {
    width: 6px;
  }
  
  &::-webkit-scrollbar-track {
    background: rgba($chart-grid, 0.2);
    border-radius: 6px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: rgba($text-secondary, 0.2);
    border-radius: 6px;
    
    &:hover {
      background: rgba($text-secondary, 0.4);
    }
  }
}

.template-item {
  display: flex;
  align-items: center;
  padding: $spacing-sm;
  background-color: $bg-secondary;
  border-radius: $border-radius;
  cursor: pointer;
  transition: $transition-quick;
  
  &:hover {
    background-color: darken($bg-secondary, 3%);
  }
  
  &.selected {
    background-color: rgba($primary-color, 0.08);
    border: 1px solid rgba($primary-color, 0.3);
  }
  
  .template-icon {
    .icon-container {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: $spacing-md;
      
      i {
        font-size: 1.2rem;
      }
      
      .icon-fallback {
        width: 20px;
        height: 20px;
        border-radius: 4px;
      }
    }
  }
  
  .template-info {
    flex: 1;
    
    .template-category {
      font-weight: 500;
      color: $text-primary;
      margin-bottom: 2px;
    }
    
    .template-details {
      display: flex;
      justify-content: space-between;
      font-size: $font-size-sm;
      color: $text-secondary;
      margin-bottom: 2px;
      
      .template-amount {
        font-weight: 500;
        color: $primary-color;
      }
    }
    
    .template-subcategories {
      font-size: $font-size-xs;
      color: $text-secondary;
      
      .subcategory-label {
        display: flex;
        align-items: center;
        
        .subcategory-count {
          margin-left: 4px;
          opacity: 0.7;
        }
      }
    }
  }
  
  .template-select {
    margin-left: $spacing-sm;
    
    .select-indicator {
      width: 22px;
      height: 22px;
      border-radius: 50%;
      border: 1px solid $chart-grid;
      display: flex;
      align-items: center;
      justify-content: center;
      color: transparent;
      transition: $transition-quick;
      
      &.selected {
        background-color: $primary-color;
        border-color: $primary-color;
        color: white;
      }
      
      i {
        font-size: 0.8rem;
      }
    }
  }
}

.templates-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: $spacing-md;
  
  .use-template-btn {
    display: flex;
    align-items: center;
    gap: $spacing-xs;
    font-size: $font-size-sm;
    
    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }
}
</style>