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
export default {
  props: {
    eventIndex: {
      type: Number,
      required: true,
    },
    dataSet: {
      type: String,
      required: true,
    },
    csv: {
      type: String,
      required: true,
    },
  },
  emits: ["remove_event"],
  methods: {
    test() {
      console.log(this.dataSet);
      console.log(this.csv);
      console.log(this.eventIndex);
    },
    remove_event() {
      this.$emit("remove_event", this.eventIndex);
    },
  },
};
</script>

<style lang=""></style>
