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
                to="/board"
                >Home</router-link
              >
            </li>
            <li class="nav-item">
              <router-link
                class="nav-link active mx-4 text-white font-monospace fs-5"
                to="#"
                >Logout</router-link
              >
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="container-fluid">
      <div class="row d-flex justify-content-center m-2">
        <div
          style="width: 600px; height: 250px"
          class="col-sm-12 col-md-6 col-lg-4 border rounded m-2"
        >
          <canvas id="linechart"></canvas>
        </div>
        <div
          style="width: 600px; height: 250px"
          class="col-sm-12 col-md-4 col-lg-4 border rounded m-2"
        >
          <canvas id="barchart"></canvas>
        </div>
        <div
          style="width: 500px; height: 500px"
          class="col-sm-12 col-md-6 col-lg-4 border rounded m-2"
        >
          <canvas id="piechart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
export default {
  data() {
    return {
      graphData: {},
    };
  },
  mounted() {
    (async function () {
      const graphData = await fetch("http://127.0.0.1:8080/api/summary", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.auth_token,
        },
      })
        .then((res) => res.json())
        .then((data) => data);
      console.log(graphData);
      let dates = [];
      let count = graphData.count
      for (let x = 0; x < count.length; x++) {
        const d = new Date(graphData.dates[x]);
        dates.push(d.toISOString().substr(0, 10));
      }
      while(dates.length > 7){
        dates.shift()
        count.shift()
      }

      new Chart(document.getElementById("linechart"), {
        type: "line",
        data: {
          labels: dates,
          datasets: [
            {
              label: "Daily Cards Completed Count (last 7 days)",
              data: count,
              borderColor: "#000000",
              backgroundColor: "#000000",
            },
          ],
        },
        options: {
          scales: {
            x: {
              ticks: {
                font: {
                  weight: "bold",
                },
              },
            },
          },
        },
      });
      new Chart(document.getElementById("piechart"), {
        type: "pie",
        data: {
          labels: [
            "Total Completed Cards - " + graphData.completed,
            "Total Uncompleted Cards - " + graphData.uncompleted,
          ],
          datasets: [
            {
              label: "Daily Cards Completed Count",
              data: [graphData.completed, graphData.uncompleted],
              backgroundColor: ["#808080", "#000000"],
            },
          ],
        },
      });
      new Chart(document.getElementById("barchart"), {
        type: "bar",
        data: {
          labels: [
            "Completed After Deadline",
            "Completed Before Cards",
            "Uncompleted and Deadline crossed",
            "Uncompleted and Deadline Remaining",
          ],
          datasets: [
            {
              label: "Daily Cards Completed Count",
              data: [
                graphData.completedAfterDeadline,
                graphData.completedBeforeDeadline,
                graphData.uncompletedDeadlineCross,
                graphData.uncompletedDeadlineNotCross,
              ],
              backgroundColor: ["#808080", "#808080", "#000000", "#000000"],
            },
          ],
        },
        options: {
          scales: {
            x: {
              ticks: {
                font: {
                  size: 6, //this change the font size
                  weight: "bold",
                },
              },
            },
          },
        },
      });
    })();
  },
  methods: {},
};
</script>

<style>
</style>