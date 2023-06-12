<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="Target:">
        <el-input v-model="form.target" placeholder="请输入探测范围" />
      </el-form-item>
      <el-form-item label="Dictionary:">
        <el-input v-model="form.text" type="textarea" :autosize="{ minRows: 10 }" placeholder="请输入字典内容(字典用空格间隔)" />
      </el-form-item>
      <el-form-item label="Result:">
        <el-table :data="tableData" stripe border style="width: 100%">
          <el-table-column prop="url" label="url" />
          <el-table-column prop="subdomain" label="subdomain" />
        </el-table>
      </el-form-item>
      
      <div class="excel" :style="{ width:'100%',height:'40px' }">
        <download-excel
          class="export-excel-wrapper"
          :data="json_data"
          :fields="json_fields"
          title="子目录爆破结果"
          name="子目录爆破结果.xls"
        >
          <el-button type="primary" size="middle" style="right: 30px;position: absolute;">导出EXCEL</el-button>
        </download-excel>
      </div>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">提交</el-button>
        <el-button @click="onCancel">重置</el-button>
      </el-form-item>
      <el-form-item>
        <div id="main" />
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import {
  createTaskInfo
} from '@/api/domain'
import echarts from 'echarts'
export default {
  data() {
    return {
      data: [],
      chart: null,
      tableData: [],
      json_fields: {
        '目标地址': 'url',
        '爆破目录': 'subdomain'
      },
      json_data: [],
      json_meta: [
        [
          {
            'key': 'charset',
            'value': 'utf-8'
          }
        ]
      ],
      form: {
        target: '',
        text: ''
      },
      rules: {
        target: [{ required: true, message: '请输入探测范围', trigger: 'blur' }],
        text: [{ required: true, message: '请输入字典内容', trigger: 'blur' }]
      }
    }
  },
  
  methods: {
    onSubmit() {
      if(this.form.target==''||this.form.text==''){
        this.$message.error('请输入正确的探测条件')
      }else{
        let arr=this.form.target.split('.')
        if(arr.length!==4){
          this.$message.error('请输入正确的目标地址')
        }else{
            for(let i of arr){
          if(Object.is(Number(i),NaN)||Number(i)>255||Number(i)<0||i[0]==='0'&&i.length!==1){
            this.$message.error('请输入正确的目标地址')
          }
        }
        }
        createTaskInfo({
        url: this.form.target,
        dictionary: this.form.text
      }).then(res => {
        console.log(res)
        if (res.code === 'success') {
          this.$message.success('查询成功')
          this.tableData = res.results
          this.json_data = res.results
          this.data=[]
          for ( let item of res.results) {
            if(this.data.length === 0){
              this.data.push({value:1,name:item.subdomain})
            }else {
              let flag = true
              for(let item1 of this.data){
                if(item1.name===item.subdomain){
                  item1.value++
                  flag =false
                }
              }
              if(flag) {
                this.data.push({value:1,name:item.subdomain})
              }
            }
          }
          this.append()
        } else {
          this.$message.error('查询失败')
        }
      })
        .catch(err => {
          this.$message.error('服务端异常，添加失败。')
        })
          }
        }
        ,
    // 取消，重置表单数据
    onCancel() {
      this.reset()
    },
    reset() {
      this.form = {
        target: '',
        text: ''
      }
    },
    append() {
      this.chart = echarts.init(document.getElementById('main'))
      var option = {
        title: {
          text: '子域名统计',
          left: 'center'
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: 'subdomain',
            type: 'pie',
            radius: '50%',
            // 在这用
            data: this.data,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };
      this.chart.setOption(option,true)
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
