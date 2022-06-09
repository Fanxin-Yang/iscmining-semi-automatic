<template lang="">
  <h3>ISC Discovery Algorithm</h3>
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
      :disabled="selectedProjection == ''"
    >
      Start Discovery
    </button>
  </div>
</template>

<script>
import axios from "axios";

// import axios from "axios";
export default {
  data() {
    return {
      selectedProjection: "",
    };
  },
  props: ["dataSet", "projections"],
  methods: {
    start_discovery() {
      const path =
        "http://localhost:5000/discovery/" +
        this.dataSet +
        "/" +
        this.selectedProjection;
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    determine_r() {},
    timestamps() {},
    remove_events() {},
    get_classifications() {},
    apply_classifications() {},
  },
  created() {
    this.get_classifications();
  },
};
</script>

<style lang=""></style>
