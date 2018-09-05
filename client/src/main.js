// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import App from './App';
import router from './router';
// eslint-disable-next-line
import moment from 'moment-timezone';
// eslint-disable-next-line
import VueMoment from 'vue-moment';

moment().tz('Asia/Tokyo').format();

Vue.config.productionTip = false;

Vue.use(BootstrapVue);
Vue.use(VueMoment, { moment });

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
