<template>
  <div class="price-chart">
    <div class="price-chart__header">
      <h3 class="price-chart__title">{{ title }}</h3>
      <div class="price-chart__controls">
        <div class="price-chart__period-selector">
          <button 
            v-for="period in periodOptions" 
            :key="period.value"
            :class="['period-button', { active: selectedPeriod === period.value }]"
            @click="setPeriod(period.value)"
          >
            {{ period.label }}
          </button>
        </div>
        <div class="price-chart__type-selector">
          <button 
            v-for="type in chartTypes" 
            :key="type.value"
            :class="['chart-type-button', { active: chartType === type.value }]"
            @click="setChartType(type.value)"
          >
            <i :class="type.icon"></i>
          </button>
        </div>
      </div>
    </div>
    
    <div class="price-chart__container" ref="chartContainer">
      <canvas ref="chartCanvas"></canvas>
      <div v-if="!hasData" class="price-chart__no-data">
        No price data available
      </div>
      <div v-if="loading" class="price-chart__loading">
        <i class="pi pi-spin pi-spinner"></i>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';
import Chart from 'chart.js/auto';
import dayjs from 'dayjs';

export default {
  name: 'PriceChart',
  
  props: {
    data: {
      type: Array,
      default: () => []
    },
    ticker: {
      type: String,
      default: ''
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['period-change'],
  
  setup(props, { emit }) {
    const chartCanvas = ref(null);
    const chartContainer = ref(null);
    const chart = ref(null);
    const selectedPeriod = ref('1m');
    const chartType = ref('line');
    
    // Chart options and settings
    const periodOptions = [
      { label: '1D', value: '1d' },
      { label: '1W', value: '1w' },
      { label: '1M', value: '1m' },
      { label: '3M', value: '3m' },
      { label: '6M', value: '6m' },
      { label: 'YTD', value: 'ytd' },
      { label: '1Y', value: '1y' },
      { label: '5Y', value: '5y' }
    ];
    
    const chartTypes = [
      { label: 'Line', value: 'line', icon: 'pi pi-chart-line' },
      { label: 'Candlestick', value: 'candlestick', icon: 'pi pi-chart-bar' }
    ];
    
    // Computed properties
    const title = computed(() => {
      return props.ticker 
        ? `${props.ticker} Price Chart` 
        : 'Price Chart';
    });
    
    const hasData = computed(() => {
      return props.data && props.data.length > 0 && props.data.some(item => 
        item.close !== undefined && item.close !== null
      );
    });
    
    // Methods
    const setPeriod = (period) => {
      // Only update if period actually changed to prevent multiple requests
      if (selectedPeriod.value !== period) {
        selectedPeriod.value = period;
        emit('period-change', getPeriodDates(period));
      }
    };
    
    const setChartType = (type) => {
      chartType.value = type;
      if (chart.value) {
        destroyChart();
        renderChart();
      }
    };
    
    const getPeriodDates = (period) => {
      const end = dayjs();
      let start;
      
      switch (period) {
        case '1d':
          start = end.subtract(1, 'day');
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '5m' };
        
        case '1w':
          start = end.subtract(1, 'week');
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '1h' };
          
        case '1m':
          start = end.subtract(1, 'month');
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '1d' };
          
        case '3m':
          start = end.subtract(3, 'month');
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '1d' };
          
        case '6m':
          start = end.subtract(6, 'month');
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '1d' };
          
        case 'ytd':
          start = dayjs(`${end.year()}-01-01`);
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '1d' };
          
        case '1y':
          start = end.subtract(1, 'year');
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '1d' };
          
        case '5y':
          start = end.subtract(5, 'year');
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '1wk' };
          
        default:
          start = end.subtract(1, 'month');
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '1d' };
      }
    };
    
    const renderChart = () => {
      // Don't attempt to render if we don't have a canvas or no data
      if (!chartCanvas.value) {
        console.warn('Chart canvas not available');
        return;
      }
      
      if (!hasData.value) {
        console.warn('No chart data available to render');
        return;
      }
      
      try {
        const ctx = chartCanvas.value.getContext('2d');
        
        if (chartType.value === 'line') {
          renderLineChart(ctx);
        } else if (chartType.value === 'candlestick') {
          renderCandlestickChart(ctx);
        }
      } catch (error) {
        console.error('Error rendering chart:', error);
      }
    };
    
    const renderLineChart = (ctx) => {
      try {
        // Filter out invalid data points to prevent chart errors
        const validData = props.data.filter(item => 
          item && item.close !== undefined && item.close !== null && item.date
        );
        
        const priceData = validData.map(item => item.close);
        const labels = validData.map(item => dayjs(item.date).format('MMM D'));
        
        // Make sure we have valid data before creating the chart
        if (!labels.length || !priceData.length) {
          console.warn('No valid data points for line chart');
          return;
        }
        
        chart.value = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: `${props.ticker} Price`,
              data: priceData,
              borderColor: '#e08200',  // Updated to match our theme
              backgroundColor: 'rgba(224, 130, 0, 0.1)',
              fill: {
                target: 'origin',
                above: 'rgba(224, 130, 0, 0.1)'
              },
              tension: 0.1,
              pointRadius: 0,
              pointHoverRadius: 5,
              pointHoverBackgroundColor: '#e08200',
              borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                  label: function(context) {
                    return `Price: $${context.raw.toFixed(2)}`;
                  }
                }
              }
            },
            scales: {
              x: {
                grid: {
                  display: false
                }
              },
              y: {
                grid: {
                  color: 'rgba(0, 0, 0, 0.05)'
                },
                ticks: {
                  callback: function(value) {
                    return '$' + value.toFixed(2);
                  }
                }
              }
            },
            interaction: {
              mode: 'index',
              intersect: false
            }
          }
        });
      } catch (error) {
        console.error('Error rendering line chart:', error);
      }
    };
    
    const renderCandlestickChart = (ctx) => {
      try {
        // Filter out invalid data points to prevent chart errors
        const validData = props.data.filter(item => 
          item && 
          item.date && 
          item.open !== undefined && item.open !== null &&
          item.high !== undefined && item.high !== null &&
          item.low !== undefined && item.low !== null &&
          item.close !== undefined && item.close !== null
        );
        
        // Make sure we have valid data before creating the chart
        if (!validData.length) {
          console.warn('No valid data points for candlestick chart');
          return;
        }
        
        const data = validData.map(item => ({
          x: dayjs(item.date).format('MMM D'),
          o: item.open,
          h: item.high,
          l: item.low,
          c: item.close
        }));
        
        const colors = data.map(item => item.o > item.c ? '#ff5252' : '#00c853');
        
        chart.value = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.map(item => item.x),
            datasets: [{
              label: 'Price',
              data: data.map((item, index) => {
                return {
                  x: index,
                  y: [item.l, item.o, item.c, item.h]
                };
              }),
              backgroundColor: colors
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                callbacks: {
                  label: function(context) {
                    const dataIndex = context.dataIndex;
                    const item = data[dataIndex];
                    return [
                      `Open: $${item.o.toFixed(2)}`,
                      `High: $${item.h.toFixed(2)}`,
                      `Low: $${item.l.toFixed(2)}`,
                      `Close: $${item.c.toFixed(2)}`
                    ];
                  }
                }
              }
            },
            scales: {
              x: {
                grid: {
                  display: false
                }
              },
              y: {
                grid: {
                  color: 'rgba(0, 0, 0, 0.05)'
                },
                ticks: {
                  callback: function(value) {
                    return '$' + value.toFixed(2);
                  }
                }
              }
            },
            interaction: {
              mode: 'index',
              intersect: false
            }
          }
        });
      } catch (error) {
        console.error('Error rendering candlestick chart:', error);
      }
    };
    
    const destroyChart = () => {
      if (chart.value) {
        chart.value.destroy();
        chart.value = null;
      }
    };
    
    // Keep track of if this is the initial load
    const initialLoad = ref(true);
    
    // Lifecycle hooks
    onMounted(() => {
      console.log('PriceChart mounted, hasData:', hasData.value);
      
      // Trigger period change on initial mount only
      if (initialLoad.value) {
        console.log('Initial load, requesting data for period:', selectedPeriod.value);
        // Use a small timeout to ensure the parent is ready to receive events
        setTimeout(() => {
          emit('period-change', getPeriodDates(selectedPeriod.value));
          initialLoad.value = false;
        }, 100);
      }
      
      // If we already have data, attempt to render the chart
      if (hasData.value && !chart.value) {
        console.log('Data already available on mount, rendering chart');
        // Small delay to ensure DOM is ready
        setTimeout(() => {
          renderChart();
        }, 150);
      }
    });
    
    onUnmounted(() => {
      destroyChart();
    });
    
    // Watch for data changes to update the chart
    watch(() => props.data, (newData) => {
      console.log('Chart data updated:', newData?.length || 0, 'data points');
      
      // Always destroy existing chart to prevent duplicates
      if (chart.value) {
        destroyChart();
      }
      
      // Make sure the component is still mounted before trying to render
      // and also ensure there's actually data to display
      if (chartCanvas.value && hasData.value) {
        console.log('Rendering chart with', newData?.length || 0, 'data points');
        // Delay the rendering slightly to ensure the DOM is ready
        setTimeout(() => {
          renderChart();
        }, 50);
      } else {
        console.log('Not rendering chart: Canvas exists:', !!chartCanvas.value, 'Has data:', hasData.value);
      }
    }, { deep: true });
    
    // Watch for loading state changes
    watch(() => props.loading, (isLoading) => {
      console.log('Chart loading state changed:', isLoading);
      // When loading finishes, check if we need to render the chart
      if (!isLoading && hasData.value && !chart.value) {
        setTimeout(() => {
          renderChart();
        }, 50);
      }
    });
    
    return {
      chartCanvas,
      chartContainer,
      selectedPeriod,
      chartType,
      periodOptions,
      chartTypes,
      title,
      hasData,
      setPeriod,
      setChartType
    };
  }
};
</script>

