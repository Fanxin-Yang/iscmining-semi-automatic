<template lang="">
  <h3>Process Model (Petri Net)</h3>
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
        '.png'
      "
      class="img-fluid"
    />
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      json: undefined,
    };
  },
  // props: ["processModel"],
  methods: {
    getJSON() {
      axios
        // .get("processmodels/" + this.$route.params.dataSet + ".json")
        .get("/pm4pytest")
        .then((res) => {
          console.log(res.status);
          this.json = res.data;
        })
        .catch((err) => {
          this.status = err.response.status;
          this.msg = err.response.data;
        });
    },
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
  created() {
    this.getJSON();
  },
};
</script>

<style lang=""></style>
