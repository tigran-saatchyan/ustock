<template>
  <div class="budget-allocation-chart" ref="chartContainer">
    <div v-if="loading" class="chart-loading">
      <i class="pi pi-spin pi-spinner"></i>
    </div>
    <div v-if="!hasData && !loading" class="chart-no-data">
      {{ noDataMessage }}
    </div>
    <div class="chart-container" ref="chart"></div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue';
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js';
import { formatCurrency } from '@/utils/formatters';

// Register the required Chart.js components
Chart.register(ArcElement, Tooltip, Legend);

export default {
  name: 'BudgetAllocationChart',
  
  props: {
    budget: {
      type: Object,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: 'doughnut', // 'doughnut' or 'pie'
      validator: (value) => ['doughnut', 'pie'].includes(value)
    },
    height: {
      type: Number,
      default: 240
    },
    noDataMessage: {
      type: String,
      default: 'No allocation data available'
    }
  },
  
  setup(props) {
    const chartContainer = ref(null);
    const chart = ref(null);
    const chartInstance = ref(null);
    
    // Check if we have data to display
    const hasData = computed(() => {
      return props.budget?.subcategory_budgets && 
             props.budget.subcategory_budgets.length > 0;
    });
    
    // Prepare the chart data
    const chartData = computed(() => {
      if (!hasData.value) return null;
      
      const subcategories = props.budget.subcategory_budgets;
      
      return {
        labels: subcategories.map(sub => sub.category_name),
        datasets: [{
          data: subcategories.map(sub => sub.amount),
          backgroundColor: subcategories.map(sub => sub.category_color),
          borderColor: subcategories.map(sub => sub.category_color),
          borderWidth: 1,
          hoverOffset: 5
        }]
      };
    });
    
    // Function to render the chart
    const renderChart = () => {
      if (!hasData.value || !chart.value) return;
      
      // Destroy previous chart if it exists
      if (chartInstance.value) {
        chartInstance.value.destroy();
      }
      
      // Create new chart
      chartInstance.value = new Chart(chart.value, {
        type: props.type,
        data: chartData.value,
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                boxWidth: 12,
                padding: 15,
                font: {
                  size: 11
                }
              }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  const label = context.label || '';
                  const value = context.raw;
                  const percentage = ((value / props.budget.amount) * 100).toFixed(1);
                  return `${label}: ${formatCurrency(value, props.budget.currency)} (${percentage}%)`;
                }
              }
            }
          },
          cutout: props.type === 'doughnut' ? '70%' : 0
        }
      });
    };
    
    // Initialize chart on mount
    onMounted(() => {
      nextTick(() => {
        if (hasData.value) {
          renderChart();
        }
      });
    });
    
    // Clean up on unmount
    onBeforeUnmount(() => {
      if (chartInstance.value) {
        chartInstance.value.destroy();
      }
    });
    
    // Watch for changes in data and re-render chart
    watch(() => props.budget, () => {
      nextTick(() => {
        renderChart();
      });
    }, { deep: true });
    
    // Watch for changes in chart type
    watch(() => props.type, () => {
      nextTick(() => {
        renderChart();
      });
    });
    
    return {
      chartContainer,
      chart,
      hasData
    };
  }
};
</script>

<style lang="scss" scoped>
.budget-allocation-chart {
  position: relative;
  width: 100%;
  height: v-bind('props.height + "px"');
  
  .chart-container {
    width: 100%;
    height: 100%;
  }
  
  .chart-loading {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 1.5rem;
    color: $primary-color;
  }
  
  .chart-no-data {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 0.9rem;
    color: $text-secondary;
    text-align: center;
    width: 100%;
  }
}
</style>