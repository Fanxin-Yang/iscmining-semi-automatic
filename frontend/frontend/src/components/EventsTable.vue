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
  <div v-else-if="error != ''" class="alert alert-danger" role="alert">
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
              @info="update_info"
              :dataSet="this.dataSet"
              :csv="this.csv"
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
        <!-- <tr>
          <nav aria-label="Page navigation example">
            <ul class="pagination">
              <li class="page-item">
                <a class="page-link" href="#">Previous</a>
              </li>
              <li class="page-item"><a class="page-link" href="#">1</a></li>
              <li class="page-item"><a class="page-link" href="#">2</a></li>
              <li class="page-item"><a class="page-link" href="#">3</a></li>
              <li class="page-item"><a class="page-link" href="#">Next</a></li>
            </ul>
          </nav>
        </tr> -->
      </tbody>
    </table>
  </div>
  <div class="col-md-12">
    <div v-if="!!info" class="alert alert-success" role="alert">
      {{ this.info }}
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
  },
  data() {
    return {
      events: {},
      showEvents: {},
      error: "",
      info: "",
      index: 0,
    };
  },
  methods: {
    get_events(dataSet, csv) {
      axios
        .get("discovery/" + dataSet + "/" + csv)
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
    update_info(data) {
      this.info = data;
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
