/**
 * CurrencyFreaks API client
 * API documentation: https://currencyfreaks.com/documentation.html
 */

import axios from 'axios';

// API key for CurrencyFreaks
const API_KEY = 'b4efa167b4834ac8a2580d62f7a0d743';
const BASE_URL = 'https://api.currencyfreaks.com';
const STORAGE_KEY = 'currency_rates_cache';
const CACHE_DURATION_MS = 24 * 60 * 60 * 1000; // 24 hours in milliseconds

// Create an Axios instance configured for CurrencyFreaks API
const currencyFreaksApi = axios.create({
  baseURL: BASE_URL,
  timeout: 15000
});

/**
 * Get latest exchange rates from CurrencyFreaks API
 * Will only fetch new rates once per day, otherwise returns cached rates
 * 
 * @returns {Promise<Object>} Promise with exchange rates object
 */
export async function getExchangeRates() {
  try {
    // Check if we have cached rates from today
    const cachedData = getCachedRates();
    if (cachedData) {
      console.log('Using cached exchange rates (updated daily)');
      return cachedData.rates;
    }
    
    // If no valid cache, fetch from API
    console.log('Fetching fresh exchange rates from API');
    const response = await currencyFreaksApi.get('/latest', {
      params: {
        apikey: API_KEY,
        format: 'json',
        // Optional parameters:
        // symbols: 'USD,EUR,GBP,CAD,AUD,JPY,CNY,INR,GEL,RUB' // Specific currencies
      }
    });

    // Handle successful response
    if (response.data && response.data.rates) {
      // The API returns rates with USD as base
      // Round all rates to 2 decimal places
      const roundedRates = {};
      for (const [currency, rate] of Object.entries(response.data.rates)) {
        roundedRates[currency] = Number(parseFloat(rate).toFixed(2));
      }
      
      // Save to cache
      cacheRates(roundedRates);
      
      return roundedRates;
    } else {
      console.error('Invalid response from CurrencyFreaks API:', response.data);
      throw new Error('Invalid response format from CurrencyFreaks API');
    }
  } catch (error) {
    console.error('Error fetching exchange rates from CurrencyFreaks:', error);
    
    // If API call fails but we have cached data (even if expired), use it as fallback
    const cachedData = localStorage.getItem(STORAGE_KEY);
    if (cachedData) {
      try {
        const parsed = JSON.parse(cachedData);
        console.warn('Using cached exchange rates as fallback after API error');
        return parsed.rates;
      } catch (e) {
        console.error('Error parsing cached rates:', e);
      }
    }
    
    // Re-throw error if no fallback available
    throw error;
  }
}

/**
 * Get cached exchange rates if they're still valid (less than 24 hours old)
 * 
 * @returns {Object|null} The cached rates or null if invalid/expired
 */
function getCachedRates() {
  try {
    const cachedData = localStorage.getItem(STORAGE_KEY);
    if (!cachedData) return null;
    
    const parsed = JSON.parse(cachedData);
    const now = new Date().getTime();
    
    // Check if cache is still valid (less than 24 hours old)
    if (now - parsed.timestamp < CACHE_DURATION_MS) {
      return parsed;
    }
    
    return null;
  } catch (e) {
    console.error('Error reading currency rates cache:', e);
    return null;
  }
}

/**
 * Save rates to localStorage cache with timestamp
 * 
 * @param {Object} rates - The exchange rates to cache
 */
function cacheRates(rates) {
  try {
    const cacheData = {
      timestamp: new Date().getTime(),
      rates: rates
    };
    
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cacheData));
  } catch (e) {
    console.error('Error saving currency rates to cache:', e);
  }
}

/**
 * Get historical exchange rates from CurrencyFreaks API
 * Also uses caching to avoid unnecessary API calls
 * 
 * @param {string} date - The date in YYYY-MM-DD format
 * @returns {Promise<Object>} Promise with historical exchange rates object
 */
export async function getHistoricalRates(date) {
  try {
    // Check if we have this date's rates in cache
    const cachedData = getHistoricalCachedRates(date);
    if (cachedData) {
      console.log(`Using cached historical exchange rates for ${date}`);
      return cachedData;
    }
    
    // If no cache, fetch from API
    console.log(`Fetching historical exchange rates for ${date} from API`);
    const response = await currencyFreaksApi.get('/historical', {
      params: {
        apikey: API_KEY,
        date: date,
        format: 'json'
      }
    });

    if (response.data && response.data.rates) {
      // Round historical rates to 2 decimal places
      const roundedRates = {};
      for (const [currency, rate] of Object.entries(response.data.rates)) {
        roundedRates[currency] = Number(parseFloat(rate).toFixed(2));
      }
      
      // Save to cache
      cacheHistoricalRates(date, roundedRates);
      
      return roundedRates;
    } else {
      console.error('Invalid response from CurrencyFreaks historical API:', response.data);
      throw new Error('Invalid response format from CurrencyFreaks historical API');
    }
  } catch (error) {
    console.error(`Error fetching historical rates for ${date}:`, error);
    
    // Try to use cached data as fallback even if expired
    const cachedData = getHistoricalCachedRates(date, true);
    if (cachedData) {
      console.warn(`Using cached historical rates for ${date} as fallback after API error`);
      return cachedData;
    }
    
    throw error;
  }
}

/**
 * Get cached historical exchange rates for a specific date
 * 
 * @param {string} date - The date in YYYY-MM-DD format
 * @param {boolean} ignoreExpiry - Whether to ignore cache expiration (for fallback purposes)
 * @returns {Object|null} The cached historical rates or null if not found
 */
function getHistoricalCachedRates(date, ignoreExpiry = false) {
  try {
    const storageKey = `historical_rates_${date}`;
    const cachedData = localStorage.getItem(storageKey);
    if (!cachedData) return null;
    
    const parsed = JSON.parse(cachedData);
    
    // Historical rates don't really expire, but we still check the cache age
    // if not explicitly told to ignore expiry
    if (!ignoreExpiry) {
      const now = new Date().getTime();
      // Cache historical rates for 30 days (rates for a specific past date don't change often)
      if (now - parsed.timestamp > 30 * 24 * 60 * 60 * 1000) {
        return null;
      }
    }
    
    return parsed.rates;
  } catch (e) {
    console.error(`Error reading historical rates cache for ${date}:`, e);
    return null;
  }
}

/**
 * Save historical rates to localStorage cache with timestamp
 * 
 * @param {string} date - The date in YYYY-MM-DD format
 * @param {Object} rates - The exchange rates to cache
 */
function cacheHistoricalRates(date, rates) {
  try {
    const storageKey = `historical_rates_${date}`;
    const cacheData = {
      timestamp: new Date().getTime(),
      rates: rates
    };
    
    localStorage.setItem(storageKey, JSON.stringify(cacheData));
  } catch (e) {
    console.error(`Error saving historical rates for ${date} to cache:`, e);
  }
}