<template lang="">
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
  <div v-if="classifiers == {}" class="alert alert-success" role="alert">
    There are {{ Object.keys(classifiers).length }} files saved.
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      attributes: {},
      selectedAtt: "",
      classifiers: {},
    };
  },
  props: ["dataSet"],
  methods: {
    getAttributes() {
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
      console.log(this.selectedAtt);
      const path =
        "http://localhost:5000/projection_transformation/" +
        this.dataSet +
        "/" +
        this.selectedAtt;
      console.log(path);
      axios
        .get(path)
        .then((res) => {
          // console.log(res.data);
          this.attributes = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.getAttributes();
  },
};
</script>

<style lang=""></style>
