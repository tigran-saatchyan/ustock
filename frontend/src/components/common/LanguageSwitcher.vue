<template>
  <div class="language-switcher">
    <button 
      @click="toggleDropdown" 
      class="language-dropdown-button"
      ref="dropdownButton"
    >
      <i class="pi pi-globe"></i>
      <span class="current-language">{{ getCurrentLanguageName }}</span>
      <i class="pi pi-chevron-down" :class="{ 'pi-chevron-up': isOpen }"></i>
    </button>
    
    <div class="language-dropdown" v-if="isOpen">
      <button 
        v-for="lang in availableLanguages" 
        :key="lang.code"
        @click="switchLanguage(lang.code)"
        class="language-option"
        :class="{ 'active': currentLanguage === lang.code }"
      >
        <span class="lang-name">{{ lang.name }}</span>
        <span class="lang-code">{{ lang.code.toUpperCase() }}</span>
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n';

export default {
  name: 'LanguageSwitcher',
  
  setup() {
    const { locale } = useI18n();
    const currentLanguage = computed(() => locale.value);
    const isOpen = ref(false);
    const dropdownButton = ref(null);
    
    const availableLanguages = [
      { code: 'en', name: 'English' },
      { code: 'ru', name: 'Русский' }
    ];
    
    const getCurrentLanguageName = computed(() => {
      const language = availableLanguages.find(lang => lang.code === currentLanguage.value);
      return language ? language.name : 'English';
    });
    
    function toggleDropdown() {
      isOpen.value = !isOpen.value;
    }
    
    function switchLanguage(langCode) {
      locale.value = langCode;
      localStorage.setItem('ustock-language', langCode);
      isOpen.value = false;
    }
    
    function handleClickOutside(event) {
      if (dropdownButton.value && !dropdownButton.value.contains(event.target) && isOpen.value) {
        isOpen.value = false;
      }
    }
    
    onMounted(() => {
      const savedLanguage = localStorage.getItem('ustock-language');
      if (savedLanguage) {
        locale.value = savedLanguage;
      }
      
      document.addEventListener('click', handleClickOutside);
    });
    
    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside);
    });
    
    return {
      currentLanguage,
      availableLanguages,
      isOpen,
      dropdownButton,
      getCurrentLanguageName,
      toggleDropdown,
      switchLanguage
    };
  }
};
</script>

<style lang="scss" scoped>
.language-switcher {
  position: relative;
  display: inline-block;
  
  .language-dropdown-button {
    display: flex;
    align-items: center;
    background-color: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.25);
    padding: 0.35rem 0.75rem;
    cursor: pointer;
    color: white;
    font-size: $font-size-sm;
    border-radius: $border-radius;
    transition: $transition-quick;
    font-weight: 500;
    
    &:hover {
      background-color: rgba(255, 255, 255, 0.25);
      border-color: rgba(255, 255, 255, 0.35);
    }
    
    .pi-globe {
      margin-right: 0.25rem;
      color: white;
    }
    
    .current-language {
      margin: 0 0.25rem;
      color: white;
    }
    
    .pi-chevron-down, 
    .pi-chevron-up {
      font-size: 0.7rem;
      transition: transform 0.2s ease;
    }
  }
  
  .language-dropdown {
    position: absolute;
    top: 100%;
    right: 0;
    margin-top: 0.25rem;
    min-width: 150px;
    background-color: white;
    border-radius: $border-radius;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    z-index: 1000;
    overflow: hidden;
    border: 1px solid rgba(0, 0, 0, 0.1);
    
    .language-option {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      padding: 0.5rem 0.75rem;
      text-align: left;
      background: none;
      border: none;
      cursor: pointer;
      transition: $transition-quick;
      
      &:hover {
        background-color: rgba($primary-color, 0.05);
      }
      
      &.active {
        background-color: rgba($primary-color, 0.1);
        font-weight: 500;
        
        .lang-name {
          color: $primary-color;
        }
      }
      
      .lang-name {
        color: #333;
        font-weight: 500;
      }
      
      .lang-code {
        color: #666;
        font-size: 0.7rem;
        opacity: 0.8;
      }
    }
  }
}
</style>