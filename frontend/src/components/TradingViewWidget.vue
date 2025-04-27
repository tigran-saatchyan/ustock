<template>
  <div class="tradingview-widget-container" ref="chartContainerRef" :style="{ height: widgetHeight }">
    <!-- This div will be the target for the widget -->
    <div :id="widgetId" class="tradingview-widget-container__widget"></div>
    <div class="tradingview-widget-copyright">
      <!-- Copyright is hidden by default with CSS -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue';
import { useStore } from 'vuex';
import { useI18n } from 'vue-i18n';

const props = defineProps({
  symbol: {
    type: String,
    required: true,
  },
  widgetHeight: {
    type: String,
    default: '550px'
  }
});

const store = useStore();
const { locale } = useI18n();

const chartContainerRef = ref(null); // Используем ref для доступа к контейнеру
// Create a valid ID by removing invalid characters and ensuring it's consistent
const widgetId = computed(() => {
  // Replace any invalid characters (like colons) with underscores and ensure it's a valid ID
  const safeSymbol = props.symbol.replace(/[^a-zA-Z0-9]/g, '_');
  return `tradingview_${safeSymbol}`;
});

let widgetInstance = null; // Сохраняем инстанс для возможного удаления/взаимодействия
let scriptLoadPromise = null; // Promise для отслеживания загрузки скрипта

// --- Функция загрузки скрипта TradingView ---
const loadTradingViewScript = () => {
  // Загружаем скрипт только один раз
  if (!scriptLoadPromise) {
    scriptLoadPromise = new Promise((resolve, reject) => {
      const existingScript = document.getElementById('tradingview-widget-script');
      if (existingScript) {
        // Если скрипт уже есть (возможно, добавлен другим инстансом виджета)
        // Проверяем, загрузился ли он уже (наличие window.TradingView)
        if (typeof window.TradingView !== 'undefined') {
          console.log('TradingView script already loaded (found existing script).');
          resolve();
        } else {
          // Если скрипт есть, но библиотека не готова, ждем onload
          existingScript.addEventListener('load', () => {
             console.log('TradingView script already loaded (onload triggered).');
             resolve();
          });
           existingScript.addEventListener('error', (e) => {
              console.error('Error loading existing TradingView script:', e);
              reject(e);
           });
        }
      } else {
        // Создаем новый скрипт
        const script = document.createElement('script');
        script.id = 'tradingview-widget-script';
        script.src = 'https://s3.tradingview.com/tv.js';
        script.async = true;
        script.onload = () => {
          console.log('TradingView script loaded successfully.');
          resolve();
        };
        script.onerror = (e) => {
          console.error('Failed to load TradingView script:', e);
          scriptLoadPromise = null; // Позволить повторную попытку загрузки
          reject(e);
        };
        document.body.appendChild(script);
      }
    });
  }
  return scriptLoadPromise;
};

