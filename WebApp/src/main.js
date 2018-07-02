// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import App from './App'
import router from './router'
// import VueResource from 'vue-resource'
import axios from 'axios'
import VueAxios from 'vue-axios'
import VueGoodTable from 'vue-good-table'
import * as VueGoogleMaps from 'vue2-google-maps'
import VueCharts from 'vue-charts'
import VeeValidate from 'vee-validate'
import VueFire from 'vuefire';
import VueSessionStorage from 'vue-sessionstorage'

const config = {
  errorBagName: 'errors', // change if property conflicts.
  fieldsBagName: 'inputs ', //Default is fields
  delay: 0, 
  locale: 'en', 
  dictionary: null, 
  strict: true, 
  enableAutoClasses: false, 
  classNames: {
  touched: 'touched', // the control has been blurred
  untouched: 'untouched', // the control hasn't been blurred
  valid: 'valid', // model is valid
  invalid: 'invalid', // model is invalid
  pristine: 'pristine', // control has not been interacted with
  dirty: 'dirty' // control has been interacted with
  },
  events: 'input|blur',
  inject: true
  };
Vue.use(VeeValidate,config)

Vue.use(VueFire);
Vue.use(VueCharts)
Vue.use(BootstrapVue)
Vue.use(VueSessionStorage)
Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyAyCEzPjAsjYJhqnH3Dug9FyWrw6QXXmhs',
    v: '3.30'
    // libraries: 'places', //// If you need to use place input
  }
})
Vue.use(VueGoodTable)
Vue.use(VueAxios, axios)
// Vue.use(VueResource)
Vue.config.productionTip = false

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    // let isAdmin = sessionStorage.getItem('isAdmin')
    let isLogin = sessionStorage.getItem('isLogin') === 'true'
    // let isAdmin = sessionStorage.getItem('isAdmin') === 'true'
    // console.log(auth)
    if (!isLogin) {
      next({
        path: '/pages/login'
        // query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next() // make sure to always call next()!
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {
    App,
  }
})
