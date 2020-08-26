<template>
  <div>
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card shadow="hover" class="mgb20" style="height:252px;">
          <div class="user-info">
            <img src="../../assets/img/img.jpg" class="user-avator" alt />
            <div class="user-info-cont">
              <div class="user-info-name">{{name}}</div>
              <div>{{role}}</div>
            </div>
          </div>
          <div class="user-info-list">
            当前浏览器时间：
            <span>{{localTime}}</span>
          </div>
        </el-card>
        <el-card shadow="hover" style="height:252px;">
          <div class="user-info-list">
            &#12288;&#12288;浏览器信息：
            <span>{{browserInfo}}</span>
          </div>
          <div class="user-info-list">
            &#12288;&#12288;&#12288;登录地点：
            <span>{{address}}</span>
          </div>
          <div class="user-info-list">
            &#12288;&#12288;&#12288;&#12288;登录IP：
            <span>{{ip}}</span>
          </div>
          <div class="user-info-list">
            &#12288;&#12288;当前用户名：
            <span>{{name}}</span>
          </div>
          <div class="user-info-list">
            &#12288;&#12288;&#12288;当前账号：
            <span>{{account}}</span>
          </div>
          <div class="user-info-list">
            &#12288;&#12288;&#12288;当前权限：
            <span>{{roleName}} ({{permissions}})</span>
          </div>
          <div class="user-info-list">
            &#12288;上次登入时间：
            <span>{{last_login_time}}</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="16">
        <el-row :gutter="20" class="mgb20">
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{padding: '0px'}">
              <div class="grid-content grid-con-1">
                <i class="el-icon-lx-people grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">欢迎使用</div>
                  <div></div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{padding: '0px'}">
              <div class="grid-content grid-con-2">
                <i class="el-icon-lx-notice grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">0</div>
                  <div>系统消息</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="8">
            <el-card shadow="hover" :body-style="{padding: '0px'}">
              <div class="grid-content grid-con-3">
                <i class="el-icon-lx-goods grid-con-icon"></i>
                <div class="grid-cont-right">
                  <div class="grid-num">0</div>
                  <div>数量</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-card shadow="hover" style="height:403px;">
          <div slot="header" class="clearfix">
            <span>待办事项</span>
            <el-button style="float: right; padding: 3px 0" type="text">添加</el-button>
          </div>
          <el-table :show-header="false" :data="todoList" style="width:100%;">
            <el-table-column width="40">
              <template slot-scope="scope">
                <el-checkbox v-model="scope.row.status"></el-checkbox>
              </template>
            </el-table-column>
            <el-table-column>
              <template slot-scope="scope">
                <div
                  class="todo-item"
                  :class="{'todo-item-del': scope.row.status}"
                >{{scope.row.title}}</div>
              </template>
            </el-table-column>
            <el-table-column width="60">
              <template>
                <i class="el-icon-edit"></i>
                <i class="el-icon-delete"></i>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Schart from 'vue-schart'
import { getCookie } from '../../assets/js/cookie'

export default {
  data () {
    return {
      name: getCookie('name'),
      todoList: [
        {
          title: '今天要---------localStorage.getItem(\'name\')',
          status: false
        },
        {
          title: '明天要---------localStorage.removeItem',
          status: true
        }
      ],
      ip: '',
      cid: '',
      localTime: '',
      address: '',
      browserInfo: '',
      account: getCookie('account'),
      roleName: getCookie('role'),
      permissions: getCookie('permissions'),
      last_login_time: getCookie('last_login_time')
    }
  },
  components: {
    Schart
  },
  computed: {
    role () {
      return this.name === 'admin' ? '超级管理员' : '普通用户'
    }
  },
  methods: {
    changeDate () {
      const now = new Date().getTime()
      this.data.forEach((item, index) => {
        const date = new Date(now - (6 - index) * 86400000)
        item.name = `${date.getFullYear()}/${date.getMonth() + 1}/${date.getDate()}`
      })
    },
    // 获取浏览器信息
    getBrowserInfo () {
      var agent = navigator.userAgent.toLowerCase()

      var regStrIE = /msie [\d.]+;/gi
      var regStrFF = /firefox\/[\d.]+/gi
      var regStrChrome = /chrome\/[\d.]+/gi
      var regStrSaf = /safari\/[\d.]+/gi

      // IE
      if (agent.indexOf('msie') > 0) {
        return agent.match(regStrIE)
      }

      // firefox
      if (agent.indexOf('firefox') > 0) {
        return agent.match(regStrFF)
      }

      // Chrome
      if (agent.indexOf('chrome') > 0) {
        return agent.match(regStrChrome)
      }

      // Safari
      if (agent.indexOf('safari') > 0 && agent.indexOf('chrome') < 0) {
        return agent.match(regStrSaf)
      }
    },
    // 获取各种需要的数据
    getShowInfo () {
      this.ip = sessionStorage.getItem('ip')
      this.cid = sessionStorage.getItem('cid')
      this.address = sessionStorage.getItem('address')
      this.browserInfo = this.getBrowserInfo()[0]
    },
    getLocalTime () {
      var dt = new Date()
      var timeStr = dt.getFullYear() + '年' + dt.getMonth() + '月' + dt.getDate() + '日 '
      timeStr += dt.getHours() + ':' + dt.getMinutes() + ':' + dt.getSeconds()
      this.localTime = timeStr
    }
  },
  created () {
    this.getShowInfo()
    window.setInterval(this.getLocalTime, 1000)
  }
}
</script>

<style scoped>
  .el-row {
    margin-bottom: 20px;
  }

  .grid-content {
    display: flex;
    align-items: center;
    height: 100px;
  }

  .grid-cont-right {
    flex: 1;
    text-align: center;
    font-size: 14px;
    color: #999;
  }

  .grid-num {
    font-size: 30px;
    font-weight: bold;
  }

  .grid-con-icon {
    font-size: 50px;
    width: 100px;
    height: 100px;
    text-align: center;
    line-height: 100px;
    color: #fff;
  }

  .grid-con-1 .grid-con-icon {
    background: rgb(45, 140, 240);
  }

  .grid-con-1 .grid-num {
    color: rgb(45, 140, 240);
  }

  .grid-con-2 .grid-con-icon {
    background: rgb(100, 213, 114);
  }

  .grid-con-2 .grid-num {
    color: rgb(45, 140, 240);
  }

  .grid-con-3 .grid-con-icon {
    background: rgb(242, 94, 67);
  }

  .grid-con-3 .grid-num {
    color: rgb(242, 94, 67);
  }

  .user-info {
    display: flex;
    align-items: center;
    padding-bottom: 20px;
    border-bottom: 2px solid #ccc;
    margin-bottom: 20px;
  }

  .user-avator {
    width: 120px;
    height: 120px;
    border-radius: 50%;
  }

  .user-info-cont {
    padding-left: 50px;
    flex: 1;
    font-size: 14px;
    color: #999;
  }

  .user-info-cont div:first-child {
    font-size: 30px;
    color: #222;
  }

  .user-info-list {
    font-size: 14px;
    color: #999;
    line-height: 25px;
  }

  .user-info-list span {
    margin-left: 70px;
  }

  .mgb20 {
    margin-bottom: 20px;
  }

  .todo-item {
    font-size: 14px;
  }

  .todo-item-del {
    text-decoration: line-through;
    color: #999;
  }

  .schart {
    width: 100%;
    height: 300px;
  }
</style>
