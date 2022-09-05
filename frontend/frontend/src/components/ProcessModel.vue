<template lang="">
  <label for="process-model-container" class="form-label">Process Model</label>
  <div
    id="process-model-container"
    ref="container"
    class="vue-bpmn-diagram-container"
  ></div>
  <!-- <img
      :src="
        'http://localhost:5000/processmodels/' +
        this.$route.params.dataSet +
        '.png'
      "
      class="img-fluid"
    /> -->
</template>

<script>
import axios from "axios";
// import BpmnViewer from "bpmn-js/dist/bpmn-modeler.development.js";
// import BpmnViewer from "bpmn-js/dist/bpmn-modeler.production.min.js";
// import BpmnViewer from "bpmn-js/lib/NavigatedViewer";
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
    dataSet: function (val) {
      this.$emit("loading");
      this.fetchDiagram(val, this.perc);
    },
    diagramXML: function (val) {
      this.bpmnViewer.importXML(val);
    },
    perc: function (val) {
      this.$emit("loading");
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
