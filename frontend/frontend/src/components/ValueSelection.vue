<template lang="">
  <h3>Value Selection</h3>
  <div class="row">
    <div class="col-auto" v-for="(l, i) in labelsUnique" :key="i">
      <label for="select" class="form-label">{{ i }}</label>
      <select
        size="10"
        v-model="selectedLabels[i]"
        class="form-select"
        multiple
        id="select"
      >
        <option v-for="(v, j) in l" :key="j">
          {{ v }}
        </option>
      </select>
    </div>
  </div>
  <!-- <p>{{ selectedLabels }}</p>
  <p>{{ labelsUnique }}</p> -->
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      labelsUnique: {},
      selectedLabels: {},
      tmp: [],
      //   labels: ["Requested_Amount"],
    };
  },
  props: ["labels"],
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
            this.selectedLabels = Object.assign({}, this.labelsUnique);
          })
          .catch((err) => {
            console.error(err);
            this.error = err.response.data;
          });
      }
    },
    test() {
      console.log(this.labelsUnique[this.labels[0]][0]);
    },
  },
  created() {
    this.get_unique();
  },
};
</script>
<style lang=""></style>
