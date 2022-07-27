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
  props: ["labels"],
  emits: ["filter"],
  methods: {
    get_unique() {
      let path =
        "http://localhost:5000/discovery/" +
        this.$route.params.dataSet +
        "/" +
        this.$route.params.csv;
      if (this.$route.params.level != "Seconds") {
        path = path + "_" + this.$route.params.level;
      }

      for (let i = 0; i < this.labels.length; i++) {
        const params = new URLSearchParams([["label", this.labels[i]]]);
        axios
          .get(path, { params })
          .then((res) => {
            this.labelsUnique[this.labels[i]] = Object.values(res.data);
            // Object.assign(this.selectedLabels, this.labelsUnique);
            this.selectedLabels[this.labels[i]] = [];
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
  created() {
    this.get_unique();
  },
};
</script>
<style lang=""></style>
