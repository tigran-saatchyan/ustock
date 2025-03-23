<template>
  <div class="category-manager">
    <div class="category-manager__header">
      <h3>{{ $t('finance.categories.manage') || 'Manage Categories' }}</h3>
      <button @click="addCategory(null)" class="add-button">
        <i class="pi pi-plus"></i>
        <span>{{ $t('finance.categories.add') || 'Add Category' }}</span>
      </button>
    </div>

    <div v-if="isLoading" class="loading-spinner">
      <div class="spinner"></div>
      <p>{{ $t('finance.categories.loading') || 'Loading categories...' }}</p>
    </div>

    <div v-else-if="mainCategories.length === 0" class="empty-state">
      <p>{{ $t('finance.categories.noCategories') || 'No categories found' }}</p>
      <button @click="addCategory(null)" class="button button--primary">
        {{ $t('finance.categories.addFirst') || 'Add your first category' }}
      </button>
    </div>

    <div v-else class="categories-list">
      <!-- Main categories -->
      <div v-for="category in mainCategories" :key="category.id" class="category-item">
        <div class="category-item__header" @click="toggleCategoryCollapse(category.id)">
          <div class="category-item__icon">
            <div class="icon-container" :style="{ backgroundColor: category.color + '15' }">
              <i v-if="category.icon" :class="category.icon" :style="{ color: category.color }"></i>
              <div v-else class="category-item__color" :style="{ backgroundColor: category.color }"></div>
            </div>
          </div>
          <div class="category-item__name">
            {{ category.name }}
            <span v-if="category.is_income" class="category-badge income">
              {{ $t('finance.categories.income') || 'Income' }}
            </span>
            <span v-else class="category-badge expense">
              {{ $t('finance.categories.expense') || 'Expense' }}
            </span>
          </div>
          <div class="category-item__collapse">
            <i v-if="hasSubcategories(category)" 
               :class="isCategoryCollapsed(category.id) ? 'pi pi-chevron-down' : 'pi pi-chevron-up'"></i>
          </div>
          <div class="category-item__actions" @click.stop>
            <button @click="addCategory(category.id)" class="action-button" :title="$t('finance.categories.addSubcategory') || 'Add Subcategory'">
              <i class="pi pi-plus-circle"></i>
            </button>
            <button @click="editCategory(category)" class="action-button" :title="$t('finance.categories.edit') || 'Edit'">
              <i class="pi pi-pencil"></i>
            </button>
            <button 
              @click="deleteCategory(category)" 
              class="action-button delete"
              :title="$t('finance.categories.delete') || 'Delete'"
              :disabled="hasSubcategories(category)"
            >
              <i class="pi pi-trash"></i>
            </button>
          </div>
        </div>

        <!-- Subcategories -->
        <div v-if="category.subcategories && category.subcategories.length > 0 && !isCategoryCollapsed(category.id)" class="subcategories-list">
          <div v-for="subcategory in category.subcategories" :key="subcategory.id" class="subcategory-item">
            <div class="subcategory-item__icon">
              <div class="icon-container" :style="{ backgroundColor: subcategory.color + '15' }">
                <i v-if="subcategory.icon" :class="subcategory.icon" :style="{ color: subcategory.color }"></i>
                <div v-else class="subcategory-item__color" :style="{ backgroundColor: subcategory.color }"></div>
              </div>
            </div>
            <div class="subcategory-item__name">{{ subcategory.name }}</div>
            <div class="subcategory-item__actions">
              <button @click="editCategory(subcategory)" class="action-button" :title="$t('finance.categories.edit') || 'Edit'">
                <i class="pi pi-pencil"></i>
              </button>
              <button @click="deleteCategory(subcategory)" class="action-button delete" :title="$t('finance.categories.delete') || 'Delete'">
                <i class="pi pi-trash"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Category Form Modal -->
    <div class="modal modern" v-if="showCategoryForm">
      <div class="modal-overlay" @click="showCategoryForm = false"></div>
      <div class="modal-container">
        <div class="modal-header">
          <h3>
            <span v-if="editMode">{{ $t('finance.categories.edit') || 'Edit Category' }}</span>
            <span v-else-if="selectedParentId">{{ $t('finance.categories.addSubcategory') || 'Add Subcategory' }}</span>
            <span v-else>{{ $t('finance.categories.add') || 'Add Category' }}</span>
          </h3>
          <button @click="showCategoryForm = false" class="close-button">
            <i class="pi pi-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <div v-if="formError" class="form-error-message">
            <i class="pi pi-exclamation-circle"></i>
            <span>{{ formError }}</span>
          </div>
          
          <!-- Category Preview Card -->
          <div class="category-preview-card">
            <div class="preview-icon-container" :style="{ backgroundColor: categoryForm.color + '15' }">
              <i v-if="categoryForm.icon" :class="categoryForm.icon" :style="{ color: categoryForm.color }"></i>
              <div v-else class="preview-fallback" :style="{ backgroundColor: categoryForm.color }"></div>
            </div>
            <div class="preview-name">
              <span v-if="categoryForm.name">{{ categoryForm.name }}</span>
              <span v-else class="preview-placeholder">{{ $t('finance.categories.name') || 'Category Name' }}</span>
            </div>
            <div class="preview-badge" v-if="!categoryForm.parent">
              <span v-if="!categoryForm.is_expense" class="category-badge income">
                {{ $t('finance.categories.income') || 'Income' }}
              </span>
              <span v-else class="category-badge expense">
                {{ $t('finance.categories.expense') || 'Expense' }}
              </span>
            </div>
          </div>
          <div class="preview-note">This is how your category will appear</div>
          
          <form @submit.prevent="saveCategory" class="category-form">
            <!-- Category Name -->
            <div class="form-group">
              <label for="category-name">{{ $t('finance.categories.name') || 'Category Name' }}</label>
              <div class="form-input-with-icon">
                <i class="pi pi-tag"></i>
                <input type="text" id="category-name" v-model="categoryForm.name" required placeholder="Enter category name">
              </div>
            </div>
            
            <!-- Parent Category (for subcategories) -->
            <div class="form-group" v-if="!editMode && !selectedParentId">
              <label for="parent-category">{{ $t('finance.categories.parent') || 'Parent Category (optional)' }}</label>
              <div class="form-input-with-icon">
                <i class="pi pi-sitemap"></i>
                <select id="parent-category" v-model="categoryForm.parent">
                  <option :value="null">{{ $t('finance.categories.noParent') || 'No parent (main category)' }}</option>
                  <option v-for="category in mainCategories" :key="category.id" :value="category.id">
                    {{ category.name }}
                  </option>
                </select>
              </div>
            </div>
            
            <!-- Category Type -->
            <div class="form-group" v-if="!selectedParentId && (!editMode || !categoryForm.parent)">
              <label>{{ $t('finance.categories.type') || 'Category Type' }}</label>
              <div class="type-selector">
                <button 
                  type="button"
                  :class="['type-button', categoryForm.is_expense ? 'active' : '']"
                  @click="setCategoryType(true)"
                >
                  <i class="pi pi-arrow-down"></i>
                  <span>{{ $t('finance.categories.expense') || 'Expense' }}</span>
                </button>
                <button 
                  type="button"
                  :class="['type-button', !categoryForm.is_expense ? 'active' : '']"
                  @click="setCategoryType(false)"
                >
                  <i class="pi pi-arrow-up"></i>
                  <span>{{ $t('finance.categories.income') || 'Income' }}</span>
                </button>
              </div>
            </div>
            
            <div class="form-row">
              <!-- Category Color -->
              <div class="form-group color-group">
                <label for="category-color">{{ $t('finance.categories.color') || 'Color' }}</label>
                <div class="color-picker-container">
                  <input type="color" id="category-color" v-model="categoryForm.color">
                  <div class="color-presets">
                    <div 
                      v-for="(color, index) in colorPresets" 
                      :key="index" 
                      class="color-preset" 
                      :style="{ backgroundColor: color }"
                      @click="categoryForm.color = color"
                    ></div>
                  </div>
                </div>
              </div>
              
              <!-- Icon Selector -->
              <div class="form-group icon-group">
                <label for="category-icon">{{ $t('finance.categories.icon') || 'Icon (optional)' }}</label>
                <div class="icon-selector">
                  <div class="selected-icon" @click="showIconDropdown = !showIconDropdown">
                    <i v-if="categoryForm.icon" :class="categoryForm.icon"></i>
                    <span v-else class="no-icon">{{ $t('finance.categories.selectIcon') || 'Select icon' }}</span>
                    <i class="pi pi-chevron-down"></i>
                  </div>
                  <div v-if="showIconDropdown" class="icon-dropdown-overlay" @click="showIconDropdown = false"></div>
                  <div v-if="showIconDropdown" class="icon-dropdown">
                    <div class="icon-search">
                      <i class="pi pi-search"></i>
                      <input 
                        type="text" 
                        v-model="iconSearch" 
                        :placeholder="$t('common.search') || 'Search'" 
                        @input="filterIcons"
                      >
                    </div>
                    <div class="icons-grid">
                      <div 
                        v-for="icon in filteredIcons" 
                        :key="icon.class" 
                        class="icon-item"
                        @click="selectIcon(icon.class)"
                      >
                        <i :class="icon.class"></i>
                        <span class="icon-name">{{ icon.name }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Form Actions -->
            <div class="form-actions">
              <button type="button" @click="showCategoryForm = false" class="button button--secondary">
                {{ $t('common.cancel') || 'Cancel' }}
              </button>
              <button type="submit" class="button button--primary">
                <i class="pi" :class="editMode ? 'pi-check' : 'pi-plus'"></i>
                {{ editMode ? ($t('common.update') || 'Update') : ($t('common.save') || 'Save') }}
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
          <h3>{{ $t('finance.confirmDelete') || 'Confirm Delete' }}</h3>
          <button @click="showDeleteConfirm = false" class="close-button">
            <i class="pi pi-times"></i>
          </button>
        </div>
        
        <div class="modal-body">
          <p class="delete-message">{{ $t('finance.categories.confirmDelete') || 'Are you sure you want to delete this category?' }}</p>
          <div v-if="categoryToDelete" class="delete-details">
            <div class="icon-container" :style="{ backgroundColor: categoryToDelete.color + '15' }">
              <i v-if="categoryToDelete.icon" :class="categoryToDelete.icon" :style="{ color: categoryToDelete.color }"></i>
              <div v-else class="color-preview" :style="{ backgroundColor: categoryToDelete.color }"></div>
            </div>
            <strong>{{ categoryToDelete.name }}</strong>
          </div>

          <div v-if="hasTransactions" class="warning-message">
            <i class="pi pi-exclamation-triangle"></i>
            <span>{{ $t('finance.categories.deleteWarning') || 'This will also delete all transactions associated with this category.' }}</span>
          </div>
          
          <div class="form-actions">
            <button @click="showDeleteConfirm = false" class="button button--secondary">
              {{ $t('common.cancel') || 'Cancel' }}
            </button>
            <button @click="confirmDelete" class="button button--delete">
              {{ $t('common.delete') || 'Delete' }}
            </button>
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

export default {
  name: 'CategoryManager',
  
  setup() {
    const store = useStore();
    const { t } = useI18n();
    
    // Local state
    const showCategoryForm = ref(false);
    const showDeleteConfirm = ref(false);
    const editMode = ref(false);
    const formError = ref('');
    const categoryToDelete = ref(null);
    const selectedParentId = ref(null);
    const hasTransactions = ref(false);
    const showIconDropdown = ref(false);
    const iconSearch = ref('');
    const collapsedCategories = ref({});
    
    // Color presets for the color picker
    const colorPresets = [
      '#E57373', // Red
      '#F06292', // Pink
      '#BA68C8', // Purple
      '#9575CD', // Deep Purple
      '#7986CB', // Indigo
      '#64B5F6', // Blue
      '#4FC3F7', // Light Blue
      '#4DD0E1', // Cyan
      '#4DB6AC', // Teal
      '#81C784', // Green
      '#AED581', // Light Green
      '#DCE775', // Lime
      '#FFD54F', // Amber
      '#FFB74D', // Orange
      '#FF8A65', // Deep Orange
      '#A1887F'  // Brown
    ];
    
    // Available icons
    const availableIcons = [
      { name: 'Home', class: 'pi pi-home' },
      { name: 'Credit Card', class: 'pi pi-credit-card' },
      { name: 'Car', class: 'pi pi-car' },
      { name: 'Gift', class: 'pi pi-gift' },
      { name: 'Food', class: 'pi pi-shopping-cart' },
      { name: 'Health', class: 'pi pi-heart' },
      { name: 'Education', class: 'pi pi-book' },
      { name: 'Travel', class: 'pi pi-globe' },
      { name: 'Entertainment', class: 'pi pi-video' },
      { name: 'Transport', class: 'pi pi-ticket' },
      { name: 'Bills', class: 'pi pi-file' },
      { name: 'Sports', class: 'pi pi-flag' },
      { name: 'Business', class: 'pi pi-briefcase' },
      { name: 'Clothing', class: 'pi pi-shopping-bag' },
      { name: 'Tech', class: 'pi pi-desktop' },
      { name: 'Phone', class: 'pi pi-mobile' },
      { name: 'Cash', class: 'pi pi-wallet' },
      { name: 'Money', class: 'pi pi-dollar' },
      { name: 'Bank', class: 'pi pi-building' },
      { name: 'Investment', class: 'pi pi-chart-line' },
      { name: 'Income', class: 'pi pi-arrow-up' },
      { name: 'Expense', class: 'pi pi-arrow-down' },
      { name: 'Calendar', class: 'pi pi-calendar' },
      { name: 'Account', class: 'pi pi-user' }
    ];
    
    // Filtered icons based on search
    const filteredIcons = ref([...availableIcons]);
    
    // Filter icons based on search term
    const filterIcons = () => {
      if (!iconSearch.value) {
        filteredIcons.value = [...availableIcons];
        return;
      }
      
      const searchTerm = iconSearch.value.toLowerCase();
      filteredIcons.value = availableIcons.filter(icon => 
        icon.name.toLowerCase().includes(searchTerm) || 
        icon.class.toLowerCase().includes(searchTerm)
      );
    };
    
    // Select an icon and close dropdown
    const selectIcon = (iconClass) => {
      categoryForm.value.icon = iconClass;
      showIconDropdown.value = false;
      
      // Scroll back to top of modal if needed
      if (document.querySelector('.modal-container')) {
        document.querySelector('.modal-container').scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      }
    };
    
    // Default form values
    const defaultForm = {
      name: '',
      parent: null,
      is_expense: true,
      is_income: false,
      color: '#e08200',
      icon: ''
    };
    
    // Form model
    const categoryForm = ref({ ...defaultForm });
    
    // Computed properties
    const isLoading = computed(() => store.getters['personalFinance/isLoading']);
    const categories = computed(() => store.getters['personalFinance/categories']);
    
    // Filter for main categories (no parent)
    const mainCategories = computed(() => 
      categories.value.filter(cat => !cat.parent)
    );
    
    // Initialize data
    onMounted(async () => {
      await store.dispatch('personalFinance/fetchCategories');
    });
    
    // Add new category (or subcategory if parentId is provided)
    const addCategory = (parentId) => {
      editMode.value = false;
      formError.value = '';
      selectedParentId.value = parentId;
      
      // Reset form
      categoryForm.value = { ...defaultForm };
      
      // If parentId is provided, set it in the form
      if (parentId) {
        categoryForm.value.parent = parentId;
        
        // Copy is_expense and is_income from parent category
        const parentCategory = categories.value.find(c => c.id === parentId);
        if (parentCategory) {
          categoryForm.value.is_expense = parentCategory.is_expense;
          categoryForm.value.is_income = parentCategory.is_income;
        }
      }
      
      showCategoryForm.value = true;
    };
    
    // Edit existing category
    const editCategory = (category) => {
      editMode.value = true;
      formError.value = '';
      selectedParentId.value = category.parent;
      
      categoryForm.value = {
        id: category.id,
        name: category.name,
        parent: category.parent,
        is_expense: category.is_expense,
        is_income: category.is_income,
        color: category.color,
        icon: category.icon || ''
      };
      
      showCategoryForm.value = true;
    };
    
    // Delete category
    const deleteCategory = (category) => {
      categoryToDelete.value = category;
      
      // Check if this category has subcategories
      if (hasSubcategories(category)) {
        formError.value = t('finance.categories.hasSubcategories') || 
          'Cannot delete a category with subcategories. Please delete subcategories first.';
        return;
      }
      
      // Check if category has associated transactions
      // For demo purposes, we'll simulate this check
      hasTransactions.value = false; // You would typically check this from the API
      
      showDeleteConfirm.value = true;
    };
    
    // Set category type (expense or income)
    const setCategoryType = (isExpense) => {
      categoryForm.value.is_expense = isExpense;
      categoryForm.value.is_income = !isExpense;
    };
    
    // Save category (create or update)
    const saveCategory = async () => {
      try {
        formError.value = '';
        
        if (editMode.value) {
          // Update existing category
          await store.dispatch('personalFinance/updateCategory', {
            id: categoryForm.value.id,
            data: { ...categoryForm.value }
          });
        } else {
          // Create new category
          await store.dispatch('personalFinance/createCategory', { ...categoryForm.value });
        }
        
        // Fetch categories to update the list immediately
        await store.dispatch('personalFinance/fetchCategories');
        
        // Reset form and close modal
        resetForm();
        showCategoryForm.value = false;
      } catch (error) {
        console.error('Error saving category:', error);
        
        if (error.response && error.response.data) {
          const errorData = error.response.data;
          
          if (errorData.detail) {
            formError.value = errorData.detail;
          } else if (errorData.non_field_errors) {
            formError.value = errorData.non_field_errors.join(', ');
          } else {
            // Check for field-specific errors
            const fieldErrors = [];
            
            for (const [field, errors] of Object.entries(errorData)) {
              if (Array.isArray(errors)) {
                fieldErrors.push(`${field}: ${errors.join(', ')}`);
              }
            }
            
            if (fieldErrors.length > 0) {
              formError.value = fieldErrors.join('; ');
            } else {
              formError.value = 'An error occurred while saving the category.';
            }
          }
        } else {
          formError.value = 'An unexpected error occurred. Please try again.';
        }
      }
    };
    
    // Confirm delete
    const confirmDelete = async () => {
      if (!categoryToDelete.value) return;
      
      try {
        await store.dispatch('personalFinance/deleteCategory', categoryToDelete.value.id);
        
        // Fetch categories to update the list immediately
        await store.dispatch('personalFinance/fetchCategories');
        
        showDeleteConfirm.value = false;
        categoryToDelete.value = null;
      } catch (error) {
        console.error('Error deleting category:', error);
        
        // Show error message
        if (error.response && error.response.data) {
          formError.value = error.response.data.detail || 'Failed to delete category';
        } else {
          formError.value = 'An unexpected error occurred while deleting the category.';
        }
      }
    };
    
    // Reset form to defaults
    const resetForm = () => {
      editMode.value = false;
      categoryForm.value = { ...defaultForm };
      selectedParentId.value = null;
    };
    
    // Check if a category has subcategories
    const hasSubcategories = (category) => {
      return category.subcategories && category.subcategories.length > 0;
    };
    
    // Toggle category collapse state
    const toggleCategoryCollapse = (categoryId) => {
      collapsedCategories.value[categoryId] = !collapsedCategories.value[categoryId];
    };
    
    // Check if a category is collapsed
    const isCategoryCollapsed = (categoryId) => {
      return !!collapsedCategories.value[categoryId];
    };
    
    return {
      showCategoryForm,
      showDeleteConfirm,
      editMode,
      formError,
      categoryToDelete,
      categoryForm,
      isLoading,
      categories,
      mainCategories,
      selectedParentId,
      hasTransactions,
      showIconDropdown,
      iconSearch,
      filteredIcons,
      collapsedCategories,
      colorPresets,
      addCategory,
      editCategory,
      deleteCategory,
      saveCategory,
      confirmDelete,
      hasSubcategories,
      toggleCategoryCollapse,
      isCategoryCollapsed,
      filterIcons,
      selectIcon,
      setCategoryType
    };
  }
};
</script>

<style lang="scss" scoped>
.category-manager {
  margin-bottom: $spacing-xl;
}

.category-manager__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-md;
  
  h3 {
    font-size: $font-size-lg;
    margin: 0;
    color: $text-primary;
    font-weight: 600;
  }
}

