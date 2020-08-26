export default {
  CHECK_TOKEN: 'http://127.0.0.1:5000/user/check_token',
  install: (Vue) => {
    Vue.prototype.BASE_URL = () => {
      return 'http://127.0.0.1:5000'
      // '/apis'
    }
    // 登入
    Vue.prototype.LOGIN = () => {
      return Vue.prototype.BASE_URL() + '/user/login'
    }
    // 验证token
    Vue.prototype.CHECK_TOKEN = () => {
      return Vue.prototype.BASE_URL() + '/user/check_token'
    }
    // 查询所有用户
    Vue.prototype.FIND_ALL_USER = () => {
      return Vue.prototype.BASE_URL() + '/user/find_all_user'
    }
    // 批量拉黑
    Vue.prototype.BATCH_BLACKOUT = () => {
      return Vue.prototype.BASE_URL() + '/user/batch_blackout'
    }
    // 取消拉黑
    Vue.prototype.REMOVE_BLACKOUT = () => {
      return Vue.prototype.BASE_URL() + '/user/remove_blackout'
    }
    // 重置密码
    Vue.prototype.RESET_PASSWORD = () => {
      return Vue.prototype.BASE_URL() + '/user/reset_password'
    }
    // 根据用户ID修改用户信息
    Vue.prototype.EDIT_USER_BY_ID = () => {
      return Vue.prototype.BASE_URL() + '/user/edit_user_by_id'
    }
    // 添加用户信息
    Vue.prototype.ADD_USER = () => {
      return Vue.prototype.BASE_URL() + '/user/add_user'
    }
    // 批量导入用户时上传csv文件，解析后返回
    Vue.prototype.UPLOAD_USER_INFO_CSV = () => {
      return Vue.prototype.BASE_URL() + '/user/upload_user_info_csv'
    }
    // 根据解析的CSV数据进行用户导入
    Vue.prototype.IMPORT_USER_INFO = () => {
      return Vue.prototype.BASE_URL() + '/user/import_user_info'
    }
    // 下载导入用户的模板
    Vue.prototype.DOWNLOAD_IMPORT_USER_TEMPLATE = () => {
      return Vue.prototype.BASE_URL() + '/user/download_import_user_template'
    }
  }
}
