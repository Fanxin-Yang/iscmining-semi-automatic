<template lang="">
  <h3>Value Selection</h3>
  <h6>
    Please select at least 1 value of each attributes. (Default: all selected.)
  </h6>
  <div class="row">
    <div class="col-auto" v-for="(l, i) in labelsUnique" :key="i">
      <div class="form-check">
        <input
          class="form-check-input"
          :id="'checkBox_' + i"
          type="checkbox"
          value=""
          :checked="
            selectedLabels[i].length == 0 ||
            selectedLabels[i].length == labelsUnique[i].length
          "
          @change="selectAll(i)"
        />
        <label class="form-check-label" :for="'checkBox_' + i">
          {{ i }}
        </label>
      </div>
      <div>
        selected length: {{ selectedLabels[i].length }} labelsUnique length:
        {{ labelsUnique[i].length }}
      </div>
      <select
        size="10"
        v-model="selectedLabels[i]"
        class="form-select"
        multiple
        id="select"
        @change="update_filter"
      >
        <option v-for="(v, j) in l" :key="j">
          {{ v }}
        </option>
      </select>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      labelsUnique: {},
      selectedLabels: {},
      tmp: [],
    };
  },
  props: {
    labels: {
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
  emits: ["filter"],
  methods: {
    get_unique(dataSet, csv, level, labels) {
      let path = "discovery/" + dataSet + "/" + csv;
      if (level != "Seconds") {
        path = path + "_" + level;
      }

      for (let i = 0; i < labels.length; i++) {
        const params = new URLSearchParams([["label", labels[i]]]);
        axios
          .get(path, { params })
          .then((res) => {
            this.labelsUnique[labels[i]] = Object.values(res.data);
            this.selectedLabels[labels[i]] = [];
            this.update_filter();
          })
          .catch((err) => {
            console.error(err);
          });
      }
    },
    update_filter() {
      this.$emit("filter", this.selectedLabels);
    },
    selectAll(i) {
      this.selectedLabels[i] = this.labelsUnique[i];
    },
  },
  watch: {
    labels: function (val) {
      this.get_unique(this.dataSet, this.csv, this.level, val);
    },
  },
  created() {
    this.get_unique(this.dataSet, this.csv, this.level, this.labels);
  },
};
</script>
<style lang=""></style>
