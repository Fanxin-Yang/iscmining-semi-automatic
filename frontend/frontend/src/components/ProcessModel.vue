<template lang="">
  <div class="col-md-12 text-center" v-if="loading">
    <div class="spinner-border m-1" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <label
    v-else
    :for="'process-model-container' + this.dataSet"
    class="form-label"
    >Process model for {{ this.dataSet }}:</label
  >
  <div
    :id="'process-model-container' + this.dataSet"
    ref="container"
    class="vue-bpmn-diagram-container"
  ></div>
</template>

<script>
import axios from "axios";
import BpmnModeler from "bpmn-js/lib/Modeler";

export default {
  name: "vue-bpmn",
  props: {
    dataSet: {
      type: String,
      required: true,
    },
    // options: {
    //   type: Object,
    // },
    perc: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      diagramXML: null,
      loading: true,
    };
  },
  mounted: function () {
    var container = this.$refs.container;

    var self = this;
    var _options = Object.assign(
      {
        container: container,
        keyboard: {
          bindTo: window,
        },
        // textRenderer: {
        //   defaultStyle: {
        //     fontSize: "28px",
        //   },
        //   externalStyle: {
        //     fontSize: "32px",
        //   },
        // },
      }
      // this.options
    );
    this.bpmnViewer = new BpmnModeler(_options);

    this.bpmnViewer.on("import.done", function (event) {
      var error = event.error;
      var warnings = event.warnings;

      if (error) {
        self.$emit("error", error);
      } else {
        self.$emit("shown", warnings);
      }

      self.bpmnViewer.get("canvas").zoom("fit-viewport");
    });

    if (this.dataSet && this.perc) {
      this.fetchDiagram(this.dataSet, this.perc);
    }
  },
  beforeUnmount: function () {
    this.bpmnViewer.destroy();
  },
  watch: {
    dataSet: {
      handler: function (val) {
        this.loading = true;
        this.fetchDiagram(val, this.perc);
      },
      deep: true,
      immediate: true,
    },
    diagramXML: function (val) {
      this.bpmnViewer.importXML(val);
    },
    perc: function (val) {
      this.fetchDiagram(this.dataSet, val);
    },
  },
  methods: {
    fetchDiagram(dataSet, perc) {
      const params = new URLSearchParams([["perc", perc]]);
      axios
        .get("processmodel/" + dataSet, { params })
        .then((res) => {
          this.diagramXML = res.data;
          this.loading = false;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style>
.vue-bpmn-diagram-container {
  height: 500px;
  width: 100%;
}
</style>
