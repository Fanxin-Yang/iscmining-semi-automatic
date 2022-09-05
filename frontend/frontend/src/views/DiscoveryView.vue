<template lang="">
  <form class="row g-3 border bg-light">
    <EventsTable
      :dataSet="this.$route.params.dataSet"
      :csv="this.$route.params.csv"
    />
    <TimestampsCoarsen
      :dataSet="this.$route.params.dataSet"
      :csv="this.$route.params.csv"
    />
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
