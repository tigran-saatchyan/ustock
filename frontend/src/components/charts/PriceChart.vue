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
              @click.prevent="setPeriod(period.value)"
              type="button"
          >
            {{ period.label }}
          </button>
        </div>
        <div class="price-chart__type-selector">
          <button
              v-for="type in chartTypes"
              :key="type.value"
              :class="['chart-type-button', { active: chartType === type.value }]"
              @click.prevent="setChartType(type.value)"
              type="button"
          >
            <i :class="type.icon"></i>
          </button>
        </div>
      </div>
    </div>

    <div class="price-chart__container" ref="chartContainer"></div>

    <div v-if="loading" class="price-chart__loading">
      <i class="pi pi-spin pi-spinner"></i>
    </div>
    <div v-if="!hasData && !loading" class="price-chart__no-data">
      No price data available
    </div>
  </div>
</template>

<script>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue';
import dayjs from 'dayjs';
import { createChart } from 'lightweight-charts';

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
    const chartContainer = ref(null);
    const chart = ref(null);
    let candleSeries = null;
    let lineSeries = null;
    let volumeSeries = null;
    let resizeObserver = null;

    const selectedPeriod = ref('1m');
    const chartType = ref('line');

    const hasData = computed(() => props.data && props.data.length > 0);

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

    const title = computed(() => props.ticker ? `${props.ticker} Price Chart` : 'Price Chart');

    const setPeriod = (period) => {
      if (selectedPeriod.value !== period) {
        selectedPeriod.value = period;
        emit('period-change', getPeriodDates(period));
      }
    };

    const setChartType = (type) => {
      if (chartType.value !== type) {
        chartType.value = type;
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
          start = dayjs().startOf('year');
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '1d' };
        case '1y':
          start = end.subtract(1, 'year');
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '1d' };
        case '5y':
          start = end.subtract(5, 'year');
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '1w' };
        default:
          start = end.subtract(1, 'month');
          return { start: start.format('YYYY-MM-DD'), end: end.format('YYYY-MM-DD'), interval: '1d' };
      }
    };

    // Обработка изменения размера окна
    const handleResize = () => {
      if (chart.value && chartContainer.value) {
        chart.value.applyOptions({
          width: chartContainer.value.clientWidth
        });
      }
    };

    // Форматирование данных для графика
    const formatChartData = (data) => {
      if (!data || data.length === 0) return [];

      return data.map(item => ({
        time: typeof item.date === 'string' ? item.date : new Date(item.date).toISOString().split('T')[0],
        open: Number(item.open),
        high: Number(item.high),
        low: Number(item.low),
        close: Number(item.close),
        volume: item.volume ? Number(item.volume) : undefined
      }));
    };

    // Инициализация графика
    const initChart = () => {
      if (!chartContainer.value) return;

      // Очищаем предыдущий график, если он существует
      if (chart.value) {
        chart.value.remove();
        chart.value = null;
      }

      const container = chartContainer.value;

      chart.value = createChart(container, {
        width: container.clientWidth,
        height: container.clientHeight || 400,
        layout: {
          backgroundColor: '#ffffff',
          textColor: '#333333',
        },
        grid: {
          vertLines: {
            color: 'rgba(197, 203, 206, 0.5)',
          },
          horzLines: {
            color: 'rgba(197, 203, 206, 0.5)',
          },
        },
        timeScale: {
          timeVisible: true,
          secondsVisible: false,
        },
        crosshair: {
          mode: 1,
          vertLine: {
            width: 1,
            color: 'rgba(224, 227, 235, 0.8)',
            style: 0,
          },
          horzLine: {
            width: 1,
            color: 'rgba(224, 227, 235, 0.8)',
            style: 0,
          },
        },
      });

      // Настраиваем ResizeObserver для автоматического изменения размера
      if (resizeObserver) {
        resizeObserver.disconnect();
      }

      resizeObserver = new ResizeObserver(entries => {
        if (entries.length === 0 || !entries[0].contentRect) return;
        const newWidth = entries[0].contentRect.width;

        if (chart.value) {
          chart.value.applyOptions({ width: newWidth });
        }
      });

      resizeObserver.observe(container);

      renderChart();
    };

    // Отрисовка графика согласно выбранному типу
    const renderChart = () => {
      if (!chart.value || !hasData.value) return;

      // Удаляем предыдущие серии (если они есть)
      if (candleSeries && chart.value) {
        try {
          chart.value.removeSeries(candleSeries);
        } catch(e) {
          console.error("Failed to remove candleSeries:", e);
        }
        candleSeries = null;
      }

      if (lineSeries && chart.value) {
        try {
          chart.value.removeSeries(lineSeries);
        } catch(e) {
          console.error("Failed to remove lineSeries:", e);
        }
        lineSeries = null;
      }

      if (volumeSeries && chart.value) {
        try {
          chart.value.removeSeries(volumeSeries);
        } catch(e) {
          console.error("Failed to remove volumeSeries:", e);
        }
        volumeSeries = null;
      }

      // Форматирование данных для графика
      const formattedData = formatChartData(props.data);

      if (chartType.value === 'candlestick') {
        // Создаем свечной график
        try {
          candleSeries = chart.value.addCandlestickSeries({
            upColor: '#26a69a',
            downColor: '#ef5350',
            borderVisible: false,
            wickUpColor: '#26a69a',
            wickDownColor: '#ef5350',
          });

          candleSeries.setData(formattedData);

          // Добавляем серию объема под свечами, если данные содержат объем
          if (formattedData.length > 0 && 'volume' in formattedData[0]) {
            volumeSeries = chart.value.addHistogramSeries({
              color: '#26a69a',
              priceFormat: {
                type: 'volume',
              },
              priceScaleId: '', // Отдельная шкала для объема
              scaleMargins: {
                top: 0.8, // Отступ сверху
                bottom: 0,
              },
            });

            const volumeData = formattedData.map(item => ({
              time: item.time,
              value: item.volume || 0,
              color: item.close >= item.open ? '#26a69a' : '#ef5350'
            }));

            volumeSeries.setData(volumeData);
          }
        } catch(e) {
          console.error("Failed to create candlestick series:", e);
        }
      } else {
        // Создаем линейный график
        try {
          // Используем addAreaSeries вместо addLineSeries, если это нужно
          // или проверьте документацию для правильного метода
          lineSeries = chart.value.addLineSeries({
            lineColor: '#2196F3',
            topColor: 'rgba(33, 150, 243, 0.4)',
            bottomColor: 'rgba(33, 150, 243, 0.1)',
            lineWidth: 2,
          });

          // Для линейного графика нужны только время и цена закрытия
          const lineData = formattedData.map(item => ({
            time: item.time,
            value: item.close
          }));

          lineSeries.setData(lineData);
        } catch(e) {
          console.error("Failed to create line series:", e);
          // Если не сработал addAreaSeries, попробуем addBaselineSeries
          try {
            lineSeries = chart.value.addBaselineSeries({
              baseValue: { type: 'price', price: Math.min(...formattedData.map(item => item.close)) },
              topLineColor: '#2196F3',
              topFillColor1: 'rgba(33, 150, 243, 0.4)',
              topFillColor2: 'rgba(33, 150, 243, 0.1)',
              lineWidth: 2,
            });

            const lineData = formattedData.map(item => ({
              time: item.time,
              value: item.close
            }));

            lineSeries.setData(lineData);
          } catch(e2) {
            console.error("Failed to create baseline series as fallback:", e2);
          }
        }
      }

      try {
        // Автоматически подгоняем масштаб для отображения всех данных
        if (chart.value) {
          chart.value.timeScale().fitContent();
        }
      } catch(e) {
        console.error("Failed to fit content:", e);
      }
    };

    // Жизненный цикл компонента
    onMounted(() => {
      nextTick(() => {
        initChart();
      });

      // Добавляем обработчик события resize
      window.addEventListener('resize', handleResize);

      // Инициируем загрузку данных, если selectedPeriod не соответствует значению по умолчанию
      if (selectedPeriod.value !== '1m') {
        emit('period-change', getPeriodDates(selectedPeriod.value));
      } else {
        // Иначе просим загрузить данные по умолчанию
        emit('period-change', getPeriodDates('1m'));
      }
    });

    onBeforeUnmount(() => {
      // Удаляем обработчик события resize
      window.removeEventListener('resize', handleResize);

      // Отключаем ResizeObserver
      if (resizeObserver) {
        resizeObserver.disconnect();
        resizeObserver = null;
      }

      // Удаляем график
      if (chart.value) {
        chart.value.remove();
        chart.value = null;
      }
    });

    // Следим за изменениями данных
    watch(() => props.data, () => {
      nextTick(() => {
        if (hasData.value) {
          renderChart();
        }
      });
    }, { deep: true });

    // Следим за изменением контейнера
    watch(() => chartContainer.value, () => {
      nextTick(() => {
        initChart();
      });
    });

    return {
      chartContainer,
      chartType,
      selectedPeriod,
      periodOptions,
      chartTypes,
      hasData,
      title,
      setPeriod,
      setChartType,
      handleResize  // Обязательно возвращаем handleResize в return объекте
    };
  }
};
</script>

<style scoped>
.price-chart {
  display: flex;
  flex-direction: column;
  width: 100%;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.price-chart__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.price-chart__title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.price-chart__controls {
  display: flex;
  gap: 15px;
}

.price-chart__period-selector {
  display: flex;
  gap: 5px;
}

.price-chart__type-selector {
  display: flex;
  gap: 5px;
}

.period-button,
.chart-type-button {
  padding: 6px 10px;
  background-color: #f5f5f5;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.period-button:hover,
.chart-type-button:hover {
  background-color: #e0e0e0;
}

.period-button.active,
.chart-type-button.active {
  background-color: #2196F3;
  color: white;
}

.price-chart__container {
  width: 100%;
  height: 400px; /* Важно: фиксированная высота для графика */
  position: relative;
}

.price-chart__loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #2196F3;
}

.price-chart__no-data {
  width: 100%;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-style: italic;
}
</style>
