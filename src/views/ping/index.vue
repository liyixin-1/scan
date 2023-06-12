<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="Target:" required="True">
        <el-input v-model="form.target" placeholder="请输入探测范围" />
      </el-form-item>
      <el-form-item  label="Result:">
        <el-table :data="tableData" stripe border style="width: 100%">
          <el-table-column prop="ip" label="ip" />
          <el-table-column prop="mac" label="mac" />
          <el-table-column prop="state" label="state" />
        </el-table>
      </el-form-item>
      <div class="excel" :style="{ width:'100%',height:'40px' }">
        <download-excel
          class="export-excel-wrapper"
          :data="json_data"
          :fields="json_fields"
          title="IP地址扫描结果"
          name="IP地址扫描结果.xls"
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
} from '@/api/ipscan'
import echarts from 'echarts'
export default {
  data() {
    return {
      data: [],
      chart: null,
      tableData: [],
      json_fields: {
        'IP地址': 'ip',
        'MAC地址': 'mac',
        '状态': 'state'
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
        target: ''
      }
    }
  },
  methods: {
    onSubmit() {
      // console.log('121212')
      createTaskInfo({
        IPs: this.form.target
      }).then(res => {
        console.log(res)
        if (res.code === 'success') {
          this.$message.success('查询成功')
          this.tableData = res.results
          this.json_data = res.results
          this.data= []
          for ( let item of res.results) {
            if(this.data.length === 0){
              this.data.push({value:1,name:item.mac})
            }else {
              let flag = true
              for(let item1 of this.data){
                if(item1.name===item.mac){
                  item1.value++
                  flag =false
                }
              }
              if(flag) {
                this.data.push({value:1,name:item.mac})
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
    },
    onCancel() {
      this.reset()
    },
    append() {
      this.chart = echarts.init(document.getElementById('main'))
      var option = {
        title: {
          text: 'MAC地址统计',
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
            name: 'MAC',
            type: 'pie',
            radius: '50%',
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
        target: ''
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
