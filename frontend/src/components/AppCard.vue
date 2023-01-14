<template>
  <div @dragover.prevent
          @dragenter.prevent @dragstart ="startDrag($event, cid)"
            draggable="true" class="card mx-2 mb-3" style="width: 95%; min-height: 10rem">
    <div class="card-body">
      <div class="card-title">
        <div class="dropdown d-flex justify-content-around align-item-center">
          <div class="btn bg-light mx-1" style="width: 85%">{{ ctitle }}</div>
          <div v-if="this.cstatus">
            <button class="btn p-0 m-0">
              <i class="bi bi-check-circle-fill" style="font-size: 28px"></i>
            </button>
          </div>
          <div v-else>
            <button @click="mark" class="btn p-0 m-0">
              <i class="bi bi-check-circle" style="font-size: 28px"></i>
            </button>
          </div>
        </div>
      </div>
      <p class="card-text d-flex justify-content-center border rounded">
        {{ ccontent }}
      </p>
    </div>

    <!-- card delete and edit button  -->
    <div class="d-flex justify-content-between mx-2" style="text-align: center">
      <p class="card-text m-0 d-flex align-items-center">
        Deadline: {{ this.deadline }}
      </p>

      <div class="col-5 row btn-group" role="group" aria-label="Basic example">
        <p class="col-5"></p>
        <button type="button" @click="deleteCard" class="btn col-3 p-0">
          <i class="bi bi-trash" style="font-size: 20px"></i>
        </button>
        <router-link
          :to="{ name: 'editcard', params: { card_id: cid } }"
          type="button"
          class="btn col-3 p-0"
        >
          <i class="bi bi-pencil-square" style="font-size: 20px"></i>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      deadline: "",
    };
  },
  props: [
    "cid",
    "ctitle",
    "ccontent",
    "cdeadline",
    "cstatus",
    "cdatecompleted",
  ],
  mounted() {
    const d = new Date(this.cdeadline);
    this.deadline =
      d.getDate() + "/" + d.getMonth() + 1 + "/" + d.getFullYear();
  },
  methods: {
    deleteCard() {
      if (confirm("Do you really want to delete Card?")) {
        fetch("http://127.0.0.1:8080/api/card", {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "Authentication-Token": localStorage.auth_token,
          },
          body: JSON.stringify({
            id: this.cid,
          }),
        }).then((res) => {
          if (res.ok) {
            this.$router.go();
          }
        });
      }
    },
    startDrag(event, cardId) {
      event.dataTransfer.dropEffect = "move";
      event.dataTransfer.effectAllowed = "move";
      event.dataTransfer.setData("cardID", cardId);
    },

    mark() {
      fetch("http://127.0.0.1:8080/api/card", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": localStorage.auth_token,
        },
        body: JSON.stringify({
          id: this.cid,
          completed_status: "true",
        }),
      }).then((res) => {
        if (res.ok) {
          this.$router.go();
        }
      });
    }

  },
};
</script>

<style>
</style>