<template lang="">
  <h3>Projection & Transformation</h3>
  <div class="row">
    <div class="col-md-6">
      <select v-model="selectedAtt" class="form-select">
        <option selected disabled value="">
          Choose a event attribute (recommanded: org:resource)
        </option>
        <option v-for="(att, index) in attributes" :key="index">
          {{ att }}
        </option>
      </select>
      <div class="alert alert-light" role="alert">
        Selected event attribute: {{ selectedAtt }}
      </div>
    </div>
    <div class="col-md-4">
      <button
        type="button"
        class="btn btn-outline-primary"
        @click="transformation"
        :disabled="!selectedAtt"
      >
        Projection & Transformation
      </button>
    </div>
  </div>
  <div
    class="text-center"
    v-if="loading && Object.keys(projections).length == 0"
  >
    <div class="spinner-border m-5" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div
    v-else-if="Object.keys(projections).length > 15"
    class="alert alert-warning"
    role="alert"
  >
    There are {{ Object.keys(projections).length }} files saved. Recommanded
    event attribute is org:resource.
  </div>
  <div
    v-else-if="Object.keys(projections).length > 0"
    class="alert alert-success"
    role="alert"
  >
    There are {{ Object.keys(projections).length }} files saved.
  </div>

  <div v-if="Object.keys(projections).length > 0" class="row">
    <div class="col-md-6">
      <select v-model="selectedProjection" class="form-select">
        <option selected disabled value="">Choose a file</option>
        <option v-for="(number, tmp) in projections" :key="tmp">
          {{ tmp }}.csv
        </option>
      </select>
      <div class="alert alert-light" role="alert">
        Selected projection: {{ selectedProjection }}
      </div>
    </div>
    <div class="col-md-4">
      <button
        type="button"
        class="btn btn-primary"
        @click="start_discovery"
        :disabled="!selectedProjection"
      >
        Start Discovery
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      attributes: {},
      selectedAtt: undefined,
      projections: {},
      selectedProjection: undefined,
      loading: false,
    };
  },
  // props: ["dataSet", "projections"],
  methods: {
    get_attributes() {
      // console.log(this.dataSet);
      // const path =
      //   "http://localhost:5000/projection_transformation/" + this.dataSet;
      const path =
        "http://localhost:5000/projection_transformation/" +
        this.$route.params.dataSet;
      axios
        .get(path)
        .then((res) => {
          // console.log(res.data);
          this.attributes = res.data;
          // console.log(this.attributes);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    transformation() {
      this.loading = true;
      const path =
        "http://localhost:5000/projection_transformation/" +
        this.$route.params.dataSet +
        "/" +
        this.selectedAtt;
      // console.log(path);
      axios
        .get(path)
        .then((res) => {
          // this.$emit("update:projections", res.data);
          this.loading = false;
          this.projections = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    start_discovery() {
      let tmp =
        this.$router.currentRoute.value.fullPath +
        "/" +
        this.selectedProjection.substring(
          0,
          this.selectedProjection.lastIndexOf(".")
        );
      this.$router.push(tmp);
    },
  },
  created() {
    this.get_attributes();
  },
};
</script>

<style lang=""></style>
