<template>
  <footer class="app-footer">
    <div class="app-footer__container">
      <div class="app-footer__content">
        <div class="app-footer__brand">
          <h2 class="app-footer__title">StockTic</h2>
          <p>Financial market data powered by Yahoo Finance API</p>
        </div>
        
        <div class="app-footer__links">
          <div class="app-footer__links-section">
            <h3>Resources</h3>
            <ul>
              <li><a href="#">Documentation</a></li>
              <li><a href="#">API Reference</a></li>
              <li><a href="#">Support</a></li>
            </ul>
          </div>
          
          <div class="app-footer__links-section">
            <h3>Legal</h3>
            <ul>
              <li><a href="#">Terms of Service</a></li>
              <li><a href="#">Privacy Policy</a></li>
              <li><a href="#">Disclaimer</a></li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="app-footer__bottom">
        <p>&copy; {{ currentYear }} StockTic - All rights reserved</p>
        <p>Data provided by Yahoo Finance</p>
      </div>
    </div>
  </footer>
</template>

<script>
import { computed } from 'vue';

export default {
  name: 'AppFooter',
  
  setup() {
    // Get current year for copyright notice
    const currentYear = computed(() => new Date().getFullYear());
    
    return {
      currentYear
    };
  }
};
</script>

<style lang="scss" scoped>
.app-footer {
  background-color: $secondary-color;
  background-image: linear-gradient(to bottom, $secondary-color, darken($secondary-color, 10%));
  color: white;
  padding: $spacing-xl 0;
  margin-top: $spacing-xl;
  
  &__container {
    max-width: 1440px;
    margin: 0 auto;
    padding: 0 $spacing-md;
  }
  
  &__content {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin-bottom: $spacing-xl;
  }
  
  &__brand {
    flex: 1;
    min-width: 250px;
    margin-right: $spacing-xl;
    
    p {
      color: rgba(255, 255, 255, 0.7);
      margin-top: $spacing-sm;
    }
  }
  
  &__title {
    font-size: $font-size-xl;
    font-weight: 700;
    margin: 0 0 $spacing-sm;
    color: white;
  }
  
  &__links {
    display: flex;
    flex-wrap: wrap;
    
    &-section {
      margin-left: $spacing-xl;
      min-width: 150px;
      
      h3 {
        font-size: $font-size-md;
        margin-bottom: $spacing-md;
        color: white;
      }
      
      ul {
        list-style: none;
        padding: 0;
        margin: 0;
        
        li {
          margin-bottom: $spacing-sm;
          
          a {
            color: rgba(255, 255, 255, 0.7);
            text-decoration: none;
            transition: $transition-quick;
            
            &:hover {
              color: white;
              text-decoration: underline;
            }
          }
        }
      }
    }
  }
  
  &__bottom {
    padding-top: $spacing-lg;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    
    p {
      color: rgba(255, 255, 255, 0.5);
      font-size: $font-size-sm;
      margin: $spacing-sm 0;
    }
  }
}

// Responsive adjustments
@media (max-width: $breakpoint-md) {
  .app-footer {
    &__brand {
      width: 100%;
      margin-bottom: $spacing-lg;
    }
    
    &__links {
      width: 100%;
      
      &-section {
        margin-left: 0;
        margin-right: $spacing-xl;
        margin-bottom: $spacing-lg;
      }
    }
    
    &__bottom {
      flex-direction: column;
      text-align: center;
    }
  }
}
</style>