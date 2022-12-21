<template>
  <div id="background">
    <!--  <img src="../images/loginimg.png"/>-->

    <div class="auth-form" style="margin-top: 5%">
      <h1 style="margin-bottom: 20px;text-align: center;font-size: 45px">Bridge课程系统</h1>
      <h2 style="text-align: center">老师端</h2>
      <div class="auth-form-body">
        <el-form ref="form" label-width="80" :model="loginForm">
          <label>教工号</label>
          <el-input class="input-info" v-model="loginForm.teacher_id" placeholder="请输入教工号"
                    prefix-icon="el-icon-user"></el-input>
          <div style="padding: 16px 0;position: relative">
            <label>密码</label>
            <el-link type="primary" style="position: absolute; top: 16px;right: 0;font-size: 14px"
                     @click="handleForgotPassword">忘记密码？
            </el-link>
            <el-input class="input-info" show-password v-model="loginForm.teacher_password" placeholder="请输入密码"
                      prefix-icon="el-icon-lock"></el-input>

            <el-button type="success" style="width: 100% ;margin-top: 16px" @click="handleLogin">登录</el-button>
          </div>
        </el-form>
      </div>

      <div class="auth-form-body" style="margin-top: 16px;text-align: center;position: relative">
        <label>没有账号？尝试去</label>
        <el-link type="primary" style="font-size: 14px;position: absolute;top: 16px" @click="dialogVisible=true">注册
        </el-link>
        <label style="margin-left: 31px">吧！</label>
      </div>

    </div>

    <el-dialog
      title="欢迎老师注册"
      center
      :visible.sync="dialogVisible"
      width="38%"
      :before-close="handleRegisterCancel"
      append-to-body
      top="8vh">
      <el-form :model="registerForm" label-width="auto" ref="registerForm">
        <el-form-item label='教工号' prop="teacher_id">
          <label slot="label">教&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;工&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;号</label>
          <el-input placeholder="请输入您的教工号" v-model="registerForm.teacher_id"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="teacher_realName">
          <label slot="label">真&nbsp;&nbsp;&nbsp;实&nbsp;&nbsp;&nbsp;姓&nbsp;&nbsp;&nbsp;名</label>
          <el-input placeholder="请输入您的真实姓名" v-model="registerForm.teacher_realName"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <label slot="label">邮&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;箱</label>
          <el-input placeholder="请输入您的邮箱" v-model="registerForm.email"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="teacher_password1">
          <label slot="label">密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码</label>
          <el-input show-password placeholder="请输入您的密码" v-model="registerForm.teacher_password1"></el-input>
        </el-form-item>
        <el-form-item label="请再次输入密码" prop="teacher_password2">
          <label slot="label">请再次输入密码</label>
          <el-input show-password placeholder="请再次输入您的密码" v-model="registerForm.teacher_password2"></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
    <el-button @click="handleRegisterCancel">取消</el-button>
    <el-button type="primary" @click="handleRegister">确定</el-button>
  </span>
    </el-dialog>

  </div>
</template>

<script>
export default {
  name: "Login",

  data() {
    return {
      loginForm: {
        teacher_id: '',
        teacher_password: '',
      },

      registerForm: {
        teacher_id: '',
        teacher_password1: '',
        teacher_password2: '',
        teacher_realName: '',
        email: '',
      },

      dialogVisible: false,
    };

  },

  methods: {
    handleLogin() {
      this.$axios.post("http://127.0.0.1:8000/teacher/login/", JSON.stringify(this.loginForm)
      ).then(response => {
          console.log(response)
          let code = response.data.code

          if (code === 200) {
            this.$message({
              message: "登录成功！",
              type: "success"
            });

            sessionStorage.clear();
            sessionStorage.username = this.loginForm.teacher_id;

            setTimeout(() => {
              this.$router.push("/teacher/main");
            }, 500);

          } else {
            this.$alert(response.data.prompt, {
              type: "error",
              confirmButtonText: "确定",
              callback: action => {
                this.loginForm.teacher_id = "";
                this.loginForm.teacher_password = "";
              }
            })
          }
        }
      ).catch(error => {
        console.log(error)

        this.$message({
          message: "服务器错误或响应超时",
          type: 'error'
        })
      })

    },

    handleForgotPassword() {
    },


    handleRegister() {
      this.$axios.post('http://127.0.0.1:8000/teacher/register/', JSON.stringify(this.registerForm)).then(response => {
          console.log(response);

          if (response.data.code === 200) {

            this.$message({
                message: "注册成功！",
                type: "success"
              }
            );

            this.dialogVisible = false;

            this.$refs["registerForm"].resetFields();
          } else {
            this.$alert(response.data.error, {
                type: "error",
                confirmButtonText: "确定",
                callback: action => {
                  this.$refs["registerForm"].resetFields();
                }
              }
            );
          }
        }
      ).catch(error => {
          console.log(error);

          this.$message({
            message: "服务器错误或响应超时",
            type: 'error'
          })
        }
      )
    },

    handleRegisterCancel() {
      this.$refs['registerForm'].resetFields();
    }
  }

}
</script>

<style scoped>
#background {
  background: url("../../assets/R-C.png") center center no-repeat;
  width: 100%;
  height: 100%;
  position: fixed;
  background-size: cover;
}


.auth-form {
  width: 340px;
  margin: 0 auto;
  text-align: left;
}

.auth-form-body {
  border-radius: 6px;
  padding: 16px;
  font-size: 14px;
  background-color: #f6f8fa;
  border: 1px solid hsla(210, 18%, 87%, 1);
}

.input-info {
  padding: 5px 0;
  font-size: 14px;
}

</style>
