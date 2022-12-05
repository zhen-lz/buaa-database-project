<template>
  <div class="base">
    <!-- 注册登录界面 -->
    <div  class="loginAndRegister">
      <!--登录表单-->
      <div  class="loginArea">
        <transition
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInUp"
          leave-active-class="animate__zoomOut"
          appear
        >
          <!-- 标语 -->
          <div v-show="isShow" class="title">
            LOGIN
          </div>
        </transition>
        <transition
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInUp"
          leave-active-class="animate__zoomOut"
          appear
        >
          <el-form v-show="isShow">

          </el-form>
          <!-- 密码框和用户名框 -->
          <div v-show="isShow" class="pwdArea">
            <div style="flex: 1;justify-content: center;display: flex;align-items: center">
              用&nbsp;户&nbsp;名:&nbsp;
              <el-input class="username" v-model="loginUser.name" style="width: 165px;"  placeholder="用户名" size="medium"></el-input>
            </div>
            <div style="flex: 1;justify-content: center;display: flex;align-items: center">
              密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码:&nbsp;
              <el-input placeholder="密码"  v-model="loginUser.password" style="width: 165px" show-password size="medium"></el-input>
            </div>
          </div>
        </transition>
        <transition
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInUp"
          leave-active-class="animate__zoomOut"
          appear
        >
          <!-- 登录注册按钮 -->
          <div v-show="isShow" class="btnArea">
            <el-button type="success" round style="background-color: #257B5E;letter-spacing: 5px" @click="UserLogin"  >登录</el-button>
          </div>
        </transition>
      </div>
      <!-- 注册表单 -->
      <div class="registerArea">
        <transition
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInUp"
          leave-active-class="animate__zoomOut"
          appear
        >
          <!--  注册表头-->
          <div v-show="!isShow" class="rigesterTitle">
            注册
          </div>
        </transition>
        <transition
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInUp"
          leave-active-class="animate__zoomOut"
          appear
        >
          <!--            注册表单-->
          <div  v-show="!isShow" class="registerForm">
            <div style="flex: 1;display: flex;justify-content: center;align-items: center">
              用&nbsp;&nbsp;&nbsp;户&nbsp;&nbsp;&nbsp;名:
              <el-input
                placeholder="请输入用户名"
                v-model="regUser.regUsername"
                style="width: 165px;margin-left: 10px"
                clearable
                size="medium"
              >
              </el-input>
            </div>
            <div style="flex: 1;display: flex;justify-content: center;align-items: center">
              密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码:
              <el-input placeholder="请输入密码" style="width: 165px;margin-left: 10px" v-model="regUser.regPwd" show-password size="medium"></el-input>
            </div>
            <div style="flex: 1;display: flex;justify-content: center;align-items: center;">
              确&nbsp;认&nbsp;密&nbsp;码:
              <el-input placeholder="请再次输入密码" style="width: 165px;margin-left: 10px" v-model="regUser.regRePwd" show-password size="medium"></el-input>
            </div>
          </div>
        </transition>
        <transition
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInUp"
          leave-active-class="animate__zoomOut"
          appear
        >
          <!--            注册按钮-->
          <div  v-show="!isShow" class="registerBtn">
            <el-button type="success" round style="background-color: #257B5E;letter-spacing: 5px" @click="userRegister">注册</el-button>
          </div>
        </transition>
      </div>
      <!-- 信息展示界面 -->
      <div id="aaa" class="showInfo"
           :style="{
             borderTopRightRadius:styleObj.bordertoprightradius,
             borderBottomRightRadius:styleObj.borderbottomrightradius,
             borderTopLeftRadius:styleObj.bordertopleftradius,
             borderBottomLeftRadius:styleObj.borderbottomleftradius,
             right:styleObj.rightDis
            }"
           ref="showInfoView">

        <transition
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInUp"
          leave-active-class="animate__zoomOut"
          appear
        >
          <!-- 没有用户输入用户名或者找不到用户名的时候 -->
          <div v-show="isShow" style="display: flex;flex-direction: column;align-items: center;justify-content: center;width: 100%;height: 100%">
            <!-- 欢迎语 -->
            <div style="flex: 2;display: flex;align-items: center;font-size: 22px;color: #FFFFFF;font-weight: bold">
              欢迎登入后台管理系统
            </div>
            <!-- 欢迎图片 -->
            <div style="flex: 2">
              <el-button type="success"  style="background-color:#257B5E;border: 1px solid #ffffff;" round @click="changeToRegister">还没有账户？点击注册</el-button>
            </div>
          </div>
        </transition>
        <!-- 用户输入用户名时展示头像以及姓名 -->
        <!--           <div>-->

        <!--           </div>-->
        <transition
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInUp"
          leave-active-class="animate__zoomOut"
          appear
        >
          <!-- 用户注册的时候展示信息 -->
          <div v-show="!isShow" style="display: flex;flex-direction: column;align-items: center;justify-content: center;width: 100%;height: 100%">
            <!-- 欢迎语 -->
            <div style="flex: 2;display: flex;align-items: center;font-size: 22px;color: #FFFFFF;font-weight: bold">
              欢迎注册
            </div>
            <!-- 欢迎图片 -->
            <div style="flex: 2">
              <el-button type="success"  style="background-color:#257B5E;border: 1px solid #ffffff;" round @click="changeToLogin">已有账户？点击登录</el-button>
            </div>
          </div>
        </transition>
      </div>
    </div>

  </div>
