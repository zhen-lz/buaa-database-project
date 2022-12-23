<template>
  <div class="base">
    <!-- 注册登录界面 -->
    <div class="loginAndRegister">
      <!--登录表单-->
      <div class="loginArea">
        <transition
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInUp"
          leave-active-class="animate__zoomOut"
          appear>

          <div v-show="isShow">
            <div class="title">
              登录
            </div>

            <el-form ref="loginUser"
                     label-position="top"
                     :model="loginUser"
                     status-icon
                     :rules="loginRules">
              <el-form-item label="学号" prop="stu_id">
                <el-input class="input-info" v-model="loginUser.stu_id" placeholder="请输入学号"
                          prefix-icon="el-icon-user"></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="stu_password">
                <el-input class="input-info" show-password v-model="loginUser.stu_password" placeholder="请输入密码"
                          prefix-icon="el-icon-lock"></el-input>
              </el-form-item>

              <el-button type="success" style="width: 100% ;margin-top: 16px" round @click="userLogin">登录
              </el-button>

            </el-form>
          </div>
        </transition>

      </div>
      <!-- 注册表单 -->
      <div class="registerArea">
        <transition
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInUp"
          leave-active-class="animate__zoomOut"
          appear>
          <div v-show="!isShow">
            <div class="title">
              注册
            </div>

            <el-form ref="regUser"
                     label-width="auto"
                     label-position="right"
                     size="mini"
                     :model="regUser"
                     status-icon
                     :rules="regRules">
              <el-form-item label="学号" prop="stu_id">
                <el-input class="input-info" v-model="regUser.stu_id" placeholder="请输入学号"
                          prefix-icon="el-icon-user"></el-input>
              </el-form-item>
              <el-form-item label="姓名" prop="stu_realName">
                <el-input class="input-info" v-model="regUser.stu_realName" placeholder="请输入姓名"
                          prefix-icon="el-icon-s-custom"></el-input>
              </el-form-item>
              <el-form-item label="邮箱" prop="email">
                <el-input class="input-info" v-model="regUser.email" placeholder="请输入邮箱"
                          prefix-icon="el-icon-message"></el-input>
              </el-form-item>
              <el-form-item label="密码" prop="stu_password1">
                <el-input class="input-info" show-password v-model="regUser.stu_password1" placeholder="请输入密码"
                          prefix-icon="el-icon-lock"></el-input>
              </el-form-item>
              <el-form-item prop="stu_password2">
                <div slot="label">
                  <div style="font-size: 12px">再次输入密码</div>
                </div>
                <el-input class="input-info" show-password v-model="regUser.stu_password2"
                          placeholder="请再次输入密码"
                          prefix-icon="el-icon-lock"></el-input>
              </el-form-item>

              <el-button type="success" style="width: 100% ;margin-top: 12px" round @click="userRegister">注册
              </el-button>

            </el-form>

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

          <div v-show="isShow"
               style="display: flex;flex-direction: column;align-items: center;justify-content: center;width: 100%;height: 100%">

            <div style="flex: 2;display: flex;align-items: center;font-size: 22px;color: #FFFFFF;font-weight: bold">
              欢迎登入Bridge平台
            </div>

            <div style="flex: 2">
              <el-button type="success" style="background-color:#257B5E;border: 1px solid #ffffff;" round
                         @click="changeToRegister">还没有账户？点击注册
              </el-button>

              <div style="text-align: center;margin-top: 10px">
                <el-link @click="teacherLogin">教师登录</el-link>
              </div>

            </div>
          </div>
        </transition>


        <transition
          name="animate__animated animate__bounce"
          enter-active-class="animate__fadeInUp"
          leave-active-class="animate__zoomOut"
          appear
        >

          <div v-show="!isShow"
               style="display: flex;flex-direction: column;align-items: center;justify-content: center;width: 100%;height: 100%">
            <div style="flex: 2;display: flex;align-items: center;font-size: 22px;color: #FFFFFF;font-weight: bold">
              欢迎注册
            </div>

            <div style="flex: 2">
              <el-button type="success" style="background-color:#257B5E;border: 1px solid #ffffff;" round
                         @click="changeToLogin">已有账户？点击登录
              </el-button>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>

</template>

<script>
import '../../../node_modules/animate.css/animate.css';
// eslint-disable-next-line no-unused-vars

