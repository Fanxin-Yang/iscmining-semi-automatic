<template lang="">
  <form>
    <div class="mb-3">
      <label for="formFile" class="form-label">{{ msg }}</label>
      <input
        class="form-control"
        type="file"
        id="formFile"
        @change="upload_file"
        ref="file"
      />
      <button type="button" class="btn btn-primary" @click="submit_file">
        Upload
      </button>
      <div v-if="status == 400" class="alert alert-danger" role="alert">
        {{ info }}
      </div>
      <div v-if="status == 406" class="alert alert-warning" role="alert">
        {{ info }}
      </div>
      <div v-if="status == 200" class="alert alert-success" role="alert">
        {{ info }}
      </div>
    </div>
  </form>
</template>

<script>
import axios from "axios";
export default {
  name: "UploadFile",
  data() {
    return {
      msg: "",
      info: "",
      status: null,
      file: "",
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
          res.data.files;
          this.status = res.status;
          this.info = res.data;
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
