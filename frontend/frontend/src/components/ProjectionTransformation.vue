<template lang="">
  <div class="col-md-4">
    <select v-model="selectedAtt" class="form-select" id="select-attribute">
      <option selected disabled value="">
        Choose a event attribute (recommanded: org:resource)
      </option>
      <option v-for="(att, index) in attributes" :key="index">
        {{ att }}
      </option>
    </select>
    <label for="select-attribute">
      Selected event attribute: {{ selectedAtt }}
    </label>
  </div>
  <div class="col-md-3">
    <button
      type="button"
      class="btn btn-outline-primary"
      @click="transformation"
      :disabled="!selectedAtt"
    >
      Projection & Transformation
    </button>
  </div>

  <div class="col-md-4" v-if="Object.keys(projections).length > 0">
    <select
      v-model="selectedProjection"
      class="form-select"
      id="select-projection"
    >
      <option selected disabled value="">Choose a file</option>
      <option v-for="(number, tmp) in projections" :key="tmp">
        {{ tmp }}.csv
      </option>
    </select>
    <label for="select-projection">
      Selected projection: {{ selectedProjection }}
    </label>
  </div>
  <!-- <div class="col-md-4">
      <button
        type="button"
        class="btn btn-primary"
        @click="start_discovery"
        :disabled="!selectedProjection"
      >
        Start Discovery
      </button>
    </div> -->
  <div class="col-md-12">
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
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: {
    dataSet: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      attributes: {},
      selectedAtt: undefined,
      projections: {},
      selectedProjection: undefined,
      loading: false,
    };
  },
  methods: {
    get_attributes(val) {
      axios
        .get("projection_transformation/" + val)
        .then((res) => {
          this.attributes = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    transformation() {
      this.loading = true;
      axios
        .get(
          "projection_transformation/" + this.dataSet + "/" + this.selectedAtt
        )
        .then((res) => {
          this.loading = false;
          this.projections = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    // start_discovery() {
    //   let tmp =
    //     this.$router.currentRoute.value.fullPath +
    //     "/" +
    //     this.selectedProjection.substring(
    //       0,
    //       this.selectedProjection.lastIndexOf(".")
    //     );
    //   this.$router.push(tmp);
    // },
  },
  watch: {
    dataSet: function (val) {
      this.get_attributes(val);
      this.projections = {};
      this.selectedProjection = undefined;
    },
    selectedProjection: function (val) {
      if (val) {
        let tmp =
          "/iscmining-semi-automatic/" +
          this.dataSet +
          "/" +
          val.substring(0, val.lastIndexOf("."));
        this.$router.push(tmp);
      }
    },
    selectedAtt: function (val) {
      console.log(val);
      this.selectedProjection = undefined;
      this.projections = {};
      let tmp = "/iscmining-semi-automatic/" + this.dataSet;
      this.$router.push(tmp);
    },
  },
  created() {
    this.get_attributes(this.dataSet);
  },
};
</script>

<style lang=""></style>
