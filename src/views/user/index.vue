<template>
  <div class="app-container">
    <!-- 添加用户信息按钮 -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" icon="el-icon-plus" size="mini" @click="handleAdd">新增</el-button>
      </el-col>
    </el-row>
    <!--用户信息列表 -->
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column prop="id" label="序号" width="150" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="phonenumber" label="电话号码" />
      <el-table-column prop="email" label="电子邮箱" />
      <el-table-column prop="role" label="角色" />
      <el-table-column label="操作" width="300" align="center">
        <template slot-scope="scope">
          <el-button size="mini" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
          <el-button size="mini" @click="handlecz(scope.$index, scope.row)">重置</el-button>
          <el-button size="mini" type="danger" @click="handleDe(scope.$index, scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog
      title="提示"
      :visible.sync="centerDialogVisible1"
      width="30%"
      center>
      <span>确认操作</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="centerDialogVisible1 = false">取 消</el-button>
        <el-button type="primary" @click="save1">确 定</el-button>
      </span>
    </el-dialog>
    <!--添加用户信息表单-->
    <el-dialog :title="dialogTitle" :visible.sync="centerDialogVisible" width="50%" center>
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="电话号码">
          <el-input v-model="form.phonenumber" />
        </el-form-item>
        <el-form-item label="电子邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role" clearable placeholder="角色">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
        </el-form-item>

      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="cancel">取 消</el-button>
        <el-button type="primary" @click="save">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import { createUserInfo,
  getUsersInfo,
  UpdateUserInfoById,
  DeleteUserInfoById } from '@/api/username'

export default {
  data() {
    return {
      tableData: [], // 页面表格数据,即作者信息列表
      centerDialogVisible: false, // 用于控制添加与编辑作者信息表单组件是否显示
      centerDialogVisible1: false,
      form: { // 用户信息
        id: 0,
        username: '',
        phonenumber: '',
        email:'',
        role: []
      },
      options: [{
        value: 'admin',
        label: 'admin'
      }, {
        value: 'editor',
        label: 'editor'
      },]
    }
  },
  mounted() {
    this.getUserList()
  },
  methods: {
    // 添加按钮事件
    handleAdd() {
      this.dailogTitle='添加用户信息'
      this.centerDialogVisible = true
      this.title = '添加用户信息'
    },
    handleEdit(index, row) {
      this.centerDialogVisible = true
      this.title = '编辑用户信息'
      this.dailogTitle='编辑用户信息'
      this.form = row
    },
    handleRe(){
      UpdateUserInfoById(this.form.id, this.form)
        .then(res => {
          if (res.code === 'success') {
            this.$message.success('重置成功')
            this.getUserList()
          } else {
            this.$message.error('重置失败')
          }
        })
        .catch(err => {
          this.$message.error('服务端异常，更新失败。')
        })
    },
    handleDelete() {
      const auhtorId = this.form.id
      DeleteUserInfoById(auhtorId)
        .then(res => {
          if (res.code === 'success') {
            this.$message.success('删除成功')
            this.getUserList()
          } else {
            this.$message.error('删除失败')
          }
        })
        .catch(err => {
          this.$message.error('删除失败')
        })
    },
    handleDe(index, row){
      this.form=row
      this.title='删除'
      this.centerDialogVisible1 = true
    },
    handlecz(index,row){
      this.form=row
      this.form.password='123456'
      this.title='重置'
      this.centerDialogVisible1 = true
    },
    save() {
      if (this.title === '添加用户信息') {
        this.handleCreate()
      }
      if (this.title === '编辑用户信息') {
        this.handleUpdate()
      }
      this.centerDialogVisible = false

    },
    save1(){
      if(this.title==='重置'){
        this.handleRe()
      }
      if(this.title==='删除'){
        this.handleDelete()
      }
      this.centerDialogVisible1 = false
    },
    // 弹窗中的取消按钮事件
    cancel() {
      this.centerDialogVisible = false
      this.reset()
    },
    // 重置表单数据
    reset() {
      this.form = {
        username: '',
        password: '',
        role: []
      }
    },
    handleCreate() {
      this.centerDialogVisible = false
      // console.log('tianjia')
      createUserInfo({
        username: this.form.username,
        password: '123456',
        phonenumber:this.form.phonenumber,
        email:this.form.email,
        role: this.form.role
      })
        .then(res => {
          console.log(res)
          if (res.code === 'success') {
            this.$message.success('添加成功')
            this.getUserList()
          } else {
            this.$message.error('添加失败')
          }
        })
        .catch(err => {
          this.$message.error('服务端异常，添加失败。')
        })
    },
    handleUpdate() {
      console.log(this.form)
      UpdateUserInfoById(this.form.id, this.form)
        .then(res => {
          if (res.code === 'success') {
            this.$message.success('更新成功')
            this.getUserList()
          } else {
            this.$message.error('更新失败')
          }
        })
        .catch(err => {
          this.$message.error('服务端异常，更新失败。')
        })
    },
    getUserList() {
      getUsersInfo()
        .then(res => {
          console.log('获取信息成功')
          if (res.code === 'success') {
            this.tableData = res.results
          } else {
            this.$message.error('获取信息失败')
          }
        })
        .catch(err => {
          this.$message.error('服务端异常，请联系管理员解决。')
        })
    },
    
  }
}
</script>
