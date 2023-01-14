<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-black">
      <div class="container-fluid">
        <router-link class="navbar-brand border rounded" to="/">
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
                to="/login"
                >Login</router-link
              >
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div v-if="errors.length" style="color:grey">
                <p class="alert alert-danger p-1 my-0" v-for="error,index in errors" :key="index">{{ error }}</p>
    </div>
    <div class="mb-5 mx-5 mt-3">
      <div class="d-flex justify-content-between">
        <h1
          class="h2 d-flex align-items-center"
          style="font-family: monospace, serif"
        >
          Welcome to Kanban Board!
        </h1>
      </div>
      <div class="d-flex justify-content-center">
        <div class="shadow-lg bg-dark my-5" style="border-radius: 30px">
          <form class="p-3">
            <div class="d-flex row justify-content-center">
              <h2 class="col" style="color: white">Create Account</h2>
            </div>
            <div class="form-group row d-flex justify-content-between">
              <div class="w-45 col">
                <label for="fname" style="color: white">First Name</label>
                <input
                  v-model="fname"
                  type="text"
                  class="form-control"
                  id="fname"
                  placeholder="First name"
                />
              </div>
              <div class="w-45 col">
                <label for="lname" style="color: white">Last Name</label>
                <input
                  v-model="lname"
                  type="text"
                  class="form-control"
                  id="lname"
                  placeholder="Last name"
                />
              </div>
            </div>
            <div class="form-group">
              <label for="username" style="color: white">Email address</label>
              <input
                v-model="email"
                type="email"
                class="form-control"
                id="username"
                aria-describedby="emailHelp"
                placeholder="Enter email"
              />
              <small
                id="emailHelp"
                class="form-text mx-2"
                style="color: white; font-size: x-small"
                >We'll never share your email with anyone else.</small
              >
            </div>
            <div class="form-group mb-2">
              <label for="pass" style="color: white">Password</label>
              <input
                v-model="password"
                type="password"
                class="form-control"
                id="pass"
                placeholder="Password"
              />
            </div>
            <div class="form-group mb-2">
              <label for="confpass" style="color: white"
                >Confirm Password</label
              >
              <input
                v-model="conpassword"
                type="password"
                class="form-control"
                id="conpass"
                placeholder="Confirm Password"
              />
            </div>
            <div class="d-flex justify-content-center mt-5">
              <a
                @click="registerUser"
                class="btn btn-success d-flex justify-content-center"
                href="#"
                role="button"
                style="width: 30%"
                >Register</a
              >
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      fname: "",
      lname: "",
      email: "",
      password: "",
      conpassword: "",
      errors: [],
    };
  },
  methods: {
    registerUser() {
      if (
        this.fname &&
        this.lname &&
        this.email &&
        this.password &&
        this.conpassword
      ) {
        fetch("http://127.0.0.1:8080/api/user", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            fname: this.fname,
            lname: this.lname,
            email: this.email,
            password: this.password,
          }),
        }).then((res) => {
          if (res.ok) {
            this.$router.push("/login");
          }
        });
      }
      this.errors = []
      if (!this.fname.length) {
        this.errors.push("First Name Required");
      }
      if (!this.lname.length) {
        this.errors.push("Last Name Required");
      }
      if (!this.email.length) {
        this.errors.push("Email Required");
      }
      else if (!this.validEmail(this.email)) {
        this.errors.push("Valid email required.");
      }
      if (!this.password.length) {
        this.errors.push("Password Required");
      }
      if (this.password != this.conpassword) {
        this.errors.push("Password don't match");
      }
    },
    validEmail: function (email) {
      var re =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    },
  },
};
</script>

<style>
</style>