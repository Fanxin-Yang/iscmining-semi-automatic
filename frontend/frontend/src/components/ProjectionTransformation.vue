<template lang="">
  <h3>Projection & Transformation</h3>
  <div class="col-md-6">
    <select v-model="selectedAtt" class="form-select">
      <option selected disabled value="">
        Choose a event attribute (recommanded org:resource)
      </option>
      <option v-for="(att, index) in attributes" :key="index">{{ att }}</option>
    </select>
    <div class="alert alert-light" role="alert">
      Selected event attribute: {{ selectedAtt }}
    </div>
  </div>
  <div class="col-md-4">
    <button
      type="button"
      class="btn btn-primary"
      @click="transformation"
      :disabled="selectedAtt == ''"
    >
      Start Transformation
    </button>
  </div>
  <div
    v-if="Object.keys(projections).length > 0"
    class="alert alert-success"
    role="alert"
  >
    There are {{ Object.keys(projections).length }} files saved.
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      attributes: {},
      selectedAtt: "",
    };
  },
  props: ["dataSet", "projections"],
  methods: {
    get_attributes() {
      // console.log(this.dataSet);
      const path =
        "http://localhost:5000/projection_transformation/" + this.dataSet;
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
      const path =
        "http://localhost:5000/projection_transformation/" +
        this.dataSet +
        "/" +
        this.selectedAtt;
      // console.log(path);
      axios
        .get(path)
        .then((res) => {
          this.$emit("update:projections", res.data);
          console.log(this.projections);
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.get_attributes();
  },
};
</script>

<style lang=""></style>
