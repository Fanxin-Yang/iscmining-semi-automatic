<template lang="">
  <div class="col-md-3" v-if="Object.keys(commonArr).length > 0">
    <select v-model="selectedAtt" class="form-select" id="select-attribute">
      <option selected disabled value="">
        Choose a event attribute (recommanded: org:resource)
      </option>
      <option v-for="(att, index) in commonArr" :key="index">
        {{ att }}
      </option>
    </select>
    <label for="select-attribute">
      Selected event attribute: {{ selectedAtt }}
    </label>
  </div>
  <div class="col-md-3" v-if="Object.keys(commonArr).length > 0">
    <button
      type="button"
      class="btn btn-outline-primary"
      @click="transformation"
      :disabled="!selectedAtt"
    >
      Projection & Transformation
    </button>
  </div>

  <div class="col-md-3" v-if="Object.keys(projections).length > 0">
    <select
      v-model="selectedProjection"
      multiple
      class="form-select"
      id="select-projection"
    >
      <!-- <option selected disabled value="">Choose a file</option> -->
      <option v-for="(tmp, index) in projections" :key="index">
        {{ tmp }}
      </option>
    </select>
    <label for="select-projection"> Selected: {{ selectedProjection }} </label>
  </div>
  <div class="col-md-3" v-if="Object.keys(selectedProjection).length >= 1">
    <button
      type="button"
      class="btn btn-primary"
      @click="start_discovery"
      :disabled="!selectedProjection"
    >
      Merge & Start Discovery
    </button>
  </div>

  <div class="col-md-12">
    <div
      class="text-center"
      v-if="loading && Object.keys(projections).length == 0"
    >
      <div class="spinner-border m-5" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-else-if="mergeInfo" class="alert alert-success" role="alert">
      {{ mergeInfo }}
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
    processLogs: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      attributes: {},
      commonArr: new Array(),
      selectedAtt: undefined,
      projections: new Array(),
      selectedProjection: new Array(),
      loading: false,
      mergeInfo: undefined,
    };
  },
  methods: {
    get_common_attributes(val) {
      for (var i = 0; i < val.length; ++i) {
        const log = val[i];
        axios
          .get("projection_transformation/" + log)
          .then((res) => {
            if (Object.values(this.processLogs).includes(log)) {
              this.attributes[log] = Object.values(res.data);
              this.commonArr = Object.values(res.data);
            }
          })
          .catch((err) => {
            console.error(err);
          });
      }
    },
    transformation() {
      this.projections = new Array();
      this.selectedProjection = new Array();
      for (var i = 0; i < Object.keys(this.attributes).length; ++i) {
        this.loading = true;
        const log = Object.keys(this.attributes)[i];
        axios
          .get("projection_transformation/" + log + "/" + this.selectedAtt)
          .then((res) => {
            this.loading = false;
            for (let i = 0; i < Object.values(res.data).length; i++) {
              if (!this.projections.includes(Object.values(res.data)[i])) {
                this.projections.push(...Object.values(res.data));
              }
            }
            // this.projections.push(...Object.values(res.data));
          })
          .catch((err) => {
            console.error(err);
          });
      }
    },
    start_discovery() {
      let tmp = "";
      for (var i = 0; i < Object.keys(this.selectedProjection).length; ++i) {
        if (i != 0) {
          tmp += "&";
        }
        tmp += this.selectedProjection[i].split(" ").join("_");
      }
      let url =
        "/iscmining-semi-automatic/" + this.processLogs.join("&") + "/" + tmp;
      if (
        Object.keys(this.selectedProjection).length == 1 &&
        Object.keys(this.processLogs).length == 1
      ) {
        this.$router.push(url);
      } else {
        axios
          .get("merge/" + this.processLogs.join("&") + "/" + tmp)
          .then((res) => {
            this.loading = false;
            this.mergeInfo = res.data;
            this.$router.push(url);
          })
          .catch((err) => {
            console.error(err);
          });
      }
    },
  },
  watch: {
    processLogs: function (val) {
      this.commonArr = new Array();
      this.attributes = {};
      this.get_common_attributes(val);
    },
    attributes: {
      handler: function (val) {
        for (const log in val) {
          this.commonArr = this.commonArr.filter((att) =>
            this.attributes[log].includes(att)
          );
        }
        this.selectedAtt = undefined;
      },
      deep: true,
      immediate: true,
    },
    selectedProjection: {
      handler: function () {
        this.mergeInfo = undefined;
        let tmp = "/iscmining-semi-automatic/" + this.processLogs.join("&");
        this.$router.push(tmp);
      },
      deep: true,
      immediate: true,
    },
    selectedAtt: function () {
      if (Object.keys(this.selectedProjection).length != 0) {
        this.selectedProjection = new Array();
      }
      if (Object.keys(this.projections).length != 0) {
        this.projections = new Array();
      }
    },
  },
  created() {
    this.get_common_attributes(this.processLogs);
  },
};
</script>

<style lang=""></style>
