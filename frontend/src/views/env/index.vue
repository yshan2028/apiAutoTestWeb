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
      <el-table-column label="描述" min-width="150px">
        <template slot-scope="{ row }">
          <span>{{ row.desc }}</span>
        </template>
      </el-table-column>

      <el-table-column label="基准地址" min-width="150px">
        <template slot-scope="{ row }">
          <span>{{ row.base_url }}</span>
        </template>
      </el-table-column>

      <el-table-column label="所属项目">
        <template slot-scope="{ row }">
          <span>{{ row.project.name }}</span>
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
        label-width="100px"
        style="width: 400px"
      >
        <el-form-item label="项目" prop="project_id">
          <el-select
            filterable
            class="filter-item"
            v-model="temp.project_id"
            placeholder="请选择项目"
            @change="$forceUpdate()"
          >
            <!--  $forceUpdate() 强制刷新-->
            <el-option
              v-for="project in projects"
              :key="project.id"
              :label="project.name"
              :value="project.id"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="名称" prop="name">
          <el-input v-model="temp.name" />
        </el-form-item>
        <el-form-item label="基准地址" prop="base_url">
          <el-input v-model="temp.base_url" />
        </el-form-item>
        <el-form-item label="基准header" prop="base_header">
          <!-- <vue-json-editor
            v-model="temp.base_header"
            :showBtns="false"
            :mode="'code'"
            @json-change="onJsonChange"
          /> -->
          <el-input
            v-model="temp.base_header"
            :autosize="{ minRows: 2, maxRows: 4 }"
            type="textarea"
            placeholder="Please input"
          />
        </el-form-item>
        <el-form-item label="数据库配置">
          <vue-json-editor
            v-model="mysql_default"
            :showBtns="true"
            :mode="'code'"
            @json-change="onJsonChange"
            lang="zh" 
            @json-save="connectTest"
          />
        </el-form-item>
        <el-form-item label="描述信息">
          <el-input
            v-model="temp.desc"
            :autosize="{ minRows: 2, maxRows: 4 }"
            type="textarea"
            placeholder="Please input"
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
  createEnv,
  projectList,
  updateEnv,
  deleteEnv,
} from "@/api/env";
import waves from "@/directive/waves"; // waves directive
import Pagination from "@/components/Pagination"; // secondary package based on el-pagination
import vueJsonEditor from "vue-json-editor";


/**
 * 
 * 
 * {
  "host": "http://localhost",
  "port": "123456",
  "charset":"utf8mb4",
  "user":"root",
  "password":"123456",
  "db_name":"uniapp_shop"
}
 */
export default {
  name: "ComplexTable",
  components: { Pagination, vueJsonEditor },
  directives: { waves },
  data() {
    return {
      projects: [],
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,

      mysql_default: {
  "host": "http://localhost",
  "port": "3306",
  "charset":"utf8mb4",
  "user":"root",
  "password":"123456",
  "database":"uniapp_shop"
},
      // 默认查询所有接口参数
      listQuery: {
        page: 1,
        limit: 20,
      },
      sortOptions: [
        { label: "ID Ascending", key: "+id" },
        { label: "ID Descending", key: "-id" },
      ],
      showReviewer: false,
      // 弹出框表单
      temp: {
        project_id: "",
        name: "",
        base_url: "",
        desc: "",
        base_header: '{}',
        db_settings: null
      },
      dialogFormVisible: false,
      dialogStatus: "",
      textMap: {
        update: "编辑",
        create: "创建",
      },
      rules: {
        name: [{ required: true, message: "请填写环境名称", trigger: "blur" }],
        project_id: [
          { required: true, message: "请选择项目", trigger: "blur" },
        ],
        base_url: [
          {
            required: true,
            message: "请填写基准地址",
            trigger: "blur",
            type: "url",
          },
        ],
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
    },
    resetTemp() {
      this.temp = {
        project_id: "",
        name: "",
        base_url: "",
        base_header: '{}',
        desc: "",
        db_settings: null
      };
    },
    // 点击新增按钮需要调用project列表接口
    handleCreate() {
      this.resetTemp();
      this.dialogStatus = "create";
      projectList().then((res) => {
        this.projects = res.data.items;
      });
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    createData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          createEnv(this.temp).then((res) => {
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
      projectList().then((res) => (this.projects = res.data.items));
      this.temp = Object.assign({}, row); // copy obj
      this.temp.project_id = this.temp.project.id;
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    updateData() {
      this.$refs["dataForm"].validate((valid) => {
        if (valid) {
          updateEnv(this.temp).then((res) => {
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
      deleteEnv(row.id).then((res) => {
        this.$notify({
          title: "Success",
          message: "删除成功",
          type: "success",
          duration: 2000,
        });
        this.getList();
      });
    },

    onJsonChange(value) {
      this.temp.base_header = value;
    },
    
    connectTest(value){
      console.log(value)
    }
  },
};
</script>

<style lang="scss">
.el-table {
  margin-top: 20px;
}

.jsoneditor-poweredBy {
  display: none;
}
</style>
