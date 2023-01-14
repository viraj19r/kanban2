<template>
  <div>
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
              <router-link
                class="nav-link active mx-4 text-white font-monospace fs-5"
                aria-current="page"
                to="/board/summary"
                >Summary</router-link
              >
            </li>
            <li class="nav-item">
              <router-link
                class="nav-link active mx-4 text-white font-monospace fs-5"
                aria-current="page"
                to="#"
                >Logout</router-link
              >
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container">
      <div class="mb-5 mx-5 mt-3">
        <div class="d-flex justify-content-between">
          <h1
            class="h2 d-flex align-items-center"
            style="font-family: monospace, serif"
          >
            Add a list to your board :
          </h1>
        </div>
      </div>
      <div class="d-flex justify-content-center">
        <div
          class="
            d-flex
            justify-content-center
            bg-dark
            rounded-pill
            py-5
            px-1
            w-100
            shadow-lg
          "
        >
          <div class="" style="height: 30%; width: 60%">
            <div class="d-flex justify-content-center">
              <h2 style="color: white">Add List</h2>
            </div>
            <div class="mb-3">
              <label for="name" class="form-label" style="color: white"
                >Name</label
              >
              <input
                type="text"
                v-model="lname"
                class="form-control"
                id="name"
                placeholder="list-A"
              />
            </div>
            <div class="mb-3">
              <label for="desc" class="form-label" style="color: white"
                >Description</label
              >
              <textarea
                class="form-control"
                v-model="ldesc"
                id="desc"
                rows="3"
                placeholder="Description"
              ></textarea>
            </div>
            <div class="d-flex justify-content-center mt-3">
              <a
                class="btn btn-primary d-flex justify-content-center"
                @click="saveList"
                href="#"
                role="button"
                style="width: 30%"
                >Save</a
              >
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      lname: "",
      ldesc: "",
    };
  },
  methods: {
    saveList() {
      // console.log(this.lname,this.ldesc)
      if (this.lname.length != 0 && this.ldesc.length != 0) {
        fetch("http://127.0.0.1:8080/api/list", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.auth_token,
          },
          body: JSON.stringify({
            name: this.lname,
            description: this.ldesc,
          }),
        }).then((res) => { if (res.ok){ this.$router.push('/board'); }});
      }
    },
  },
};
</script>

<style>
</style>