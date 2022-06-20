<template lang="">
  <form class="row g-3">
    <h3 class="display-4">ISC Discovery Algorithm</h3>
    <div class="col-md-12">
      <DeleteEventsVue />
    </div>
  </form>
</template>

<script>
import DeleteEventsVue from "../components/DeleteEvents.vue";
export default {
  components: {
    DeleteEventsVue,
  },
};
</script>

<style lang=""></style>
