<template>
  <div class="goals-view">
    <finance-navigation />
    
    <div class="goals-container">
      <div class="goals-header">
        <h2 class="goals-title">{{ $t('finance.goals.title') }}</h2>
        
        <button @click="showGoalForm = true" class="add-button">
          <i class="pi pi-plus"></i>
          <span>{{ $t('finance.goals.add') }}</span>
        </button>
      </div>
      
      <div v-if="isLoading" class="loading-spinner">
        <div class="spinner"></div>
        <p>{{ $t('finance.goals.loading') }}</p>
      </div>
      
      <!-- Goals Grid -->
      <div v-else-if="savingsGoals.length" class="goals-grid">
        <div 
          v-for="goal in savingsGoals" 
          :key="goal.id"
          class="goal-card"
          :class="{ 'achieved': goal.is_achieved }"
        >
          <div class="goal-card__header" :style="{ backgroundColor: goal.color }">
            <i :class="goal.icon || 'pi pi-flag'"></i>
            <div class="goal-card__status">
              {{ goal.is_achieved ? $t('finance.goals.status.achieved') : $t('finance.goals.status.inProgress') }}
            </div>
          </div>
          
          <div class="goal-card__content">
            <h3 class="goal-card__title">{{ goal.name }}</h3>
            
            <div class="goal-card__amounts">
              <div class="goal-card__current">{{ formatCurrency(goal.current_amount) }}</div>
              <div class="goal-card__target">{{ $t('common.of') }} {{ formatCurrency(goal.target_amount) }}</div>
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
              <i class="pi pi-calendar"></i>
              <span>{{ $t('finance.goals.form.targetDate') }}: {{ formatDate(goal.deadline) }}</span>
            </div>
            
            <div class="goal-card__buttons">
              <button 
                @click="showAddSavingsForm(goal)" 
                class="button button--outline"
                :style="{ borderColor: goal.color, color: goal.color }"
              >
                <i class="pi pi-plus"></i>
                <span>{{ $t('finance.goals.addSavings') }}</span>
              </button>
            </div>
          </div>
          
          <div class="goal-card__actions">
            <button @click="editGoal(goal)" class="action-button">
              <i class="pi pi-pencil"></i>
            </button>
            <button @click="deleteGoalConfirm(goal)" class="action-button delete">
              <i class="pi pi-trash"></i>
            </button>
          </div>
        </div>
      </div>
      
      <div v-else-if="!isLoading" class="empty-state">
        <p>{{ $t('finance.goals.noGoalsFound') }}</p>
        <button @click="showGoalForm = true" class="button button--primary">
          {{ $t('finance.goals.addFirst') }}
        </button>
      </div>
      
      <!-- Goal Form Modal -->
      <div class="modal" v-if="showGoalForm">
        <div class="modal-overlay" @click="showGoalForm = false"></div>
        <div class="modal-container">
          <div class="modal-header">
            <h3>{{ editMode ? $t('finance.goals.edit') : $t('finance.goals.add') }}</h3>
            <button @click="showGoalForm = false" class="close-button">
              <i class="pi pi-times"></i>
            </button>
          </div>
          
          <div class="modal-body">
            <form @submit.prevent="saveGoal" class="goal-form">
              <!-- Goal Name -->
              <div class="form-group">
                <label for="name">{{ $t('finance.goals.form.goalName') }}</label>
                <input type="text" id="name" v-model="goalForm.name" required>
              </div>
              
              <!-- Target and Current Amount -->
              <div class="form-row">
                <div class="form-group">
                  <label for="target-amount">{{ $t('finance.goals.form.targetAmount') }}</label>
                  <input type="number" id="target-amount" v-model="goalForm.target_amount" step="0.01" min="0.01" required>
                </div>
                
                <div class="form-group">
                  <label for="current-amount">{{ $t('finance.goals.form.currentAmount') }}</label>
                  <input type="number" id="current-amount" v-model="goalForm.current_amount" step="0.01" min="0">
                </div>
              </div>
              
              <!-- Deadline Date -->
              <div class="form-group">
                <label for="deadline">{{ $t('finance.goals.form.targetDate') }}</label>
                <input type="date" id="deadline" v-model="goalForm.deadline">
              </div>
              
              <!-- Color and Icon -->
              <div class="form-row">
                <div class="form-group">
                  <label for="color">{{ $t('finance.goals.form.goalColor') }}</label>
                  <input type="color" id="color" v-model="goalForm.color">
                </div>
                
                <div class="form-group">
                  <label for="icon">{{ $t('finance.goals.form.goalIcon') }}</label>
                  <select id="icon" v-model="goalForm.icon">
                    <option value="pi pi-flag">{{ $t('finance.goals.icons.flag') }}</option>
                    <option value="pi pi-home">{{ $t('finance.goals.icons.house') }}</option>
                    <option value="pi pi-car">{{ $t('finance.goals.icons.car') }}</option>
                    <option value="pi pi-shopping-cart">{{ $t('finance.goals.icons.shopping') }}</option>
                    <option value="pi pi-plane">{{ $t('finance.goals.icons.travel') }}</option>
                    <option value="pi pi-heart">{{ $t('finance.goals.icons.health') }}</option>
                    <option value="pi pi-book">{{ $t('finance.goals.icons.education') }}</option>
                    <option value="pi pi-briefcase">{{ $t('finance.goals.icons.business') }}</option>
                    <option value="pi pi-gift">{{ $t('finance.goals.icons.gift') }}</option>
                    <option value="pi pi-university">{{ $t('finance.goals.icons.retirement') }}</option>
                  </select>
                </div>
              </div>
              
              <!-- Form Actions -->
              <div class="form-actions">
                <button type="button" @click="showGoalForm = false" class="button button--secondary">
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
      
      <!-- Add Savings Modal -->
      <div class="modal" v-if="showAddSavings">
        <div class="modal-overlay" @click="showAddSavings = false"></div>
        <div class="modal-container small-dialog">
          <div class="modal-header">
            <h3>{{ $t('finance.goals.addSavings') }}</h3>
            <button @click="showAddSavings = false" class="close-button">
              <i class="pi pi-times"></i>
            </button>
          </div>
          
          <div class="modal-body">
            <form @submit.prevent="addSavings" class="savings-form">
              <div v-if="selectedGoal" class="goal-info">
                <div class="goal-info__name">{{ selectedGoal.name }}</div>
                <div class="goal-info__progress">
                  <div>{{ $t('finance.goals.form.currentAmount') }}: {{ formatCurrency(selectedGoal.current_amount) }}</div>
                  <div>{{ $t('finance.goals.form.targetAmount') }}: {{ formatCurrency(selectedGoal.target_amount) }}</div>
                </div>
              </div>
              
              <div class="form-group">
                <label for="amount">{{ $t('finance.goals.form.currentAmount') }}</label>
                <input type="number" id="amount" v-model="savingsAmount" step="0.01" min="0.01" required>
              </div>
              
              <div class="form-actions">
                <button type="button" @click="showAddSavings = false" class="button button--secondary">
                  {{ $t('common.cancel') }}
                </button>
                <button type="submit" class="button button--primary">
                  {{ $t('common.add') }}
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
            <p>{{ $t('finance.goals.confirmDelete') }}</p>
            <p v-if="goalToDelete" class="delete-details">
              <strong>{{ goalToDelete.name }}</strong>
              <span>{{ formatCurrency(goalToDelete.current_amount) }} / {{ formatCurrency(goalToDelete.target_amount) }}</span>
            </p>
            
            <div class="form-actions">
              <button @click="showDeleteConfirm = false" class="button button--secondary">
                {{ $t('common.cancel') }}
              </button>
              <button @click="deleteGoal" class="button button--delete">
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

