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

// Finance views (lazy loaded)
const FinanceDashboardView = () => import('@/views/finance/DashboardView.vue');
const FinanceTransactionsView = () => import('@/views/finance/TransactionsView.vue');
const FinanceBudgetsView = () => import('@/views/finance/BudgetsView.vue');
const FinanceAccountsView = () => import('@/views/finance/AccountsView.vue');
const FinanceGoalsView = () => import('@/views/finance/GoalsView.vue');
const FinanceSettingsView = () => import('@/views/finance/SettingsView.vue');

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
    path: '/finance',
    name: 'finance',
    component: FinanceDashboardView,
    meta: {
      title: 'Personal Finance - UStock',
      requiresAuth: true
    }
  },
  {
    path: '/finance/transactions',
    name: 'finance-transactions',
    component: FinanceTransactionsView,
    meta: {
      title: 'Transactions - UStock Finance',
      requiresAuth: true
    }
  },
  {
    path: '/finance/budgets',
    name: 'finance-budgets',
    component: FinanceBudgetsView,
    meta: {
      title: 'Budgets - UStock Finance',
      requiresAuth: true
    }
  },
  {
    path: '/finance/accounts',
    name: 'finance-accounts',
    component: FinanceAccountsView,
    meta: {
      title: 'Accounts - UStock Finance',
      requiresAuth: true
    }
  },
  {
    path: '/finance/goals',
    name: 'finance-goals',
    component: FinanceGoalsView,
    meta: {
      title: 'Savings Goals - UStock Finance',
      requiresAuth: true
    }
  },
  {
    path: '/finance/settings',
    name: 'finance-settings',
    component: FinanceSettingsView,
    meta: {
      title: 'Settings - UStock Finance',
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
  // Add debug logging
  console.log('Navigation to:', to.path, to.name);
  
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
    console.log('Auth required, redirecting to login');
    // Save current location to redirect after login
    store.dispatch('auth/setLoginRedirect', to.fullPath);
    
    // Redirect to login page
    next('/auth/login');
  } else if (isAuthenticated && isLoginPage) {
    console.log('Already authenticated, redirecting to home');
    // Redirect to home if already logged in and trying to access login page
    next('/');
  } else {
    console.log('Proceeding to route:', to.name);
    next();
  }
});

export default router;