.add-button {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  padding: $spacing-xs $spacing-sm;
  background-color: $primary-color;
  color: white;
  border: none;
  border-radius: $border-radius;
  font-size: $font-size-sm;
  cursor: pointer;
  transition: $transition-quick;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  
  &:hover {
    background-color: $primary-dark;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  }
}

.categories-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.category-item {
  background-color: $bg-primary;
  border: 1px solid $chart-grid;
  border-radius: $border-radius;
  overflow: hidden;
  transition: $transition-quick;
  margin-bottom: $spacing-sm;
  
  &:hover {
    box-shadow: $box-shadow;
  }
  
  &__header {
    display: flex;
    align-items: center;
    padding: $spacing-sm $spacing-md;
    cursor: pointer;
  }
  
  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: $spacing-sm;
    
    .icon-container {
      width: 32px;
      height: 32px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      
      i {
        font-size: 1.2rem;
      }
    }
  }
  
  &__color {
    width: 16px;
    height: 16px;
    border-radius: 50%;
  }
  
  &__name {
    flex: 1;
    font-weight: 500;
    color: $text-primary;
    display: flex;
    align-items: center;
    gap: $spacing-sm;
  }
  
  &__collapse {
    margin-right: $spacing-sm;
    color: $text-secondary;
  }
  
  &__actions {
    display: flex;
    gap: $spacing-xs;
  }
}