export default {

  name: 'Login',
  data() {
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error('密码不能为空'));
      } else {
        if (this.regUser.stu_password2 !== "") {
          this.$refs.regUser.validateField('checkPass');
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error('密码不能为空'));
      } else if (value !== this.regUser.stu_password1) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
    };
    return {
      loginUser: {
        stu_id: "",
        stu_password: ""
      },
      loginRules: {
        stu_id: [{
          required: true, message: '用户名不能为空', trigger: 'blur'
        }],
        stu_password: [{
          required: true, message: '密码不能为空', trigger: 'blur'
        }]
      },
      regUser: {
        stu_realName: "",
        stu_id: "",
        email: "",
        stu_password1: "",
        stu_password2: "",
      },
      regRules: {
        stu_id: [{
          required: true, message: '学号不能为空', trigger: 'blur'
        }],
        stu_realName: [{
          required: true, message: '姓名不能为空', trigger: 'blur'
        }],
        stu_password1: [{
          validator: validatePass, trigger: 'blur'
        }],
        stu_password2: [{
          validator: validatePass2, trigger: 'blur'
        }],
      },

      styleObj: {
        bordertoprightradius: '15px',
        borderbottomrightradius: '15px',
        bordertopleftradius: '0px',
        borderbottomleftradius: '0px',
        rightDis: '0px'
      },
      isShow: true
    }
  }
  ,
  created() {
    // this.loadInfoOfAdmin();
  },
  methods: {
    changeToRegister() {
      this.styleObj.bordertoprightradius = '0px'
      this.styleObj.borderbottomrightradius = '0px'
      this.styleObj.bordertopleftradius = '15px'
      this.styleObj.borderbottomleftradius = '15px'
      this.styleObj.rightDis = '50%'
      this.isShow = !this.isShow
    }
    ,
    changeToLogin() {
      this.styleObj.bordertoprightradius = '15px'
      this.styleObj.borderbottomrightradius = '15px'
      this.styleObj.bordertopleftradius = '0px'
      this.styleObj.borderbottomleftradius = '0px'
      this.styleObj.rightDis = '0px'
      this.isShow = !this.isShow
    }
    ,
    userLogin() {
      this.$refs["loginUser"].validate((valid) => {
        if (valid) {
          this.$axios.post("http://127.0.0.1:8000/stu/login/", JSON.stringify(this.loginUser)).then(response => {
            if (response.data.code === 200) {
              this.$message({
                message: "登录成功！",
                type: "success"
              });

              sessionStorage.clear();
              sessionStorage.username = this.loginUser.stu_id;
              sessionStorage.password = this.loginUser.stu_password;

              setTimeout(() => {
                this.$router.push("/studentmain");
              }, 500);
            } else {
              this.$alert(response.data.prompt, {
                type: "error",
                confirmButtonText: "确定",
              })
            }
          }).catch(response => {
            console.log(response)
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      })
    }
    ,
    userRegister() {
      this.$refs["regUser"].validate((valid) => {
        if (valid) {
          this.$axios.post('http://127.0.0.1:8000/stu/register/', JSON.stringify(this.regUser)).then(response => {
            if (response.data.code === 200) {

              this.$message({
                  message: "注册成功！",
                  type: "success"
                }
              );

              this.$refs["regUser"].resetFields();
            } else {
              this.$alert(response.data.prompt, {
                type: "error",
                confirmButtonText: "确定",
              })
            }
          }).catch(response => {
            console.log(response)
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      })
    },
    teacherLogin(){
      this.$router.push("teacher/login");
    }
  },


}
</script>

<style>
/* @import '../images/css/Login.css' */
.base {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: url("../../../static/images/loginimg.png");
  background-size: 100%;
}

.loginAndRegister {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.loginArea {
  background-color: rgba(255, 255, 255, 0.8);
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

.registerArea {
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
  height: 400px;
  width: 350px;
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.showInfo {
  border-top-right-radius: 15px;
  border-bottom-right-radius: 15px;
  position: absolute;
  height: 400px;
  width: 350px;
  z-index: 2;
  top: 0;
  right: 0;
  background-image: url("../../../static/images/loginimg2.png");
  background-size: 90%;
}

.showInfo:hover {
  background-size: 100%;
  background-position: -50px -50px;
}

.title {
  border-bottom: 1px solid #257B5E;
  color: #257B5E;
  font-weight: bold;
  font-size: 24px;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 25px 0;
  width: 300px;
}

#aaa {
  transition: 0.3s linear;
}

.pwdArea input {
  outline: none;
  height: 30%;
  border-radius: 13px;
  padding-left: 10px;
  font-size: 12px;
  border: 1px solid gray;
}

.pwdArea input:focus {
  border: 2px solid #409EFF;
}

.registerForm input {
  outline: none;
  height: 30%;
  border-radius: 13px;
  padding-left: 10px;
  font-size: 12px;
  border: 1px solid gray;
}

.registerForm input:focus {
  border: 2px solid #257B5E;
}
</style>
