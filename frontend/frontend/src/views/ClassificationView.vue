<template lang="">
  <form class="row g-5">
    <h3 class="display-4">Classification Algorithm</h3>
    <!-- <div class="col-md-12">
      <p class="h6">Dataset: {{ this.$route.params.dataSet }}</p>
      <p class="h6">Classifier: {{ this.$route.params.csv }}</p>
      <div class="text-center" v-if="Object.keys(events).length == 0">
        <div class="spinner-border m-5" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <div
        class="table-responsive"
        v-else-if="Object.keys(this.events).length > 0"
      >
        <table class="table table-striped table-hover table-sm table-bordered">
          <thead class="header">
            <tr>
              <th scope="col"></th>
              <th v-for="(index, value) in events[0]" :key="index">
                {{ value }}
                <div class="dropdown">
                  <a
                    v-if="value != 'case:concept:name'"
                    class="dropdown-toggle"
                    href="#"
                    role="button"
                    id="dropdownMenuLink"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  >
                    {{ value }}
                  </a>
                  <ul
                    class="dropdown-menu"
                    aria-labelledby="dropdownMenuButton1"
                  >
                    <li><a class="dropdown-item" href="#">Action</a></li>
                  </ul>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(event, index) in events" :key="index">
              <th scope="row"></th>
              <td v-for="(value, key) in event" :key="key">{{ value }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div> -->
    <div class="col-md-12" v-if="Object.keys(this.events).length > 0">
      <ValueSelection :labels="labels" @filter="update_filter" />
    </div>
    <div class="col-md-12" v-if="Object.keys(this.events).length > 0">
      <ClassificationTechniques
        :labels="labels"
        @technique="update_technique"
      />
    </div>
    <div class="d-grid col-4 mx-auto">
      <div class="text-center" v-if="this.status == 1">
        <div class="spinner-border m-8" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <button
        v-else
        type="button"
        class="btn btn-primary btn-lg"
        @click="apply"
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
        Apply {{ technique }} Algorithm
      </button>
    </div>
    <div class="col-md-12" v-if="this.status == 405">
      <div class="alert alert-danger" role="alert">
        {{ msg }}
      </div>
    </div>
    <div class="col-md-12" v-else-if="this.status == 201 || this.status == 200">
      <div class="row" v-if="this.ccp_alphas">
        <div class="col-8">
          <label for="ccp_alphas" class="form-label">ccp_alphas</label>
          <select
            v-model="ccp_alpha"
            class="form-select"
            id="ccp_alphas"
            aria-label="ccp_alphasHelp"
            @change="change"
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
        <div class="col-3">
          <button
            type="button"
            class="btn btn-primary btn-lg"
            @click="apply"
            :disabled="!ccp_alpha"
          >
            Pruning
          </button>
        </div>
      </div>
      <div class="alert alert-success" role="alert">
        <div v-if="this.status == 200">{{ msg }}</div>
        <div v-else-if="this.status == 201">
          Decision tree with default parameters. You can choose other ccp_alpha
          value to prune the decision tree.
        </div>
      </div>
      <img
        :src="
          'http://localhost:5000/decisiontree/' +
          this.$route.params.dataSet +
          '/' +
          this.$route.params.csv +
          '_' +
          this.$route.params.level +
          '?cache=' +
          this.cacheKey
        "
        class="img-fluid"
      />
    </div>
  </form>
</template>

<script>
import axios from "axios";
import ClassificationTechniques from "../components/ClassificationTechniques.vue";
import ValueSelection from "../components/ValueSelection.vue";
export default {
  components: {
    ClassificationTechniques,
    ValueSelection,
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
      ccp_alpha: undefined,
      cacheKey: +new Date(),
    };
  },
  methods: {
    get_events() {
      let path =
        "http://localhost:5000/discovery/" +
        this.$route.params.dataSet +
        "/" +
        this.$route.params.csv;
      if (this.$route.params.level != "Seconds") {
        path = path + "_" + this.$route.params.level;
      }
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
      this.ccp_alpha = undefined;
    },
    apply() {
      this.applied = [
        this.technique,
        this.classLabel,
        this.inputSamples,
        this.filter,
        this.encoder,
      ];
      this.cacheKey = +new Date();
      this.status = 1;
      const params = new URLSearchParams([
        ["classLabel", this.classLabel],
        ["inputSamples", this.inputSamples],
        ["encoder", this.encoder],
      ]);
      if (this.ccp_alpha) {
        let ccp_alpha_float = parseFloat(this.ccp_alpha);
        params.append("ccp_alpha", ccp_alpha_float);
      }
      for (let i = 0; i < Object.keys(this.filter).length; i++) {
        const label = Object.keys(this.filter)[i];
        params.append(label, this.filter[label]);
      }
      axios
        .get(
          "discovery/" +
            this.$route.params.dataSet +
            "/" +
            this.$route.params.csv +
            "_" +
            this.$route.params.level +
            "/" +
            this.technique.replace(/\s+/g, "").toLowerCase(),
          { params }
        )
        .then((res) => {
          this.status = res.status;
          if (this.status == 201) {
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
  created() {
    this.get_events();
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
