<template>
  <div class="not-found-view">
    <div class="app-container">
      <div class="not-found-content">
        <div class="not-found-icon">
          <i class="pi pi-chart-line"></i>
        </div>
        <h1 class="not-found-title">404</h1>
        <p class="not-found-message">Oops! The page you are looking for cannot be found.</p>
        <p class="not-found-suggestion">
          The stock market has ups and downs, but this page seems to be permanently delisted.
        </p>
        <router-link to="/" class="not-found-button">
          Return to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFoundView'
};
</script>

<style lang="scss" scoped>
.not-found-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.not-found-content {
  text-align: center;
  padding: $spacing-xl;
  max-width: 500px;
  margin: 0 auto;
}

.not-found-icon {
  font-size: 5rem;
  color: $primary-color;
  margin-bottom: $spacing-md;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0px);
  }
}

.not-found-title {
  font-size: 6rem;
  font-weight: 800;
  color: $primary-color;
  margin: 0 0 $spacing-md;
  line-height: 1;
}

.not-found-message {
  font-size: $font-size-xl;
  color: $text-primary;
  margin-bottom: $spacing-md;
}

.not-found-suggestion {
  color: $text-secondary;
  margin-bottom: $spacing-xl;
}

.not-found-button {
  display: inline-block;
  background-color: $primary-color;
  color: white;
  font-weight: 600;
  padding: $spacing-sm $spacing-lg;
  border-radius: $border-radius;
  text-decoration: none;
  transition: $transition-quick;
  
  &:hover {
    background-color: $primary-dark;
    transform: translateY(-2px);
  }
}
</style>