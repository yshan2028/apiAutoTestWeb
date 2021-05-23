<template>
  <div style="margin: 20px">
    <div class="info">
      <div class="baisc">
        <span>{{ this.reportInfo.name }}测试报告</span>
        <el-table :data="infoList" border :show-header="false">
          <el-table-column width="90" prop="name"> </el-table-column>
          <el-table-column width="180" prop="value"> </el-table-column>
        </el-table>
      </div>
      <!-- 饼图 -->
      <div id="pt"></div>
    </div>
    <div class="data">
      <el-table :data="tableData" style="width: 100%" :cell-style="cellStyle">
        <el-table-column type="expand">
          <template slot-scope="props">
            <el-tabs v-model="activeName">
              <el-tab-pane label="请求信息" name="request">
                <div class="vs">
                  <vue-json-editor
                    v-model="props.row.source"
                    :showBtns="false"
                    :mode="'code'"
                  />
                  <div class="tips">初始信息 VS 最终请求</div>
                  <vue-json-editor
                    v-model="props.row.request"
                    :showBtns="false"
                    :mode="'code'"
                  />
                </div>
              </el-tab-pane>
              <el-tab-pane label="提取参数" name="extra">
                <vue-json-editor
                  v-model="props.row.extra"
                  :showBtns="false"
                  :mode="'code'"
                />
              </el-tab-pane>
              <el-tab-pane label="响应结果" name="response">
                <vue-json-editor
                  v-model="props.row.response.data"
                  :showBtns="false"
                  :mode="'code'"
              /></el-tab-pane>
              <el-tab-pane label="断言信息" name="expect">
                <vue-json-editor
                  v-model="props.row.expect"
                  :showBtns="false"
                  :mode="'code'"
                />
              </el-tab-pane>
              <el-tab-pane label="当前参数池" name="pool">
                <vue-json-editor
                  v-model="props.row.pool"
                  :showBtns="false"
                  :mode="'code'"
                />
              </el-tab-pane>
              <el-tab-pane label="异常信息" name="error">{{
                props.row.error_code
              }}</el-tab-pane>
            </el-tabs>
          </template>
        </el-table-column>
        <el-table-column label="用例名称" prop="info.name"> </el-table-column>
        <el-table-column label="接口名称" prop="info.interface.name">
        </el-table-column>
        <el-table-column label="请求方法" prop="request.method">
        </el-table-column>
        <el-table-column label="数据格式" prop="request.content_type">
        </el-table-column>
        <el-table-column label="接口地址" prop="info.interface.path">
        </el-table-column>
        <el-table-column label="状态码" prop="response.status">
        </el-table-column>
        <el-table-column label="响应时间(ms)" prop="response.time">
        </el-table-column>
        <el-table-column
          label="测试结果"
          prop="result"
          :cell-style="cellStyle"
          width="90"
          :filters="[
            { text: '正常', value: '正常' },
            { text: '失败', value: '失败' },
            { text: '异常', value: '异常' }
          ]"
          :filter-method="filterStatus"
          placement="bottom-end"
        >
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<style lang="scss">
.el-tabs {
  height: 400px;
}
.el-tabs__content {
  height: 280px;
}
.jsoneditor-vue {
  height: 260px;
}
.vs {
  display: flex;
  width: 100%px;
  justify-content: space-between;
  .jsoneditor-vue {
    width: 400px;
  }
  .tips {
    text-align: center;
    line-height: 200px;
    font: bold;
    font-size: 26px;
  }
}
.info {
  height: 300px;
  display: flex;
  justify-content: space-around;
  .baisc {
    margin-top: 10px;
    text-align: center;
    span {
      font-size: 16px;
      font-weight: bold;
    }
    .el-table {
      margin-top: 20px;
    }
  }
  #pt {
    width: 400px;
    height: 300px;
  }
}
.result {
  color: red($color: #000000);
}
.demo-table-expand {
  font-size: 0;
}
.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}
.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}
</style>

<script>
// 导入模块
import vueJsonEditor from "vue-json-editor";
import { fetchReport } from "@/api/report";
var echarts = require("echarts");

export default {
  components: { vueJsonEditor },
  mounted() {
    this.getInfo();
  },
  methods: {
    getClassifyCase(pt) {
      // 基于准备好的dom，初始化echarts实例
      var myChart = echarts.init(document.getElementById("pt"));
      // 指定图表的配置项和数据
      let option = {
        //这里的颜色是显示在部分扇形里的，依次调用颜色
        color: ["#3ADF00", "#FF4000", "#ffaa00"],
        title: {
          text: "用例执行情况",
          x: "center"
        },
        // 筛选项所在位置
        legend: {
          orient: "vertical",
          left: "left",
          //   bottom: "bottom",
          data: ["正常", "失败", "异常"] //名称
        },
        tooltip: {},
        series: pt
      };
      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
    },

    getInfo() {
      fetchReport(this.$route.query.id).then(res => {
        this.reportInfo = res.data;
        this.pt.data = [
          {
            value: this.reportInfo.data.pass,
            name: "正常"
          },
          {
            value: this.reportInfo.data.fail,
            name: "失败"
          },
          {
            value: this.reportInfo.data.expect,
            name: "异常"
          }
        ];
        this.tableData = res.data.data.suite_info;
        this.infoList = [
          { name: "所属项目", value: this.reportInfo.data.project },
          { name: "开始时间", value: this.reportInfo.start },
          { name: "结束时间", value: this.reportInfo.end },
          { name: "用例总数", value: this.tableData.length },
          { name: "运行平台", value: "apiAutoTestWeb" }
        ];
        this.getClassifyCase(this.pt);
      });
    },
    // 第8列样式设置
    cellStyle(value) {
      if (value.columnIndex == 8 && value.row.result == "异常") {
        return "background: #ffaa00;  text-align: center;";
      } else if (value.columnIndex == 8 && value.row.result == "正常") {
        return "background: #3ADF00;  text-align: center;";
      } else if (value.columnIndex == 8 && value.row.result == "失败") {
        return "background: #FF4000;  text-align: center;";
      }
    },
    // 状态筛选
    filterStatus(value, row) {
      console.log(value, row);
      return row.result === value;
    }
  },
  data() {
    return {
      pt: {
        type: "pie", //饼状视图
        radius: "55%",
        // center: ['50%', '60%'],
        data: [],
        label: {
          //   position:'inside' ,//如果需要文字显示在图形里面则设置
          fontSize: "16" //字体大小
        }
      },
      infoList: [],
      reportInfo: [],
      tableData: [],
      activeName: "request"
    };
  }
};
</script>
