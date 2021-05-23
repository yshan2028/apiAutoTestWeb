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
      <!-- <el-table-column label="token">
        <template slot-scope="{ row }">
          <span>{{ formatToken(row.token) }}</span>
        </template>
      </el-table-column> -->

      <el-table-column label="请求参数" min-width="150px">
        <template slot-scope="{ row }">
          <span>{{ row.body }}</span>
        </template>
      </el-table-column>

      <el-table-column label="提取参数" min-width="150px">
        <template slot-scope="{ row }">
          <span>{{ row.extra }}</span>
        </template>
      </el-table-column>
      <el-table-column label="预期结果" min-width="150px">
        <template slot-scope="{ row }">
          <span>{{ row.expect }}</span>
        </template>
      </el-table-column>
      <el-table-column label="归属接口">
        <template slot-scope="{ row }">
          <span>{{ row.interface.name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="所属项目">
        <template slot-scope="{ row }">
          <span>{{ row.interface.project.name }}</span>
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
        width="230"
        class-name="small-padding fixed-width"
      >
        <template slot-scope="{ row }">
          <el-button type="primary" size="mini" @click="handleUpdate(row)">
            编辑
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

    <!-- 弹出框，新增，编辑 -->
    <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form
        ref="dataForm"
        :rules="rules"
        :model="temp"
        label-position="left"
        label-width="150px"
        style="width: 400px"
      >
        <el-form-item label="选择接口" prop="interface_id">
          <!-- @change="handleChange" -->
          <el-cascader
            v-model="values"
            :options="projects"
            :props="optionProps"
            filterable
            placeholder="输入名字快速查找"
            @change="handleChange"
          ></el-cascader>
        </el-form-item>

        <el-form-item label="名称" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="参数类型" prop="keyword" v-if="standard">
          <el-radio-group v-model="temp.content_type">
            <el-radio label="params"></el-radio>
            <el-radio label="data"></el-radio>
            <el-radio label="json"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="query语句" prop="query" v-else>
          <el-input
            v-model="temp.query"
            :autosize="{ minRows: 2, maxRows: 4 }"
            type="textarea"
            placeholder="Please input"
          />
        </el-form-item>
        <el-form-item label="请求参数">
          <el-input
            v-model="temp.body"
            :autosize="{ minRows: 2, maxRows: 4 }"
            type="textarea"
            placeholder='{参数名:参数值} => {"username":"123456"}'
          />
        </el-form-item>
            <el-form-item label="提取参数">
          <el-input
            v-model="temp.extra"
            :autosize="{ minRows: 2, maxRows: 4 }"
            type="textarea"
            placeholder='{参数名:提取参数表达式} => {"token": "$.token"}'
          />
        </el-form-item>
            <el-form-item label="后置sql">
          <el-input
            v-model="temp.backend_sql"
            :autosize="{ minRows: 2, maxRows: 4 }"
            type="textarea"
            placeholder='后置sql,多sql使用 ; 分隔'
          />
        </el-form-item>
        <el-form-item label="预期结果" prop="expect">
          <el-input
            v-model="temp.expect"
            :autosize="{ minRows: 2, maxRows: 4 }"
            type="textarea"
            placeholder='{实际:预期} => {"$.code":200}'
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false"> 取消 </el-button>
        <el-button
          type="primary"
          @click="dialogStatus === 'create' ? createData() : updateData()"
        >
          提交
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  fetchList,
  projectList,
  deleteCase,
  fetchInterface,
  createCase,
  updateCase,
} from "@/api/case";
import waves from "@/directive/waves"; // waves directive
import Pagination from "@/components/Pagination"; // secondary package based on el-pagination

export default {
  name: "ComplexTable",
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      standard: true, // 接口规范 restful true
      values: [], // el-cascader 级联选择器编辑时数据丢失问题
      // el-cascader 级联选择器 解决后端返回内容与前端不一致问题
      optionProps: {
        value: "id",
        label: "name",
        children: "Interfaces",
      },
      projects: [],
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      // 默认查询所有接口参数
      listQuery: {
        page: 1,
        limit: 20,
      },
      // 弹出框表单
      temp: {
        interface_id: "",
        name: "",
        content_type: "params",
        extra: null,
        expect: null,
        body: null,
        query: null,
        backend_sql: null
      },
      dialogFormVisible: false,
      dialogStatus: "",
      textMap: {
        update: "编辑",
        create: "创建",
      },
      rules: {
        name: [{ required: true, message: "请填写用例名称", trigger: "blur" }],
        interface_id: [
          { required: true, message: "请选择接口", trigger: "blur" },
        ],
        query: [{
           required: true,
            message: "请填写query语句",
            trigger: "blur",
        }],
        expect: [{
          required: true,
          message: "请填写预期结果",
          trigger: "blur"
        }]
      },
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
            projectList().then((res) => (this.projects = res.data.items));
    },
    resetTemp() {
      this.temp = {
        interface_id: "",
        name: "",
        body: null,
        extra: null,
        content_type: "params",
        expect: null,
        query: null,
        backend_sql: null
      };
      this.values = [];
    },
    // 点击新增按钮需要调用project列表接口
    handleCreate() {
      this.resetTemp();
      this.dialogStatus = "create";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    createData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          createCase(this.temp).then((res) => {
            this.dialogFormVisible = false;
            this.$notify({
              title: "Success",
              message: "创建成功",
              type: "success",
              duration: 2000,
            });
            this.getList();
          });
        }
      });
    },
    handleUpdate(row) {
      this.standard = row.interface.standard == "graphql" ? false : true;
      this.temp = Object.assign({}, row); // copy obj
      this.temp.interface_id = this.temp.interface.id;
      this.values = [this.temp.interface.project.id, this.temp.interface.id];
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    updateData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          updateCase(this.temp).then((res) => {
            this.dialogFormVisible = false;
            this.$notify({
              title: "Success",
              message: "更新成功",
              type: "success",
              duration: 2000,
            });
            this.getList();
          });
        }
      });
    },
    DeleteData(row) {
      deleteCase(row.id).then((res) => {
        this.$notify({
          title: "Success",
          message: "删除成功",
          type: "success",
          duration: 2000,
        });
        this.getList();
      });
    },

    handleChange(value) {
      if (value.length != 0) {
        // 获取接口id
        this.temp.interface_id = value[1];
        // 获取接口详细信息
        fetchInterface(value[1]).then((res) => {
          // 拿到 接口规范
          this.standard = res.data.standard == "graphql" ? false : true;
          this.temp.content_type = this.standard?'params':'json'
  
        });
      }
    },

    // 滑块改变事件
    tokenChange(value) {
      if (!value) {
        // 重置 token_path 内容
        this.temp.token_path = null;
      }
    },
  },
};
</script>

<style lang="scss">
.el-table {
  margin-top: 20px;
}
</style>
