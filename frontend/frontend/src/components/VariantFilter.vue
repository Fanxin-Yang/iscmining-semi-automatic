<template lang="">
  <label for="variant-list">Variants Filter</label>
  <ul class="list-group col-md-8" id="variant-list">
    <li
      class="list-group-item list-group-item-action"
      v-for="(variant, index) in variants"
      :key="index"
    >
      <!-- <input
        class="form-check-input me-1"
        type="checkbox"
        v-model="selected"
        :id="'variant' + index"
      /> -->
      <label class="form-check-label" :for="'variant' + index">
        <div class="d-flex w-100 justify-content-between">
          <input
            class="form-check-input me-1"
            type="checkbox"
            v-model="selectedVariantsIndex[index]"
            :id="'variant' + index"
            @change="onChange"
          />
          <h5 class="mb-1 flex-grow-1">Vatiant {{ index }}</h5>
          <small class="text-muted">Count: {{ variant[1] }}</small>
        </div>
        <!-- <p class="mb-1">Some placeholder content in a paragraph.</p> -->
        <small class="d-flex">{{ variant[0] }}</small>
      </label>
    </li>
  </ul>
  <div class="col-md-3">
    <div class="d-grid gap-3">
      <div>
        <label for="filtering-method" class="form-label"
          >Filtering Method:</label
        >
        <select
          v-model="filtering"
          class="form-select"
          id="filtering-method"
          aria-label="filtering-methodHelp"
        >
          <option value="0">Positive: Keep selected variant</option>
          <option value="1">Negative: Remove selected variant</option>
        </select>
      </div>
      <button
        type="button"
        class="btn btn-outline-primary"
        @click="apply_filter"
      >
        Apply Fitler
      </button>
    </div>
  </div>
  <div class="col-md-3"></div>

  <div class="col-md-12">
    <div v-if="!!info" class="alert alert-success" role="alert">
      {{ this.info }}
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  // components: {
  // },
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
      variants: undefined,
      selectedVariantsIndex: [],
      filtering: "0",
      info: undefined,
      error: "",
    };
  },
  methods: {
    get_variants(dataSet, csv) {
      axios
        .get("filter/" + dataSet + "/" + csv)
        .then((res) => {
          this.variants = res.data;
          this.selectedVariantsIndex = new Array(
            Object.keys(this.variants).length
          );
          for (var i = 0; i < this.selectedVariantsIndex.length; ++i) {
            this.selectedVariantsIndex[i] = true;
          }
        })
        .catch((err) => {
          console.error(err);
          this.error = err.response.data;
        });
    },
    apply_filter() {
      let url = "filter/" + this.dataSet + "/" + this.csv + "/";
      if (!this.$route.params.level) {
        url += "Seconds";
      } else {
        url += this.$route.params.level;
      }
      if (this.filtering == 1) {
        for (var i = 0; i < this.selectedVariantsIndex.length; ++i) {
          this.selectedVariantsIndex[i] = !this.selectedVariantsIndex[i];
        }
        this.filtering = 0;
      }
      const params = new URLSearchParams([
        ["variants", this.selectedVariantsIndex],
      ]);
      axios
        .get(url, { params })
        .then((res) => {
          this.info = res.data;
        })
        .catch((err) => {
          console.error(err);
          this.error = err.response.data;
        });
    },
  },
  watch: {
    csv: function (val) {
      this.get_variants(this.dataSet, val);
    },
  },
  created() {
    this.get_variants(this.dataSet, this.csv);
  },
};
</script>

<style></style>