export default {
  name: 'GoalsView',
  
  components: {
    FinanceNavigation
  },
  
  setup() {
    const store = useStore();
    // eslint-disable-next-line no-unused-vars
    const { locale, t } = useI18n(); // t is used in template
    
    // State
    const showGoalForm = ref(false);
    const showAddSavings = ref(false);
    const showDeleteConfirm = ref(false);
    const editMode = ref(false);
    const goalToDelete = ref(null);
    const selectedGoal = ref(null);
    const savingsAmount = ref('');
    
    // Default form values
    const defaultForm = {
      name: '',
      target_amount: '',
      current_amount: 0,
      deadline: '',
      color: '#f7c73a',
      icon: 'pi pi-flag'
    };
    
    // Form model
    const goalForm = ref({ ...defaultForm });
    
    // Store getters
    const isLoading = computed(() => store.getters['personalFinance/isLoading']);
    const savingsGoals = computed(() => store.getters['personalFinance/savingsGoals']);
    
    // Initialize data
    onMounted(async () => {
      await store.dispatch('personalFinance/fetchSavingsGoals');
    });
    
    // Edit goal
    const editGoal = (goal) => {
      editMode.value = true;
      
      goalForm.value = {
        id: goal.id,
        name: goal.name,
        target_amount: goal.target_amount,
        current_amount: goal.current_amount,
        deadline: goal.deadline || '',
        color: goal.color,
        icon: goal.icon
      };
      
      showGoalForm.value = true;
    };
    
    // Show add savings form
    const showAddSavingsForm = (goal) => {
      selectedGoal.value = goal;
      savingsAmount.value = '';
      showAddSavings.value = true;
    };
    
    // Add savings to goal
    const addSavings = async () => {
      if (!selectedGoal.value || !savingsAmount.value) return;
      
      try {
        await store.dispatch('personalFinance/addToSavingsGoal', {
          id: selectedGoal.value.id,
          amount: parseFloat(savingsAmount.value)
        });
        
        showAddSavings.value = false;
        selectedGoal.value = null;
        savingsAmount.value = '';
      } catch (error) {
        console.error('Error adding to savings goal:', error);
        // Error handling would go here
      }
    };
    
    // Save goal (create or update)
    const saveGoal = async () => {
      try {
        if (editMode.value) {
          // Update existing goal
          await store.dispatch('personalFinance/updateSavingsGoal', {
            id: goalForm.value.id,
            data: { ...goalForm.value }
          });
        } else {
          // Create new goal
          await store.dispatch('personalFinance/createSavingsGoal', { ...goalForm.value });
        }
        
        // Reset form and close modal
        resetForm();
        showGoalForm.value = false;
      } catch (error) {
        console.error('Error saving goal:', error);
        // Error handling would go here
      }
    };
    
    // Confirm goal delete
    const deleteGoalConfirm = (goal) => {
      goalToDelete.value = goal;
      showDeleteConfirm.value = true;
    };
    
    // Delete goal
    const deleteGoal = async () => {
      if (!goalToDelete.value) return;
      
      try {
        await store.dispatch('personalFinance/deleteSavingsGoal', goalToDelete.value.id);
        showDeleteConfirm.value = false;
        goalToDelete.value = null;
      } catch (error) {
        console.error('Error deleting goal:', error);
        // Error handling would go here
      }
    };
    
    // Reset form to defaults
    const resetForm = () => {
      editMode.value = false;
      goalForm.value = { ...defaultForm };
    };
    
    // Helper function to format currency
    const formatCurrency = (amount) => {
      const currencyLocale = locale.value === 'ru' ? 'ru-RU' : 'en-US';
      const currencyCode = 'USD'; // This could be dynamic based on user settings
      
      return new Intl.NumberFormat(currencyLocale, {
        style: 'currency',
        currency: currencyCode
      }).format(amount);
    };
    
    // Helper function to format dates
    const formatDate = (dateString) => {
      if (!dateString) return '';
      
      const dateLocale = locale.value === 'ru' ? 'ru-RU' : 'en-US';
      const date = new Date(dateString);
      
      return new Intl.DateTimeFormat(dateLocale, {
        month: 'long',
        day: 'numeric',
        year: 'numeric'
      }).format(date);
    };
    
    return {
      showGoalForm,
      showAddSavings,
      showDeleteConfirm,
      editMode,
      goalToDelete,
      selectedGoal,
      savingsAmount,
      goalForm,
      isLoading,
      savingsGoals,
      editGoal,
      showAddSavingsForm,
      addSavings,
      saveGoal,
      deleteGoalConfirm,
      deleteGoal,
      formatCurrency,
      formatDate
    };
  }
};
</script>

