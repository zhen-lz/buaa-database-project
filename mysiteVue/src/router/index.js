import Vue from 'vue'
import Router from 'vue-router'
import LoginRegister from "../components/student/LoginRegister";
import HelloWorld from "../components/HelloWorld";
import TLogin from "../components/teacher/TLogin";
import Main from "../components/Main";
import StudentMain from "../components/student/StudentMain";
import ClassGround from "../components/student/ClassGround";
import ThemePost from "../components/student/ThemePost";
import Forum from "../components/student/Forum";
import TMain from "../components/teacher/TMain";
import TClassGround from "../components/teacher/TClassGround";

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
      path: '/teacher/login',
      component: TLogin
    },
    {
      path: '/teacher/main',
      component: TMain
    },
    {
      path: '/teacher/classground',
      component: TClassGround
    },
    {
      path: '/teacher/forum',
      component: TMain
    },
    {
      path: '/teacher/themepost',
      component: TMain
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
