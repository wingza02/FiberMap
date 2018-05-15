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
Vue.use(VeeValidate)
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
    App
  }
})