.subcategories-list {
  margin-left: $spacing-xl;
  margin-bottom: $spacing-sm;
  background-color: $bg-secondary;
  border-radius: 0 0 $border-radius $border-radius;
}

.subcategory-item {
  display: flex;
  align-items: center;
  padding: $spacing-xs $spacing-md;
  border-left: 2px solid $chart-grid;
  border-bottom: 1px solid rgba($chart-grid, 0.5);
  
  &:last-child {
    border-bottom: none;
  }
  
  &__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: $spacing-sm;
    
    .icon-container {
      width: 26px;
      height: 26px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      justify-content: center;
      
      i {
        font-size: 1rem;
      }
    }
  }
  
  &__color {
    width: 12px;
    height: 12px;
    border-radius: 50%;
  }
  
  &__name {
    flex: 1;
    font-size: $font-size-sm;
    color: $text-primary;
  }
  
  &__actions {
    display: flex;
    gap: $spacing-xs;
  }
}

.action-button {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  border: none;
  color: $text-secondary;
  cursor: pointer;
  transition: $transition-quick;
  
  &:hover {
    background-color: rgba($primary-color, 0.1);
    color: $primary-color;
  }
  
  &.delete:hover {
    background-color: rgba($negative, 0.1);
    color: $negative;
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    
    &:hover {
      background-color: transparent;
      color: $text-secondary;
    }
  }
}

