<template>
  <div>
    <div class="filter-container">
      <div class="info">
        扩展脚本：可以自定义函数，然后在用例中被使用${方法名(参数1,参数2)}
      </div>
      <el-button
        class="filter-item"
        style="margin-right: 10px"
        type="primary"
        icon="el-icon-edit"
        @click="saveCode"
      >
        保存
      </el-button>
    </div>
    <codemirror v-model="code" :options="options"></codemirror>
  </div>
</template>

<script>
import { codemirror } from "vue-codemirror";
// 核心样式
import "codemirror/lib/codemirror.css";
// 引入主题后还需要在 options 中指定主题才会生效
import "codemirror/theme/darcula.css";
import "codemirror/mode/python/python.js";

import { get_code, put_code } from "@/api/util";

export default {
  data() {
    return {
      code: "", // 编辑器绑定的值
      // 默认配置
      options: {
        tabSize: 4, // 缩进格式,
        indentUnit: 4,
        autocorrect: true,
        spellcheck: true,
        autocapitalize: true,
        theme: "darcula", // 主题，对应主题库 JS 需要提前引入 monokai
        lineNumbers: true, // 显示行号
        mode: "python",
        line: true,
        matchBrackets: true, // 括号匹配
        styleActiveLine: true, // 高亮选中行
        readonly: false, // 是否为只读
        hintOptions: {
          completeSingle: true, // 当匹配只有一项的时候是否自动补全
        },
        autocomplete: true,
        extraKeys: { Ctrl: "autocomplete" }, //自定义快捷键
      },

      // 按钮loading状态
      saveloding: false,
    };
  },
  components: {
    codemirror,
  },
  methods: {
    getCode() {
      // 获取脚本
      get_code().then((res) => (this.code = res.data));
    },
    saveCode() {
      put_code(this.code).then((res) => {
        const type = res.code == "200" ? "success" : "error";
        this.$notify({
          title: "消息提醒",
          message: res.message,
          type,
        });
      });
    },
  },
  created() {
    this.getCode();
  },
};
</script>

<style lang="scss">
div {
  .CodeMirror {
    height: 800px;
    margin: 20px;
  }
}
.save {
  position: fixed;
  background: #fff;
  margin-right: 0px;
  top: 15%;
  right: 5%;
  z-index: 100;
}
.filter-container {
  display: flex;
  justify-content: space-between;
  height: 38px;
  .info {
    margin-left: 2%;
    text-align: center;
    line-height: 38px;
    font-size: 24px;
  }
}
</style>