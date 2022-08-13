<template lang="">
  <form class="row g-3">
    <h3 class="display-4">Pre-process: {{ this.$route.params.dataSet }}</h3>

    <div class="col-md-12">
      <ProcessModel
        :url="
          'http://localhost:5000/processmodel/' +
          this.$route.params.dataSet +
          '.bpmn'
        "
      />
    </div>
    <div class="col-md-12">
      <ProjectionTransformation />
    </div>
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
};
</script>

<style lang=""></style>
