<template lang="">
  <label for="classification-technique-weka"
    >Choose a Classificaton Technique (Weka).</label
  >
  <div class="col-md-12">
    <select
      v-model="selectedCT"
      class="form-select"
      id="classification-technique-weka"
      aria-label="techniqueHelp"
    >
      <option v-for="(ct, index) in classificationTechniques" :key="index">
        {{ ct }}
      </option>
    </select>
    <div id="techniqueHelp" class="form-text" v-if="selectedCT == 'JRip'">
      {{ this.algDescription }}

      The selected algorithm: {{ selectedCT }} hasn't been implemented yet.
      Please select Decision Tree Algorithm for now.
    </div>
  </div>
  <div v-if="selectedCT == 'JRip'" class="row">
    <div class="col-md-6">
      <!-- <label for="attribute-JRip" class="form-label"
        >Select the attribute to use as the class</label
      > -->
      <select
        v-model="selectedLabel"
        class="form-select"
        id="attributes-JRip"
        aria-label="attributes-JRip-Help"
      >
        <option v-for="(l, index) in labels" :key="index">
          {{ l }}
        </option>
      </select>
      <div id="attributes-JRip-Help" class="form-text">
        Select the attribute to use as the class
      </div>
    </div>
    <div class="col-md-3">
      <div class="form-check form-switch">
        <input
          v-model="usePruning"
          class="form-check-input"
          type="checkbox"
          role="switch"
          id="usePruning-check"
          checked
        />
        <label class="form-check-label" for="usePruning-check"
          >usePruning: {{ usePruning }}</label
        >
      </div>
    </div>
  </div>
  <div v-if="selectedCT" class="d-grid col-6 mx-auto gap-2">
    <button
      type="button"
      class="btn btn-primary btn-lg"
      @click="apply_weka"
      :disabled="!selectedCT"
    >
      Apply Algorithm (Weka)
    </button>
  </div>
  <div class="text-center" v-if="this.status == 1">
    <div class="spinner-border m-8" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div class="col-md-12" v-else-if="this.status == 200">
    <DecisionRule
      :dataSet="this.dataSet"
      :csv="this.csv"
      :status="this.status"
      :alg="this.selectedCT"
      :refresh="this.cacheKey"
    />
    <div class="alert alert-success" role="alert">
      {{ msg }}
    </div>
  </div>
  <div class="col-md-12" v-else-if="this.status == 405">
    <div class="alert alert-danger" role="alert">
      {{ msg }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
import DecisionRule from "./DecisionRule.vue";
export default {
  components: {
    DecisionRule,
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
    labels: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      selectedCT: undefined,
      classificationTechniques: undefined,
      algDescription: undefined,
      selectedLabel: "concept:name",
      msg: undefined,
      status: undefined,
      usePruning: true,
      cacheKey: +new Date(),
    };
  },
  methods: {
    get_classification_techniques() {
      axios
        .get("/classification_weka")
        .then((res) => {
          this.classificationTechniques = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    apply_weka() {
      this.status = 1;
      let tmp = "";
      if (this.selectedCT == "JRip") {
        tmp = "-F 3 -N 2.0 -O 2 -S 1";
        if (this.usePruning == false) {
          tmp += " -P";
        }
      }
      const params = new URLSearchParams([
        ["cls_options", tmp],
        ["class_name", this.selectedLabel],
      ]);
      axios
        .get(
          "/classification_weka/" +
            this.dataSet +
            "/" +
            this.csv +
            "_modified/" +
            "/" +
            this.selectedCT,
          { params }
        )
        .then((res) => {
          this.msg = res.data;
          this.status = res.status;
          this.cacheKey = +new Date();
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  watch: {
    selectedCT: function (val) {
      axios
        .get("/alg_description/" + val)
        .then((res) => {
          this.algDescription = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.get_classification_techniques();
  },
  mounted() {
    window.scrollTo(
      0,
      document.body.scrollHeight || document.documentElement.scrollHeight
    );
  },
};
</script>

<style lang=""></style>
