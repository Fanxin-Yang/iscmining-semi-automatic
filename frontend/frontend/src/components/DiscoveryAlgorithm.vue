<template lang="">
  <h3>ISC Discovery Algorithm</h3>
  <div class="col-md-6">
    <select v-model="selectedProjection" class="form-select">
      <option selected disabled value="">Choose a file</option>
      <option v-for="(number, tmp) in projections" :key="tmp">
        {{ tmp }}.csv
      </option>
    </select>
    <div class="alert alert-light" role="alert">
      Selected projection: {{ selectedProjection }}
    </div>
  </div>
  <div class="col-md-4">
    <button
      type="button"
      class="btn btn-primary"
      @click="get_events"
      :disabled="selectedProjection == ''"
    >
      Start Discovery
    </button>
  </div>

  <div class="table-responsive">
    <table class="table table-striped table-hover table-sm table-bordered">
      <thead class="header">
        <tr>
          <th scope="col">#</th>
          <th scope="col">First</th>
          <th scope="col">Last</th>
          <th scope="col">Handle</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th scope="row">
            <button
              type="button"
              class="btn-close"
              aria-label="Delete"
            ></button>
          </th>
          <td>Mark</td>
          <td>Otto</td>
          <td>@mdo</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Jacob</td>
          <td>Thornton</td>
          <td>@fat</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td colspan="2">Larry the Bird</td>
          <td>@twitter</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Jacob</td>
          <td>Thornton</td>
          <td>@fat</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td colspan="2">Larry the Bird</td>
          <td>@twitter</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Jacob</td>
          <td>Thornton</td>
          <td>@fat</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td colspan="2">Larry the Bird</td>
          <td>@twitter</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Jacob</td>
          <td>Thornton</td>
          <td>@fat</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td colspan="2">Larry the Bird</td>
          <td>@twitter</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Jacob</td>
          <td>Thornton</td>
          <td>@fat</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td colspan="2">Larry the Bird</td>
          <td>@twitter</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Jacob</td>
          <td>Thornton</td>
          <td>@fat</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td colspan="2">Larry the Bird</td>
          <td>@twitter</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Jacob</td>
          <td>Thornton</td>
          <td>@fat</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td colspan="2">Larry the Bird</td>
          <td>@twitter</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Jacob</td>
          <td>Thornton</td>
          <td>@fat</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td colspan="2">Larry the Bird</td>
          <td>@twitter</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Jacob</td>
          <td>Thornton</td>
          <td>@fat</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td colspan="2">Larry the Bird</td>
          <td>@twitter</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Jacob</td>
          <td>Thornton</td>
          <td>@fat</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td colspan="2">Larry the Bird</td>
          <td>@twitter</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Jacob</td>
          <td>Thornton</td>
          <td>@fat</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td colspan="2">Larry the Bird</td>
          <td>@twitter</td>
        </tr>
        <tr>
          <th scope="row">2</th>
          <td>Jacob</td>
          <td>Thornton</td>
          <td>@fat</td>
        </tr>
        <tr>
          <th scope="row">3</th>
          <td colspan="2">Larry the Bird</td>
          <td>@twitter</td>
        </tr>
      </tbody>
    </table>
  </div>
  <p>sdffsfds</p>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      selectedProjection: "",
      evnets: {},
    };
  },
  props: ["dataSet", "projections"],
  methods: {
    get_events() {
      const path =
        "http://localhost:5000/discovery/" +
        this.dataSet +
        "/" +
        this.selectedProjection;
      console.log(path);
      axios
        .get(path)
        .then((res) => {
          this.evnets = res.data;
          console.log(res.data);
        })
        .catch((err) => {
          console.error(err);
        });
    },
    determine_r() {},
    timestamps() {},
    remove_events() {},
    get_classifications() {},
    apply_classifications() {},
  },
  created() {
    // this.get_classifications();
  },
};
</script>

<style>
/* tbody {
  display: block;
  max-height: 200px;
  overflow-y: auto;
} */
.table-responsive {
  max-height: 300px;
  margin-top: 20px;
}
.header {
  position: sticky;
  top: 0;
  background-color: lightgrey;
}
</style>
