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
 * @param {string|Date} dateValue - Date to format
 * @param {object} options - Intl.DateTimeFormat options
 * @returns {string} Formatted date string
 */
export function formatDate(dateValue, options = {}) {
  if (!dateValue) return '';
  
  const date = typeof dateValue === 'string' ? new Date(dateValue) : dateValue;
  
  // Default formatting options
  const defaultOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  };
  
  // Merge default options with provided options
  const mergedOptions = { ...defaultOptions, ...options };
  
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
  
  return new Intl.DateTimeFormat(locale, mergedOptions).format(date);
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