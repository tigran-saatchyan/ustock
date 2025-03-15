import dayjs from 'dayjs';

/**
 * Format a number as currency
 * @param {number} value - The number to format
 * @param {string} currency - The currency code
 * @param {number} decimals - The number of decimal places
 * @returns {string} - The formatted currency string
 */
export const formatCurrency = (value, currency = 'USD', decimals = 2) => {
  if (value === null || value === undefined || isNaN(value)) {
    return 'N/A';
  }
  
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(value);
};

/**
 * Format a number with commas and optional decimals
 * @param {number} value - The number to format
 * @param {number} decimals - The number of decimal places
 * @returns {string} - The formatted number
 */
export const formatNumber = (value, decimals = 2) => {
  if (value === null || value === undefined || isNaN(value)) {
    return 'N/A';
  }
  
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: decimals
  }).format(value);
};

/**
 * Format a number as a percentage
 * @param {number} value - The number to format (0.1 = 10%)
 * @param {number} decimals - The number of decimal places
 * @returns {string} - The formatted percentage
 */
export const formatPercent = (value, decimals = 2) => {
  if (value === null || value === undefined || isNaN(value)) {
    return 'N/A';
  }
  
  return new Intl.NumberFormat('en-US', {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(value);
};

/**
 * Format a date string
 * @param {string} dateString - The date string to format
 * @param {string} format - The format string (dayjs format)
 * @returns {string} - The formatted date
 */
export const formatDate = (dateString, format = 'MMM D, YYYY') => {
  if (!dateString) return 'N/A';
  
  return dayjs(dateString).format(format);
};

/**
 * Format a large number with abbreviations (K, M, B, T)
 * @param {number} value - The number to format
 * @param {number} decimals - The number of decimal places
 * @returns {string} - The formatted number with abbreviation
 */
export const formatLargeNumber = (value, decimals = 1) => {
  if (value === null || value === undefined || isNaN(value)) {
    return 'N/A';
  }
  
  if (value === 0) return '0';
  
  const abs = Math.abs(value);
  const sign = value < 0 ? '-' : '';
  
  if (abs >= 1000000000000) {
    return sign + (abs / 1000000000000).toFixed(decimals) + 'T';
  }
  if (abs >= 1000000000) {
    return sign + (abs / 1000000000).toFixed(decimals) + 'B';
  }
  if (abs >= 1000000) {
    return sign + (abs / 1000000).toFixed(decimals) + 'M';
  }
  if (abs >= 1000) {
    return sign + (abs / 1000).toFixed(decimals) + 'K';
  }
  
  return sign + abs.toFixed(decimals);
};

/**
 * Get CSS class for a numeric value (positive/negative)
 * @param {number} value - The numeric value
 * @returns {string} - The CSS class
 */
export const getValueColorClass = (value) => {
  if (value === null || value === undefined || isNaN(value)) {
    return '';
  }
  
  return value >= 0 ? 'financial-value--positive' : 'financial-value--negative';
};

/**
 * Add plus sign to positive numbers
 * @param {number} value - The number to format
 * @returns {string} - The formatted number with sign
 */
export const formatWithSign = (value) => {
  if (value === null || value === undefined || isNaN(value)) {
    return 'N/A';
  }
  
  return value > 0 ? `+${value}` : `${value}`;
};

/**
 * Get a color based on a value (for charts, etc.)
 * @param {number} value - The value to get color for
 * @returns {string} - The color code
 */
export const getValueColor = (value) => {
  if (value === null || value === undefined || isNaN(value)) {
    return '#757575';
  }
  
  return value >= 0 ? '#00c853' : '#ff5252';
};