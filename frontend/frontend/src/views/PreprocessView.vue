<template lang="">
  <form class="row g-3">
    <h3 class="display-4">Pre-process: {{ this.$route.params.dataSet }}</h3>
    <label for="perc" class="form-label"
      >Process Model Settings: {{ perc }}%</label
    >
    <input
      type="range"
      class="form-range"
      v-model="perc"
      min="0"
      max="100"
      step="5"
      id="perc"
    />
    <div class="col-md-12">
      <ProcessModel
        :dataSet="this.$route.params.dataSet"
        :perc="this.perc / 100"
      />
    </div>
    <div class="col-md-12">
      <ProjectionTransformation />
    </div>
  </form>
</template>

<script>
// import axios from "axios";
import ProcessModel from "../components/ProcessModel.vue";
import ProjectionTransformation from "../components/ProjectionTransformation.vue";
export default {
  components: {
    ProcessModel,
    ProjectionTransformation,
  },
  data() {
    return {
      perc: 100,
    };
  },
  // methods: {
  //   getProcessModel() {
  //     const params = new URLSearchParams([["perc", this.perc]]);
  //     axios
  //       .get("processmodel/" + this.$route.params.dataSet, { params })
  //       .then((res) => {
  //         console.log(res.data);
  //       })
  //       .catch((err) => {
  //         console.error(err);
  //       });
  //   },
  // },
};
</script>

<style lang=""></style>
