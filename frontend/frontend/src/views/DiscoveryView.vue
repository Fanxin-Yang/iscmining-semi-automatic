<template lang="">
  <form class="row g-3">
    <h3 class="display-4">Discovery Algorithm</h3>
    <div class="col-md-12">
      <DeleteEvents />
    </div>
    <div class="col-md-12">
      <TimestampsCoarsen />
    </div>
  </form>
</template>

<script>
import DeleteEvents from "../components/DeleteEvents.vue";
import TimestampsCoarsen from "../components/TimestampsCoarsen.vue";
export default {
  components: {
    DeleteEvents,
    TimestampsCoarsen,
  },
};
</script>

<style lang=""></style>
