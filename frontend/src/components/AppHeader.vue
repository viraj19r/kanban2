<template>
  <nav class="navbar navbar-expand-lg bg-black">
    <div class="container-fluid">
      <router-link class="navbar-brand border rounded" to="/board">
        <img
          src="../assets/Kanban.png"
          alt="kanban"
          width="100"
          height="60"
          class="d-inline-block align-text-top my-0 rounded border-white"
        />
      </router-link>
      <button
        class="navbar-toggler bg-white"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#nav"
        aria-controls="navbarTogglerDemo03"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="nav">
        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a
              class="nav-link active mx-4 text-white font-monospace fs-5"
              aria-current="page"
              href="#"
              >Home</a
            >
          </li>
          <li class="nav-item">
            <a class="nav-link active mx-4 text-white font-monospace fs-5" href="#"
              >Link</a
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {};
</script>

<style>
</style>
