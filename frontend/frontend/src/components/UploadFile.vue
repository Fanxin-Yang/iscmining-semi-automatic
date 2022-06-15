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
    <div v-if="status == 400" class="alert alert-danger" role="alert">
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

    <div class="col-md-6">
      <select v-model="selectedFile" class="form-select">
        <option selected disabled value="">Select a data set</option>
        <option v-for="(name, index) in availableDataSets" :key="index">
          {{ name }}
        </option>
      </select>
      <!-- <div class="alert alert-light" role="alert">
        Selected data set: {{ selectedFile }}
      </div> -->
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

    <div v-if="!!dataSet" class="col-md-12">
      <ProcessModel :processModel="dataSet + '.gv.png'" />
    </div>

    <div v-if="!!dataSet" class="row">
      <ProjectionTransformation
        :dataSet="dataSet"
        v-model:projections="projections"
      />
    </div>
    <div v-if="Object.keys(projections).length > 0" class="row">
      <DiscoveryAlgorithm :dataSet="dataSet" :projections="projections" />
    </div>
  </form>
</template>

<script>
import axios from "axios";
import ProcessModel from "./ProcessModel.vue";
import ProjectionTransformation from "./ProjectionTransformation.vue";
import DiscoveryAlgorithm from "./DiscoveryAlgorithm.vue";
export default {
  components: {
    ProcessModel,
    ProjectionTransformation,
    DiscoveryAlgorithm,
  },
  data() {
    return {
      info: "",
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
      const path = "http://localhost:5000/upload";
      axios
        .get(path)
        .then((res) => {
          this.availableDataSets = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    select_files() {
      this.selectedFiles = this.$refs.file.files;
      this.status = null;
    },
    upload_file(file) {
      const path = "http://localhost:5000/upload";
      let formData = new FormData();
      formData.append("file", file);
      const headers = { "Content-Type": "multipart/form-data" };
      axios
        .post(path, formData, { headers })
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
