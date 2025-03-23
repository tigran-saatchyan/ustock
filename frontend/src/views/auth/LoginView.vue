<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-card__left">
        <div class="auth-card__branding">
          <img src="@/assets/icons/bitmap-transparent.png" alt="StockTic Logo" class="auth-logo">
          <div class="auth-title">StockTic</div>
        </div>
        <div class="auth-subtitle">{{ $t('auth.platformTitle') }}</div>
        <div class="auth-decoration">
          <div class="auth-decoration__chart">
            <div class="chart-line"></div>
            <div class="chart-dot"></div>
          </div>
        </div>
      </div>
      <div class="auth-card__right">
        <div class="login-form">
          <h1 class="login-form__title">{{ $t('auth.welcomeBack') }}</h1>
          <p class="login-form__subtitle">{{ $t('auth.signInToContinue') }}</p>
          
          <div class="alert alert--error" v-if="error">
            <i class="pi pi-exclamation-triangle"></i>
            <span>{{ error }}</span>
          </div>
          
          <div class="input-group">
            <label for="username" class="input-label">{{ $t('auth.username') }}</label>
            <div class="input-wrapper">
              <i class="pi pi-user"></i>
              <input
                id="username"
                v-model="username"
                type="text"
                class="input-field"
                :placeholder="$t('auth.enterUsername')"
                @keyup.enter="login"
                :disabled="loading"
              />
            </div>
          </div>
          
          <div class="input-group">
            <label for="password" class="input-label">{{ $t('auth.password') }}</label>
            <div class="input-wrapper">
              <i class="pi pi-lock"></i>
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                class="input-field"
                :placeholder="$t('auth.enterPassword')"
                @keyup.enter="login"
                :disabled="loading"
              />
              <button
                class="input-icon-button"
                @click="showPassword = !showPassword"
                type="button"
              >
                <i :class="showPassword ? 'pi pi-eye-slash' : 'pi pi-eye'"></i>
              </button>
            </div>
          </div>
          
          <div class="login-options">
            <div class="checkbox-wrapper">
              <input type="checkbox" id="remember" v-model="rememberMe" />
              <label for="remember">{{ $t('auth.rememberMe') }}</label>
            </div>
          </div>
          
          <button 
            class="btn btn--primary btn--block" 
            @click="login"
            :disabled="loading"
          >
            <span v-if="!loading">{{ $t('auth.signIn') }}</span>
            <div v-else class="btn-loader"></div>
          </button>
          
          <div class="login-footer">
            <p>{{ $t('auth.noAccount') }} <a href="#" @click.prevent>{{ $t('auth.contactAdmin') }}</a></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue';
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n';

export default {
  name: 'LoginView',
  
  setup() {
    const store = useStore();
    const router = useRouter();
    const { t } = useI18n();
    
    // Form fields
    const username = ref('');
    const password = ref('');
    const showPassword = ref(false);
    const rememberMe = ref(false);
    
    // Get store state
    const loading = computed(() => store.getters['auth/loading']);
    const error = computed(() => store.getters['auth/error']);
    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated']);
    
    // Clear errors when inputs change
    watch([username, password], () => {
      if (error.value) {
        store.dispatch('auth/clearError');
      }
    });
    
    // Redirect if already logged in
    if (isAuthenticated.value) {
      router.push('/');
    }
    
    // Login method
    const login = async () => {
      if (!username.value || !password.value) {
        store.dispatch('auth/clearError');
        store.commit('auth/SET_ERROR', t('auth.validation.bothRequired'));
        return;
      }
      
      const result = await store.dispatch('auth/login', {
        username: username.value,
        password: password.value
      });
      
      if (result.success) {
        // Successful login handling is managed in the auth module
      }
    };
    
    // Redirect if already authenticated
    if (isAuthenticated.value) {
      const redirectPath = store.getters['auth/loginRedirect'] || '/';
      router.push(redirectPath);
    }
    
    return {
      username,
      password,
      showPassword,
      rememberMe,
      loading,
      error,
      login,
      t
    };
  }
};
</script>

<style lang="scss" scoped>
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, lighten($secondary-color, 10%), $secondary-color);
  padding: $spacing-lg;
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('@/assets/icons/bitmap.png');
    background-size: cover;
    background-position: center;
    opacity: 0.05;
    pointer-events: none;
  }
}

.auth-card {
  display: flex;
  width: 100%;
  max-width: 1000px;
  min-height: 600px;
  background-color: $bg-primary;
  border-radius: $border-radius;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  animation: fadeInUp 0.6s ease-out;
  
  @media (max-width: $breakpoint-md) {
    flex-direction: column;
    max-width: 500px;
  }
  
  &__left {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: $spacing-xl;
    background: linear-gradient(135deg, $secondary-color, darken($secondary-color, 15%));
    color: white;
    position: relative;
    overflow: hidden;
    
    @media (max-width: $breakpoint-md) {
      padding: $spacing-lg $spacing-md;
    }
  }
  
  &__right {
    flex: 1;
    padding: $spacing-xl;
    display: flex;
    flex-direction: column;
    justify-content: center;
    
    @media (max-width: $breakpoint-md) {
      padding: $spacing-lg $spacing-md;
    }
  }
  
  &__branding {
    display: flex;
    align-items: center;
    margin-bottom: $spacing-md;
    z-index: 2;
  }
}

