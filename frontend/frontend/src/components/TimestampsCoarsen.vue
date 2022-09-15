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
      timestampsLevel: "Seconds",
      status: undefined,
      loading: false,
    };
  },
  emits: ["modify"],
  methods: {
    coarsen() {
      this.loading = true;
      axios
        .put(
          "discovery/" +
            this.dataSet +
            "/" +
            this.csv +
            "/" +
            this.timestampsLevel
        )
        .then((res) => {
          this.loading = false;
          this.status = res.data;
          let tmp =
            "/iscmining-semi-automatic/" +
            this.dataSet +
            "/" +
            this.csv +
            "/" +
            this.timestampsLevel;
          this.$router.push(tmp);
        })
        .catch((err) => {
          console.error(err);
        });
      this.$emit("modify");
    },
  },
  watch: {
    timestampsLevel: function (val) {
      console.log(val);
      this.coarsen();
    },
  },
  created() {
    let tmp =
      "/iscmining-semi-automatic/" + this.dataSet + "/" + this.csv + "/Seconds";
    this.$router.push(tmp);
  },
  // mounted() {
  //   this.$root.$on("call_coarsen", () => {
  //     this.coarsen();
  //   });
  // },
};
</script>

<style lang=""></style>
