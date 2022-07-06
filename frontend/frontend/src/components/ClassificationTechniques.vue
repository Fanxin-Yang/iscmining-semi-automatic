<template lang="">
  <h6>Choose a Classificaton Technique.</h6>
  <div class="row">
    <div class="mb-3">
      <select
        v-model="selectedCT"
        class="form-select"
        id="technique"
        aria-label="techniqueHelp"
      >
        <option selected disabled value="">
          Choose a Classificaton Technique
        </option>
        <option v-for="(ct, index) in classificationTechniques" :key="index">
          {{ ct }}
        </option>
      </select>
      <div id="techniqueHelp" class="form-text">
        Selected classification technique: {{ selectedCT }}
      </div>
    </div>
  </div>
  <form v-if="!!selectedCT">
    <div class="mb-3">
      <label for="label" class="form-label"
        >The target values (class labels)</label
      >
      <select
        v-model="selectedLabel"
        class="form-select"
        id="label"
        aria-label="labelHelp"
      >
        <!-- <option disabled selected>Choose a class label</option> -->
        <option v-for="(l, index) in labels" :key="index">
          {{ l }}
        </option>
      </select>
      <div id="labelHelp" class="form-text">
        y: array-like of shape (n_samples,) or (n_samples, n_outputs)
      </div>
    </div>
    <div class="mb-3">
      <label for="training" class="form-label"
        >The training input samples</label
      >
      <select
        v-model="selectedSamples"
        class="form-select"
        id="training"
        multiple
        aria-label="trainingHelp"
        :disabled="!selectedLabel"
      >
        <!-- <option disabled selected>
          Drag or use Ctrl to select multiple samples
        </option> -->
        <option
          v-for="(s, index) in labels"
          :key="index"
          :disabled="s == selectedLabel"
        >
          {{ s }}
        </option>
      </select>
      <div id="trainingHelp" class="form-text">
        X: {array-like, sparse matrix} of shape (n_samples, n_features)
      </div>
    </div>
  </form>
  <div class="row" v-if="selectedCT == 'Decision Tree'">
    <form>
      <div class="mb-3">
        Decision Trees (DTs) are a non-parametric supervised learning method
        used for classification and regression. The goal is to create a model
        that predicts the value of a target variable by learning simple decision
        rules inferred from the data features. A tree can be seen as a piecewise
        constant approximation.
      </div>
      <button
        type="button"
        class="btn btn-primary"
        @click="apply"
        :disabled="selectedSamples.length == 0"
      >
        <!-- type="button" default: submit, which refreshes the page -->
        Apply
      </button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      selectedCT: undefined,
      classificationTechniques: undefined,
      labels: [],
      selectedLabel: undefined,
      selectedSamples: [],
    };
  },
  props: ["events"],
  methods: {
    apply() {
      const path =
        "http://localhost:5000/discovery/" +
        this.$route.params.dataSet +
        "/" +
        this.$route.params.csv +
        "_" +
        this.$route.params.level +
        "/" +
        this.selectedCT.replace(/\s+/g, "").toLowerCase();
      const params = new URLSearchParams([
        ["selectedLabel", this.selectedLabel],
        ["selectedSamples", this.selectedSamples],
      ]);
      axios
        .get(path, { params })
        .then((res) => {
          this.status = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    get_classification_techniques() {
      const path = "http://localhost:5000/discovery";
      axios
        .get(path)
        .then((res) => {
          this.classificationTechniques = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.get_classification_techniques();
    const list = Object.keys(this.events[0]);
    for (let i = 0; i < list.length; i++) {
      if (list[i] != "No." && list[i] != "case:concept:name") {
        this.labels.push(list[i]);
      }
    }
  },
};
</script>

<style lang=""></style>