.auth-logo {
  height: 50px;
  width: auto;
  margin-right: $spacing-sm;
}

.auth-title {
  font-size: $font-size-xxl;
  font-weight: 700;
  color: white;
}

.auth-subtitle {
  color: rgba(white, 0.8);
  margin-bottom: $spacing-lg;
  z-index: 2;
}

.auth-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 70%;
  z-index: 1;
  
  &__chart {
    position: relative;
    height: 100%;
    width: 100%;
    
    .chart-line {
      position: absolute;
      bottom: 30%;
      left: -10%;
      width: 120%;
      height: 2px;
      background: linear-gradient(90deg, 
        rgba($primary-light, 0), 
        rgba($primary-light, 0.7),
        rgba($primary-light, 0.3),
        rgba($primary-light, 0.8),
        rgba($primary-light, 0.2),
        rgba($primary-light, 0.9),
        rgba($primary-light, 0)
      );
      animation: pulse 3s infinite;
    }
    
    .chart-dot {
      position: absolute;
      bottom: calc(30% - 4px);
      left: 65%;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background-color: $primary-light;
      box-shadow: 0 0 10px rgba($primary-light, 0.8);
      animation: glow 3s infinite;
    }
  }
}

.login-form {
  width: 100%;
  max-width: 380px;
  margin: 0 auto;
  
  &__title {
    font-size: $font-size-xl;
    font-weight: 700;
    color: $text-primary;
    margin-bottom: $spacing-xs;
  }
  
  &__subtitle {
    color: $text-secondary;
    margin-bottom: $spacing-xl;
  }
}

.input-group {
  margin-bottom: $spacing-lg;
}

.input-label {
  display: block;
  font-size: $font-size-sm;
  font-weight: 500;
  margin-bottom: $spacing-xs;
  color: $text-primary;
}

.input-wrapper {
  position: relative;
  
  i {
    position: absolute;
    left: $spacing-md;
    top: 50%;
    transform: translateY(-50%);
    color: $text-secondary;
  }
}

.input-field {
  width: 100%;
  height: 50px;
  padding: $spacing-sm $spacing-lg $spacing-sm $spacing-xl * 1.5;
  border: 1px solid rgba($text-disabled, 0.5);
  border-radius: $border-radius;
  font-size: $font-size-md;
  transition: $transition-quick;
  
  &:focus {
    outline: none;
    border-color: $primary-color;
    box-shadow: 0 0 0 3px rgba($primary-color, 0.1);
  }
  
  &::placeholder {
    color: $text-disabled;
  }
  
  &:disabled {
    background-color: $bg-secondary;
    cursor: not-allowed;
  }
}

.input-icon-button {
  position: absolute;
  right: $spacing-sm;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: $text-secondary;
  cursor: pointer;
  padding: $spacing-xs;
  
  &:hover {
    color: $primary-color;
  }
}

.login-options {
  display: flex;
  justify-content: flex-start;
  margin-bottom: $spacing-lg;
  
  .checkbox-wrapper {
    display: flex;
    align-items: center;
    
    input[type="checkbox"] {
      margin-right: $spacing-xs;
    }
    
    label {
      font-size: $font-size-sm;
      color: $text-secondary;
    }
  }
}

.btn--block {
  width: 100%;
  margin-bottom: $spacing-lg;
  height: 50px;
  font-size: $font-size-md;
}

.btn-loader {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

.login-footer {
  text-align: center;
  font-size: $font-size-sm;
  color: $text-secondary;
  
  a {
    color: $primary-color;
    text-decoration: none;
    font-weight: 500;
    
    &:hover {
      text-decoration: underline;
    }
  }
}

.alert {
  padding: $spacing-sm $spacing-md;
  border-radius: $border-radius;
  margin-bottom: $spacing-lg;
  display: flex;
  align-items: center;
  animation: fadeIn 0.3s ease-out;
  
  i {
    margin-right: $spacing-sm;
  }
  
  &--error {
    background-color: rgba($negative, 0.1);
    color: $negative;
    border-left: 3px solid $negative;
  }
}

// Animations
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes pulse {
  0% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.5;
  }
}

@keyframes glow {
  0% {
    box-shadow: 0 0 5px rgba($primary-light, 0.5);
  }
  50% {
    box-shadow: 0 0 15px rgba($primary-light, 0.8);
  }
  100% {
    box-shadow: 0 0 5px rgba($primary-light, 0.5);
  }
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>