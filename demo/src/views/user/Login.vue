<template>
  <div class="login-wrap">
    <div class="ms-login">
      <div class="ms-title">后台管理系统</div>
      <el-form :model="param" :rules="rules" ref="login" label-width="0px" class="ms-content">
        <el-form-item prop="username">
          <el-input v-model="param.username" placeholder="username">
            <el-button slot="prepend" icon="el-icon-lx-people"></el-button>
          </el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            type="password"
            placeholder="password"
            v-model="param.password"
            @keyup.enter.native="submitForm()"
          >
            <el-button slot="prepend" icon="el-icon-lx-lock"></el-button>
          </el-input>
        </el-form-item>
        <div class="login-btn">
          <el-button type="primary" @click="submitForm()">登录</el-button>
        </div>
        <p class="login-tips">Tips : 用户名和密码为工号和工号@ddqh。</p>
      </el-form>
    </div>
  </div>
</template>

<script>
import { setCookie } from '../../assets/js/cookie'

export default {
  data: () => {
    return {
      param: {
        username: '',
        password: ''
      },
      rules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      }
    }
  },
  methods: {
    submitForm () {
      this.$refs.login.validate(valid => {
        if (valid) {
          const params = new URLSearchParams()
          params.append('account', this.param.username)
          params.append('password', this.param.password)
          var URL = this.LOGIN()
          this.axios.post(URL, params).then((res) => {
            if (res.data.status === '200') {
              setCookie('account', res.data.account)
              setCookie('user_id', res.data.id)
              setCookie('name', res.data.name)
              setCookie('permissions', res.data.permissions)
              setCookie('role', res.data.role)
              setCookie('role_id', res.data.role_id)
              setCookie('token', res.data.token)
              setCookie('last_login_time', res.data.last_login_time)
              setTimeout(() => {
                this.$message.success('登录成功')
                this.$router.push({ path: this.INDEX_PAGE() })
                localStorage.setItem('ms_username', this.param.username)
                //                this.$router.push('/')
              }, 200)
            } else {
              this.$message.error(res.data.message)
              console.log('error submit!!')
              return false
            }
          })
        } else {
          this.$message.error('请输入账号和密码')
          console.log('error submit!!')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
  .login-wrap {
    position: relative;
    width: 100%;
    height: 100%;
    background-image: url(../../assets/img/login-bg.jpg);
    background-size: 100%;
  }
  .ms-title {
    width: 100%;
    line-height: 50px;
    text-align: center;
    font-size: 20px;
    color: #fff;
    border-bottom: 1px solid #ddd;
  }
  .ms-login {
    position: absolute;
    left: 50%;
    top: 50%;
    width: 350px;
    margin: -190px 0 0 -175px;
    border-radius: 5px;
    background: rgba(255, 255, 255, 0.3);
    overflow: hidden;
  }
  .ms-content {
    padding: 30px 30px;
  }
  .login-btn {
    text-align: center;
  }
  .login-btn button {
    width: 100%;
    height: 36px;
    margin-bottom: 10px;
  }
  .login-tips {
    font-size: 12px;
    line-height: 30px;
    color: #fff;
  }
</style>