.category-badge {
  font-size: 0.7rem;
  padding: 3px 8px;
  border-radius: 12px;
  font-weight: 600;
  
  &.expense {
    background-color: rgba($negative, 0.15);
    color: $negative;
  }
  
  &.income {
    background-color: rgba($positive, 0.15);
    color: $positive;
  }
}

.loading-spinner,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $spacing-lg;
  background-color: $bg-secondary;
  border-radius: $border-radius;
  text-align: center;
  
  .spinner {
    width: 30px;
    height: 30px;
    border: 3px solid rgba($primary-color, 0.2);
    border-radius: 50%;
    border-top-color: $primary-color;
    animation: spin 1s ease-in-out infinite;
    margin-bottom: $spacing-sm;
  }
}

.empty-state {
  p {
    margin-bottom: $spacing-md;
    color: $text-secondary;
  }
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
    font-size: $font-size-sm;
  }
}

.warning-message {
  background-color: rgba($warning, 0.1);
  border-left: 4px solid $warning;
  padding: $spacing-md;
  margin: $spacing-md 0;
  display: flex;
  align-items: center;
  border-radius: $border-radius;
  
  i {
    color: $warning;
    margin-right: $spacing-sm;
    font-size: $font-size-md;
  }
  
  span {
    color: $text-primary;
    font-size: $font-size-sm;
  }
}

