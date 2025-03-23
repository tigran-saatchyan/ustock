import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import i18n from './i18n';

// PrimeVue imports
import PrimeVue from 'primevue/config';
import Ripple from 'primevue/ripple';
import Tooltip from 'primevue/tooltip';
import 'primevue/resources/themes/saga-orange/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';

const app = createApp(App);

app.use(store);
app.use(router);
app.use(i18n);
app.use(PrimeVue, { ripple: true });

// Register directives
app.directive('ripple', Ripple);
app.directive('tooltip', Tooltip);

app.mount('#app');