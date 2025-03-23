<template>
  <div class="settings-view">
    <finance-navigation />
    
    <div class="settings-container">
      <div class="settings-header">
        <h2 class="settings-title">{{ $t('navigation.settings') }}</h2>
      </div>
      
      <div class="settings-content">
        <currency-settings />
      </div>
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { useI18n } from 'vue-i18n';
import FinanceNavigation from '@/components/finance/FinanceNavigation.vue';
import CurrencySettings from '@/components/finance/CurrencySettings.vue';

export default defineComponent({
  name: 'SettingsView',
  
  components: {
    FinanceNavigation,
    CurrencySettings
  },
  
  setup() {
    const { t } = useI18n();
    
    return {
      t
    };
  }
});
</script>

<style lang="scss" scoped>
.settings-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.settings-container {
  margin-bottom: 20px;
}

.settings-header {
  margin-bottom: 20px;
}

.settings-title {
  color: #f7941d; /* Changed to orange */
  font-size: 24px;
  margin-top: 0;
  margin-bottom: 15px;
  font-weight: 600;
}

.settings-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  
  @media (min-width: 768px) {
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  }
}
</style>