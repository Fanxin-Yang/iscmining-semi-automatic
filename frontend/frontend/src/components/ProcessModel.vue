<template lang="">
  <div>
    <slot><h3>process model</h3></slot>
    <p>{{ processModel }}</p>
    <!-- <img :src="require('./assets/processModel.png')" /> -->
  </div>
</template>

<script>
export default {
  //   data() {
  //     return {
  //       processModel: "",
  //     };
  //   },
  props: ["processModel"],
  methods: {},
};
</script>

<style lang=""></style>