<style lang="scss" scoped>
.price-chart {
  width: 100%;
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: $box-shadow;
  padding: $spacing-md;
  margin-bottom: $spacing-lg;
  
  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $spacing-md;
    flex-wrap: wrap;
    
    @media (max-width: $breakpoint-sm) {
      flex-direction: column;
      align-items: flex-start;
    }
  }
  
  &__title {
    font-size: $font-size-lg;
    font-weight: 600;
    margin: 0;
    color: $secondary-color;
  }
  
  &__controls {
    display: flex;
    align-items: center;
    
    @media (max-width: $breakpoint-sm) {
      margin-top: $spacing-md;
      width: 100%;
      justify-content: space-between;
    }
  }
  
  &__period-selector,
  &__type-selector {
    display: flex;
    
    .period-button,
    .chart-type-button {
      background: transparent;
      border: 1px solid $text-disabled;
      color: $text-secondary;
      font-size: $font-size-sm;
      padding: $spacing-xs $spacing-sm;
      cursor: pointer;
      transition: $transition-quick;
      
      &:hover {
        background-color: rgba($primary-color, 0.05);
      }
      
      &.active {
        background-color: $primary-color;
        color: white;
        border-color: $primary-color;
      }
      
      &:first-child {
        border-top-left-radius: $spacing-xs;
        border-bottom-left-radius: $spacing-xs;
      }
      
      &:last-child {
        border-top-right-radius: $spacing-xs;
        border-bottom-right-radius: $spacing-xs;
      }
    }
  }
  
  &__type-selector {
    margin-left: $spacing-md;
  }
  
  &__container {
    position: relative;
    height: 400px;
    width: 100%;
  }
  
  &__no-data,
  &__loading {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    color: $text-secondary;
    font-size: $font-size-lg;
    background-color: rgba($bg-primary, 0.8);
  }
  
  &__loading {
    font-size: 2rem;
    color: $primary-color;
  }
}
</style>