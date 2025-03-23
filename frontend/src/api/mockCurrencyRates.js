/**
 * Mock exchange rates API response
 * Used for development/testing when the actual API is not available
 *
 * Exchange rates are relative to USD
 * Last updated: 2025-03-22
 */

export const MOCK_EXCHANGE_RATES = {
  USD: 1,
  EUR: 0.93,
  GBP: 0.79,
  CAD: 1.36,
  AUD: 1.51,
  JPY: 151.62,
  CNY: 7.23,
  INR: 83.48,
  GEL: 2.65
};

/**
 * Get mock exchange rates data for testing
 * 
 * @returns {Object} Exchange rates object with currency codes as keys
 */
export function getMockExchangeRates() {
  return { ...MOCK_EXCHANGE_RATES };
}

/**
 * Get mock exchange rates data asynchronously
 * This simulates an API call with a delay
 * 
 * @param {number} delay - Delay in milliseconds
 * @returns {Promise<Object>} Promise with exchange rates object
 */
export function getMockExchangeRatesAsync(delay = 500) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ ...MOCK_EXCHANGE_RATES });
    }, delay);
  });
}