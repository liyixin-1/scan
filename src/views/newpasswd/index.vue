<template>
  <div class="app-container">
      
    <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">
              <el-form-item label="新密码" prop="newPwd">
                <el-input v-model="ruleForm.newPwd" clearable size="small" type="password"></el-input>
              </el-form-item>
              <el-form-item label="确认密码" prop="confirmPwd">
                <el-input v-model="ruleForm.confirmPwd" clearable size="small" type="password"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="onSubmit">确定</el-button>
                <el-button @click="onCancel">重置</el-button>
              </el-form-item>
            </el-form>
  </div>
</template>
<script>
import {
  newpasswd
} from '@/api/user'
import { mapGetters } from 'vuex'
export default {
    name: 'DashboardEditor',
    computed: {
    ...mapGetters(['name'])
  },
     data() {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
                callback(new Error('请输入密码'));
        } else {
          if (this.ruleForm.confirmPwd !== '') {
              this.$refs.ruleForm.validateField('confirmPwd');
          }
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
          if (value === '') {
              callback(new Error('请再次输入密码'));
          } else if (value !== this.ruleForm.newPwd) {
              callback(new Error('两次输入密码不一致!'));
          } else {
              callback();
          }
      };
      return {
        ruleForm: {
          newPwd: '',
          confirmPwd:''
        },
        rules: {
          newPwd: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 6, max: 16, message: '长度在 6 到 16 个字符', trigger: 'blur' },
            { validator: validatePass, trigger: 'blur' }
          ],
          confirmPwd:[
            { required: true, message: '请确认密码', trigger: 'blur' },
            { min: 6, max: 16, message: '长度在 6 到 16 个字符', trigger: 'blur' },
            { validator: validatePass2, trigger: 'blur', required: true }
          ],
        }
      }
    },
    
  methods: {
    onSubmit() {
        //console.log(this.name,this.ruleForm.newPwd)
      newpasswd({
        username:this.name,
        password:this.ruleForm.newPwd
      }).then(res => {
          if(res.code === 'success'){
              this.$message.success('修改成功')
          }else {
          this.$message.error('修改失败')
        }
        this.reset()
      })
        .catch(err => {
          this.$message.error('服务端异常，失败。')
        })
    },
    onCancel() {
      this.reset()
    },
    // 重置表单数据
    reset() {
      this.ruleForm = {
        newPassword: '',
        confirmPassword:''
      }
    }
  },
  watch:{
      name:function(newdata,olddata){
            console.log(newdata)
            this.username=newdata
            this.order();
      }
  }
}
</script>
<style scoped>
.line{
  text-align: center;
}
#main {
  width: 100%;
  height: 200px;
}
</style>