.delete-message {
  color: $text-primary;
  font-size: 1rem;
  margin-bottom: $spacing-md;
}

.delete-details {
  display: flex;
  align-items: center;
  padding: $spacing-md;
  background-color: $bg-secondary;
  border-radius: $border-radius;
  margin: $spacing-md 0;
  color: $text-primary;
  
  .icon-container {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: $spacing-md;
    
    i {
      font-size: 1.2rem;
    }
  }
  
  .color-preview {
    width: 20px;
    height: 20px;
    border-radius: 6px;
    margin-right: $spacing-sm;
  }
  
  strong {
    color: $text-primary;
    font-size: 1rem;
  }
}

// Modern modal styling
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

  &.modern {
    .modal-container {
      max-width: 450px;
      border-radius: 16px;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
      overflow: hidden;
    }
    
    .modal-header {
      padding: $spacing-md;
      background-color: $bg-primary;
      border-bottom: 1px solid rgba($chart-grid, 0.5);
      
      h3 {
        font-size: 1.125rem;
        font-weight: 600;
      }
    }
    
    .modal-body {
      padding: $spacing-md;
    }
  }
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
}

.modal-container {
  position: relative;
  width: 100%;
  max-width: 450px;
  max-height: 85vh;
  overflow-y: auto;
  background-color: $bg-primary;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  z-index: 1001;
  
  &.confirm-dialog {
    max-width: 380px;
  }
  
  &::-webkit-scrollbar {
    width: 8px;
  }
  
  &::-webkit-scrollbar-track {
    background: rgba($chart-grid, 0.2);
    border-radius: 10px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: rgba($text-secondary, 0.3);
    border-radius: 10px;
    
    &:hover {
      background: rgba($text-secondary, 0.5);
    }
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $spacing-md;
  border-bottom: 1px solid rgba($chart-grid, 0.5);
  
  h3 {
    margin: 0;
    color: $text-primary;
    font-size: 1.125rem;
    font-weight: 600;
  }
}

.close-button {
  width: 28px;
  height: 28px;
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
    background-color: rgba($text-secondary, 0.1);
    color: $text-primary;
  }
}

