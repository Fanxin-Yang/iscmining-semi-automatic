<template lang="">
  <form class="row g-3">
    <h3 class="display-4">Dataset</h3>
    <h6>Please select an existing data set or upload a new one.</h6>

    <div class="col-md-6">
      <input
        class="form-control"
        type="file"
        multiple
        id="formFile"
        @change="select_files"
        ref="file"
      />
    </div>
    <div class="col-md-2">
      <button
        type="button"
        class="btn btn-outline-primary"
        @click="submit_file"
      >
        Upload
      </button>
    </div>
    <div class="text-center" v-if="status == -1">
      <div class="spinner-border m-5" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="status == 400" class="alert alert-danger" role="alert">
      {{ info }}
    </div>
    <div v-else-if="status == 406" class="alert alert-warning" role="alert">
      {{ info }}
    </div>
    <div
      v-else-if="status == 200 || status == 0"
      class="alert alert-success"
      role="alert"
    >
      {{ info }}
    </div>
    <div v-else-if="!this.selectedFiles" class="alert alert-light" role="alert">
      Please choose a .xes file and click the upload button.
    </div>
    <div v-else class="alert alert-light" role="alert">
      You have choose {{ this.selectedFiles.length }} files. Please click the
      "Upload" button to complete.
    </div>

    <div class="row g-3" v-if="status != 404">
      <div class="col-md-6">
        <select v-model="selectedFile" class="form-select">
          <option selected disabled value="">Select a data set</option>
          <option v-for="(name, index) in availableDataSets" :key="index">
            {{ name }}
          </option>
        </select>
      </div>
      <div class="col-md-4">
        <button
          type="button"
          class="btn btn-primary"
          @click="start_preprocess"
          :disabled="!selectedFile"
        >
          Start Pre-process
        </button>
      </div>
      <h4>Selected data set: {{ selectedFile }}</h4>
    </div>
  </form>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      info: undefined,
      status: null,
      selectedFile: undefined,
      dataSet: undefined,
      selectedFiles: FileList,
      availableDataSets: undefined,
      next: false,
      projections: {},
    };
  },
  methods: {
    get_dataSets() {
      axios
        .get("upload")
        .then((res) => {
          this.availableDataSets = res.data;
        })
        .catch((err) => {
          console.error(err);
          this.status = err.response.status;
          this.info = err.response.data;
        });
    },
    select_files() {
      this.selectedFiles = this.$refs.file.files;
      // this.status = null;
    },
    upload_file(file) {
      let formData = new FormData();
      formData.append("file", file);
      const headers = { "Content-Type": "multipart/form-data" };
      axios
        .post("upload", formData, { headers })
        .then((res) => {
          console.log(res);
          this.get_dataSets();
          this.status = res.status;
          this.info = res.statusText;
          this.selectedFile = this.selectedFiles[0].name;
        })
        .catch((err) => {
          console.error(err);
          this.status = err.response.status;
          this.info = err.response.data;
        });
    },
    submit_file() {
      this.status = -1;
      if (this.selectedFiles.length == 0) {
        this.upload_file(this.$refs.file.files[0]);
      }
      for (let i = 0; i < this.selectedFiles.length; i++) {
        this.upload_file(this.selectedFiles[i]);
      }
    },
    start_preprocess() {
      let tmp = this.selectedFile.substring(
        0,
        this.selectedFile.lastIndexOf(".")
      );
      this.$router.replace(tmp);
    },
  },
  created() {
    this.get_dataSets();
  },
};
</script>

<style lang=""></style>