</template>

<script>
import 'animate.css';
// eslint-disable-next-line no-unused-vars
import {Axios as request} from "axios";
export default {

  name:'Login',
  data(){
    return{
      //看看用不用转成用户对象
      loginUser:{
        name:"",
        password:""
      },

      admins:{},
      ////看看用不用转成用户对象
      regUser:{
        regUsername:'',
        regRePwd:'',
        regPwd:'',
        selectValue:"",
      },
      styleObj:{
        bordertoprightradius:'15px',
        borderbottomrightradius: '15px',
        bordertopleftradius:'0px',
        borderbottomleftradius:'0px',
        rightDis:'0px'
      },
      isShow:true
    }
  },
  created() {
    // this.loadInfoOfAdmin();
  },
  methods:{
    changeToRegister(){
      this.styleObj.bordertoprightradius= '0px'
      this.styleObj.borderbottomrightradius='0px'
      this.styleObj.bordertopleftradius='15px'
      this.styleObj.borderbottomleftradius='15px'
      this.styleObj.rightDis='50%'
      this.isShow = !this.isShow
    },
    changeToLogin(){
      this.styleObj.bordertoprightradius= '15px'
      this.styleObj.borderbottomrightradius='15px'
      this.styleObj.bordertopleftradius='0px'
      this.styleObj.borderbottomleftradius='0px'
      this.styleObj.rightDis='0px'
      this.isShow = !this.isShow
    },
    //用户登录
    UserLogin(){
      this.request.post("http://localhost:9090/user/login",this.loginUser).then(res=>{
        if(res.code=="200"){
          localStorage.setItem("user",JSON.stringify(res.data))
          this.$message.success("登陆成功！")
          this.$router.push("/manage")
        }else if(res.code=="400"){
          this.$message.warning(res.msg)
        }else if(res.code=="401"){
          this.$message.error(res.msg)
        }
        else{
          this.$message.error("用户名或密码错误！")
        }
      })
    },
    //加载管理员信息
    loadInfoOfAdmin(){
      this.request.get("http://localhost:9090/user/listOfAdmin").then(res=>{
        if(res.code=="200"){
          this.admins=res.data
          return true
        }
      })
    },
    //用户注册
    userRegister(){
      if(this.regUser.regUsername===""){
        this.$message.error("用户名不能为空！")
        return false
      }else if(this.regUser.regPwd!=this.regUser.regRePwd){
        this.$message.error("两次密码输入不同，请检查后重新注册！")
        return false
      }else if(this.regUser.selectValue===""){
        this.$message.error("未选择审核员!")
        return false
      }else{
        let user = {};
        user.name = this.regUser.regUsername
        user.password = this.regUser.regPwd
        user.auditor = this.regUser.selectValue
        this.request.post("http://localhost:9090/user/register",user).then(res=>{
          if(res.code==="200"){
            this.$message.success("申请成功，请耐心等待管理员审核！")
            this.regUser={  regUsername:'',
              regRePwd:'',
              regPwd:'',
              selectValue:""}
            this.changeToLogin()
          }
          if(res.code==="400"){
            this.$message.error(res.msg)
            return
          }
        })
      }

    }
  },

}
</script>

<style>
/* @import '../images/css/Login.css' */
.base{
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: url("../assets/loginimg.png");
  background-size: 100%;
}
.loginAndRegister{
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}
.loginArea{
  background-color: rgba(255,255,255,0.8);
  border-top-left-radius: 15px;
  border-bottom-left-radius: 15px;
  height: 400px;
  width: 350px;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  overflow: hidden;
}
.registerArea{
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
  height: 400px;
  width: 350px;
  background-color: rgba(255,255,255,0.8);
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content:center ;
  align-items: center;
}
.showInfo{
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
  position: absolute;
  height: 400px;
  width: 350px;
  z-index:2;
  top: 0;
  right: 0;
  background-image: url("../assets/school.png");
  background-size: 90%;
}
.showInfo:hover{
  background-size: 100%;
  background-position: -50px -50px;
}
.title{
  width: 70%;
  flex:1;
  border-bottom: 1px solid #257B5E;
  display: flex;
  align-items: center;
  color: #257B5E;
  font-weight: bold;
  font-size: 24px;
  display: flex;
  justify-content: center;
}
#aaa{
  transition: 0.3s linear;
}
.pwdArea{
  width: 100%;
  flex:2;
  display: flex;
  flex-direction: column;
  display: flex;
  flex-direction: column;


}
.pwdArea input{
  outline: none;
  height: 30%;
  border-radius:13px ;
  padding-left: 10px;
  font-size: 12px;
  border: 1px solid gray;
}
.pwdArea input:focus{
  border: 2px solid #257B5E;
}
.btnArea{
  flex:1;
  width: 100%;
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.rigesterTitle{
  width: 70%;
  flex: 1;
  color: #257B5E;
  font-weight: bold;
  font-size: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-bottom: 1px solid #257B5E;
}
.registerForm{
  flex: 2;
  display: flex;
  flex-direction: column;
  color: #257B5E;
  font-size: 16px;
}

.registerForm input{
  outline: none;
  height: 30%;
  border-radius:13px ;
  padding-left: 10px;
  font-size: 12px;
  border: 1px solid gray;
}
.registerForm input:focus{
  border: 2px solid #257B5E;
}
#elselect:focus{
  border: 2px solid #257B5E;
}
.registerBtn{
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}


</style>
