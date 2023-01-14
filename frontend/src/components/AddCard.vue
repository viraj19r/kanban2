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
                <h1 class="h2 d-flex align-items-center" style="font-family: monospace, serif;">Add a card to your list
                    - List-1:

                </h1>
            </div>
        </div>
        <div class="container d-flex justify-content-center">
            <div class="d-flex justify-content-center bg-dark py-5 px-1 w-75 shadow-lg " style="border-radius: 50px;">
                <div class="" style="height: 30%; width:90%;">
                    <div class="d-flex justify-content-center">
                        <h2 style="color: white;">Add Card</h2>
                    </div>
                    <div class="mb-3">
                        <label for="title"  class="form-label" style="color: white;">Title</label>
                        <input type="text" v-model="title" class="form-control" id="title" placeholder="card-1">
                    </div>
                    <div class="mb-3">
                        <label for="content" class="form-label" style="color: white;">Content</label>
                        <textarea class="form-control" v-model="content" id="content" rows="3" placeholder="content..."></textarea>
                    </div>
                    <div class="mb-3">
                        <label for="date" class="form-label" style="color: white;">Date  : </label>
                        <input class="border rounded py-2 px-2 w-100" v-model="deadline" value="2022-02-19"  type="date" name="date"
                            id="date"> <!-- update this value using python current date attribute -->
                        </div>
                    <!-- <div class="mb-3">
                        <label for="list" style= "color: white;">Choose List :</label>
                        <select v-model="category" name="list" id="list" class="border rounded w-100 p-2">
                            <option v-for="list in lists" :key="list.id" :value="list.id" v-text="list.name" :selected="list.id == category? 'selected' : ''" ></option>
                        </select>
                    </div> -->
    
                    <div class="d-flex justify-content-center">
                        <div class="btn-group btn-group-toggle" data-toggle="buttons">
                            <label class="btn btn-success bg-dark">
                                <input type="radio" value="true" v-model="completed_status" name="options" id="option1" autocomplete="off"> Completed
                            </label>
                            <label class="btn btn-primary bg-dark active">
                                <input type="radio" value="false" v-model="completed_status" name="options" id="option2" autocomplete="off" checked> Uncompleted
                            </label>
                        </div>
                    </div>
                    <div class="d-flex justify-content-center mt-3">
                        <a @click="addCard" class="btn btn-primary d-flex justify-content-center" href="#" role="button"
                            style="width: 30%;">Save</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
  data(){
    return {
      lists : [],
      title : "",
      content : "",
      deadline : "",
      completed_status : false
    }
  },
  props:['list_id'],
  mounted() {
    fetch("http://127.0.0.1:8080/api/list", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": localStorage.auth_token
      },
    }).then((res)=> res.json()).then((data) => { this.lists = data });
  },
  methods:{
    addCard(){
      fetch("http://127.0.0.1:8080/api/card", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authentication-Token": localStorage.auth_token
      },
      body : JSON.stringify({
      "title": this.title,
      "content" : this.content,
      "deadline" : this.deadline,
      "list_id" : this.list_id,
      "completed_status" : this.completed_status
})
    }).then((res)=> {if(res.ok){ this.$router.push('/board')}});
      
      

    },
    
  },
  computed:{
      category(){
        return this.list_id
      }

    }
};
</script>

<style>
</style>