<template lang="">
  <form class="row g-3 border bg-light">
    <h6 class="col-md-11">
      Please select an existing data set or upload a new one.
    </h6>
    <div class="col-md-5">
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
        :disabled="this.selectedFiles.length == 0"
      >
        Upload
      </button>
    </div>

    <div class="col-md-4" v-if="status != 404">
      <select
        multiple
        id="selected-dataset"
        v-model="processLogs"
        class="form-select"
      >
        <option v-for="(name, index) in availableDataSets" :key="index">
          {{ name }}
        </option>
      </select>
    </div>

    <div class="col-md-12">
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
      <div
        v-else-if="!this.selectedFiles"
        class="alert alert-light"
        role="alert"
      >
        Please choose a .xes file and click the upload button.
      </div>
      <div v-else class="alert alert-light" role="alert">
        You have choose {{ this.selectedFiles.length }} files. Please click the
        "Upload" button to complete.
      </div>
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
      processLogs: [],
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
    },
    upload_file(file) {
      let formData = new FormData();
      formData.append("file", file);
      const headers = { "Content-Type": "multipart/form-data" };
      axios
        .post("upload", formData, { headers })
        .then((res) => {
          this.get_dataSets();
          this.status = res.status;
          this.info = res.statusText;
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
      this.processLogs = [];
      for (let i = 0; i < this.selectedFiles.length; i++) {
        this.upload_file(this.selectedFiles[i]);
      }
    },
  },
  watch: {
    processLogs: {
      handler: function (val) {
        if (val.length > 0) {
          let tmp = "/iscmining-semi-automatic/";
          for (let i = 0; i < val.length; i++) {
            if (i > 0) {
              tmp += "&";
            }
            tmp += val[i].substring(0, val[i].lastIndexOf("."));
          }
          this.$router.push(tmp);
        }
      },
      deep: true,
      immediate: true,
    },
  },
  created() {
    this.get_dataSets();
  },
};
</script>

<style lang=""></style>
