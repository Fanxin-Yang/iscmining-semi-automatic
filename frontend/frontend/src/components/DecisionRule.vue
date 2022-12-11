<template lang="">
  <div class="table-responsive" id="decision-rules-table">
    <label for="decision-rules-table">{{ lastline }}</label>
    <table
      class="table table-striped table-hover table-sm table-bordered"
      v-if="Object.keys(rules).length > 0"
    >
      <thead class="header">
        <tr>
          <th scope="col"></th>
          <th>{{ tabletitle }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(rule, index) in rules" :key="index">
          <th scope="row">
            {{ index + 1 }}
          </th>
          {{
            rule
          }}
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      rules: [],
      tabletitle: "",
      lastline: "",
    };
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
    alg: {
      type: String,
      required: true,
    },
    refresh: {
      type: Number,
      required: true,
    },
  },
  methods: {
    get_decisiionrules(dataSet, csv, alg) {
      axios
        .get("decisionrule/" + dataSet + "/" + csv + "_modified/" + alg)
        .then((res) => {
          const tmp = res.data;
          this.tabletitle = tmp[0];
          this.lastline = res.data[Object.keys(tmp).length - 2];
          this.rules = Object.values(tmp);
          this.rules = this.rules.splice(3, Object.keys(tmp).length - 6);
        })
        .catch((err) => {
          console.error(err);
          this.error = err.response.data;
        });
    },
  },
  created() {
    this.get_decisiionrules(this.dataSet, this.csv, this.alg);
  },
  watch: {
    refresh: function () {
      this.get_decisiionrules(this.dataSet, this.csv, this.alg);
    },
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
