<template>
  <div @dragover.prevent @dragenter.prevent class="col-sm-6 col-md-4 col-lg-3">
    <div class="bg-dark card m-2 shadow-lg w-100">
      <!-- List header  -->
      <div class="card-header row bg-white m-1 p-0">
        <h3 class="col-7 pt-1 d-flex justify-content-end">{{ lname }}</h3>
        <div
          class="col-5 row btn-group"
          role="group"
          aria-label="Basic example"
        >
          <p class="col-5"></p>
          <button type="button" @click="deleteList" class="btn col-3 p-0">
            <i class="bi bi-trash" style="font-size: 30px"></i>
          </button>
          <router-link
            :to="{ name: 'editlist', params: { list_id: lid } }"
            type="button"
            class="btn col-3 p-0"
          >
            <i class="bi bi-pencil-square" style="font-size: 30px"></i>
          </router-link>
        </div>
      </div>

      <!-- List body -->
      <div class="card-body pt-2 px-0">
        <!-- Cards -->
        <div
          style="min-height: 10px"
          @drop="onDrop($event, lid)"
          @dragover.prevent
          @dragenter.prevent
          class="d-flex flex-column"
        >
          <!-- Card -->
          <AppCard
            v-for="(card, index) in cards"
            :key="index"
            :cid="card.id"
            :ctitle="card.title"
            :ccontent="card.content"
            :cdeadline="card.deadline"
            :cstatus="card.completed_status"
            :cdatecompleted="card.date_completed"
            @dragstart="startDrag($event, card)"
            draggable="True"
            @dragenter.prevent
            @dragover.prevent
          />

          <!-- add card button  -->
          <div class="d-flex justify-content-center">
            <router-link
              :to="{ name: 'addcard', params: { list_id: lid } }"
              class="btn btn-light border rounded-pill px-4 py-3"
            >
              <span>&#43;</span>
            </router-link>
          </div>
          <div class="d-flex justify-content-end mx-2">
            <p></p>
            <a @click="exportList"
              class="btn border rounded-pill px-2 py-2"
              style="color: white"
              >Export
              <i v-if="exported" class="bi bi-file-arrow-up-fill"></i> 
              <i v-else class="bi bi-file-arrow-up"></i>
          </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AppCard from "./AppCard.vue";
export default {
  data() {
    return {
      cards: [],
      exported : false,
      job_id : "",
      intervalObj : {}
    };
  },
  components: {
    AppCard,
  },
  props: ["lid", "lname", "ldesc"],
  mounted() {
    fetch("http://127.0.0.1:8080/api/card/" + this.lid, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": localStorage.auth_token,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        this.cards = data;
      });
  },

  methods: {
    deleteList() {
      if (this.cards == 0) {
        if (confirm("Do you really want to delete List?")) {
          fetch("http://127.0.0.1:8080/api/list", {
            method: "DELETE",
            headers: {
              "Content-Type": "application/json",
              "Authentication-Token": localStorage.auth_token,
            },
            body: JSON.stringify({
              id: this.lid,
            }),
          }).then((res) => {
            if (res.ok) {
              this.$router.go();
            }
          });
        }
      } else {
        alert("Cannot delete List, First try moving cards in different list");
      }
    },

    startDrag(event, card) {
      console.log(card, event, "startdrag id");
      event.dataTransfer.dropEffect = "move";
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("cardID", card.id);
    },
    onDrop(event, listID) {
      const cardID = event.dataTransfer.getData("cardID"); // get the card id
      // now update the cards list id in the data base
      console.log(listID, "list");
      console.log(cardID, "card");
      fetch("http://127.0.0.1:8080/api/card", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.auth_token,
        },
        body: JSON.stringify({
          id: cardID,
          list_id: listID,
        }),
      }).then((res) => {
        if (res.ok) {
          this.$router.go();
        }
      });
    },

    exportList() {
      fetch("http://127.0.0.1:8080/api/export_list/"+ this.lid, {
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
          this.intervalObj = setInterval(this.checkStatus, 2000);
          // console.log(typeof(this.intervalObj))
        });
    },

    checkStatus() {
      fetch("http://127.0.0.1:8080/api/taskliststatus/" + this.job_id, {
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
            alert("List - "+ this.lname +" Exported Successfully, Downloading......");
            fetch(
              "http://127.0.0.1:8080/list" + this.lid + ".csv/download",
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