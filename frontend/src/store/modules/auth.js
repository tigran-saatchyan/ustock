import axios from 'axios';
import router from '@/router';

export default {
  namespaced: true,
  
  state: {
    token: localStorage.getItem('auth_token') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
    loading: false,
    error: null,
    loginRedirect: '/',
  },
  
  getters: {
    isAuthenticated: state => !!state.token,
    user: state => state.user,
    loading: state => state.loading,
    error: state => state.error,
    loginRedirect: state => state.loginRedirect,
  },
  
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token;
      if (token) {
        localStorage.setItem('auth_token', token);
      } else {
        localStorage.removeItem('auth_token');
      }
    },
    
    SET_USER(state, user) {
      state.user = user;
      if (user) {
        localStorage.setItem('user', JSON.stringify(user));
        localStorage.setItem('auth_user', user.username);  // Save username for getCurrentUser
      } else {
        localStorage.removeItem('user');
        localStorage.removeItem('auth_user');
      }
    },
    
    SET_LOADING(state, loading) {
      state.loading = loading;
    },
    
    SET_ERROR(state, error) {
      state.error = error;
    },
    
    SET_LOGIN_REDIRECT(state, path) {
      state.loginRedirect = path;
    },
    
    CLEAR_ERROR(state) {
      state.error = null;
    }
  },
  
  actions: {
    /**
     * Attempt to log in with credentials
     */
    async login({ commit, dispatch, state }, { username, password }) {
      commit('SET_LOADING', true);
      commit('CLEAR_ERROR');
      
      try {
        // Create auth credentials
        const { authService } = require('@/services/api');
        const authHeader = 'Basic ' + btoa(`${username}:${password}`);
        
        console.log('Attempting login with username:', username);
        
        // Authenticate with the backend
        const response = await authService.login(username, password);
        console.log('Login response:', response);
        
        // Store auth info if successful
        commit('SET_TOKEN', authHeader);
        commit('SET_USER', {
          username: response.data.username,
          ...response.data
        });
        
        // Set the auth header for future API requests
        dispatch('setApiAuthHeader', authHeader, { root: true });
        
        // Redirect to previous page or home
        const redirectPath = state.loginRedirect || '/';
        commit('SET_LOGIN_REDIRECT', '/');
        router.push(redirectPath);
        
        return { success: true };
      } catch (error) {
        console.error('Login error:', error);
        let errorMsg = 'Login failed. Please check your credentials.';
        
        if (error.response) {
          console.error('Response status:', error.response.status);
          console.error('Response data:', error.response.data);
          
          if (error.response.status === 401) {
            errorMsg = 'Invalid username or password. Note: Django passwords are hashed in the database.';
          } else if (error.response.data && error.response.data.error) {
            errorMsg = error.response.data.error;
          } else if (error.response.status === 500) {
            errorMsg = 'Server error. Please check if Django server is running on port 8000.';
          }
        } else if (error.request) {
          console.error('No response received:', error.request);
          errorMsg = 'No response from server. Check if Django is running on port 8000.';
        } else {
          console.error('Error message:', error.message);
          errorMsg = `Error: ${error.message}`;
        }
        
        commit('SET_ERROR', errorMsg);
        return { success: false, error: errorMsg };
      } finally {
        commit('SET_LOADING', false);
      }
    },
    
    /**
     * Log the user out
     */
    logout({ commit }) {
      // Clear auth data
      commit('SET_TOKEN', null);
      commit('SET_USER', null);
      
      // Remove auth header
      delete axios.defaults.headers.common['Authorization'];
      
      // Redirect to login page
      router.push('/auth/login');
    },
    
    /**
     * Set the redirect path for after login
     */
    setLoginRedirect({ commit }, path) {
      commit('SET_LOGIN_REDIRECT', path || '/');
    },
    
    /**
     * Clear any auth errors
     */
    clearError({ commit }) {
      commit('CLEAR_ERROR');
    },
    
    /**
     * Check if the user is authenticated and redirect if not
     */
    checkAuth({ state, dispatch }) {
      if (!state.token) {
        // Save current location for redirect after login
        dispatch('setLoginRedirect', router.currentRoute.value.fullPath);
        
        // Redirect to login
        router.push('/auth/login');
        return false;
      }
      
      // Set the auth header for API requests (in case of page reload)
      dispatch('setApiAuthHeader', state.token, { root: true });
      
      return true;
    },
    
    /**
     * Initialize auth from localStorage on app start
     */
    initAuth({ state, dispatch }) {
      if (state.token) {
        // Set the auth header for API requests on app initialization
        dispatch('setApiAuthHeader', state.token, { root: true });
      }
    }
  }
};