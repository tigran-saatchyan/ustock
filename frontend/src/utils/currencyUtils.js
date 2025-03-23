import { useStore } from 'vuex';
import { formatCurrency } from './formatters';

/**
 * Format currency value with support for dual currency display
 * based on currency settings in the store
 *
 * @param {number} value - The value to format
 * @param {string|null} forceCurrency - Optional currency to use instead of store settings
 * @returns {string} Formatted currency string
 */
export function useDualCurrencyFormatter() {
  const store = useStore();
  
  /**
   * Format a number in both primary and secondary currencies if enabled
   */
  const formatDualCurrency = (value, forceCurrency = null) => {
    if (value === null || value === undefined) return '';
    
    try {
      // Ensure value is a number
      const numValue = Number(value);
      if (isNaN(numValue)) {
        console.error('Invalid value for currency formatting:', value);
        return 'Invalid amount';
      }
      
      // Get currency settings from store
      const primaryCurrency = forceCurrency || store.getters['personalFinance/primaryCurrency'] || 'USD';
      const secondaryCurrency = store.getters['personalFinance/secondaryCurrency'] || 'USD';
      const showSecondaryCurrency = store.getters['personalFinance/showSecondaryCurrency'];
      
      // Format in primary currency
      const primaryFormatted = formatCurrency(numValue, primaryCurrency);
      
      // If secondary currency is not enabled or is the same as primary
      if (!showSecondaryCurrency || primaryCurrency === secondaryCurrency) {
        return primaryFormatted;
      }
      
      // Get exchange rates (optionally for a specific date)
      const date = store.state.personalFinance.selectedYear && store.state.personalFinance.selectedMonth 
        ? `${store.state.personalFinance.selectedYear}-${String(store.state.personalFinance.selectedMonth).padStart(2, '0')}-01` 
        : null;
      const primaryRate = store.getters['personalFinance/getExchangeRate'](primaryCurrency, date) || 1;
      const secondaryRate = store.getters['personalFinance/getExchangeRate'](secondaryCurrency, date) || 1;
      
      // Convert value to USD first (if not already USD), then to secondary currency
      const valueInUSD = primaryCurrency === 'USD' ? numValue : numValue / primaryRate;
      const valueInSecondary = valueInUSD * secondaryRate;
      
      // Format secondary value
      const secondaryFormatted = formatCurrency(valueInSecondary, secondaryCurrency);
      
      // Return both formatted strings
      return `${primaryFormatted} (${secondaryFormatted})`;
    } catch (error) {
      console.error('Error in formatDualCurrency:', error);
      return 'Error formatting';
    }
  };

  return {
    formatDualCurrency
  };
}

/**
 * Convert a value from one currency to another using exchange rates
 * 
 * @param {number} value - The value to convert
 * @param {string} fromCurrency - The source currency code
 * @param {string} toCurrency - The target currency code
 * @param {object} rates - Exchange rates object (relative to USD)
 * @returns {number} The converted value
 */
export function convertCurrency(value, fromCurrency, toCurrency, rates) {
  if (fromCurrency === toCurrency) return value;
  
  // Get rates (default to 1 if not found)
  const fromRate = fromCurrency === 'USD' ? 1 : (rates[fromCurrency] || 1);
  const toRate = toCurrency === 'USD' ? 1 : (rates[toCurrency] || 1);
  
  // Convert to USD first (if not already USD), then to target currency
  const valueInUSD = fromCurrency === 'USD' ? value : value / fromRate;
  return valueInUSD * toRate;
}