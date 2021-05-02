<template>
  <div>
    <div class="shortcut">
      <el-card shadow="hover" body-style="{text-}">
        {{ list.project }}项目
      </el-card>

      <el-card shadow="hover"> {{ list.interface }}接口 </el-card>
      <el-card shadow="hover"> {{ list.case }}用例 </el-card>
      <!-- <el-card shadow="hover"> {{ list.task }}任务 </el-card> -->
      <el-card shadow="hover"> {{ list.report }}报告 </el-card>
    </div>
    <div id="myChart"></div>
  </div>
</template>

<script>
import { list } from "@/api/user";

// vue文件中引入echarts工具
const echarts = require("echarts/lib/echarts");
require("echarts/lib/component/grid");
require("echarts/lib/chart/bar");
import { TitleComponent } from 'echarts/components'
echarts.use([TitleComponent]);

export default {
  name: "Dashboard",
  // created() {
  //   this.getData();
  // },
  mounted() {
    this.getData();
  },
  data() {
    return {
      list: {},
      datas: []
    };
  },
  methods: {
    getData() {
      list().then(res => {
        this.list = res.data;
        this.mainInit(res.data.today)
      });
    },
    // 初始化图表
    mainInit(datas) {
      let myChart = echarts.init(document.getElementById("myChart"));
      let option =  {
        color: ["yellowgreen"],
        title: {
          text: "今日新增趋势",
          x: 'center'
        },
        xAxis: {
          type: "category",
          data: ["项目", "环境", "接口", "用例", "任务", "报告"]
        },
        yAxis: {
          type: "value"
        },
        series: [
          {
            data: datas,
            type: "bar",
            label: {
              show: true,
              position: "inside",
              color: "black"
            }
          }
        ]
      }
      myChart.setOption(option);
      
    }
  }
};
</script>

<style lang="scss">
.shortcut {
  display: flex;
  margin: 20px;
  height: 100px;
  justify-content: space-around;
  .el-card {
    width: 15%;
    text-align: center;
    line-height: 50px;
  }
}
#myChart {
  width: 100%;
  height: 570px;
  margin: 30px;
}
</style>
