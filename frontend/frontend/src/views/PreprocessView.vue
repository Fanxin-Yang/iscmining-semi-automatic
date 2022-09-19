<template lang="">
  <form class="row g-3 border bg-light">
    <div class="col-md-12">
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
    </div>
    <div class="col-md-12">
      <ProcessModel
        :dataSet="this.$route.params.dataSet"
        :perc="this.perc / 100"
      />
    </div>
    <ProjectionTransformation :dataSet="this.$route.params.dataSet" />
  </form>
</template>

<script>
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
};
</script>

<style lang=""></style>
