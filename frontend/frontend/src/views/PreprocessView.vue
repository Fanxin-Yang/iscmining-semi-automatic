<template lang="">
  <form class="row g-3 border bg-light">
    <div class="col-md-12">
      <label for="perc" class="form-label"
        >Process Model Setting: {{ perc }}% <br />
        According to percentage, only the most frequent paths are retained. For
        the default value 0 the most frequent path is retrieved.</label
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

    <nav>
      <div class="nav nav-tabs" id="nav-tab" role="tablist">
        <button
          class="nav-link active"
          id="nav-home-tab"
          data-bs-toggle="tab"
          data-bs-target="#nav-home"
          type="button"
          role="tab"
          aria-controls="nav-home"
          aria-selected="true"
          @click="click(this.processLogs[0])"
        >
          {{ this.processLogs[0] }}
        </button>
        <button
          class="nav-link"
          :id="'nav-tab' + dataSet"
          data-bs-toggle="tab"
          :data-bs-target="'#nav-' + dataSet"
          type="button"
          role="tab"
          aria-controls="'nav-' + dataSet"
          aria-selected="false"
          v-for="(dataSet, index) in this.processLogs.slice(1)"
          :key="index"
          @click="click(dataSet)"
        >
          {{ dataSet }}
        </button>
      </div>
    </nav>
    <ProcessModel :dataSet="this.selectedLog" :perc="this.perc / 100" />
    <ProjectionTransformation :processLogs="this.processLogs" />
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
      perc: 0,
      processLogs: this.$route.params.dataSet.split("&"),
      selectedLog: undefined,
    };
  },
  methods: {
    click(dataSet) {
      this.selectedLog = dataSet;
    },
  },
  created() {
    this.selectedLog = this.processLogs[0];
  },
  watch: {
    "$route.params.dataSet": {
      handler: function (val) {
        this.processLogs = val.split("&");
      },
      deep: false,
      immediate: true,
    },
    processLogs: {
      handler: function (val) {
        this.selectedLog = val[0];
      },
      deep: true,
      immediate: true,
    },
  },
};
</script>

<style lang=""></style>
