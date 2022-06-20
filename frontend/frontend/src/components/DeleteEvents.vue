<template lang="">
  <h6>Click the button to delete irrelevant events.</h6>
  <div
    class="text-center"
    v-if="Object.keys(events).length == 0 && error == ''"
  >
    <div class="spinner-border m-5" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
  <div class="text-center" v-if="error != ''">
    {{ error }}
  </div>
  <div class="table-responsive" v-if="Object.keys(events).length > 0">
    <table class="table table-striped table-hover table-sm table-bordered">
      <thead class="header">
        <tr>
          <th scope="col"></th>
          <th v-for="(index, value) in events[0]" :key="index">
            <div v-if="value != 'case:concept:name'">
              {{ value }}
            </div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(event, index) in events" :key="index">
          <th scope="row">
            <DeleteModal :eventIndex="event['No.']" />
          </th>
          <td v-for="(value, key) in event" :key="key">{{ value }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from "axios";
import DeleteModal from "./DeleteModal.vue";

export default {
  components: {
    DeleteModal,
  },
  data() {
    return {
      events: {},
      error: "",
    };
  },
  methods: {
    get_events() {
      const path =
        "http://localhost:5000/discovery/" +
        this.$route.params.dataSet +
        "/" +
        this.$route.params.csv;
      axios
        .get(path)
        .then((res) => {
          this.events = res.data;
        })
        .catch((err) => {
          console.error(err);
          this.error = err.response.data;
        });
    },
    determine_r() {},
    timestamps() {},
    remove_events() {},
    get_classifications() {},
    apply_classifications() {},
  },
  created() {
    this.get_events();
  },
};
</script>

<style>
.table-responsive {
  max-height: 400px;
  margin-top: 20px;
}
.header {
  position: sticky;
  top: 0;
  background-color: lightgrey;
}
</style>
