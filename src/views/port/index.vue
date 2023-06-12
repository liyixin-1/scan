<template>
  <div class="app-container">
    <el-form ref="form" :model="form" label-width="120px">
      <el-form-item label="Target:" required="True">
        <el-input v-model="form.target" placeholder="请输入IP地址或地址段" />
      </el-form-item>
      <el-form-item label="Arguments:" required="True">
        <el-select v-model="form.argument" clearable placeholder="请选择探测模式">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="Port:" required="True">
        <el-input v-model="form.port" autosize type="textarea" placeholder="请输入端口（0-65535）" />
      </el-form-item>
      
      <el-form-item  label="Result:">
        <el-table :data="tableData" stripe border style="width: 100%" max-height="300">
          <el-table-column prop="host" label="host" width="150" />
          <el-table-column prop="protocol" label="potocol" />
          <el-table-column prop="port" label="port" />
          <el-table-column prop="state" label="state" />
          <el-table-column prop="reason" label="reason" />
          <el-table-column prop="name" label="name" />
        </el-table>
      </el-form-item>
      <div class="excel" :style="{ width:'100%',height:'40px' }">
        <download-excel
          class = 'export-excel-wrapper'
          :data = 'json_data'
          :fields = 'json_fields'
          title='端口扫描结果'
          name = '端口扫描结果.xls'>
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
} from '@/api/port'
import echarts from 'echarts'
export default {
  data() {
    return {
      data: [],
      chart: null,
      tableData: [],
      json_fields:{
        "主机地址":'host',
        "协议":'protocol',
        "端口号":'port',
        "名字":'name',
        "状态":'state',
        "原因":'reason',
      },
      json_data:[],
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
        argument: '',
        port: ''
      },
      options: [{
        value: '-sT',
        label: 'TCP方式'
      }, {
        value: '-sS',
        label: 'SYN方式'
      }, {
        value: '-sF',
        label: 'FIN方式'
      }, {
        value: '-sP',
        label: 'Ping方式'
      }, {
        value: '-sU',
        label: 'UDP方式'
      }, {
        value: '-sA',
        label: 'ACK方式'
      }],
      valuetype: '-sS'
    }
  },
  methods: {
    onSubmit() {
      console.log(this.form.target)
      if(this.form.target==''||this.form.port==''||this.form.argument==''){
        this.$message.error('请正确输入扫描条件')
      }else{
      createTaskInfo({
        IP: this.form.target,
        argument: this.form.argument,
        port: this.form.port
      }).then(res => {
        console.log(res)
        if (res.code === 'success') {
          this.$message.success('查询成功')
          // console.log('success')
          this.tableData = res.results
          this.json_data = res.results
          this.data= []
          for ( let item of res.results) {
            if(this.data.length === 0){
              this.data.push({value:1,name:item.host})
            }else {
              let flag = true
              for(let item1 of this.data){
                if(item1.name===item.host){
                  item1.value++
                  flag =false
                }
              }
              if(flag) {
                this.data.push({value:1,name:item.host})
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
      
    },
    append() {
      this.chart = echarts.init(document.getElementById('main'))
      var option = {
        title: {
          text: '数据统计图',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b} : {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top:'bottom'
        },
        toolbox: {
          show: true,
          feature: {
            mark: { show: true },
            dataView: { show: true, readOnly: false },
            restore: { show: true },
            saveAsImage: { show: true }
          }
        },
        series: [
          {
            name: '各IP占比',
            type: 'pie',
            radius: [80,150],
            roseType: 'radius',
            itemStyle: {
              borderRadius: 5
            },
            label: {
              show: false
            },
            // 在这用
            data: this.data,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              },
              label: {
                show: true
              }
            }
          }
        ]
      };
      this.chart.setOption(option,true)
    },
    onCancel() {
      this.reset()
    },
    // 重置表单数据
    reset() {
      this.form = {
        target: '',
        argument: '',
        port: ''
      }
    }
  }
}
</script>
<style scoped>
.line{
  text-align: center;
}
/* 宽高在这改 */
#main {
  width: 100%;
  height: 400px;
}
</style>
