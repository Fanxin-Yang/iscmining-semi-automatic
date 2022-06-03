<template lang="">
  <div class="col-md-6">
    <select v-model="selectedAtt" class="form-select">
      <option selected disabled value="">
        Choose a event attribute (recommand org:resource)
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
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      attributes: [],
      selectedAtt: "",
    };
  },
  props: ["dataSet"],
  methods: {
    getAttributes() {
      console.log(this.dataSet);
      const path =
        "http://localhost:5000/projection_transformation/" + this.dataSet;
      axios
        .get(path)
        .then((res) => {
          console.log(res.data);
          this.attributes = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    transformation() {},
  },
  created() {
    this.getAttributes();
  },
};
</script>

<style lang=""></style>
