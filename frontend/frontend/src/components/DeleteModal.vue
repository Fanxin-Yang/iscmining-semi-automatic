<template>
  <!-- Button trigger modal -->
  <button
    type="button"
    class="btn btn-close"
    data-bs-toggle="modal"
    :data-bs-target="'#modal' + eventIndex"
  ></button>
  <!-- Modal -->
  <div
    class="modal fade"
    :id="'modal' + eventIndex"
    tabindex="-1"
    aria-labelledby="modaleTitle"
    aria-hidden="true"
  >
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modaleTitle">Remove Event</h5>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></button>
        </div>
        <div class="modal-body">
          Are you sure that you want to remove this event from this csv file?
          This process cannot be resumed.
        </div>
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            data-bs-dismiss="modal"
            @click="test"
          >
            Cancel
          </button>
          <button
            type="button"
            class="btn btn-primary"
            data-bs-dismiss="modal"
            @click="remove_event"
          >
            Remove
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  props: ["eventIndex", "info"],
  emits: ["info"],
  methods: {
    test() {
      console.log(this.eventIndex);
    },
    remove_event() {
      const path =
        "http://localhost:5000/discovery/" +
        this.$route.params.dataSet +
        "/" +
        this.$route.params.csv +
        "/" +
        this.eventIndex;
      axios
        .delete(path)
        .then((res) => {
          this.$emit("info", res.data);
          this.$parent.get_events();
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>

<style lang=""></style>
