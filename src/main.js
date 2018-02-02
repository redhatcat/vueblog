// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import App from './App'
import router from './router'
import store from './store'

import BootstrapVue from 'bootstrap-vue'

import VueTimeago from 'vue-timeago'
import Prism from 'prismjs/prism.js'
import 'prismjs/themes/prism-tomorrow.css'
import 'font-awesome/css/font-awesome.min.css'
import 'simple-line-icons/css/simple-line-icons.css'

// Load any local javascript there may be
// This is typically where prism languages get added
import '@/local.css'
import '@/local.js'

Vue.use(BootstrapVue)
Vue.use(Vuex)
Vue.use(VueTimeago, {
  name: 'timeago', // component name, `timeago` by default
  locale: 'en-US',
  locales: {
    // you will need json-loader in webpack 1
    'en-US': require('vue-timeago/locales/en-US.json')
  }
})
Vue.use(Prism)

Vue.config.productionTip = false

store.dispatch('setAuthToken')
store.dispatch('renewAuthToken')

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  template: '<App/>',
  components: { App }
})
