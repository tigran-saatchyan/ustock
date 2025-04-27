/**
 * Format a number as currency with the specified currency
 * @param {number} value - The numeric value to format
 * @param {string} currency - The currency code to use for formatting (default 'USD')
 * @param {number} decimals - The number of decimal places (default 2)
 * @returns {string} Formatted currency string
 */
export function formatCurrency(value, currency = 'USD', decimals = 2) {
  if (value === null || value === undefined) return '';

  try {
    // Ensure value is a number
    const numValue = Number(value);
    if (isNaN(numValue)) {
      console.error('Invalid value for formatCurrency:', value);
      return 'Invalid amount';
    }

    // Get locale from i18n or browser
    const getLocale = () => {
      // Try to get it from i18n if available
      try {
        if (window.i18n && window.i18n.global) {
          return window.i18n.global.locale.value || navigator.language || 'en-US';
        }
      } catch (e) {
        console.error('Error accessing i18n locale:', e);
      }

      // Fallback to browser locale
      return navigator.language || 'en-US';
    };

    const locale = getLocale();

    // Ensure currency is valid
    if (!currency || typeof currency !== 'string') {
      console.warn('Invalid currency provided to formatCurrency:', currency, 'using USD instead');
      currency = 'USD';
    }

    // Use Intl.NumberFormat for proper currency formatting
    const formatter = new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });

    return formatter.format(numValue);
  } catch (error) {
    console.error('Error in formatCurrency:', error, 'value:', value, 'currency:', currency);
    return 'Error formatting';
  }
}

/**
 * Format a date in the user's locale
 * @param {string|Date|number} dateValue - Date to format (can be string, Date object, or timestamp in ms)
 * @param {object} options - Intl.DateTimeFormat options
 * @returns {string} Formatted date string
 */
export function formatDate(dateValue, options = {}) {
  // 1. Проверка на null/undefined
  if (dateValue === null || dateValue === undefined || dateValue === '') {
      console.warn('formatDate called with null or undefined value.');
      return ''; // Возвращаем пустую строку
  }

  try {
    // 2. Преобразование в объект Date
    const date = new Date(dateValue);

    // 3. Проверка валидности объекта Date
    if (!(date instanceof Date) || isNaN(date.getTime())) {
      console.warn('Invalid date value after conversion:', dateValue, '->', date);
      return 'Invalid Date'; // Возвращаем сообщение об ошибке
    }

    // 4. Определение локали
    const getLocale = () => {
      try {
        if (window.i18n && window.i18n.global) {
          return window.i18n.global.locale.value || navigator.language || 'en-US';
        }
      } catch (e) { /* ignore */ }
      return navigator.language || 'en-US';
    };
    const locale = getLocale();

    // 5. Определение опций форматирования
    let formattingOptions;
    const hasOptions = Object.keys(options).length > 0;
    const hasStyleOptions = options.dateStyle || options.timeStyle;

    if (hasStyleOptions) {
      // Если переданы dateStyle или timeStyle, используем ТОЛЬКО их
      // (и другие валидные для стилей опции, если они есть в options)
      formattingOptions = { ...options }; // Копируем переданные опции
      // Удаляем несовместимые опции, если они случайно попали
      delete formattingOptions.year;
      delete formattingOptions.month;
      delete formattingOptions.day;
      delete formattingOptions.hour;
      delete formattingOptions.minute;
      delete formattingOptions.second;
      // Убедимся, что хотя бы один стиль задан
      if (!formattingOptions.dateStyle && !formattingOptions.timeStyle) {
          // Если передали пустые стили, вернемся к дефолту
          formattingOptions = { year: 'numeric', month: 'short', day: 'numeric' };
      }
    } else if (hasOptions) {
      // Если переданы опции, но НЕ dateStyle/timeStyle, используем их
      formattingOptions = { ...options };
    } else {
      // Если опции не переданы, используем дефолтные
      formattingOptions = {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      };
    }

    // 6. Форматирование
    // console.log('Formatting date:', date, 'with options:', formattingOptions, 'and locale:', locale); // Для отладки
    const formatter = new Intl.DateTimeFormat(locale, formattingOptions);
    return formatter.format(date);

  } catch (error) {
    // Ловим ошибку именно Intl.DateTimeFormat
    console.error('Error in Intl.DateTimeFormat:', error);
    console.error('Details:', { value: dateValue, options: options });
    // Возвращаем что-то безопасное
    return 'Date Format Error';
  }
}

/**
 * Format a percentage value
 * @param {number} value - The value to format as a percentage
 * @param {number} decimals - The number of decimal places (default 1)
 * @returns {string} Formatted percentage string
 */
export function formatPercentage(value, decimals = 1) {
  if (value === null || value === undefined) return '';

  // Get browser locale
  const locale = navigator.language || 'en-US';

  // Use Intl.NumberFormat for proper percentage formatting
  const formatter = new Intl.NumberFormat(locale, {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  });

  return formatter.format(value / 100);
}

/**
 * Format a large number with abbreviations (K, M, B)
 * @param {number} value - The number to format
 * @param {number} decimals - The number of decimal places (default 1)
 * @returns {string} Formatted number string with abbreviation
 */
export function formatLargeNumber(value, decimals = 1) {
  if (value === null || value === undefined) return '';

  const formatter = new Intl.NumberFormat('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  });

  // Define thresholds and abbreviations
  const abbreviations = [
    { threshold: 1e12, abbr: 'T' }, // Trillion
    { threshold: 1e9, abbr: 'B' },  // Billion
    { threshold: 1e6, abbr: 'M' },  // Million
    { threshold: 1e3, abbr: 'K' }   // Thousand
  ];

  // Find the appropriate abbreviation
  const item = abbreviations.find(item => Math.abs(value) >= item.threshold);

  if (item) {
    return formatter.format(value / item.threshold) + item.abbr;
  }

  return formatter.format(value);
}

/**
 * Determine CSS class based on a numeric value (positive, negative, or neutral)
 * @param {number} value - The numeric value to evaluate
 * @returns {string} CSS class name based on the value
 */
export function getValueColorClass(value) {
  if (value === null || value === undefined) return '';

  // Convert to number if it's a string
  const numValue = Number(value);

  // Check if it's a valid number
  if (isNaN(numValue)) return '';

  if (numValue > 0) return 'positive';
  if (numValue < 0) return 'negative';
  return ''; // neutral
}
