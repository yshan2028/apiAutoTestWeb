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
      <el-button
        class="filter-item"
        style="margin-left: 10px"
        type="primary"
        icon="el-icon-upload"
        @click="handleExport"
      >
        接口导入
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

      <el-table-column label="接口规范">
        <template slot-scope="{ row }">
          <span>{{ row.standard }}</span>
        </template>
      </el-table-column>

      <el-table-column label="请求方法">
        <template slot-scope="{ row }">
          <span>{{ row.method }}</span>
        </template>
      </el-table-column>

      <el-table-column label="路径">
        <template slot-scope="{ row }">
          <span>{{ row.path }}</span>
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
        <!-- 规范选择 -->
        <el-form-item label="规范">
          <el-radio-group v-model="temp.standard" @change="radioChange">
            <el-radio label="restful" />
            <el-radio label="graphql" />
          </el-radio-group>
        </el-form-item>

        <el-form-item label="方法&路径">
          <el-input v-model="temp.path" class="input-with-select">
            <el-select
              v-model="temp.method"
              slot="prepend"
              style="width: 100px"
              :disabled="temp.standard == 'graphql' ? true : false"
            >
              <el-option label="GET" value="get"></el-option>
              <el-option label="POST" value="post"></el-option>
              <el-option label="DELETE" value="delete"></el-option>
              <el-option label="PUT" value="put"></el-option>
            </el-select>
          </el-input>
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

    <!-- 弹出框导入接口 -->
    <el-dialog title="导入接口" :visible.sync="exportVisible">
      <el-form
        ref="importForm"
        :model="exportForm"
        label-width="80px"
        :rules="exportRules"
        style="width: 400px"
        
      >
        <el-form-item label="项目" prop="project_id">
          <el-select
            filterable
            class="filter-item"
            v-model="exportForm.project_id"
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
        <el-form-item label="规范">
          <el-radio-group v-model="exportForm.standard" @change="radioChange">
            <el-radio label="restful" />
            <el-radio label="graphql" disabled />
          </el-radio-group>
        </el-form-item>
        <el-form-item label="文件">
          <el-switch v-model="fileUpload" @change="taskTypeChange" disabled>
          </el-switch>
        </el-form-item>
        <el-form-item v-if="fileUpload" label="文件" prop="file">
          <el-upload
            class="upload-demo"
            drag
            action="https://jsonplaceholder.typicode.com/posts/"
            multiple
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <div class="el-upload__tip" slot="tip">
              只能上传openapi.json/schema.gql(暂不支持)文件
            </div>
          </el-upload>
        </el-form-item>
        <el-form-item label="地址" prop="url" v-show="!fileUpload">
          <el-input v-model="exportForm.url" placeholder="http://49.232.203.244:8000/openapi.json"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="exportVisible = false">取 消</el-button>
        <el-button type="primary" @click="importInterfaceData">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import {
  fetchList,
  projectList,
  deleteInterface,
  createInterface,
  updateInterface,
  importInterfaces
} from "@/api/interface";
import waves from "@/directive/waves"; // waves directive
import Pagination from "@/components/Pagination"; // secondary package based on el-pagination

export default {
  name: "ComplexTable",
  components: { Pagination },
  directives: { waves },
  data() {
    return {
      // 导入按钮弹出表单控制
      exportVisible: false,
      fileUpload: false,
      exportForm: {
        project_id: null,
        standard: "restful",
        url: "",
        // 上传文件
        file: null
      },
      exportRules: {
        project_id: [
          { required: true, message: "请选择项目", trigger: "blur" }
        ],
        url: [
          {
            required: true,
            message: "请填写swagger openapi.json 的url地址",
            trigger: "blur",
            type: "url"
          }
        ]
      },
      projects: [],
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      // 默认查询所有接口参数
      listQuery: {
        page: 1,
        limit: 20
      },
      // 弹出框表单
      temp: {
        project_id: "",
        name: "",
        base_url: "",
        desc: "",
        standard: "restful"
      },
      dialogFormVisible: false,
      dialogStatus: "",
      textMap: {
        update: "编辑",
        create: "创建"
      },
      rules: {
        name: [{ required: true, message: "请填写接口名称", trigger: "blur" }],
        project_id: [{ required: true, message: "请选择项目", trigger: "blur" }]
      },
      downloadLoading: false
    };
  },
  created() {
    this.getList();
    this.getProjects();
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
    getProjects() {
      projectList().then(res => {
        this.projects = res.data.items;
      });
    },
    resetTemp() {
      this.temp = {
        project_id: "",
        name: "",
        path: "",
        desc: "",
        method: "get",
        standard: "restful"
      };
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
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          createInterface(this.temp).then(res => {
            this.dialogFormVisible = false;
            this.$notify({
              title: "Success",
              message: "创建成功",
              type: "success",
              duration: 2000
            });
            this.getList();
          });
        }
      });
    },
    handleUpdate(row) {
      this.temp = Object.assign({}, row); // copy obj
      this.temp.project_id = this.temp.project.id;
      this.dialogStatus = "update";
      this.dialogFormVisible = true;
      this.$nextTick(() => {
        this.$refs["dataForm"].clearValidate();
      });
    },
    updateData() {
      this.$refs["dataForm"].validate(valid => {
        if (valid) {
          updateInterface(this.temp).then(res => {
            this.dialogFormVisible = false;
            this.$notify({
              title: "Success",
              message: "更新成功",
              type: "success",
              duration: 2000
            });
            this.getList();
          });
        }
      });
    },
    DeleteData(row) {
      deleteInterface(row.id).then(res => {
        this.$notify({
          title: "Success",
          message: "删除成功",
          type: "success",
          duration: 2000
        });
        this.getList();
      });
    },

    // 单选框事件
    radioChange(value) {
      if (value == "graphql") {
        this.temp.method = "post";
      } else if (value == "restful") {
        this.temp.method = "get";
      }
    },

    resetImport() {
      this.exportForm = {
        project_id: null,
        standard: "restful",
        url: "",
        // 上传文件
        file: null
      };
    },
    // 点击导入
    handleExport() {
      this.resetImport();
      this.exportVisible = true;
      this.$nextTick(() => {
        this.$refs["importForm"].clearValidate();
      });
    },

    // 选择接口文档导入接口
    importInterfaceData() {
      this.$refs["importForm"].validate(valid => {
        if (valid) {
          importInterfaces(this.exportForm).then(res => {
            this.exportVisible = false;
            this.$notify({
              title: "Success",
              message: res.message,
              type: "success",
              duration: 2000
            });
            this.getList()
          });
        }
      });
    },

    taskTypeChange() {}
  }
};
</script>

<style lang="scss">
.el-table {
  margin-top: 20px;
}
</style>
