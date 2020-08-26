// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import axios from 'axios'
import VueAxios from 'vue-axios'
import Vue from 'vue'
// import $ from 'jquery'
// import 'bootstrap'
import './assets/css/bootstrap.min.css'
import './assets/main/css/style.css'
import './assets/main/css/theme.css'
import './assets/main/css/fonts.css'

import './assets/js/bootstrap.min'
import './assets/js/jquery-3.3.1'
// import './assets/js/bootsnav'
import './assets/css/toastr.css'
import toastr from './assets/js/toastr'
// import './assets/css/sweetalert2.css'
// import './assets/css/bootsnav.css'
// import './assets/js/sweetalert2'
// import './assets/css/bootstrap-datetimepicker.min.css'
// import './assets/js/bootstrap-datetimepicker'
// import './assets/js/bootstrap-datetimepicker.zh-CN'
// import 'url-search-params-polyfill'
// import './assets/css/font-awesome.min.css'
// import './assets/css/bootstrap-select.min.css'
// import './assets/js/bootstrap-select.min'
// import './assets/css/select2.css';
// import './assets/js/select2';
// import './assets/css/ion.rangeSlider.css'
// import './assets/js/ion.rangeSlider'
import echarts from 'echarts'
// import htmlToPdf from './assets/js/htmlToPdf'
// import 'bootstrap-suggest-plugin'; // 搜索补全
// import './assets/js/bootstrap-suggest'
// import './assets/css/summernote.css'
// import './assets/js/summernote'
// import './assets/js/summernote-zh-CN'
// import Velocity from 'velocity-animate'
// import jspdf from 'jspdf'
// import Print from 'vue-print-nb'

import ElementUI from 'element-ui'
import VueI18n from 'vue-i18n'
import { messages } from './assets/common/i18n'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/css/icon.css'
import './assets/common/directives'
import 'babel-polyfill'

import base from './flask/base'
import user from './flask/user'

import App from './App'
import router from './router'

import { delCookie } from './assets/js/cookie'

Vue.use(VueAxios, axios)
Vue.use(base)
Vue.use(user)
Vue.use(VueI18n)

Vue.use(ElementUI, {
  size: 'small'
})
const i18n = new VueI18n({
  locale: 'zh',
  messages
})

Vue.config.productionTip = false
Vue.prototype.$echarts = echarts

axios.interceptors.response.use(function (response) { //eslint-disable-line
  var status = response.data.status
  if (status === '40100') {
    toastr.error(response.data.message)
    delCookie('account')
    delCookie('user_id')
    delCookie('name')
    delCookie('token')
    delCookie('role')
    delCookie('role_id')
    delCookie('permissions')
    setTimeout(function (){ location.reload(); }, 2000); //eslint-disable-line
  } else if (status === '20300') {
    toastr.error(response.data.message)
  } else {
    return response
  }
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  i18n,
  components: { App },
  template: '<App/>'
})
