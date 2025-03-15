import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

// PrimeVue imports
import PrimeVue from 'primevue/config';
import Ripple from 'primevue/ripple';
import 'primevue/resources/themes/lara-light-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';

const app = createApp(App);

app.use(store);
app.use(router);
app.use(PrimeVue, { ripple: true });

// Register directives
app.directive('ripple', Ripple);

app.mount('#app');