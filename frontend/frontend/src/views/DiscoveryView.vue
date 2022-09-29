<template lang="">
  <form class="row g-3 border bg-light">
    <LogSummary
      :dataSet="this.dataSet"
      :csv="this.csv"
      :refresh="this.cacheKey"
    />
    <EventsTable
      :dataSet="this.dataSet"
      :csv="this.csv"
      :refresh="this.cacheKey"
    />
    <!-- <TimestampsCoarsen
      :dataSet="this.dataSet"
      :csv="this.csv"
      @modify="modify"
    />
    <VariantFilter :dataSet="this.dataSet" :csv="this.csv" @modify="modify" /> -->
    <ModifyLog
      :dataSet="this.dataSet"
      :csv="this.csv"
      @modify="modify"
      :info="this.info"
    />
  </form>
</template>

<script>
import EventsTable from "../components/EventsTable.vue";
// import TimestampsCoarsen from "../components/TimestampsCoarsen.vue";
// import VariantFilter from "../components/VariantFilter.vue";
import LogSummary from "../components/LogSummary.vue";
import ModifyLog from "../components/ModifyLog.vue";
import axios from "axios";
export default {
  components: {
    EventsTable,
    // TimestampsCoarsen,
    // VariantFilter,
    LogSummary,
    ModifyLog,
  },
  data() {
    return {
      dataSet: this.$route.params.dataSet,
      csv: this.$route.params.csv,
      error: "",
      info: undefined,
      cacheKey: +new Date(),
    };
  },
  methods: {
    modify(level, selectedVariantsIndex) {
      let url = "modify/" + this.dataSet + "/" + this.csv + "/" + level;
      const params = new URLSearchParams([["variants", selectedVariantsIndex]]);
      console.log(selectedVariantsIndex);
      axios
        .get(url, { params })
        .then((res) => {
          this.info = res.data;
          let tmp =
            "/iscmining-semi-automatic/" +
            this.dataSet +
            "/" +
            this.csv +
            "/modified";
          this.$router.push(tmp);
          this.cacheKey = +new Date();
        })
        .catch((err) => {
          console.error(err);
          this.error = err.response.data;
        });
    },
  },
  watch: {
    "$route.params.dataSet": {
      handler: function (val) {
        this.dataSet = val;
      },
      deep: true,
      immediate: true,
    },
    "$route.params.csv": {
      handler: function (val) {
        this.csv = val;
      },
      deep: true,
      immediate: true,
    },
  },
};
</script>

<style lang=""></style>
