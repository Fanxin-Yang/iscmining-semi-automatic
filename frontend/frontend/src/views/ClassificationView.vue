<template lang="">
  <form class="row g-3">
    <h3 class="display-4">ISC Discovery Algorithm</h3>
    <div class="col-md-12">
      <label class="form-label"
        >Dataset: {{ this.$route.params.dataSet }}</label
      >
      <label class="form-label">Classifier: {{ this.$route.params.csv }}</label>
      <div class="table-responsive" v-if="Object.keys(events).length > 0">
        <table class="table table-striped table-hover table-sm table-bordered">
          <thead class="header">
            <tr>
              <th scope="col"></th>
              <th v-for="(index, value) in events[0]" :key="index">
                <div v-if="value != 'case:concept:name'">
                  {{ value }}
                </div>
                <!-- <div class="dropdown">
                  <a
                    v-if="value != 'case:concept:name'"
                    class="dropdown-toggle"
                    href="#"
                    role="button"
                    id="dropdownMenuLink"
                    data-bs-toggle="dropdown"
                    aria-expanded="false"
                  >
                    {{ value }}
                  </a>
                  <ul
                    class="dropdown-menu"
                    aria-labelledby="dropdownMenuButton1"
                  >
                    <li><a class="dropdown-item" href="#">Action</a></li>
                  </ul>
                </div> -->
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(event, index) in events" :key="index">
              <th scope="row"></th>
              <td v-for="(value, key) in event" :key="key">{{ value }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="col-md-12">
      <ClassificationTechniques :events="events" />
    </div>
  </form>
</template>

<script>
import axios from "axios";
import ClassificationTechniques from "../components/ClassificationTechniques.vue";
export default {
  components: {
    ClassificationTechniques,
  },
  data() {
    return {
      events: {},
      error: "",
    };
  },
  methods: {
    get_events() {
      let path =
        "http://localhost:5000/discovery/" +
        this.$route.params.dataSet +
        "/" +
        this.$route.params.csv;
      if (this.$route.params.level != "Seconds") {
        path = path + "_" + this.$route.params.level;
      }
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