<style lang="scss" scoped>
.goals-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.goals-container {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.goals-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.goals-title {
  margin: 0;
  color: #333333;
  font-size: 24px;
  font-weight: 600;
}

.add-button {
  display: flex;
  align-items: center;
  padding: 8px 16px;
  background-color: #f7941d; /* Changed to orange */
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background-color: #e58714; /* Darker orange */
  }
  
  i {
    margin-right: 4px;
  }
}

.goals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.goal-card {
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
  position: relative;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
  
  &__header {
    background-color: #f7941d; /* Changed to orange */
    color: white;
    padding: 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    i {
      font-size: 24px;
    }
  }
  
  &__status {
    font-size: 14px;
    opacity: 0.9;
    background-color: rgba(255, 255, 255, 0.2);
    padding: 2px 8px;
    border-radius: 12px;
  }
  
  &__content {
    padding: 16px;
  }
  
  &__title {
    font-size: 18px;
    font-weight: 600;
    margin: 0 0 8px 0;
  }
  
  &__amounts {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
  }
  
  &__current {
    font-size: 20px;
    font-weight: 700;
    color: #f7941d; /* Changed to orange */
  }
  
  &__target {
    color: #666666;
    display: flex;
    align-items: flex-end;
  }
  
  &__progress {
    margin-bottom: 16px;
  }
  
  &__deadline {
    display: flex;
    align-items: center;
    color: #666666;
    margin-bottom: 16px;
    font-size: 14px;
    
    i {
      margin-right: 4px;
    }
  }
  
  &__buttons {
    display: flex;
    justify-content: center;
  }
  
  &__actions {
    position: absolute;
    top: 16px;
    right: 16px;
    display: flex;
    gap: 4px;
    
    .action-button {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: rgba(255, 255, 255, 0.2);
      border: none;
      color: white;
      cursor: pointer;
      transition: all 0.2s ease;
      
      &:hover {
        background-color: rgba(255, 255, 255, 0.3);
      }
      
      &.delete:hover {
        background-color: rgba(255, 0, 0, 0.2);
      }
    }
  }
  
  &.achieved {
    .goal-card__header {
      background-color: #4caf50;
    }
    
    .goal-card__current,
    .progress-bar__fill {
      color: #4caf50;
      background-color: #4caf50;
    }
    
    &::after {
      content: '';
      position: absolute;
      width: 40px;
      height: 40px;
      background-color: #4caf50;
      top: -20px;
      right: -20px;
      transform: rotate(45deg);
      z-index: 1;
    }
    
    &::before {
      content: '\e930'; // Checkmark icon
      font-family: 'primeicons';
      position: absolute;
      top: 5px;
      right: 5px;
      color: white;
      z-index: 2;
      font-size: 12px;
    }
  }
}

