import Vue from 'vue'
import Router from 'vue-router'
import LoginRegister from "../components/LoginRegister";
import HelloWorld from "../components/HelloWorld";
import demo from "../components/demo";
import Login from "../components/Login";
import Main from "../components/Main";
import StudentMain from "../components/StudentMain";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/login',
      component: Login
    },
    {
      path: '/main',
      component: Main
    },
    {
      path: '/hello-world',
      component: HelloWorld
    },
    {
      path:'/stumain',
      component:StudentMain
    },
    {
      path:'/loginres',
      component:LoginRegister
    }
  ],
  mode:'history'
})
