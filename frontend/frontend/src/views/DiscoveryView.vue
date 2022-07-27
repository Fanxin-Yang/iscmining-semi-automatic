<template lang="">
  <form class="row g-3">
    <h3 class="display-4">Discovery Algorithm</h3>
    <div class="col-md-12">
      <EventsTable />
    </div>
    <div class="col-md-12">
      <TimestampsCoarsen />
    </div>
  </form>
</template>

<script>
import EventsTable from "../components/EventsTable.vue";
import TimestampsCoarsen from "../components/TimestampsCoarsen.vue";
export default {
  components: {
    EventsTable,
    TimestampsCoarsen,
  },
};
</script>

<style lang=""></style>
