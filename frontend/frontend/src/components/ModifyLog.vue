<template lang="">
  <label for="select-timestamps-level">Choose a Timestamps Level.</label>
  <div class="col-md-8">
    <select
      v-model="timestampsLevel"
      class="form-select"
      id="select-timestamps-level"
    >
      <option selected>Seconds</option>
      <option>Minutes</option>
      <option>Hours</option>
      <option>Days</option>
      <option>Months</option>
      <option>Years</option>
    </select>
  </div>
  <div class="col-md-12 text-center" v-if="loading">
    <div class="spinner-border m-5" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div class="col-md-12">
    <div class="alert alert-success" role="alert" v-if="!!info">
      {{ info }}
    </div>
  </div>

  <label for="variant-list">Variants Filter</label>
  <ul class="list-group col-md-8" id="variant-list">
    <li
      class="list-group-item list-group-item-action"
      v-for="(variant, index) in variants"
      :key="index"
    >
      <label class="form-check-label" :for="'variant' + index">
        <div class="d-flex w-100 justify-content-between">
          <input
            class="form-check-input me-1"
            type="checkbox"
            v-model="selectedVariantsIndex[index]"
            :id="'variant' + index"
            @change="onChange"
          />
          <h5 class="mb-1 flex-grow-1">Variant {{ index }}</h5>
          <small class="text-muted">Count: {{ variant[1] }}</small>
        </div>
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
      <button type="button" class="btn btn-outline-primary" @click="modify">
        Apply Filter
      </button>
      <button
        type="button"
        class="btn btn-outline-secondary"
        @click="skip_modify"
      >
        Skip
      </button>
    </div>
  </div>
  <div class="col-md-3"></div>
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
    info: {
      required: true,
    },
  },
  data() {
    return {
      timestampsLevel: "Seconds",
      loading: false,
      variants: undefined,
      selectedVariantsIndex: [],
      filtering: "0",
      error: "",
    };
  },
  emits: ["modify"],
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
      if (this.filtering == 1) {
        for (var i = 0; i < this.selectedVariantsIndex.length; ++i) {
          this.selectedVariantsIndex[i] = !this.selectedVariantsIndex[i];
        }
        this.filtering = 0;
      }
    },
    modify() {
      this.apply_filter();
      this.$emit("modify", this.timestampsLevel, this.selectedVariantsIndex);
    },
    skip_modify() {
      this.$emit("modify", this.timestampsLevel, this.selectedVariantsIndex);
    },
  },
  watch: {
    csv: function (val) {
      this.get_variants(this.dataSet, val);
    },
    timestampsLevel: function (val) {
      console.log(val);
      this.modify();
    },
  },
  created() {
    let tmp =
      "/iscmining-semi-automatic/" + this.dataSet + "/" + this.csv + "/Seconds";
    this.$router.push(tmp);
    this.get_variants(this.dataSet, this.csv);
  },
};
</script>

<style lang=""></style>
