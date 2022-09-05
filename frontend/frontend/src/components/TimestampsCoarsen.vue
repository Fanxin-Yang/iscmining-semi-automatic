<template lang="">
  <label for="select-timestamps-level">Choose a Timestamps Level.</label>
  <div class="col-md-8">
    <select
      v-model="timestampsLevel"
      class="form-select"
      id="select-timestamps-level"
    >
      <option selected>Seconds</option>
      <option>Minutes</option>
      <option>Hours</option>
      <option>Days</option>
      <option>Months</option>
      <option>Years</option>
    </select>
  </div>
  <div class="col-md-12 text-center" v-if="loading">
    <div class="spinner-border m-5" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div class="col-md-12">
    <div class="alert alert-success" role="alert" v-if="!!status">
      {{ status }}
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
    csv: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      timestampsLevel: undefined,
      status: undefined,
      loading: false,
    };
  },
  methods: {
    coarsen(dataSet, csv, timestampsLevel) {
      this.loading = true;
      axios
        .put("discovery/" + dataSet + "/" + csv + "/" + timestampsLevel)
        .then((res) => {
          this.loading = false;
          this.status = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  watch: {
    csv: function (val) {
      this.coarsen(this.dataSet, val, this.timestampsLevel);
    },
    timestampsLevel: function (val) {
      this.coarsen(this.dataSet, this.csv, val);
      let tmp =
        "/iscmining-semi-automatic/" +
        this.dataSet +
        "/" +
        this.csv +
        "/" +
        val;
      this.$router.push(tmp);
    },
  },
};
</script>

<style lang=""></style>
