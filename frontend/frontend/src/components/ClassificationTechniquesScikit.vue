<template lang="">
  <label for="classification-technique-scikit"
    >Choose a Classificaton Technique (Scikit-learn).</label
  >
  <div class="col-md-12">
    <select
      v-model="selectedCT"
      class="form-select"
      id="classification-technique-scikit"
      aria-label="techniqueHelp"
    >
      <!-- <option selected disabled value="">
        Choose a Classificaton Technique
      </option> -->
      <option v-for="(ct, index) in classificationTechniques" :key="index">
        {{ ct }}
      </option>
    </select>
    <div
      id="techniqueHelp"
      class="form-text"
      v-if="selectedCT == 'Decision Tree'"
    >
      <a
        target="_blank"
        href="https://scikit-learn.org/stable/modules/tree.html"
        >Decision Trees (DTs)</a
      >
      are a non-parametric supervised learning method used for classification
      and regression. The goal is to create a model that predicts the value of a
      target variable by learning simple decision rules inferred from the data
      features. A tree can be seen as a piecewise constant approximation.
    </div>
    <div v-else>
      The selected algorithm: {{ selectedCT }} hasn't been implemented yet.
      Please select Decision Tree Algorithm for now.
    </div>
  </div>
  <div v-if="selectedCT == 'Decision Tree'" class="row">
    <div class="col-md-4">
      <label for="label" class="form-label">Target (class label)</label>
      <select
        v-model="selectedLabel"
        class="form-select"
        id="label"
        aria-label="labelHelp"
      >
        <option v-for="(l, index) in labels" :key="index">
          {{ l }}
        </option>
      </select>
      <div id="labelHelp" class="form-text">
        Choose an attribute whose values are to be modeled and classified by
        others.
      </div>
    </div>
    <div class="col-md-4">
      <label for="training" class="form-label">Input</label>

      <select
        v-model="selectedSamples"
        class="form-select"
        id="training"
        multiple
        aria-label="trainingHelp"
        :disabled="!selectedLabel"
      >
        <option
          v-for="(s, index) in labels"
          :key="index"
          :disabled="s == selectedLabel"
        >
          {{ s }}
        </option>
      </select>
      <div id="trainingHelp" class="form-text">
        Choose one or more attributes that will be used to calssify the target
        values.
      </div>
    </div>
    <div class="col-md-3">
      <label for="encoder" class="form-label">Encoder</label>
      <select
        v-model="selectedEncoder"
        class="form-select"
        id="encoder"
        aria-label="encoderHelp"
        :disabled="selectedSamples.length == 0"
      >
        <option value="0">Ordinal Encoder</option>
        <option value="1">One-Hot Encoder</option>
      </select>
      <div v-if="selectedEncoder == '0'" id="encoderHelp" class="form-text">
        <a
          target="_blank"
          href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OrdinalEncoder.html#sklearn.preprocessing.OrdinalEncoder"
          >Ordinal Encoder</a
        >
        is suitable for categorical variables with ordinal relationship.
      </div>
      <div
        v-else-if="selectedEncoder == '1'"
        id="encoderHelp"
        class="form-text"
      >
        <a
          target="_blank"
          href="https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html?highlight=encoder#sklearn.preprocessing.OneHotEncoder"
          >One-Hot Encoder</a
        >
        is suitable for categorical variables without ordinal relationship.
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      selectedCT: undefined,
      classificationTechniques: undefined,
      selectedLabel: undefined,
      selectedSamples: [],
      msg: undefined,
      status: undefined,
      selectedEncoder: "0",
    };
  },
  props: ["labels"],
  emits: ["technique"],
  methods: {
    get_classification_techniques() {
      axios
        .get("/classification_scikit")
        .then((res) => {
          this.classificationTechniques = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  watch: {
    selectedCT: function (val) {
      this.status = 0;
      this.$emit(
        "technique",
        val,
        this.selectedLabel,
        this.selectedSamples,
        this.selectedEncoder
      );
    },
    selectedLabel: function (val) {
      this.status = 0;
      this.$emit(
        "technique",
        this.selectedCT,
        val,
        this.selectedSamples,
        this.selectedEncoder
      );
    },
    selectedSamples: function (val) {
      this.status = 0;
      this.$emit(
        "technique",
        this.selectedCT,
        this.selectedLabel,
        val,
        this.selectedEncoder
      );
    },
    selectedEncoder: function (val) {
      this.status = 0;
      this.$emit(
        "technique",
        this.selectedCT,
        this.selectedLabel,
        this.selectedSamples,
        val
      );
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
