<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="Destination:" :required="true">
        <el-input v-model="form.destination" placeholder="请输入目标地址" />
      </el-form-item>
      <el-form-item label="Num:" :required="true">
        <el-input-number v-model="form.num" :min="0" :step="1" label="请输入攻击数目" @change="handleChange" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">提交</el-button>
        <el-button @click="onCancel">重置</el-button>
      </el-form-item>
      <div class="excel" :style="{ width:'100%',height:'40px' }">
        <download-excel
          class="export-excel-wrapper"
          :data="json_data"
          :fields="json_fields"
          title="SYN攻击结果"
          name="SYN攻击结果.xls"
        >
          <el-button type="primary" size="middle" style="right: 30px;position: absolute;">导出EXCEL</el-button>
        </download-excel>
      </div>
      <el-form-item label="Result:">
        <el-table :data="tableData" :cell-style="addClass" style="width: 100%" max-height="300">
          <el-table-column prop="destination" label="destination" />
          <el-table-column prop="attacknum" label="attacknum" />
          <el-table-column prop="attacktype" label="attacktype" />
          <el-table-column prop="result" label="results" />
        </el-table>
      </el-form-item>
      <el-form-item>
        <div id="main" />
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
// let echarts = require('echarts');
import {
  createTaskInfo,
  getAttackInfo
} from '@/api/attack'
import echarts from 'echarts'
export default {
  data() {
    return {
      data: [],
      chart: null,
      tableData: [],
      json_fields: {
        '目标地址': 'destination',
        '攻击数目': 'attacknum',
        '攻击类型': 'attacktype',
        '结果': 'result'
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
        destination: '',
        num: 0
      },
      atype: 'SYN'
    }
  },
  methods: {

    handleChange(value) {
      console.log(value)
    },
    onSubmit() {
      if(this.form.destination==''||this.form.num==0){
        this.$message.error('请输入正确的探测条件')
      }else{
        let arr=this.form.destination.split('.')
        if(arr.length!==4){
          this.$message.error('请输入正确的目标地址')
        }else{
            for(let i of arr){
                if(Object.is(Number(i),NaN)||Number(i)>255||Number(i)<0||i[0]==='0'&&i.length!==1){
                  this.$message.error('请输入正确的目标地址')
              }
            }
                createTaskInfo({
                  destination: this.form.destination,
                  attacktype: 'syn',
                  attacknum: this.form.num
                }).then(res => {
                  console.log(res)
                  if (res.code === 'success') {
                  this.$message.success('查询成功')
                  // this.tableData = res.results
                  this.getAttackList()
                } else {
                  this.$message.error('查询失败')
                }
                  })
                  .catch(err => {
                    this.$message.error('服务端异常，添加失败。')
                  })
        }
      }
    },
    onCancel() {
      this.reset()
    },
    getAttackList() {
      getAttackInfo(this.atype).then(res => {
        if (res.code === 'success') {
          this.tableData = res.results
          this.json_data = res.results
          this.data=[]
          for ( let item of res.results) {
            if(this.data.length === 0){
              this.data.push({value:1,name:item.result})
            }else {
              let flag = true
              for(let item1 of this.data){
                if(item1.name===item.result){
                  item1.value++
                  flag =false
                }
              }
              if(flag) {
                this.data.push({value:1,name:item.result})
              }
            }
          }
          this.append()
        } else {
          this.$message.error('获取信息失败')
        }
      })
        .catch(err => {
          this.$message.error('服务端异常，请联系管理员解决。')
        })
    },
    addClass({ row, column, rowIndex, columnIndex }) {
      if (column.label === 'results') {
        if (row.result === 'success') {
          return 'background: #48a915'
        } else if (row.result === 'fail') {
          return 'background: rgb(202, 37, 8)'
        }
        return ''
      }
    },
    append() {
      this.chart = echarts.init(document.getElementById('main'))
      var option = {
        title: {
          text: '成功占比统计',
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
            name: '成功',
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
    },
    // 重置表单数据
    reset() {
      this.form = {
        target: '',
        num: 0
      }
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
