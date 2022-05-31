<template lang="">
  <div>
    <slot><h3>Process Model</h3></slot>
    <!-- <h3>{{ processModel }}</h3> -->
    <button type="button" class="btn btn-primary" @click="showPNG">Show</button>
    <button type="button" class="btn btn-link" @click="hidePNG">Hide</button>
    <!-- <p>{{ pngLink }}</p> -->
    <img v-if="show" :src="pngLink" />
    <div v-else-if="alert" class="alert alert-warning" role="alert">
      No process model available
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      pngLink: "",
      show: false,
      alert: false,
    };
  },
  props: ["processModel"],
  methods: {
    showPNG() {
      if (!this.processModel) {
        this.show = false;
        this.alert = true;
      } else {
        const pngLink =
          "http://localhost:5000/graphs/" + this.$props.processModel;
        this.pngLink = pngLink;
        this.show = true;
        this.alert = false;
      }
    },
    hidePNG() {
      this.show = false;
      this.alert = false;
    },
  },
};
</script>

<style lang=""></style>
