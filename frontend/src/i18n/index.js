import { createI18n } from 'vue-i18n';
import en from './locales/en.json';
import ru from './locales/ru.json';

// Create i18n instance
const i18n = createI18n({
  legacy: false, // Using Composition API
  locale: localStorage.getItem('ustock-language') || 'en', // Default language
  fallbackLocale: 'en', // Fallback language
  messages: {
    en,
    ru
  }
});

// Expose i18n globally for formatters and utilities
if (typeof window !== 'undefined') {
  window.i18n = i18n;
}

export default i18n;