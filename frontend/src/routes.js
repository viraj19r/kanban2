// import AppBoard from './components/AppBoard.vue'
import RegisterUser from './components/RegisterUser.vue'
import LoginUser from './components/LoginUser.vue'
import AppHome from './components/AppHome.vue'
import AppBoard from './components/AppBoard.vue'
import AppSummary from './components/AppSummary.vue'
import AddList from './components/AddList.vue'
import AddCard from './components/AddCard.vue'
import EditList from './components/EditList.vue'
import EditCard from './components/EditCard.vue'

export default [
    {
      path: '/',
      redirect: '/login',
      name : 'root',
      component : LoginUser,
      
    },
    {
      path: '/login',
      name : 'login',
      component : LoginUser
    },
    {
      path: '/register',
      name : 'register',
      component : RegisterUser
    },
    {
      path: '/board',
      component : AppHome,
      children : [
        {
          // UserProfile will be rendered inside User's <router-view>
          // when /board is matched
          path: '/',
          name : 'board',
          component: AppBoard,
          children : [
            
          ]
        },
        {
          // when /board/summary is matched
          path: 'summary',
          component: AppSummary
        },
        {
          // when /board/addlist is matched
          path: 'addlist',
          component: AddList
        },
        {
          // when /board/addcard is matched
          path: 'addcard/:list_id',
          name : 'addcard',
          component: AddCard,
          props: true
        },
        {
          path: 'editlist/:list_id',
          name : 'editlist',
          component: EditList,
          props: true
          
        },
        {
          path: 'editcard/:card_id',
          name : 'editcard',
          component: EditCard,
          props: true
          
        }
        
    ]
    },
  
    
  ]




