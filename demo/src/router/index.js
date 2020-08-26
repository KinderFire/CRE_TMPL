/* eslint-disable */
import Vue from 'vue'
import Router from 'vue-router'
import { delCookie, getCookie } from '@/assets/js/cookie'
import Login from '@/views/user/Login'
import Index from '@/views/main/Index'
import UploadShfeExcel from '@/views/upload/UploadShfeExcel'
import VUE403 from '@/views/status/403'
import VUE404 from '@/views/status/404'
import UserManage from '@/views/admin/UserManage'
import Home from '@/assets/common/Home'
import UserJs from '@/flask/user'
import axios from 'axios'
Vue.use(Router)

// export default new Router({
var router = new Router({
  mode: 'history',
  fallback: false,
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: { title: '登录' }
    },{
      path: '/',
      redirect: '/index'
    },
    {
      path: '/',
      component: Home,
      meta: { title: '自述文件' },
      children: [
        {
          path: '/index',
          name: 'Index',
          component: Index,
          meta: { title: '系统首页' }
        },{
          path: '/uploadShfeExcel',
          name: 'UploadShfeExcel',
          component: UploadShfeExcel,
          meta: { title: '上期所文件上传' }
        },{
          path: '/403',
          component: VUE403,
          meta: { title: '403' }
        },{
          path: '/404',
          component: VUE404,
          meta: { title: '404' }
        },{
          path: '/userManage',
          component: UserManage,
          meta: { title: '用户管理' }
        }
      ]
    },
    {
      path: '*',
      redirect: '/404'
    }
  ]
})

var Permission = {
  'Level_1': 1, // 浏览
  'Level_2': 3, // 评论
  'Level_3': 7, // 添加数据
  'Level_4': 15, // 修改数据
  'Level_5': 31 // 管理
}

var routerConfig = {
  '/login': {
    'role': Permission['Level_1'],
    'login': false
  },
  '/index': {
    'role': Permission['Level_1'],
    'login': true
  },
  '/403': {
    'role': Permission['Level_1'],
    'login': true
  },
  '/404': {
    'role': Permission['Level_1'],
    'login': true
  },
  '/uploadShfeExcel': {
    'role': Permission['Level_3'],
    'login': true
  },
  '/userManage': {
    'role': Permission['Level_5'],
    'login': true
  }
}

var DelCookie = () => {
  delCookie('account')
  delCookie('user_id')
  delCookie('name')
  delCookie('token')
  delCookie('role')
  delCookie('role_id')
  delCookie('permissions')
}

var CheckLogin = () => {
  var flag = true
  if (getCookie('user_id') === '') {
    flag = false
  }
  if (getCookie('role_id') === '') {
    flag = false
  }
  if (getCookie('permissions') === '') {
    flag = false
  }
  if (getCookie('token') === '') {
    flag = false
  }
  if (getCookie('name') === '') {
    flag = false
  }
  if (getCookie('account') === '') {
    flag = false
  }
  if (getCookie('role') === '') {
    flag = false
  }
  return flag
}

router.beforeEach(function (to, from, next) {
  var nextPath = to.path
  if (nextPath === '' || nextPath === '/' || nextPath === '//') {
    nextPath = '/index'
  }
  if (routerConfig.hasOwnProperty(nextPath) === false) {
    console.log(nextPath)
    nextPath = '/login'
  }
  var cfg = routerConfig[nextPath]
  var flag = CheckLogin() // 判断是否登入
  if (cfg['login']) {
    if (!flag) {
      DelCookie()
      next({path: '/login'})
    }
    if (!Permission.hasOwnProperty(getCookie('role'))) {
      console.log(getCookie('role'))
      DelCookie()
      next({path: '/login'})
    }
    if (parseInt(getCookie('permissions')) !== parseInt(Permission[getCookie('role')])) {
      DelCookie()
      next({path: '/login'})
    }
    const params = new URLSearchParams()
    params.append('token', getCookie('token'))
    params.append('user_id', getCookie('user_id'))
    params.append('role_id', getCookie('role_id'))
    params.append('last_login_time', getCookie('last_login_time'))
    var URL = UserJs.CHECK_TOKEN
    axios.post(URL, params).then((res) => {
      if (res.data.status === '200') {
        // 这里检查 cfg 中的权限是否足够，不够跳转到index
        next()
      } else {
        DelCookie()
        next({path: '/login'})
      }
    })
  } else {
    if (flag) {
      next({path: '/'})
    } else {
      next()
    }
  }
})
export default router
