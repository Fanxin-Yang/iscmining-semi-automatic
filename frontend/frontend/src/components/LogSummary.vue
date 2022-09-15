<template lang="">
  <div>
    <label for="summary"><b>Summary:</b></label>
    <table class="table table-boardered" id="summary">
      <thead>
        <tr>
          <th scope="col">Process</th>
          <th scope="col">Partial Log</th>
          <th scope="col">Variants</th>
          <th scope="col">Cases</th>
          <th scope="col">Events</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">{{ this.dataSet }}.xes</th>
          <td>{{ this.csv }}.csv</td>
          <td v-if="this.shape">
            {{ this.shape["cases"][0] }}/{{ this.shape["cases"][1] }}
          </td>
          <td v-if="this.shape">
            {{ this.shape["events"][0] }}/{{ this.shape["events"][1] }}
          </td>
          <td v-if="this.shape">
            {{ this.shape["variants"][0] }}/{{ this.shape["variants"][1] }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";

export default {
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
      shape: undefined,
      info: undefined,
      error: "",
    };
  },
  methods: {
    summary(dataSet, csv) {
      axios
        .get("summary/" + dataSet + "/" + csv)
        .then((res) => {
          this.shape = res.data;
        })
        .catch((err) => {
          console.error(err);
          this.error = err.response.data;
        });
    },
  },
  watch: {
    csv: function (val) {
      this.summary(this.dataSet, val);
    },
  },
  created() {
    this.summary(this.dataSet, this.csv);
  },
};
</script>

<style lang=""></style>
