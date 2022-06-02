<template lang="">
  <div>
    <select class="form-select" aria-label="Default select example">
      <option selected>
        Choose a event attribute for dimenstion reduction
      </option>
      <option v-for="(att, index) in attributes" :key="index">{{ att }}</option>
    </select>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      dataSet: "",
      attributes: [],
    };
  },
  methods: {
    getAttributes() {
      const path =
        "http://localhost:5000/projectiontransformation" + this.dataSet;
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
  },
  created() {
    this.getAttributes();
  },
};
</script>

<style lang=""></style>