.progress-bar {
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  margin-bottom: 4px;
  overflow: hidden;
  
  &__fill {
    height: 100%;
    background-color: #f7941d; /* Changed to orange */
    border-radius: 4px;
    transition: width 0.3s ease;
  }
  
  &__percentage {
    font-size: 14px;
    text-align: right;
    color: #666666;
  }
}

.button {
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  
  i {
    margin-right: 4px;
  }
  
  &--outline {
    background: none;
    border: 1px solid #f7941d; /* Changed to orange */
    color: #f7941d; /* Changed to orange */
    
    &:hover {
      background-color: rgba(247, 148, 29, 0.05); /* Changed to orange */
    }
  }
  
  &--primary {
    background-color: #f7941d; /* Changed to orange */
    color: white;
    border: none;
    
    &:hover {
      background-color: #e58714; /* Darker orange */
    }
  }
  
  &--secondary {
    background-color: #f5f5f5;
    color: #333333;
    border: none;
    
    &:hover {
      background-color: #e8e8e8;
    }
  }
  
  &--delete {
    background-color: #f44336;
    color: white;
    border: none;
    
    &:hover {
      background-color: #d32f2f;
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
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  z-index: 1001;
  
  &.confirm-dialog,
  &.small-dialog {
    max-width: 400px;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #e0e0e0;
  
  h3 {
    margin: 0;
    color: #333333;
    font-size: 20px;
  }
}

.close-button {
  background: none;
  border: none;
  font-size: 18px;
  color: #666666;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    color: #333333;
  }
}

.modal-body {
  padding: 24px;
}

// Form styles
.goal-form,
.savings-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
  
  label {
    font-size: 14px;
    margin-bottom: 4px;
    color: #666666;
    font-weight: 500;
  }
  
  input, select {
    padding: 8px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    font-size: 16px;
    transition: all 0.2s ease;
    
    &:focus {
      border-color: #f7941d; /* Changed to orange */
      outline: none;
    }
  }
  
  input[type="color"] {
    height: 40px;
    cursor: pointer;
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 16px;
}

.goal-info {
  background-color: #f5f5f5;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  
  &__name {
    font-weight: 600;
    margin-bottom: 4px;
  }
  
  &__progress {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
    color: #666666;
  }
}

.delete-details {
  display: flex;
  justify-content: space-between;
  padding: 16px;
  background-color: #f5f5f5;
  border-radius: 8px;
  margin: 16px 0;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  
  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(247, 148, 29, 0.2); /* Changed to orange */
    border-radius: 50%;
    border-top-color: #f7941d; /* Changed to orange */
    animation: spin 1s ease-in-out infinite;
    margin-bottom: 16px;
  }
  
  p {
    color: #666666;
  }
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #666666;
  
  p {
    margin-bottom: 16px;
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>