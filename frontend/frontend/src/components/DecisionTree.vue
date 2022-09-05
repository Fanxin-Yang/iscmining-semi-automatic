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
  <!-- <div class="alert alert-success" role="alert">
        <div v-if="this.status == 200">{{ msg }}</div>
        <div v-else-if="this.status == 201">
          Decision tree with default parameters. You can choose other ccp_alpha
          value to prune the decision tree.
        </div>
      </div> -->
  <img
    :src="
      'http://localhost:5000/decisiontree/' +
      dataSet +
      '/' +
      csv +
      '_' +
      level +
      '?cache=' +
      this.cacheKey
    "
    class="img-fluid"
    v-if="this.ccp_alphas"
  />
</template>

<script>
export default {
  data() {
    return {
      ccp_alpha: undefined,
      cacheKey: +new Date(),
    };
  },
  props: {
    ccp_alphas: {
      type: Array,
      required: true,
    },
    dataSet: {
      type: String,
      required: true,
    },
    csv: {
      type: String,
      required: true,
    },
    level: {
      type: String,
      required: true,
    },
  },
  emits: ["apply"],
  methods: {
    apply_ccp() {
      this.cacheKey = +new Date();
      this.$emit("apply", this.ccp_alpha);
    },
  },
};
</script>

<style lang=""></style>
