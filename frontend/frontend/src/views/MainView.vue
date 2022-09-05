<template lang="">
  <div class="row">
    <div class="col-2">
      <div id="menu" class="list-group">
        <a class="list-group-item list-group-item-action" href="#dataset"
          >1. Dataset</a
        >
        <a class="list-group-item list-group-item-action" href="#preprocess"
          >2. Preprocess</a
        >
        <a class="list-group-item list-group-item-action" href="#discovery"
          >3. Discovery</a
        >
        <a class="list-group-item list-group-item-action" href="#classification"
          >4. Classification</a
        >
      </div>
    </div>
    <div class="col-10">
      <div
        data-bs-spy="scroll"
        data-bs-target="#menu"
        data-bs-smooth-scroll="true"
        class="scrollspy-example"
        tabindex="0"
      >
        <div class="container overflow-hidden text-left">
          <div class="row my-3">
            <h3 class="display-6" id="dataset"><u>Dataset</u></h3>
          </div>
          <DatasetView />
          <div class="row my-3">
            <h3 class="display-6" id="preprocess"><u>Preprocess</u></h3>
          </div>
          <div v-if="this.$route.params.dataSet"><PreprocessView /></div>
          <div v-else>Please select or upload a dataset first.</div>

          <div class="row my-3">
            <h3 class="display-6" id="discovery"><u>Discovery Algorithm</u></h3>
          </div>
          <div v-if="this.$route.params.csv"><DiscoveryView /></div>
          <div v-else>Please select a csv file first.</div>

          <div class="row my-3">
            <h3 class="display-6" id="classification">
              <u>Classification Algorithm</u>
            </h3>
          </div>
          <div v-if="this.$route.params.level">
            <ClassificationView
              :dataSet="this.$route.params.dataSet"
              :csv="this.$route.params.csv"
              :level="this.$route.params.level"
            />
          </div>
          <div v-else>Please select a timestamp level.</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DatasetView from "./DatasetView.vue";
import PreprocessView from "./PreprocessView.vue";
import DiscoveryView from "./DiscoveryView.vue";
import ClassificationView from "./ClassificationView.vue";

export default {
  components: {
    DatasetView,
    PreprocessView,
    DiscoveryView,
    ClassificationView,
  },
};
</script>

<style lang=""></style>
