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
