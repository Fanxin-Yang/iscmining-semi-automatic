<template lang="">
  <form class="row g-3 border bg-light">
    <div v-if="Object.keys(this.events).length > 0">
      <ClassificationTechniquesWeka
        :dataSet="dataSet"
        :csv="csv"
        :labels="labels"
      />
      <ClassificationTechniquesScikit
        :labels="labels"
        @technique="update_technique"
      />
    </div>
    <div class="d-grid col-6 mx-auto">
      <div class="text-center" v-if="this.status == 1">
        <div class="spinner-border m-8" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <button
        v-else
        type="button"
        class="btn btn-primary btn-lg"
        @click="apply_scikit(undefined)"
        :disabled="
          !inputSamples ||
          inputSamples.length == 0 ||
          (applied[0] == technique &&
            applied[1] == classLabel &&
            applied[2] == inputSamples &&
            applied[3] == filter &&
            applied[4] == encoder)
        "
      >
        Apply Algorithm (Scikit)
      </button>
    </div>
    <div class="col-md-12" v-if="this.status == 405">
      <div class="alert alert-danger" role="alert">
        {{ msg }}
      </div>
    </div>

    <div
      class="row"
      v-else-if="this.status == 201 || this.status == 200 || this.status == 202"
    >
      <div v-if="this.status == 202" class="alert alert-warning" role="alert">
        The decision tree has too much nodes. Please select other parmaeters or
        try to prune the tree using different ccp_alpha value.
      </div>

      <DecisionTree
        :ccp_alphas="this.ccp_alphas"
        :dataSet="this.dataSet"
        :csv="this.csv"
        :status="this.status"
        @apply="apply_scikit"
      />
    </div>
  </form>
</template>

<script>
import axios from "axios";
import ClassificationTechniquesScikit from "../components/ClassificationTechniquesScikit.vue";
import ClassificationTechniquesWeka from "../components/ClassificationTechniquesWeka.vue";
import DecisionTree from "../components/DecisionTree.vue";
export default {
  components: {
    ClassificationTechniquesScikit,
    ClassificationTechniquesWeka,
    DecisionTree,
  },
  props: {
    dataSet: {
      type: String,
      required: true,
    },
    csv: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      events: {},
      labels: [],
      filter: {},
      technique: undefined,
      classLabel: undefined,
      inputSamples: undefined,
      encoder: "0",
      applied: [],
      status: undefined,
      msg: undefined,
      ccp_alphas: undefined,
    };
  },
  methods: {
    get_events(dataSet, csv) {
      let path = "/discovery/" + dataSet + "/" + csv + "_modified";
      axios
        .get(path)
        .then((res) => {
          this.events = res.data;
          this.labels = Object.keys(this.events[0]).filter(
            (value) => value != "No."
          );
        })
        .catch((err) => {
          this.status = err.response.status;
          this.msg = err.response.data;
        });
    },
    update_filter(selectedLabels) {
      this.filter = selectedLabels;
    },
    update_technique(
      selectedCT,
      selectedLabel,
      selectedSamples,
      selectedEncoder
    ) {
      this.technique = selectedCT;
      this.classLabel = selectedLabel;
      this.inputSamples = selectedSamples;
      this.encoder = selectedEncoder;
      this.ccp_alphas = undefined;
    },
    apply_scikit(ccp_alpha) {
      this.applied = [
        this.technique,
        this.classLabel,
        this.inputSamples,
        this.filter,
        this.encoder,
      ];
      this.status = 1;
      const params = new URLSearchParams([
        ["classLabel", this.classLabel],
        ["inputSamples", this.inputSamples],
        ["encoder", this.encoder],
      ]);
      if (ccp_alpha) {
        let ccp_alpha_float = parseFloat(ccp_alpha);
        params.append("ccp_alpha", ccp_alpha_float);
      }

      axios
        .get(
          "classification/" +
            this.dataSet +
            "/" +
            this.csv +
            "_modified/" +
            this.technique.replace(/\s+/g, "").toLowerCase(),
          { params }
        )
        .then((res) => {
          this.status = res.status;
          if (this.status == 201 || this.status == 202) {
            this.ccp_alphas = res.data;
          } else {
            this.msg = res.data;
          }
        })
        .catch((err) => {
          this.status = err.response.status;
          this.msg = err.response.data;
          console.error(err);
        });
    },
  },
  watch: {
    dataSet: function (val) {
      this.get_events(val, this.csv);
    },
    csv: function (val) {
      this.get_events(this.dataSet, val);
    },
  },
  created() {
    this.get_events(this.dataSet, this.csv);
  },
};
</script>

<style>
.table-responsive {
  max-height: 400px;
  margin-top: 20px;
}
.header {
  position: sticky;
  top: 0;
  background-color: lightgrey;
}
</style>
