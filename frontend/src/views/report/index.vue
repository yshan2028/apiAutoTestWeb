<template>
  <div class="app-container">

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

      <el-table-column label="报告名称">
        <template slot-scope="{ row }">
          <span>{{ row.name }}</span>
        </template>
      </el-table-column>

            <el-table-column label="用例总数" min-width="80">
        <template slot-scope="{ row }">
          <span>{{ row.data.suite_info.length }}</span>
        </template>
      </el-table-column>
                  <el-table-column label="测试开始时间" min-width="150px">
        <template slot-scope="{ row }">
          <span>{{ row.start }}</span>
        </template>
      </el-table-column>
                  <el-table-column label="测试结束时间" min-width="150px">
        <template slot-scope="{ row }">
          <span>{{ row.end }}</span>
        </template>
      </el-table-column>

      <el-table-column label="创建时间" width="150px" align="center">
        <template slot-scope="{ row }">
          <span>{{ row.created_at | formatDate }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="Actions"
        align="center"
        width="230"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="{ row }">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            查看
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
  deleteReport,
} from "@/api/report";
import waves from "@/directive/waves"; // waves directive
import Pagination from "@/components/Pagination"; // secondary package based on el-pagination

export default {
  name: "ComplexTable",
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      // 默认查询所有接口参数
      listQuery: {
        page: 1,
        limit: 20,
      },

      showReviewer: false,
      downloadLoading: false,
    };
  },
  created() {
    this.getList();
  },
  methods: {
    getList() {
      this.listLoading = true;
      fetchList(this.listQuery).then((response) => {
        this.list = response.data.items;
        this.total = response.data.total;

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false;
        }, 1.5 * 1000);
      });
    },
    handleUpdate(row) {
      this.$router.push({ name: "info",query: {id:row.id}});
    },
    DeleteData(row) {
      deleteReport(row.id).then((res) => {
        this.$notify({
          title: "Success",
          message: "删除成功",
          type: "success",
          duration: 2000,
        });
        this.getList();
      });
    },
  },
};
</script>

<style lang="scss">
.el-table {
  margin-top: 20px;
}
</style>