.modal-body {
  padding: $spacing-md;
}

// Category preview card
.category-preview-card {
  display: flex;
  align-items: center;
  padding: $spacing-md;
  background-color: $bg-secondary;
  border-radius: 12px;
  margin-bottom: $spacing-xs;
  
  .preview-icon-container {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-right: $spacing-md;
    
    i {
      font-size: 1.4rem;
    }
    
    .preview-fallback {
      width: 24px;
      height: 24px;
      border-radius: 6px;
    }
  }
  
  .preview-name {
    flex: 1;
    font-weight: 600;
    font-size: 1rem;
    color: $text-primary;
    
    .preview-placeholder {
      color: $text-secondary;
      opacity: 0.7;
    }
  }
}

.preview-note {
  font-size: 0.8rem;
  color: $text-secondary;
  text-align: center;
  margin-bottom: $spacing-md;
  font-style: italic;
}

// Form styling
.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: $spacing-md;
  
  label {
    font-size: $font-size-sm;
    margin-bottom: $spacing-xs;
    color: $text-secondary;
    font-weight: 500;
  }
  
  .form-input-with-icon {
    position: relative;
    
    i {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      color: $text-secondary;
    }
    
    input, select {
      padding-left: 35px;
      width: 100%;
    }
  }
  
  input, select {
    padding: 10px 12px;
    border: 1px solid rgba($chart-grid, 0.8);
    border-radius: 8px;
    font-size: $font-size-md;
    transition: $transition-quick;
    background-color: $bg-primary;
    color: $text-primary;
    
    &:focus {
      border-color: $primary-color;
      outline: none;
      box-shadow: 0 0 0 2px rgba($primary-color, 0.15);
    }
    
    &::placeholder {
      color: rgba($text-secondary, 0.5);
    }
  }
  
  input[type="color"] {
    height: 36px;
    cursor: pointer;
    appearance: none;
    -webkit-appearance: none;
    padding: 0;
    border: none;
    border-radius: 4px;
    overflow: hidden;
    
    &::-webkit-color-swatch-wrapper {
      padding: 0;
    }
    
    &::-webkit-color-swatch {
      border: none;
      border-radius: 4px;
    }
  }
}

