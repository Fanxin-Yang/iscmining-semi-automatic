<template lang="">
  <h3>Process Model (Petri Net)</h3>
  <div ref="container" class="vue-bpmn-diagram-container"></div>
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
// import axios from "axios";
import BpmnJS from "bpmn-js/dist/bpmn-navigated-viewer.production.min.js";

export default {
  name: "vue-bpmn",
  props: {
    url: {
      type: String,
      required: true,
    },
    options: {
      type: Object,
    },
  },
  data() {
    return {
      // bpmn: undefined,
      diagramXML: null,
    };
  },
  mounted: function () {
    var container = this.$refs.container;

    var self = this;
    var _options = Object.assign(
      {
        container: container,
      },
      this.options
    );
    this.bpmnViewer = new BpmnJS(_options);

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

    if (this.url) {
      this.fetchDiagram(this.url);
    }
  },
  beforeUnmount: function () {
    this.bpmnViewer.destroy();
  },
  watch: {
    url: function (val) {
      this.$emit("loading");
      this.fetchDiagram(val);
    },
    diagramXML: function (val) {
      this.bpmnViewer.importXML(val);
    },
  },
  methods: {
    // getBPMN() {
    //   axios
    //     // .get("processmodels/" + this.$route.params.dataSet + ".bpmn")
    //     .get("/pm4pytest")
    //     .then((res) => {
    //       this.bpmn = res.data;
    //       console.log(this.bpmn);
    //     })
    //     .catch((err) => {
    //       this.status = err.response.status;
    //       this.msg = err.response.data;
    //     });
    // },
    fetchDiagram: function (url) {
      var self = this;

      fetch(url)
        .then(function (response) {
          return response.text();
        })
        .then(function (text) {
          self.diagramXML = text;
        })
        .catch(function (err) {
          self.$emit("error", err);
        });
    },
  },
  // created() {
  //   this.getBPMN();
  // },
};
</script>

<style>
.vue-bpmn-diagram-container {
  height: 500px;
  width: 100%;
}
</style>
