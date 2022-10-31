<template lang="">
  <label for="ccp_alphas" v-if="this.ccp_alphas"
    >Choose a ccp_alpha value</label
  >
  <div class="col-md-8">
    <!-- <label for="ccp_alphas" class="form-label">ccp_alphas</label> -->
    <select
      v-model="this.ccp_alpha"
      class="form-select"
      id="ccp_alphas"
      aria-label="ccp_alphasHelp"
    >
      <option v-for="(c, index) in ccp_alphas" :key="index">
        {{ c }}
      </option>
    </select>
    <div id="ccp_alphasHelp" class="form-text">
      Greater values of ccp_alpha increase the number of nodes pruned.
      <br />
      More details:
      <a
        target="_blank"
        href="https://scikit-learn.org/stable/auto_examples/tree/plot_cost_complexity_pruning.html"
        >Post pruning decision trees with cost complexity pruning.</a
      >
    </div>
  </div>
  <div class="col-md-3">
    <button
      type="button"
      class="btn btn-outline-primary btn-lg"
      @click="apply_ccp"
      :disabled="!this.ccp_alpha"
    >
      Pruning
    </button>
  </div>

  <img
    :src="
      'http://127.0.0.1:5000/decisiontree/' +
      dataSet +
      '/' +
      csv +
      '_modified' +
      '?cache=' +
      this.cacheKey
    "
    class="img-fluid"
    v-if="this.status == 200 || this.status == 201"
  />

  <div
    class="table-responsive"
    id="rules-table"
    v-if="this.status == 200 || this.status == 201"
  >
    <table class="table table-striped table-hover table-sm table-bordered">
      <thead class="header">
        <tr>
          <th scope="col"></th>
          <th>Decision Rules</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(rule, index) in rules" :key="index">
          <th scope="row">
            {{ index }}
          </th>
          {{
            rule
          }}
        </tr>
      </tbody>
    </table>
  </div>

  <!-- <button
    type="button"
    class="btn btn-primary btn-lg"
    @click="download"
    :disabled="!this.ccp_alpha"
  >
    Download Results as PDF
  </button> -->
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      ccp_alpha: undefined,
      rules: {},
      selectedRules: new Array(),
      cacheKey: +new Date(),
    };
  },
  props: {
    ccp_alphas: {
      // type: Object,
      // required: true,
    },
    dataSet: {
      type: String,
      required: true,
    },
    csv: {
      type: String,
      required: true,
    },
    status: {
      type: Number,
      required: true,
    },
  },
  emits: ["apply"],
  methods: {
    get_decisiionrules(dataSet, csv) {
      axios
        .get("decisionrule/" + dataSet + "/" + csv + "_modified")
        .then((res) => {
          this.rules = res.data;
        })
        .catch((err) => {
          console.error(err);
          this.error = err.response.data;
        });
    },
    apply_ccp() {
      this.cacheKey = +new Date();
      this.$emit("apply", this.ccp_alpha);
    },
  },
  created() {
    this.get_decisiionrules(this.dataSet, this.csv);
  },
};
</script>

<style lang=""></style>
