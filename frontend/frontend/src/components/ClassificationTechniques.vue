<template lang="">
  <h6>Choose a Classificaton Technique.</h6>
  <div class="row">
    <div class="col-md-8">
      <select v-model="selectedCT" class="form-select">
        <option selected disabled value="">
          Choose a Classificaton Technique
        </option>
        <option v-for="(ct, index) in classificationTechniques" :key="index">
          {{ ct }}
        </option>
      </select>
      <div class="alert alert-light" role="alert">
        Selected classification technique: {{ selectedCT }}
      </div>
    </div>
    <div class="col-md-3">
      <button
        type="button"
        class="btn btn-outline-primary"
        @click="apply_classification"
        :disabled="!selectedCT"
      >
        Apply
      </button>
    </div>
  </div>
  <!-- <div class="alert alert-success" role="alert" v-if="!!status">
    {{ status }}
  </div> -->
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      selectedCT: undefined,
      classificationTechniques: undefined,
    };
  },
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
        this.selectedCT;
      console.log(path);
      axios
        .put(path)
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
          console.log(res.data);
          this.classificationTechniques = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
  created() {
    this.get_classification_techniques();
  },
};
</script>

<style lang=""></style>
