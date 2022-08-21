<script setup>
import { RouterView } from "vue-router";
</script>

<template>
  <header>
    <div class="wrapper">
      <h1 class="green">ISC Mining</h1>
      <h5>
        It is a project which based on the approach introduced in
        <a target="_blank" href="https://ieeexplore.ieee.org/document/8089866"
          >this paper.</a
        >
      </h5>

      <nav style="--bs-breadcrumb-divider: '>'" aria-label="breadcrumb">
        <ol class="breadcrumb">
          <li
            v-if="this.$route.name == 'home'"
            class="breadcrumb-item active"
            aria-current="page"
          >
            Home
          </li>
          <li v-else class="breadcrumb-item">
            <a href="/">Home</a>
          </li>
          <li
            v-if="this.$route.name == 'dataset'"
            class="breadcrumb-item active"
            aria-current="page"
          >
            Dataset
          </li>
          <li v-else-if="this.$route.name != 'home'" class="breadcrumb-item">
            <!-- <a href="/iscmining-semi-automatic/dataset">Dataset</a> -->
            <a href="/dataset">Dataset</a>
          </li>
          <li
            v-if="this.$route.name == 'preprocess'"
            class="breadcrumb-item active"
            aria-current="page"
          >
            Preprocess
          </li>
          <li
            v-else-if="
              this.$route.name != 'home' && this.$route.name != 'dataset'
            "
            class="breadcrumb-item"
          >
            <!-- <a :href="'/iscmining-semi-automatic/' + this.$route.params.dataSet"
              >Preprocess</a
            > -->
            <a :href="'/' + this.$route.params.dataSet">Preprocess</a>
          </li>
          <li
            v-if="this.$route.name == 'discovery'"
            class="breadcrumb-item active"
            aria-current="page"
          >
            Discovery
          </li>
          <li
            v-else-if="
              this.$route.name != 'home' &&
              this.$route.name != 'dataset' &&
              this.$route.name != 'preprocess'
            "
            class="breadcrumb-item"
          >
            <!-- <a
              :href="
                '/iscmining-semi-automatic/' +
                this.$route.params.dataSet +
                '/' +
                this.$route.params.csv
              "
              >Discovery</a
            > -->
            <a
              :href="
                '/' + this.$route.params.dataSet + '/' + this.$route.params.csv
              "
              >Discovery</a
            >
          </li>
          <li
            v-if="this.$route.name == 'classification'"
            class="breadcrumb-item active"
            aria-current="page"
          >
            Classification
          </li>
          <li
            v-else-if="
              this.$route.name != 'home' &&
              this.$route.name != 'dataset' &&
              this.$route.name != 'preprocess' &&
              this.$route.name != 'discovery'
            "
            class="breadcrumb-item"
          >
            <!-- <a
              :href="
                '/iscmining-semi-automatic/' +
                this.$route.params.dataSet +
                '/' +
                this.$route.params.csv +
                '/' +
                this.$route.params.level
              "
              >Classification</a
            > -->
            <a
              :href="
                '/' +
                this.$route.params.dataSet +
                '/' +
                this.$route.params.csv +
                '/' +
                this.$route.params.level
              "
              >Classification</a
            >
          </li>
        </ol>
      </nav>
    </div>
  </header>

  <div class="container">
    <RouterView />
  </div>
</template>

<style>
#app {
  margin-top: 60px;
  padding: 20px;
}
</style>
