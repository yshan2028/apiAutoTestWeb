<template>
  <div class="mavonEditor">
    <mavon-editor
      :subfield="false"
      :editable="false"
      :defaultOpen="defaultOpen"
      v-model="text"
    />
  </div>
</template>

<script>
import { help_doc } from "@/api/util";

export default {
  name: "Help",
  data() {
    return {
      text: "",
      defaultOpen: "preview",
    };
  },
  methods: {
    get_doc() {
      help_doc().then((res) => {
        this.text = res.data;
      });
    },
  },
  created() {
    this.get_doc();
  },
};
</script>

<style lang="scss">
.help {
  margin: 20px;
  height: 700px;
  width: 100%;
  .mavonEditor {
    width: 100%;
    height: 100%;
  }
}
</style>
