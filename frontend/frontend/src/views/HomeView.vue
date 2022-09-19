<template lang="">
  <h1 class="display-4">Introduction:</h1>
  <form class="row g-5">
    <div class="accordion" id="accordionExample">
      <div class="accordion-item">
        <h2 class="accordion-header" id="headingOne">
          <button
            class="accordion-button"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapseOne"
            aria-expanded="true"
            aria-controls="collapseOne"
          >
            Step 1: Upload new process execution logs or select an existing one
          </button>
        </h2>
        <div
          id="collapseOne"
          class="accordion-collapse collapse show"
          aria-labelledby="headingOne"
          data-bs-parent="#accordionExample"
        >
          <div class="accordion-body">
            Choose one or multiple <strong>XES</strong> files from local
            repository. Selected files will be uploaded to the server by
            clicking <strong>"Upload"</strong> button. <br />
            You can see the if the upload is successful or failed. <br />
            Then you can select one of the uploaded datasets that you want to
            discover. Move to the next step with the button
            <strong>"Start Pro-process"</strong>.
          </div>
        </div>
      </div>
      <div class="accordion-item">
        <h2 class="accordion-header" id="headingTwo">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapseTwo"
            aria-expanded="false"
            aria-controls="collapseTwo"
          >
            Step 2: Process model, Projection and transformation algorithm
          </button>
        </h2>
        <div
          id="collapseTwo"
          class="accordion-collapse collapse"
          aria-labelledby="headingTwo"
          data-bs-parent="#accordionExample"
        >
          <div class="accordion-body">
            The process model using Petri Net of the process execution log is
            providede to offer you a more clear insight of the whole process.
            The model is mined using [Inductive Miner] by PM4PY.<br />
            Choose an instance-spanning event attribute and click the
            <strong>"Projection & Transformation"</strong> button to reduce
            dimensions which allows for discovering ISC candidates.<br />
            <strong><code>org:resource</code></strong> is hightly recommanded,
            since instance-spanning parts usually relate to organizational
            resources. <br />
            Partial logs are transformed to <strong>CSV</strong> files. Then
            select one of the CSV file and click
            <strong>"Start Discovery"</strong> button to discover ISC
            candidates.
          </div>
        </div>
      </div>
      <div class="accordion-item">
        <h2 class="accordion-header" id="headingThree">
          <button
            class="accordion-button collapsed"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#collapseThree"
            aria-expanded="false"
            aria-controls="collapseThree"
          >
            Step 3: ISC candidate discovery algorithm per csv file
          </button>
        </h2>
        <div
          id="collapseThree"
          class="accordion-collapse collapse"
          aria-labelledby="headingThree"
          data-bs-parent="#accordionExample"
        >
          <div class="accordion-body">
            Table, Delete<br />
            <strong>"Timestamps Coarsen"</strong> <strong>"Next Step"</strong>
            <br />
            Filter: select value of each attribute <br />
            Apply classification technique (Decision tree)
            <strong>"Apply Decision Tree Algorithm"</strong>
            Pruning with minimal cost-complexity decision tree model visualized
            with dtreeviz
          </div>
        </div>
      </div>
    </div>
    <div class="d-grid gap-2 col-3 mx-auto">
      <button type="button" class="btn btn-primary btn-lg" @click="start()">
        Start
      </button>
    </div>
  </form>
</template>

<script>
export default {
  methods: {
    start() {
      this.$router.push("/iscmining-semi-automatic");
    },
  },
};
</script>
<style lang=""></style>
