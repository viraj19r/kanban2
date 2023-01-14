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
              <a
                class="nav-link active mx-4 text-white font-monospace fs-5"
                aria-current="page"
                @click="exportBoard"
                >Export<i v-if="exported" class="bi bi-file-arrow-up-fill"></i
                ><i v-else class="bi bi-file-arrow-up"></i>
              </a>
            </li>
            <li class="nav-item">
              <a
                class="nav-link active mx-4 text-white font-monospace fs-5"
                aria-current="page"
                @click="logout"
                >Logout</a
              >
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <!-- <h1 class="container">This is our board</h1> -->
    <div v-if="lists.length != 0">
      <div class="mb-2 mx-5 mt-3">
        <div class="d-flex justify-content-between">
          <h3
            class="h3 d-flex align-items-center"
            style="font-family: monospace, serif"
          >
            Welcome back!
          </h3>
          <router-link
            to="/board/addlist"
            class="btn btn-dark border rounded-pill p-4 shadow-lg"
            >Add <span>&#43;</span></router-link
          >
        </div>
      </div>
      <div class="container-fluid row mb-5 p-0">
        <AppList
          v-for="(list, index) in lists"
          :key="index"
          :lid="list.id"
          :lname="list.name"
          :ldesc="list.description"
        />
      </div>
    </div>
    <div v-else class="container-fluid mb-5 p-0">
      <div class="mb-5 mx-5 mt-3">
        <div class="d-flex justify-content-between">
          <h1
            class="h2 d-flex align-items-center"
            style="font-family: monospace, serif"
          >
            Welcome, Nice to have you here!
          </h1>
        </div>
        <div class="d-flex flex-row justify-content-center m-5">
          <h3 class="d-flex align-items-center mx-5">Create list here</h3>
          <router-link
            to="/board/addlist"
            class="btn btn-dark border rounded-pill p-4 shadow-lg"
            >Add <span>&#43;</span></router-link
          >
        </div>
        <div class="d-flex flex-row justify-content-center p-2">
          <div class="bg-white">
            <h3 class="px-2 my-3">
              Use this Kanban board for better work management
            </h3>
            <ul class="list-group">
              <li class="list-group-item">
                Visualize Your Workflow on the Kanban Board
              </li>
              <li class="list-group-item">
                Use the Kanban Board to Limit Work in Progress and Focus
              </li>
              <li class="list-group-item">
                Collect Key Workflow Metrics and Improve as your summary
              </li>
            </ul>
            <h3 class="px-2 py-2 my-3">Kanban elements Used</h3>
            <ul class="list-group">
              <li class="list-group-item px-2 py-3">
                <strong>Kanban Lists - </strong>Each column on the board
                represents a different stage of your workflow. The cards go
                through the workflow until their full completion.
              </li>
              <li class="list-group-item px-2 py-3">
                <strong> Kanban Cards – </strong> This is the visual
                representation of tasks. Each card contains information about
                the task and its status, such as deadline, assignee,
                description, etc.
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppList from "./AppList.vue";

export default {
  data() {
    return {
      lists: [],
      exported: false,
      job_id: "",
      user_id: 0,
      intervalObj: {},
    };
  },
  components: {
    AppList,
  },
  mounted() {
    fetch("http://127.0.0.1:8080/api/list", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": localStorage.auth_token,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        this.lists = data;
      });
  },
  methods: {
    logout() {
      fetch("http://127.0.0.1:8080/logout", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      }).then((res) => {
        if (res.ok) {
          localStorage.removeItem("auth_token");
          this.$router.push("/login");
        }
      });
    },
    exportBoard() {
      fetch("http://127.0.0.1:8080/api/export_board", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.auth_token,
        },
      })
        .then((res) => {
          if (res.ok) {
            return res.json();
          }
        })
        .then((data) => {
          this.job_id = data.job_id;
          this.user_id = data.user_id;
          this.intervalObj = setInterval(this.checkStatus, 2000);
          // console.log(typeof(this.intervalObj))
        });
    },

    checkStatus() {
      fetch("http://127.0.0.1:8080/api/taskboardstatus/" + this.job_id, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.auth_token,
        },
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.state == "SUCCESS") {
            clearInterval(this.intervalObj);
            this.exported = true
            alert("Board Exported Successfully, Downloading......");
            fetch(
              "http://127.0.0.1:8080/board" + this.user_id + ".csv/download",
              {
                method: "GET",
                headers: {
                  "Content-Type": "application/json",
                },
              }
            )
              .then((res) => res.blob())
              .then((blob) => {
                var file = window.URL.createObjectURL(blob);
                window.location.assign(file);
              });
          }
        });
    },
  },
};
</script>

<style>
</style>