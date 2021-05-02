<template>
  <div class="app-container">
    <div class="filter-container">
      <el-button
        class="filter-item"
        style="margin-left: 10px"
        type="primary"
        icon="el-icon-edit"
        @click="handleCreate"
      >
        新增
      </el-button>
      tip: 目前版本定时任务是存放在内存中，所以如果应用重启，定时任务将失效.
    </div>

    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      type="index"
      highlight-current-row
      style="width: 100%"
    >
      <el-table-column label="序号" type="index" align="center" width="80">
      </el-table-column>

      <el-table-column label="名称">
        <template slot-scope="{ row }">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="所选环境" min-width="150px">
        <template slot-scope="{ row }">
          <span>{{ row.env.name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="所属项目" min-width="150px">
        <template slot-scope="{ row }">
          <span>{{ row.env.project.name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="创建时间" width="150px" align="center">
        <template slot-scope="{ row }">
          <span>{{ row.created_at | formatDate }}</span>
        </template>
      </el-table-column>
      <el-table-column label="更新时间" width="150px" align="center">
        <template slot-scope="{ row }">
          <span>{{ row.modified_at | formatDate }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="Actions"
        align="center"
        width="500"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="{ row }">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            编辑
          </el-button>
          <el-button type="primary" size="mini" @click="run(row)">
            立即执行
          </el-button>
          <el-button type="primary" size="mini" @click="background(row)">
            后台执行
          </el-button>
          <el-button type="primary" size="mini" @click="timerInfo(row)">
            定时信息
          </el-button>

          <el-button
            v-if="row.status != 'deleted'"
            size="mini"
            type="danger"
            @click="DeleteData(row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <pagination
      v-show="total > 0"
      :total="total"
      :page.sync="listQuery.page"
      :limit.sync="listQuery.limit"
      @pagination="getList"
    />
  </div>
</template>

<script>
import {
  fetchList,
  deleteTask,
  runCase,
  backgroundRun,
  getTimerInfo
} from "@/api/task";
import waves from "@/directive/waves"; // waves directive
import Pagination from "@/components/Pagination"; // secondary package based on el-pagination

export default {
  name: "ComplexTable",
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      interfaces: [],
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      // 默认查询所有接口参数
      listQuery: {
        page: 1,
        limit: 20
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    getList() {
      this.listLoading = true;
      fetchList(this.listQuery).then(response => {
        this.list = response.data.items;
        this.total = response.data.total;

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false;
        }, 1.5 * 1000);
      });
    },
    // 点击新增按钮需要调用project列表接口
    handleCreate() {
      this.$router.push({ name: "add" });
    },

    handleUpdate(row) {
      this.$router.push({ name: "edit", params: row });
    },
    DeleteData(row) {
      deleteTask(row.id).then(res => {
        this.$notify({
          title: "Success",
          message: "删除成功",
          type: "success",
          duration: 2000
        });
        this.getList();
      });
    },

    // run
    run(row) {
      runCase(row.id).then(res => {
        this.$notify({
          title: "Success",
          message: "运行完成.",
          type: "success",
          duration: 2000
        });
        this.$router.push({ name: "info", query: { id: res.data.id } });
      });
    },

    // 后台运行测试任务
    background(row) {
      backgroundRun(row.id).then(res => {
        this.$notify({
          title: "Success",
          message: res.message,
          type: "success",
          duration: 2000
        });
      });
    },

    // timer
    timerInfo(row) {
      getTimerInfo(row.id).then(res => {
        this.$message({
          message: res.data
        });
      });
    }
  }
};
</script>

<style lang="scss">
.el-table {
  margin-top: 20px;
}
</style>
