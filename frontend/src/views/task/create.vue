<template>
  <div class="app-container">
    <el-form
      ref="ruleForm"
      :model="ruleForm"
      label-width="120px"
      :rules="rules"
      class="demo-ruleForm"
    >
      <el-form-item label="任务名称" prop="name">
        <el-input v-model="ruleForm.name" />
      </el-form-item>
      <el-form-item label="选择环境" prop="env_id">
        <el-cascader
          clearable
          v-model="values"
          :options="projects"
          :props="optionProps"
          filterable
          placeholder="输入名字快速查找"
          @change="handleChange"
          style="width: 100%"
        ></el-cascader>
      </el-form-item>

      <el-form-item label="选择用例" prop="case_list">
        <div class="edit_dev">
<el-transfer
          filterable
          :filter-method="filterMethod"
          filter-placeholder="请输入用例名称"
          v-model="ruleForm.case_list"
          :data="cases"
          :props="{ key: 'id', label: 'name', disabled: true }"
          target-order="push"
          :titles="['可选用例列表', '已选中用例']"
          
        >
        </el-transfer>
        </div>
        
      </el-form-item>
      <el-form-item label="定时任务开关">
          <el-switch
            v-model="ruleForm.is_timer"
            @change="taskTypeChange"
          >
          </el-switch>
        </el-form-item>
        <el-form-item
          v-if="ruleForm.is_timer"
          label="定时规则"
          prop="cron"
        >
          <el-input placeholder="* * * * *(每分钟触发,依次是分 时 日 月 年)" v-model="ruleForm.cron" />
        </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('form')">提交</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { createTask, projectList, caseList, updateTask } from "@/api/task";
export default {
  data() {
    return {
      // 级联选择框被选择数据
      values: [],
      cases: [],
      projects: [],
      // 项目 - 环境 级联展示属性设置
      optionProps: {
        value: "id",
        label: "name",
        children: "envs",
      },
      ruleForm: {
        name: "",
        env_id: "",
        case_list: [],
        is_timer: false,
        cron: null,
      },
      // 表单验证
      rules: {
        name: [{ required: true, message: "请输入任务名称", trigger: "blur" }],
        env_id: [
          { required: true, message: "请选择运行环境", trigger: "blur" },
        ],
        case_list: [{ required: true, message: "请选择接口", trigger: "blur" }],
        cron: [{
          required: true, message: "CRON", trigger: "blur"
        }]
      },
    };
  },
  // todo el-select 编辑按钮时 先前数据丢失， 待解决
  methods: {
    // 如果 路由为edit
    update() {
      if (this.$route.path === "/task/edit") {
        // 数据回写
        this.ruleForm = {
          id: this.$route.params.id,
          name: this.$route.params.name,
          env_id: this.$route.params.env.id,
          cron: this.$route.params.cron,
          is_timer: this.$route.params.is_timer,
          case_list: this.$route.params.cases.map((item) => {
            return item.id;
          }),
        };
        this.values = [
          this.$route.params.env.project.id,
          this.$route.params.env.id,
        ];
        caseList(this.values[0]).then((res) => {
          this.cases = res.data.items;
        });
      }
    },
    filterMethod(query, item) {
      //  返回query在字符串中首次出现的位置。 检索的字符串值没有出现，则该方法返回 -1。
      return item.name.indexOf(query) > -1;
    },
    getProjects() {
      projectList().then((res) => (this.projects = res.data.items));
    },
    submitForm() {
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          if (this.ruleForm.id) {
            updateTask(this.ruleForm).then((res) => {
              this.$notify({
              title: "Success",
              message: res.message,
              type: "success",
              duration: 2000,
            });
            });
            this.$router.push({ name: "Task" });
          } else {
            createTask(this.ruleForm).then((res) => {
              this.$notify({
              title: "Success",
              message: res.message,
              type: "success",
              duration: 2000,
            });
             this.$router.push({ name: "Task" });
            });
          }
        }
      });
    },
          // 滑块取值
      taskTypeChange(value) {
        if(!value){
          this.ruleForm.cron = null
        }
      },
    handleChange(value) {
      // 获取env id
      this.ruleForm.env_id = value[1];
      //  获取项目
      caseList(value[0]).then((res) => {
        this.cases = res.data.items;
      });
    },
    // transferChange(value) {
    //   // console.log(value)
    // }
  },
  created() {
    this.getProjects();
    this.update();
  },
};
</script>

<style scoped>
.line {
  text-align: center;
}
.edit_dev >>> .el-transfer-panel {
     width:300px;
   }
</style>
