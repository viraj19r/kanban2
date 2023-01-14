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
                to="/register"
                >Register</router-link
              >
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div v-if="errors.length" style="color:grey">
                <p class="alert alert-danger my-0 p-1" v-for="error,index in errors" :key="index">{{ error }}</p>
    </div>
    <div class="container">
      

      <div class="mb-5 mx-5 mt-3">
        <div class="d-flex justify-content-between">
          <h1
            class="h2 d-flex align-items-center"
            style="font-family: monospace, serif"
          >
            Happy to See you again !
          </h1>
          
        </div>
      </div>
      <div class="d-flex justify-content-center">
        <div
          class="d-flex justify-content-center bg-dark p-5 shadow-lg"
          style="border-radius: 50px"
        >
          <form class="" @submit.prevent="login" >
          
            <div class="form-group mb-2">
              <label for="username" style="color: white">Email address</label>
              <input
                v-model="email"
                type="email"
                class="form-control"
                id="username"
                aria-describedby="emailHelp"
                placeholder="Enter email"
              />
              <small id="emailHelp" class="form-text text-muted"
                >We'll never share your email with anyone else.</small
              >
            </div>
            <div class="form-group mb-5">
              <label for="pass" style="color: white">Password</label>
              <input
                v-model="password"
                class="form-control"
                id="pass"
                placeholder="Password"
              />
            </div>
            <div class="d-flex justify-content-center mt-5">
              <a
                @click="login"
                class="btn btn-success d-flex justify-content-center"
                href="#"
                role="button"
                style="width: 30%"
                >Log In</a
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
      email: "",
      password: "",
      errors: [],
    };
  },

  computed: {},
  methods: {
    login() {
      if (this.email && this.password) {
      
        fetch("http://127.0.0.1:8080/login?include_auth_token", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        })
          .then((response) => {if(response.ok) {return response.json()} else{ this.errors.push('invalid credentials')}})
          .then((data) => {
            localStorage.auth_token = data.response.user.authentication_token;
            this.$router.push("/board");
          });
        }
        this.errors = [];

      if (!this.email) {
        this.errors.push('Email required.');
      }else if (!this.validEmail(this.email)) {
        this.errors.push('Valid email required.');
      }
      if (!this.password) {
        this.errors.push('Password required.');
      }
    },
    validEmail: function (email) {
      var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(email);
    }
    
  },
  
};
</script>

<style>
</style>