// Color presets
.color-picker-container {
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
  
  .color-presets {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 6px;
    
    .color-preset {
      width: 100%;
      aspect-ratio: 1;
      border-radius: 4px;
      cursor: pointer;
      transition: $transition-quick;
      
      &:hover {
        transform: scale(1.15);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      }
    }
  }
}

// Form layout
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-md;
  
  .color-group {
    grid-column: 1;
  }
  
  .icon-group {
    grid-column: 2;
  }
}

// Type selector
.type-selector {
  display: flex;
  gap: 10px;
  
  .type-button {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px;
    border-radius: 8px;
    background-color: $bg-secondary;
    border: 1px solid transparent;
    color: $text-secondary;
    font-weight: 500;
    transition: all 0.2s ease;
    cursor: pointer;
    
    i {
      font-size: 0.875rem;
    }
    
    &:hover {
      background-color: darken($bg-secondary, 3%);
    }
    
    &.active {
      &:first-child {
        background-color: rgba($negative, 0.1);
        color: $negative;
        border-color: rgba($negative, 0.3);
        
        i {
          color: $negative;
        }
      }
      
      &:last-child {
        background-color: rgba($positive, 0.1);
        color: $positive;
        border-color: rgba($positive, 0.3);
        
        i {
          color: $positive;
        }
      }
    }
  }
}

