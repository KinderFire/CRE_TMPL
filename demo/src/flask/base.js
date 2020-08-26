export default {
  install: (Vue) => {
    Vue.prototype.BASE_URL = () => {
      return 'http://127.0.0.1:5000'
      // return '/apis'
    }
    Vue.prototype.INDEX_PAGE = () => {
      return '/index'
    }
  }
}
