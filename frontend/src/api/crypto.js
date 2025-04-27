import axios from 'axios';
import { API_URL } from '@/config';

/**
 * API client for crypto trading functionality
 */
export default {
  /**
   * Get account balance
   * @param {string} exchange - Exchange name (default: binance)
   * @returns {Promise} - Promise with account balance data
   */
  getAccountBalance(exchange = 'binance') {
    const url = exchange === 'binance' 
      ? `${API_URL}/financials/crypto/balance/` 
      : `${API_URL}/financials/crypto/balance/${exchange}/`;
    return axios.get(url);
  },

  /**
   * Get ticker price
   * @param {string} symbol - Trading pair symbol (e.g., 'BTCUSDT')
   * @param {string} exchange - Exchange name (default: binance)
   * @returns {Promise} - Promise with ticker price data
   */
  getTickerPrice(symbol, exchange = 'binance') {
    const url = exchange === 'binance'
      ? `${API_URL}/financials/crypto/ticker/${symbol}/`
      : `${API_URL}/financials/crypto/ticker/${symbol}/${exchange}/`;
    return axios.get(url);
  },

  /**
   * Get order book
   * @param {string} symbol - Trading pair symbol (e.g., 'BTCUSDT')
   * @param {number} limit - Number of orders to return (default: 20)
   * @param {string} exchange - Exchange name (default: binance)
   * @returns {Promise} - Promise with order book data
   */
  getOrderBook(symbol, limit = 20, exchange = 'binance') {
    const url = exchange === 'binance'
      ? `${API_URL}/financials/crypto/orderbook/${symbol}/`
      : `${API_URL}/financials/crypto/orderbook/${symbol}/${exchange}/`;
    return axios.get(url, { params: { limit } });
  },

  /**
   * Create order
   * @param {Object} orderData - Order data
   * @param {string} orderData.symbol - Trading pair symbol (e.g., 'BTCUSDT')
   * @param {string} orderData.side - Order side (BUY or SELL)
   * @param {string} orderData.type - Order type (LIMIT, MARKET, etc.)
   * @param {number} orderData.quantity - Order quantity
   * @param {number} orderData.price - Order price (required for LIMIT orders)
   * @param {string} exchange - Exchange name (default: binance)
   * @returns {Promise} - Promise with order data
   */
  createOrder(orderData, exchange = 'binance') {
    const url = exchange === 'binance'
      ? `${API_URL}/financials/crypto/orders/`
      : `${API_URL}/financials/crypto/orders/${exchange}/`;
    return axios.post(url, orderData);
  },

  /**
   * Get open orders
   * @param {string} symbol - Trading pair symbol (e.g., 'BTCUSDT') (optional)
   * @param {string} exchange - Exchange name (default: binance)
   * @returns {Promise} - Promise with open orders data
   */
  getOpenOrders(symbol = null, exchange = 'binance') {
    const url = exchange === 'binance'
      ? `${API_URL}/financials/crypto/orders/open/`
      : `${API_URL}/financials/crypto/orders/open/${exchange}/`;
    const params = symbol ? { symbol } : {};
    return axios.get(url, { params });
  },

  /**
   * Cancel order
   * @param {string} symbol - Trading pair symbol (e.g., 'BTCUSDT')
   * @param {string} orderId - Order ID
   * @param {string} exchange - Exchange name (default: binance)
   * @returns {Promise} - Promise with cancellation result
   */
  cancelOrder(symbol, orderId, exchange = 'binance') {
    const url = exchange === 'binance'
      ? `${API_URL}/financials/crypto/orders/${symbol}/${orderId}/`
      : `${API_URL}/financials/crypto/orders/${symbol}/${orderId}/${exchange}/`;
    return axios.delete(url);
  },

  /**
   * Get exchange information
   * @param {string} exchange - Exchange name (default: binance)
   * @returns {Promise} - Promise with exchange information
   */
  getExchangeInfo(exchange = 'binance') {
    const url = exchange === 'binance'
      ? `${API_URL}/financials/crypto/exchange/`
      : `${API_URL}/financials/crypto/exchange/${exchange}/`;
    return axios.get(url);
  },

  /**
   * Get all ticker prices
   * @param {string} exchange - Exchange name (default: binance)
   * @returns {Promise} - Promise with all ticker prices
   */
  getAllTickers(exchange = 'binance') {
    const url = exchange === 'binance'
      ? `${API_URL}/financials/crypto/tickers/`
      : `${API_URL}/financials/crypto/tickers/${exchange}/`;
    return axios.get(url);
  },

  /**
   * Get API keys
   * @param {string} exchange - Exchange name (optional)
   * @returns {Promise} - Promise with API keys data
   */
  getApiKeys(exchange = null) {
    const url = exchange
      ? `${API_URL}/financials/crypto/api-keys/${exchange}/`
      : `${API_URL}/financials/crypto/api-keys/`;
    return axios.get(url);
  },

  /**
   * Create or update API keys
   * @param {Object} apiKeyData - API key data
   * @param {string} apiKeyData.exchange - Exchange name
   * @param {string} apiKeyData.api_key - API key
   * @param {string} apiKeyData.api_secret - API secret
   * @returns {Promise} - Promise with API key data
   */
  createApiKey(apiKeyData) {
    const url = `${API_URL}/financials/crypto/api-keys/`;
    return axios.post(url, apiKeyData);
  },

  /**
   * Delete API keys
   * @param {string} exchange - Exchange name
   * @returns {Promise} - Promise with deletion result
   */
  deleteApiKey(exchange) {
    const url = `${API_URL}/financials/crypto/api-keys/${exchange}/`;
    return axios.delete(url);
  }
};