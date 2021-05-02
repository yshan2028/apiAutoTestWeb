<template>
  <div class="json">
    <vue-json-editor
      v-model="resultInfo"
      :showBtns="false"
      :mode="'code'"
     
      @json-change="onJsonChange"
      @json-save="onJsonSave"
      @has-error="onError"
    />
    <br>
  </div>
</template>

<script>
  // 导入模块
  import vueJsonEditor from 'vue-json-editor'

  export default {
    // 注册组件
    components: { vueJsonEditor },
    data() {
      return {
        hasJsonFlag:true,  // json是否验证通过
        // json数据
        resultInfo: {
          'employees': [
            {
            'firstName': 'Bill',
            'lastName': 'Gates'
            },
            {
              'firstName': 'George',
              'lastName': 'Bush'
            },
            {
              'firstName': 'Thomas',
              'lastName': 'Carter'
            }
          ]
        }
      }
    },
    mounted: function() {
    },
    methods: {
      onJsonChange (value) {
        this.onJsonSave(value)
      },
      onJsonSave (value) {
        // console.log('保存value:', value);
        this.resultInfo = value
      },
      onError(value) {
        // console.log();
        this.$message.error("json错误了value:", value)
      },
    }
  }
</script>

<style lang="scss">
.jsoneditor-vue{
    height: 700px;
    margin: 20px;
}

</style>