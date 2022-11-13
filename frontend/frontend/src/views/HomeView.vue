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
            Step 1: Upload New Process Execution Logs or Select an Existing One
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
            Then you can select one or more datasets that you want to analyze.
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
            Step 2: Process Model, Projection and Transformation Algorithm
          </button>
        </h2>
        <div
          id="collapseTwo"
          class="accordion-collapse collapse"
          aria-labelledby="headingTwo"
          data-bs-parent="#accordionExample"
        >
          <div class="accordion-body">
            The process model of the process execution log is mined and depicted
            to offer you a more clear insight of the whole process. The model is
            mined using [Inductive Miner] by PM4PY.<br />
            Choose an instance-spanning event attribute and click the
            <strong>"Projection & Transformation"</strong> button to reduce
            dimensions which allows for discovering ISC candidates.<br />
            <strong><code>org:resource</code></strong> is hightly recommanded,
            since instance-spanning parts usually relate to organizational
            resources. <br />
            Then you can select one or more projections and click
            <strong>"Merge & Start Discovery"</strong> button to discover ISC
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
            Step 3: ISC Candidates Discovery Algorithm
          </button>
        </h2>
        <div
          id="collapseThree"
          class="accordion-collapse collapse"
          aria-labelledby="headingThree"
          data-bs-parent="#accordionExample"
        >
          <div class="accordion-body">
            Events from the pre-processed log has been displayed in a table.<br />
            You can delete any event by clicking the delete icon in fromt of
            each row. By choosing a time level, the timestamps are corasened to
            this level. And you can filter the log on tis variants.
            <br />
            Different classification techniques from Weka and Scikit-learn can
            be applied seperately on the log. According to the algorithms
            parameters have to be determined. The results are displayed either
            in a table or a figure.
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
