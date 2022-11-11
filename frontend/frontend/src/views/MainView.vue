<template lang="">
  <div class="row">
    <!-- <div class="col-2">
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
    </div> -->
    <nav
      class="navbar sticky-top navbar-dark navbar-expand-lg bg-primary"
      id="menu"
    >
      <div class="container-fluid">
        <a class="navbar-brand" href="#" @click="reset">Reset All</a>
        <div class="collapse navbar-collapse" id="navbarScroll">
          <ul
            class="navbar-nav me-auto my-2 my-lg-0 navbar-nav-scroll"
            style="--bs-scroll-height: 100px"
          >
            <li class="nav-item">
              <a class="nav-link active" href="#dataset">1. Dataset</a>
            </li>
            <li class="nav-item">
              <a class="nav-link active" href="#preprocess">2. Preprocess</a>
            </li>
            <li class="nav-item">
              <a class="nav-link active" href="#discovery">3. Discovery</a>
            </li>
            <li class="nav-item">
              <a class="nav-link active" href="#classification"
                >4. Classification</a
              >
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="col-12">
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
            <h3 class="display-6" id="discovery"><u>Discovery</u></h3>
          </div>
          <div v-if="this.$route.params.csv"><DiscoveryView /></div>
          <div v-else>Please select a csv file first.</div>

          <div class="row my-3">
            <h3 class="display-6" id="classification">
              <u>Classification</u>
            </h3>
          </div>
          <div v-if="this.$route.params.modified">
            <ClassificationView
              :dataSet="this.$route.params.dataSet"
              :csv="this.$route.params.csv"
            />
          </div>
          <div v-else>Please apply filter or click Skip button.</div>
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
  methods: {
    reset() {
      let url = "/iscmining-semi-automatic/";
      this.$router.push(url);
    },
  },
};
</script>

<style lang=""></style>
