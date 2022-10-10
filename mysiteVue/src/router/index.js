import Vue from 'vue'
import Router from 'vue-router'
import LoginRegister from "../components/LoginRegister";
import HelloWorld from "../components/HelloWorld";
import demo from "../components/demo";
import Login from "../components/Login";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/hello-world',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