// Icon selector
.icon-selector {
  position: relative;
  width: 100%;
  
  .icon-dropdown-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.3);
    z-index: 1001;
  }
  
  .selected-icon {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 12px;
    border: 1px solid rgba($chart-grid, 0.8);
    border-radius: 8px;
    cursor: pointer;
    background-color: $bg-primary;
    
    i {
      font-size: 1.1rem;
      margin-right: $spacing-sm;
      color: $text-primary;
    }
    
    .no-icon {
      color: rgba($text-secondary, 0.7);
    }
  }
  
  .icon-dropdown {
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 80%;
    max-width: 400px;
    height: auto;
    max-height: 80vh;
    background-color: $bg-primary;
    border: 1px solid rgba($chart-grid, 0.5);
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    z-index: 1002;
    overflow: hidden;
    
    .icon-search {
      padding: $spacing-sm;
      border-bottom: 1px solid rgba($chart-grid, 0.5);
      
      input {
        width: 100%;
        padding: 8px 12px 8px 36px;
        border: 1px solid rgba($chart-grid, 0.8);
        border-radius: 6px;
        font-size: $font-size-sm;
      }
      
      i {
        position: absolute;
        left: 18px;
        top: 19px;
        color: $text-secondary;
      }
    }
    
    .icons-grid {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 8px;
      padding: $spacing-sm;
      max-height: 60vh;
      overflow-y: auto;
      
      &::-webkit-scrollbar {
        width: 6px;
      }
      
      &::-webkit-scrollbar-track {
        background: rgba($chart-grid, 0.1);
        border-radius: 10px;
      }
      
      &::-webkit-scrollbar-thumb {
        background: rgba($text-secondary, 0.2);
        border-radius: 10px;
        
        &:hover {
          background: rgba($text-secondary, 0.4);
        }
      }
      
      .icon-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 8px 6px;
        border-radius: 6px;
        cursor: pointer;
        
        &:hover {
          background-color: rgba($primary-color, 0.08);
        }
        
        i {
          font-size: 1.2rem;
          margin-bottom: 4px;
          color: $text-primary;
        }
        
        .icon-name {
          font-size: 0.65rem;
          text-align: center;
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
          width: 100%;
          color: $text-secondary;
        }
      }
    }
  }
}

// Form actions
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: $spacing-md;
  margin-top: $spacing-lg;
}

// Buttons
.button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  
  i {
    font-size: 0.85rem;
  }
  
  &--primary {
    background-color: $primary-color;
    color: white;
    box-shadow: 0 2px 5px rgba($primary-color, 0.3);
    
    &:hover {
      background-color: $primary-dark;
      box-shadow: 0 4px 8px rgba($primary-color, 0.4);
      transform: translateY(-1px);
    }
    
    &:active {
      transform: translateY(0);
      box-shadow: 0 2px 3px rgba($primary-color, 0.3);
    }
  }
  
  &--secondary {
    background-color: $bg-secondary;
    color: $text-primary;
    border: 1px solid rgba($chart-grid, 0.5);
    
    &:hover {
      background-color: darken($bg-secondary, 3%);
      border-color: rgba($chart-grid, 0.8);
    }
  }
  
  &--delete {
    background-color: $negative;
    color: white;
    box-shadow: 0 2px 5px rgba($negative, 0.3);
    
    &:hover {
      background-color: darken($negative, 8%);
      box-shadow: 0 4px 8px rgba($negative, 0.4);
      transform: translateY(-1px);
    }
    
    &:active {
      transform: translateY(0);
      box-shadow: 0 2px 3px rgba($negative, 0.3);
    }
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>