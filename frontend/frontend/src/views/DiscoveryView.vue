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
      @delete_event="delete_event"
      :refresh="this.cacheKey"
      :deleteInfo="this.deleteInfo"
    />
    <ModifyLog
      :dataSet="this.dataSet"
      :csv="this.csv"
      @modify="modify"
      :modifyInfo="this.modifyInfo"
      :loading="this.modifyLoading"
    />
  </form>
</template>

<script>
import EventsTable from "../components/EventsTable.vue";
import LogSummary from "../components/LogSummary.vue";
import ModifyLog from "../components/ModifyLog.vue";
import axios from "axios";
export default {
  components: {
    EventsTable,
    LogSummary,
    ModifyLog,
  },
  data() {
    return {
      dataSet: this.$route.params.dataSet,
      csv: this.$route.params.csv,
      error: "",
      modifyInfo: undefined,
      deleteInfo: undefined,
      modifyLoading: false,
      cacheKey: +new Date(),
    };
  },
  methods: {
    modify(level, selectedVariantsIndex) {
      this.modifyLoading = true;
      let url = "modify/" + this.dataSet + "/" + this.csv + "/" + level;
      const params = new URLSearchParams([["variants", selectedVariantsIndex]]);
      axios
        .get(url, { params })
        .then((res) => {
          this.modifyLoading = false;
          this.modifyInfo = res.data;
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
          this.modifyLoading = false;
          console.error(err);
          this.error = err.response.data;
        });
    },
    delete_event(eventIndex) {
      const params = new URLSearchParams([["eventIndex", eventIndex]]);
      axios
        .delete("discovery/" + this.dataSet + "/" + this.csv, { params })
        .then((res) => {
          this.deleteInfo = res.data;
          this.cacheKey = +new Date();
        })
        .catch((err) => {
          console.error(err);
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
  mounted() {
    window.scrollTo(
      0,
      document.body.scrollHeight || document.documentElement.scrollHeight
    );
  },
};
</script>

<style lang=""></style>
