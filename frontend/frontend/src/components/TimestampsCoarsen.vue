<template lang="">
  <h6>Choose a Timestamps Level.</h6>
  <div class="row">
    <div class="col-md-6">
      <select v-model="timestampsLevel" class="form-select">
        <option selected>Seconds</option>
        <option>Minutes</option>
        <option>Hours</option>
        <option>Days</option>
        <option>Months</option>
        <option>Years</option>
      </select>
      <div class="alert alert-light" role="alert">
        Selected timestamps level: {{ timestampsLevel }}
      </div>
    </div>
    <div class="col-md-4">
      <button
        type="button"
        class="btn btn-outline-primary"
        @click="coarsen"
        :disabled="!timestampsLevel"
      >
        Timestamps Coarsen
      </button>
    </div>
  </div>
  <div class="alert alert-success" role="alert" v-if="!!status">
    {{ status }}
  </div>
  <button type="button" class="btn btn-primary" @click="next_step">
    Next Step
  </button>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      timestampsLevel: "Seconds",
      status: undefined,
    };
  },
  methods: {
    coarsen() {
      const path =
        "http://localhost:5000/discovery/" +
        this.$route.params.dataSet +
        "/" +
        this.$route.params.csv +
        "/" +
        this.timestampsLevel;
      axios
        .put(path)
        .then((res) => {
          this.status = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    next_step() {
      let tmp =
        this.$router.currentRoute.value.fullPath + "/" + this.timestampsLevel;
      this.$router.push(tmp);
    },
  },
};
</script>

<style lang=""></style>
