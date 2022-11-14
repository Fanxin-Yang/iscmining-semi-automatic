<template lang="">
  <label for="events-table"
    >Click the button to delete irrelevant events.</label
  >
  <div
    class="col-md-12 text-center"
    v-if="Object.keys(events).length == 0 && error == ''"
  >
    Loading...
  </div>
  <div
    v-else-if="Object.keys(events).length == 0 && error != ''"
    class="alert alert-danger"
    role="alert"
  >
    {{ error }}
  </div>

  <div class="table-responsive" id="events-table" v-else>
    <table class="table table-striped table-hover table-sm table-bordered">
      <thead class="header">
        <tr>
          <th scope="col"></th>
          <th v-for="(index, value) in events[0]" :key="index">
            <div v-if="value != 'case:concept:name'">
              {{ value }}
            </div>
            <div v-else>case</div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr class="text-center" v-if="index > 1">
          <td :colspan="Object.keys(events[0]).length + 1">
            <button type="button" class="btn btn-link" @click="previous">
              Previous
            </button>
          </td>
        </tr>
        <tr v-for="(event, index) in showEvents" :key="index">
          <th scope="row">
            <DeleteModal
              :eventIndex="event['No.']"
              :dataSet="this.dataSet"
              :csv="this.csv"
              @remove_event="remove_event"
            />
          </th>
          <td v-for="(value, key) in event" :key="key">{{ value }}</td>
        </tr>
        <tr
          class="text-center"
          v-if="index > 0 && index * 100 < Object.keys(this.events).length"
        >
          <td :colspan="Object.keys(events[0]).length + 1">
            <button type="button" class="btn btn-link" @click="next">
              Next
            </button>
          </td>
        </tr>
        <tr class="text-center" v-else>
          <td :colspan="Object.keys(events[0]).length + 1">
            The End of the Event Table.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div class="col-md-12">
    <div v-if="!!deleteInfo" class="alert alert-success" role="alert">
      {{ this.deleteInfo }}
    </div>
  </div>
</template>

<script>
import axios from "axios";
import DeleteModal from "./DeleteModal.vue";

export default {
  components: {
    DeleteModal,
  },
  props: {
    dataSet: {
      type: String,
      required: true,
    },
    csv: {
      type: String,
      required: true,
    },
    refresh: {
      type: Number,
      required: true,
    },
    deleteInfo: {
      type: String || undefined,
      required: false,
    },
  },
  data() {
    return {
      events: {},
      showEvents: {},
      error: "",
      index: 0,
    };
  },
  emits: ["delete_event"],
  methods: {
    remove_event(eventIndex) {
      this.$emit("delete_event", eventIndex);
    },
    get_events(dataSet, csv) {
      axios
        .get("discovery/" + dataSet + "/" + csv + "_modified")
        .then((res) => {
          this.events = res.data;
          this.index = 1;
        })
        .catch((err) => {
          console.error(err);
          this.error = err.response.data;
        });
    },
    previous() {
      this.index = this.index - 1;
    },
    next() {
      this.index = this.index + 1;
    },
  },
  watch: {
    csv: function (val) {
      this.get_events(this.dataSet, val);
    },
    index: function (val) {
      let j = 0;
      this.showEvents = {};
      const min = Math.min(val * 100, Object.keys(this.events).length);
      for (var i = (val - 1) * 100; i < min; ++i) {
        this.showEvents[j] = this.events[i];
        ++j;
      }
    },
    refresh: function () {
      this.get_events(this.dataSet, this.csv);
    },
    events: function () {
      this.showEvents = {};
      for (var i = 0; i < 100; ++i) {
        this.showEvents[i] = this.events[i];
      }
    },
  },
  created() {
    this.get_events(this.dataSet, this.csv);
  },
};
</script>

<style>
.table-responsive {
  max-height: 400px;
  margin-top: 20px;
  margin-bottom: 20px;
}
.header {
  position: sticky;
  top: 0;
  background-color: lightgrey;
}
</style>
