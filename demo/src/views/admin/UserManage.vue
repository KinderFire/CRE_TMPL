<template>
  <div class="userManage">
    <!--最顶上显示条-->
    <div class="crumbs">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item>
          <i class="el-icon-lx-cascades"></i> 用户管理
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!--主要内容-->
    <div class="container">
      <!--搜索部分-->
      <div class="handle-box">
        <el-button type="primary" icon="el-icon-lock" class="handle-del mr10" @click="delAllSelection">批量拉黑</el-button>
        <el-select placeholder="用户权限" class="handle-select mr10" v-model="query.roleName" @change="handleRoleChange">
          <el-option key="0" label="所有" value=""></el-option>
          <el-option key="1" label="一级权限" value="Level_1"></el-option>
          <el-option key="2" label="二级权限" value="Level_2"></el-option>
          <el-option key="3" label="三级权限" value="Level_3"></el-option>
          <el-option key="4" label="四级权限" value="Level_4"></el-option>
          <el-option key="5" label="五级权限" value="Level_5"></el-option>
          <el-option key="6" label="拉黑" value="Level_0"></el-option>
        </el-select>
        <el-input v-model="query.keyword" placeholder="用户名或账号" class="handle-input mr10"></el-input>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
        <el-button type="primary" icon="el-icon-lx-friendadd" class="handle-del mr10" style="margin-left: 100px;" @click="showAddUser">添加用户</el-button>
        <el-button type="primary" icon="el-icon-lx-addressbook" class="handle-del mr10" @click="showBatchAddUser">批量导入</el-button>
      </div>
      <!--表格部分-->
      <el-table :data="tableData" border class="table" ref="multipleTable" header-cell-class-name="table-header"
        @selection-change="handleSelectionChange" >
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column prop="id" label="ID" width="55" align="center"></el-table-column>
        <el-table-column label="姓名" width="180" align="center">
          <template slot-scope="scope">
            <el-popover trigger="hover" placement="top">
              <p>&#12288;&#12288;注册时间: &#12288;{{ scope.row.member_since }}</p>
              <p>最后登入时间: &#12288;{{ scope.row.last_login_time }}</p>
              <div slot="reference" class="name-wrapper">
                <el-tag size="medium">{{ scope.row.name }}</el-tag>
              </div>
            </el-popover>
          </template>
        </el-table-column>
        <el-table-column prop="account" label="账号" align="center"></el-table-column>
        <el-table-column prop="role_name" label="权限等级" align="center"></el-table-column>
        <el-table-column prop="confirmed" label="当前状态" align="center"></el-table-column>
        <el-table-column label="其他" width="180" align="center">
          <template slot-scope="scope">
            <el-button type="text" v-if="scope.row.confirmed !== '正常'" icon="el-icon-lx-profile" @click="handleUnseal(scope.$index, scope.row)">恢复正常</el-button>
            <el-button type="text" icon="el-icon-lx-timefill" @click="handleRestPassword(scope.$index, scope.row)">密码重置</el-button>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.$index, scope.row)" >编辑</el-button>
            <el-button type="text" v-if="false" icon="el-icon-delete" class="red" @click="handleDelete(scope.$index, scope.row)" >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <!--分页-->
      <div class="pagination">
        <el-pagination background layout="total, prev, pager, next"
                       :current-page="query.pageIndex" :page-size="query.pageSize" :total="pageTotal"
          @current-change="handlePageChange"></el-pagination>
      </div>
    </div>
    <!--编辑弹窗-->
    <el-dialog title="编辑" :visible.sync="editVisible" width="25%" style="text-align: center">
      <el-form ref="form" :model="editForm" label-width="70px">
        <el-form-item label="用户名">
          <el-input v-model="editForm.name" style="width:200px;"></el-input>
        </el-form-item>
        <el-form-item label="账号">
          <el-input v-model="editForm.account" style="width:200px;"></el-input>
        </el-form-item>
        <el-form-item label="权限">
          <el-select placeholder="用户权限" class="handle-select mr10" v-model="editForm.role_name" style="width:200px;">
            <el-option key="1" label="一级权限" value="Level_1"></el-option>
            <el-option key="2" label="二级权限" value="Level_2"></el-option>
            <el-option key="3" label="三级权限" value="Level_3"></el-option>
            <el-option key="4" label="四级权限" value="Level_4"></el-option>
            <el-option key="5" label="五级权限" value="Level_5"></el-option>
          </el-select>
        </el-form-item>
        <!--密码默认账号加上@ddqh-->
      </el-form>
      <span slot="footer" class="dialog-footer">
          <el-button @click="editVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveEdit">确 定</el-button>
      </span>
    </el-dialog>
    <!--添加弹窗-->
    <el-dialog title="新增用户" :visible.sync="addVisible" width="25%" style="text-align: center">
      <el-form ref="form" :model="addForm" label-width="70px">
        <el-form-item label="用户名">
          <el-input v-model="addForm.name" style="width:200px;"></el-input>
        </el-form-item>
        <el-form-item label="账号">
          <el-input v-model="addForm.account" style="width:200px;"></el-input>
        </el-form-item>
        <el-form-item label="权限">
          <el-select placeholder="用户权限" class="handle-select mr10" v-model="addForm.role_name" style="width:200px;">
            <el-option key="1" label="一级权限" value="Level_1"></el-option>
            <el-option key="2" label="二级权限" value="Level_2"></el-option>
            <el-option key="3" label="三级权限" value="Level_3"></el-option>
            <el-option key="4" label="四级权限" value="Level_4"></el-option>
            <el-option key="5" label="五级权限" value="Level_5"></el-option>
          </el-select>
        </el-form-item>
        <!--密码默认账号加上@ddqh-->
      </el-form>
      <span slot="footer" class="dialog-footer">
          <el-button @click="addVisible = false">取 消</el-button>
          <el-button type="primary" @click="addUser">确 定</el-button>
      </span>
    </el-dialog>
    <!--批量导入用户弹框-->
    <el-dialog title="批量导入用户" :visible.sync="batchAddVisible" width="30%" style="text-align: center;">
      <div style="margin: -20px 0 0 30px;text-align:left;">
        <p>下载模板</p>
        <p style="color: #A1A1A1;font-size:12px;margin: 10px 0;">为提高导入的成功率，请下载并使用系统提供的模板。</p>
        <button style="width:100px;height:30px;background:#F5A400;color: #fff;border-radius:2px;border:none;" @click="downloadImportUserTemplate">下载模板</button>
      </div>
      <span slot="footer" class="dialog-footer">
          <el-button type="primary" @click="gotoImportInterface">开始导入</el-button>
      </span>
    </el-dialog>
    <!--批量导入用户主界面-->
    <el-dialog title="批量导入用户" :visible.sync="batchAddNextVisible" width="35%" style="text-align: center;">
      <div style="margin: -20px 0 0 30px;text-align:left;">
        <el-upload class="upload-demo" ref="upload" action="#" :http-request="httpRequest"
          :on-preview="handlePreview" :on-remove="handleRemove" :file-list="fileList" :auto-upload="false"
          :on-exceed="handleExceed" :limit="1" accept=".csv" :on-change = "handleChangeUpload" >
          <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
          <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">解析文件</el-button>
          <div slot="tip" class="el-upload__tip">只能上传CSV文件，确认导入后会覆盖原有数据</div>
        </el-upload>
      </div>
      <el-table :data="uploadData" style="width: 100%;margin-top: 20px;" max-height="250" v-show="uploadTableVisible">
        <el-table-column prop="username" label="姓名" width="120"> </el-table-column>
        <el-table-column prop="account" label="账号" width="120"> </el-table-column>
        <el-table-column prop="role_name" label="权限名称" width="120"> </el-table-column>
        <el-table-column fixed="right" label="操作" width="120">
          <template slot-scope="scope">
            <el-button @click.native.prevent="deleteRow(scope.$index, uploadData)" type="text" size="small"> 移除 </el-button>
          </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="batchAddVisible = false;batchAddNextVisible = false">取 消</el-button>
        <el-button type="primary" @click="confirmImport">确认导入</el-button>
      </span>
    </el-dialog>
    <!---->
  </div>
