import Vue from 'vue'
import Router from 'vue-router'
import LoginRegister from "../components/student/LoginRegister";
import HelloWorld from "../components/student/HelloWorld";
import Login from "../components/Login";
import Main from "../components/Main";
import StudentMain from "../components/student/StudentMain";
import ClassGround from "../components/student/ClassGround";
import ThemePost from "../components/student/ThemePost";
import Forum from "../components/student/Forum";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: LoginRegister
    },
    {
      path: '/studentmain',
      component: StudentMain
    },
    {
      path: '/loginresgister',
      component: LoginRegister
    },
    {
      path: '/classground',
      component: ClassGround
    },
    {
      path: '/themepost',
      component: ThemePost
    },
    {
      path: '/forum',
      component: Forum
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


  ],
  mode: 'history'
})
