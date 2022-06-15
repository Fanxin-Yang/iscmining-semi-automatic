<template lang="">
  <div>
    <button type="button" class="btn btn-primary" @click="start()">
      Start
    </button>
  </div>
</template>

<script>
export default {
  methods: {
    start() {
      this.$router.push("/dataset");
    },
  },
};
</script>
<style lang=""></style>