</template>

<script>
import { getCookie } from '../../assets/js/cookie'

export default {
  data () {
    return {
      query: {
        roleName: '',
        keyword: '',
        pageIndex: 1, // 当前页
        pageSize: 10 // 一页多少行
      },
      tableData: [],
      multipleSelection: [],
      delList: [],
      addVisible: false,
      editVisible: false,
      batchAddVisible: false,
      batchAddNextVisible: false,
      pageTotal: 0,
      editForm: {},
      addForm: {},
      fileList: [],
      uploadData: [],
      uploadTableVisible: false
    }
  },
  methods: {
    // 获取 easy-mock 的模拟数据
    getData () {
      const params = new URLSearchParams()
      params.append('keyword', this.query.keyword)
      params.append('filter_role', this.query.roleName)
      params.append('pageIndex', this.query.pageIndex)
      params.append('pageSize', this.query.pageSize)
      params.append('user_id', getCookie('user_id'))
      params.append('token', getCookie('token'))
      var URL = this.FIND_ALL_USER()
      this.axios.post(URL, params).then((res) => {
        if (res.data.status === '200') {
          this.tableData = res.data.lis
          this.pageTotal = res.data.total
        } else {
          this.$message.error('查询所有用户出错！')
          console.log('find all user error !!')
          return false
        }
      })
    },
    // 选择权限后触发刷新页面
    handleRoleChange () {
      this.getData()
    },
    // 触发搜索按钮
    handleSearch () {
      this.$set(this.query, 'pageIndex', 1)
      this.getData()
    },
    // 删除操作 -- 用户不作删除
    handleDelete (index, row) {
      // 二次确认删除
      this.$confirm('确定要删除吗？', '提示', {
        type: 'warning'
      }).then(() => {
        console.log(index, row)
        this.$message.success('删除成功')
        // this.tableData.splice(index, 1)
      }).catch(() => {})
    },
    // 多选操作
    handleSelectionChange (val) {
      this.multipleSelection = val
      // console.log('handleSelectionChange: ', this.multipleSelection)
    },
    // 批量拉黑
    delAllSelection () {
      if (this.multipleSelection.length < 1) {
        return
      }
      var idList = []
      for (var i = 0; i < this.multipleSelection.length; i += 1) {
        idList.push(this.multipleSelection[i].id)
      }
      const params = new URLSearchParams()
      params.append('user_id', getCookie('user_id'))
      params.append('token', getCookie('token'))
      params.append('id_list', idList)
      var URL = this.BATCH_BLACKOUT()
      this.axios.post(URL, params).then((res) => {
        if (res.data.status === '200') {
          this.$message.success(res.data.message)
          this.getData()
        } else {
          this.$message.error(res.data.message)
          console.log('batch blackout error !!')
          return false
        }
      })
    },
    // 编辑操作
    handleEdit (index, row) {
      this.editVisible = true
      this.editForm.id = row.id
      this.editForm.name = row.name
      this.editForm.account = row.account
      this.editForm.role_name = row.role_name
    },
    // 解除用户的拉黑状态
    handleUnseal (index, row) {
      const params = new URLSearchParams()
      params.append('user_id', getCookie('user_id'))
      params.append('token', getCookie('token'))
      params.append('choose_id', row.id)
      var URL = this.REMOVE_BLACKOUT()
      this.axios.post(URL, params).then((res) => {
        if (res.data.status === '200') {
          this.$message.success(res.data.message)
          this.getData()
        } else {
          this.$message.error(res.data.message)
          console.log('remove blackout error !!')
          return false
        }
      })
    },
    // 重置密码
    handleRestPassword (index, row) {
      this.$confirm('此操作将重置用户' + row.name + '的密码, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const params = new URLSearchParams()
        params.append('user_id', getCookie('user_id'))
        params.append('token', getCookie('token'))
        params.append('choose_id', row.id)
        var URL = this.RESET_PASSWORD()
        this.axios.post(URL, params).then((res) => {
          if (res.data.status === '200') {
            this.$message.success(res.data.message)
          } else {
            this.$message.error(res.data.message)
            console.log('reset user password error !!')
            return false
          }
        })
      }).catch(() => {
        this.$message.success('已取消')
      })
    },
    // 保存编辑
    saveEdit () {
      this.$confirm('此操作将根据编辑的内容修改用户ID为' + this.editForm.id + '的用户信息, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.editVisible = false
        const params = new URLSearchParams()
        params.append('user_id', getCookie('user_id'))
        params.append('token', getCookie('token'))
        params.append('edit_id', this.editForm.id)
        params.append('edit_name', this.editForm.name)
        params.append('edit_account', this.editForm.account)
        params.append('edit_role_name', this.editForm.role_name)
        var URL = this.EDIT_USER_BY_ID()
        this.axios.post(URL, params).then((res) => {
          if (res.data.status === '200') {
            this.$message.success(res.data.message)
          } else {
            this.$message.error(res.data.message)
            console.log('remove blackout error !!')
            console.log(res.data.error)
            return false
          }
        })
      }).catch(() => {
        this.$message.success('已取消')
      })
    },
    // 分页导航
    handlePageChange (val) {
      this.$set(this.query, 'pageIndex', val)
      this.getData()
    },
    // 打开添加用户界面
    showAddUser () {
      this.addVisible = true
    },
    // 打开批量导入用户界面
    showBatchAddUser () {
      this.batchAddVisible = true
    },
    // 添加用户
    addUser () {
      this.$confirm('此操作将根据您所填写的内容添加新用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.addVisible = false
        const params = new URLSearchParams()
        params.append('user_id', getCookie('user_id'))
        params.append('token', getCookie('token'))
        params.append('add_name', this.addForm.name)
        params.append('add_account', this.addForm.account)
        params.append('add_role_name', this.addForm.role_name)
        var URL = this.ADD_USER()
        this.axios.post(URL, params).then((res) => {
          if (res.data.status === '200') {
            this.$message.success(res.data.message)
            this.addForm = {}
            this.getData()
          } else {
            this.$message.error(res.data.message)
            console.log('add user error !!')
            console.log(res.data.error)
            return false
          }
        })
      }).catch(() => {
        this.$message.success('已取消')
      })
    },
    // 开始进入到导入界面
    gotoImportInterface () {
      this.batchAddVisible = false
      this.batchAddNextVisible = true
      this.uploadTableVisible = false
    },
    // 上传文件配置-解析文件
    submitUpload () {
      if (this.fileList.length < 1) {
        this.$message.warning(`请选择要导入的文件!`)
        return
      }
      var file = this.fileList[0].raw
      if (file) {
        var data = new FormData()
        data.append('file', file)
        const headers = { headers: { 'Content-Type': 'multipart/form-data' } }
        this.axios.post(this.UPLOAD_USER_INFO_CSV(), data, headers).then((res) => {
          if (res.data.status === '200') {
            this.uploadData = res.data.list
            this.uploadTableVisible = true
            // this.$message.success(res.data.message)
          } else {
            this.$message.error(res.data.message)
            console.log(res.data.error)
          }
        })
      } else {
        this.$message.warning(`文件不存在!`)
      }
    },
    // 上传csv文件后生成的数据表中的移除列
    deleteRow (index, rows) {
      rows.splice(index, 1)
    },
    httpRequest () {},
    // 上传文件配置-删除时调用
    handleRemove (file, fileList) {
      this.fileList = fileList
    },
    // 上传文件配置-选择列表文件时调用
    handlePreview (file) {
      // console.log(file)
    },
    // 上传文件配置-限制上传
    handleExceed (files, fileList) {
      this.$message.warning(`当前限制选择 1 个文件，请删除后继续上传`)
    },
    // 上传文件选择文件后触发
    handleChangeUpload (files, fileList) {
      this.fileList = fileList
    },
    // 确认导入
    confirmImport () {
      this.$confirm('此操作将覆盖原有用户数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.addVisible = false
        const params = new URLSearchParams()
        params.append('user_id', getCookie('user_id'))
        params.append('token', getCookie('token'))
        params.append('upload_data', JSON.stringify(this.uploadData))
        var URL = this.IMPORT_USER_INFO()
        this.axios.post(URL, params).then((res) => {
          if (res.data.status === '200') {
            this.$message.success(res.data.message)
          } else {
            this.$message.error(res.data.message)
            console.log('import user info error !!')
            console.log(res.data.error)
            return false
          }
        })
      }).catch(() => {
        this.$message.success('已取消')
      })
    },
    // 下载导入用户的模板
    downloadImportUserTemplate () {
      var URL = this.DOWNLOAD_IMPORT_USER_TEMPLATE()
      const params = new URLSearchParams()
      params.append('user_id', getCookie('user_id'))
      params.append('token', getCookie('token'))
      this.axios.post(URL, params, { responseType: 'arraybuffer' }).then((res) => {
        var blob = new Blob([res.data], { type: res.headers['content-type'] })
        var link = document.createElement('a')
        link.href = window.URL.createObjectURL(blob)
        link.download = '用户导入模板.csv'
        link.click()
      })
    }
  },
  created () {
    this.getData()
  },
  mounted () {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import '../../../static/H/css/label.css';

  h1, h2 {
    font-weight: normal;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: block;
    margin: 0 10px;
  }
  a {
    color: #42b983;
  }
  .handle-box {
    margin-bottom: 20px;
  }

  .handle-select {
    width: 120px;
  }

  .handle-input {
    width: 300px;
    display: inline-block;
  }
  .table {
    width: 100%;
    font-size: 14px;
  }
  .red {
    color: #ff0000;
  }
  .mr10 {
    margin-right: 10px;
  }
  .table-td-thumb {
    display: block;
    margin: auto;
    width: 40px;
    height: 40px;
  }
</style>
