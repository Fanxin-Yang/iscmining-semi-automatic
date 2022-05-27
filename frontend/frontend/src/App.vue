<script setup>
import { RouterView } from "vue-router";
</script>

<template>
  <header>
    <div class="wrapper">
      <h1 class="green">ISC Mining</h1>
      <h5>
        It is a project which based on the approach introduced in
        <a target="_blank" href="https://ieeexplore.ieee.org/document/8089866"
          >this paper.</a
        >
      </h5>

      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
          <a class="navbar-brand" href="/">Home</a>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="/">Home</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/upload">Upload</a>
              </li>
              <li class="nav-item dropdown">
                <a
                  class="nav-link dropdown-toggle"
                  href="#"
                  id="navbarDropdown"
                  role="button"
                  data-bs-toggle="dropdown"
                  aria-expanded="false"
                >
                  Dropdown
                </a>
                <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                  <li><a class="dropdown-item" href="#">Action</a></li>
                  <li><a class="dropdown-item" href="#">Another action</a></li>
                  <li><hr class="dropdown-divider" /></li>
                  <li>
                    <a class="dropdown-item" href="#">Something else here</a>
                  </li>
                </ul>
              </li>
              <li class="nav-item">
                <a
                  class="nav-link disabled"
                  href="#"
                  tabindex="-1"
                  aria-disabled="true"
                  >Disabled</a
                >
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  </header>

  <div class="container">
    <RouterView />
  </div>
</template>

<style>
#app {
  margin-top: 60px;
  padding: 20px;
}
</style>