// --- Функция создания виджета ---
const createWidget = async () => {
  // Убедимся, что символ есть
  if (!props.symbol) {
    console.warn('TradingView: Symbol is missing, cannot create widget.');
    return;
  }

  // 1. Дожидаемся загрузки скрипта
  try {
    await loadTradingViewScript();
  } catch (error) {
    console.error("TradingView: Script loading failed, cannot create widget.", error);
    return;
  }

  // 2. Дожидаемся готовности DOM контейнера
  await nextTick(); // Ждем следующего тика рендеринга Vue

  const containerElement = document.getElementById(widgetId.value);
  if (!containerElement) {
      console.error(`TradingView: Container element #${widgetId.value} not found in DOM after nextTick. Widget creation aborted.`);
      // Можно добавить дополнительную задержку и проверку, если nextTick недостаточно
      // setTimeout(createWidget, 50); // Попробовать еще раз через 50мс
      return;
  }

  // 3. Проверяем наличие библиотеки TradingView
  if (typeof window.TradingView === 'undefined' || typeof window.TradingView.widget !== 'function') {
    console.error('TradingView: window.TradingView.widget is not available after script load. Aborting widget creation.');
    // Возможно, скрипт загрузился, но произошла ошибка инициализации внутри него
    return;
  }

  // 4. Очищаем предыдущий виджет (если он был)
  destroyWidget(); // Вызываем функцию очистки

  // 5. Собираем опции
  const appTheme = store.getters.isDarkTheme ? 'dark' : 'light';
  const widgetLocale = locale.value === 'ru' ? 'ru' : 'en';

  const widgetOptions = {
    width: "100%",
    height: "100%", // Заполнение контейнера
    symbol: props.symbol, // Важно: Убедитесь, что этот символ правильный (с биржей?)
    interval: "D",
    timezone: "Etc/UTC",
    theme: appTheme,
    style: "1",
    locale: widgetLocale,
    enable_publishing: false,
    allow_symbol_change: true,
    container_id: widgetId.value
  };

  // 6. Создаем новый виджет
  try {
    console.log(`TradingView: Creating widget with options:`, widgetOptions);
    // Присваиваем инстанс переменной, чтобы можно было его потом удалить
    widgetInstance = new window.TradingView.widget(widgetOptions);
     console.log('TradingView: Widget instance created.');
  } catch (error) {
    console.error('TradingView: Error creating widget instance:', error);
  }
};

// --- Функция удаления виджета ---
const destroyWidget = () => {
  if (widgetInstance) {
     console.log(`TradingView: Attempting to remove widget instance for container ${widgetId.value}`);
     // У TradingView нет официального метода destroy, но можно попробовать вызвать remove()
     // if (typeof widgetInstance.remove === 'function') {
     //    widgetInstance.remove();
     // }
     widgetInstance = null;
  }
  // Очищаем содержимое контейнера вручную
  const container = document.getElementById(widgetId.value);
  if (container) {
    container.innerHTML = '';
     console.log(`TradingView: Container ${widgetId.value} cleared.`);
  } else {
     console.log(`TradingView: Container ${widgetId.value} not found during destroy.`);
  }
};

// --- Хуки жизненного цикла ---
onMounted(() => {
  console.log(`TradingViewWidget: Mounted for symbol ${props.symbol}, container ID ${widgetId.value}.`);
  createWidget();
});

onUnmounted(() => {
  console.log(`TradingViewWidget: Unmounted for symbol ${props.symbol}, container ID ${widgetId.value}.`);
  destroyWidget();
  // Сам скрипт tv.js не удаляем, он может быть нужен другим компонентам
});

// --- Наблюдатели ---
watch(() => props.symbol, (newSymbol, oldSymbol) => {
  if (newSymbol && newSymbol !== oldSymbol && chartContainerRef.value) { // Проверяем, что компонент еще смонтирован
    console.log(`TradingView: Symbol changed to ${newSymbol}. Recreating widget.`);
    createWidget(); // Пересоздаем виджет
  }
});

watch(() => store.getters.isDarkTheme, (newValue, oldValue) => {
  if (newValue !== oldValue && chartContainerRef.value) {
    console.log('TradingView: Theme changed. Recreating widget.');
    createWidget();
  }
});

watch(locale, (newValue, oldValue) => {
  if (newValue !== oldValue && chartContainerRef.value) {
    console.log('TradingView: Locale changed. Recreating widget.');
    createWidget();
  }
});

</script>

<style scoped>
.tradingview-widget-container {
  width: 100%;
  height: 100%; /* Заставляем контейнер занимать высоту родителя */
  min-height: 300px; /* Минимальная высота */
  position: relative;
}
.tradingview-widget-container__widget {
  width: 100%;
  height: 100%;
  display: block; /* Убедимся, что div занимает место */
}
.tradingview-widget-copyright {
  display: none; /* Скрываем копирайт */
}
</style>
