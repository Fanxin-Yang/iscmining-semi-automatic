<template lang="">
    <h3>Process Model</h3>
    <div>
      <!-- <button type="button" class="btn btn-primary" @click="showPNG">Show</button>
    <button type="button" class="btn btn-link" @click="hidePNG">Hide</button>
    <img v-if="show" :src="pngLink" />
    <div v-else-if="alert" class="alert alert-warning" role="alert">
      No process model available
    </div> -->
      <img
        :src="
          'http://localhost:5000/processmodels/' +
          this.$route.params.dataSet +
          '.gv.png'
        "
        class="img-fluid"
      />
    </div>
</template>

<script>
export default {
  //   data() {
  //     return {
  //       pngLink: "",
  //       show: false,
  //       alert: false,
  //     };
  //   },
  // props: ["processModel"],
  methods: {
    // showPNG() {
    //   if (!this.processModel) {
    //     this.show = false;
    //     this.alert = true;
    //   } else {
    //     const pngLink =
    //       "http://localhost:5000/processmodels/" + this.$props.processModel;
    //     this.pngLink = pngLink;
    //     this.show = true;
    //     this.alert = false;
    //   }
    // },
    // hidePNG() {
    //   this.show = false;
    //   this.alert = false;
    // },
  },
};
</script>

<style lang=""></style>
