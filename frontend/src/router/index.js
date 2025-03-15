import { createRouter, createWebHistory } from 'vue-router';
import store from '@/store';

// Import views
import HomeView from '@/views/HomeView.vue';
import TickerView from '@/views/TickerView.vue';
import FinancialsView from '@/views/FinancialsView.vue';
import OptionsView from '@/views/OptionsView.vue';
import NewsView from '@/views/NewsView.vue';
import NotFoundView from '@/views/NotFoundView.vue';
import LoginView from '@/views/auth/LoginView.vue';

const routes = [
  {
    path: '/auth',
    name: 'auth',
    children: [
      {
        path: 'login',
        name: 'login',
        component: LoginView,
        meta: {
          title: 'Login - StockTic',
          public: true
        }
      }
    ]
  },
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: 'StockTic - Financial Market Data',
      requiresAuth: true
    }
  },
  {
    path: '/ticker/:symbol',
    name: 'ticker',
    component: TickerView,
    props: true,
    meta: {
      title: route => `${route.params.symbol.toUpperCase()} - StockTic`,
      requiresAuth: true
    }
  },
  {
    path: '/ticker/:symbol/financials',
    name: 'financials',
    component: FinancialsView,
    props: true,
    meta: {
      title: route => `${route.params.symbol.toUpperCase()} Financials - StockTic`,
      requiresAuth: true
    }
  },
  {
    path: '/ticker/:symbol/options',
    name: 'options',
    component: OptionsView,
    props: true,
    meta: {
      title: route => `${route.params.symbol.toUpperCase()} Options - StockTic`,
      requiresAuth: true
    }
  },
  {
    path: '/ticker/:symbol/news',
    name: 'news',
    component: NewsView,
    props: true,
    meta: {
      title: route => `${route.params.symbol.toUpperCase()} News - StockTic`,
      requiresAuth: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
    meta: {
      title: 'Page Not Found - UStock'
    }
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior() {
    // Always scroll to top on navigation
    return { top: 0 };
  }
});

// Navigation guard for auth
router.beforeEach((to, from, next) => {
  // Set the document title based on route metadata
  if (to.meta.title) {
    document.title = typeof to.meta.title === 'function'
      ? to.meta.title(to)
      : to.meta.title;
  }
  
  // Check if the route requires authentication
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  // Check if this is a public route (like login)
  const isLoginPage = to.matched.some(record => record.meta.public);
  const isAuthenticated = store.getters['auth/isAuthenticated'];
  
  if (requiresAuth && !isAuthenticated) {
    // Save current location to redirect after login
    store.dispatch('auth/setLoginRedirect', to.fullPath);
    
    // Redirect to login page
    next('/auth/login');
  } else if (isAuthenticated && isLoginPage) {
    // Redirect to home if already logged in and trying to access login page
    next('/');
  } else {
    next();
  }
});

export default router;