<script setup>
import axios from "axios";
import ProcessModel from "./ProcessModel.vue";
</script>

<template lang="">
  <form class="row g-3">
    <h3>{{ msg }}</h3>
    <div class="col-md-6">
      <input
        class="form-control"
        type="file"
        id="formFile"
        @change="upload_file"
        ref="file"
      />
    </div>
    <div class="col-md-2">
      <button type="button" class="btn btn-primary" @click="submit_file">
        Upload
      </button>
    </div>
    <div v-if="status == 400" class="alert alert-danger" role="alert">
      {{ info }}
    </div>
    <div v-if="status == 406" class="alert alert-warning" role="alert">
      {{ info }}
    </div>
    <div
      v-if="status == 200 || status == 0"
      class="alert alert-success"
      role="alert"
    >
      {{ info }}
    </div>
    <div class="col-md-12">
      <ProcessModel :processModel="graph" />
    </div>
  </form>
</template>

<script>
export default {
  components: {
    ProcessModel,
  },
  data() {
    return {
      msg: "",
      info: "",
      status: null,
      file: "",
      graph: "",
    };
  },
  methods: {
    getResponse() {
      const path = "http://localhost:5000/upload";
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          this.msg = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    upload_file() {
      this.file = this.$refs.file.files[0];
    },
    // upload_file(event) {
    //   this.file = event.target.files[0];
    // },
    submit_file() {
      const path = "http://localhost:5000/upload";
      let formData = new FormData();
      formData.append("file", this.file);
      const headers = { "Content-Type": "multipart/form-data" };
      axios
        .post(path, formData, { headers })
        .then((res) => {
          console.log(res);
          this.status = res.status;
          this.info = res.statusText;
          this.graph = res.data;
        })
        .catch((err) => {
          console.error(err);
          this.status = err.response.status;
          this.info = err.response.data;
        });
    },
  },
  created() {
    this.getResponse();
  },
};
</script>

<style lang=""></style>
