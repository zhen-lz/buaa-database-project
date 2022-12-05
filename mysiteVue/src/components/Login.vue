<template>
  <div id="background">
    <!--  <img src="../images/loginimg.png"/>-->

    <div class="auth-form" style="margin-top: 10%">
      <h1 style="margin-bottom: 20px;text-align: center;font-size: 45px">Bridge课程系统</h1>
      <div class="auth-form-body">
        <el-form ref="form" label-width="80">
          <label>学号</label>
          <el-input class="input-info" v-model="username" placeholder="请输入学号"
                    prefix-icon="el-icon-user"></el-input>
          <div style="padding: 16px 0;position: relative">
            <label>密码</label>
            <el-link type="primary" style="position: absolute; top: 16px;right: 0;font-size: 14px"
                     @click="handleForgotPassword">忘记密码？
            </el-link>
            <el-input class="input-info" show-password v-model="password" placeholder="请输入密码"
                      prefix-icon="el-icon-lock"></el-input>

            <el-button type="success" style="width: 100% ;margin-top: 16px" @click="handleLogin">登录</el-button>
          </div>
        </el-form>
      </div>

      <div class="auth-form-body" style="margin-top: 16px;text-align: center;position: relative">
        <label>还没有账号？尝试去</label>
        <el-link type="primary" style="font-size: 14px;position: absolute;top: 16px" @click="dialogVisible=true">注册
        </el-link>
        <label style="margin-left: 31px">吧！</label>
      </div>

    </div>

    <el-dialog
      title="欢迎注册"
      center
      :visible.sync="dialogVisible"
      width="38%"
      :before-close="handleClose"
      append-to-body>
      <el-form :model="registerForm" label-width="auto" ref="registerForm">
        <el-form-item label='学号' prop="stu_id">
          <label slot="label">学&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;号</label>
          <el-input v-model="registerForm.stu_id"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="stu_realName">
          <label slot="label">姓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;名</label>
          <el-input v-model="registerForm.stu_realName"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <label slot="label">邮&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;箱</label>
          <el-input v-model="registerForm.email"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="stu_password1">
          <label slot="label">密&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;码</label>
          <el-input v-model="registerForm.stu_password1"></el-input>
        </el-form-item>
        <el-form-item label="请再次输入密码" prop="stu_password2">
          <el-input v-model="registerForm.stu_password2"></el-input>
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
      username: "",
      password: "",

      registerForm: {
        stu_id: '',
        stu_password1: '',
        stu_password2: '',
        stu_realName: '',
        email: '',
      },

      dialogVisible: false,
    };

  },

  methods: {
    handleLogin() {
      if (this.check(this.username) && this.check(this.password)) {
        let data = {"stu_id": this.username, "stu_password": this.password};

        this.$axios.post("http://127.0.0.1:8000/stu/login/", JSON.stringify(data)
        ).then(response => {
            console.log(response.data)

            let code = response.data.code

            if (code === 200) {
              this.$message({
                message: "登录成功！",
                type: "success"
              });

              sessionStorage.clear();
              sessionStorage.username = this.username;
              sessionStorage.password = this.password;

              setTimeout(() => {
                this.$router.push("/studentmain");
              }, 1000);

            } else {
              this.$alert(response.data.prompt, {
                type: "error",
                confirmButtonText: "确定",
                callback: action => {
                  this.password = "";
                  this.username = "";
                }
              })
            }
          }
        ).catch(error => {
          console.log(error)
        })
      } else {
        let str = "请输入";
        if (!this.check(this.username)) {
          str = str + '用户名';
        }
        if (!this.check(this.username) && !this.check(this.password)) {
          str = str + '、';
        }
        if (!this.check(this.password)) {
          str = str + '密码';
        }
        this.$message({message: str, type: 'warning'})
      }
    },

    handleForgotPassword() {
    },
    //TODO

    check(value) {
      return value !== '';
    },

    handleRegister() {
      if (this.check(this.registerForm.stu_id) && this.check(this.registerForm.stu_realName)
        && this.check(this.registerForm.email) && this.check(this.registerForm.stu_password1)
        && this.check(this.registerForm.stu_password2)) {

        this.$axios.post('http://127.0.0.1:8000/stu/register/', JSON.stringify(this.registerForm)).then(response => {
            console.log(response.data);

            if (response.data.code === 200) {

              this.$message({
                  message: "注册成功！",
                  type: "success"
                }
              );

              this.dialogVisible = false;

              this.$refs["registerForm"].resetFields();
            } else {
              this.$message({
                  message: "注册失败！" + response.data.error,
                  type: 'warning'
                }
              );
            }
          }
        ).catch(error => {
            console.log(error);
          }
        )
      } else {
        this.$message({message: '请输入完整内容！', type: 'warning'})
      }
    },

    handleClose(done) {
      this.$confirm('确认关闭？')
        .then(_ => {
          done();
        })
        .catch(_ => {
        });
    },
    handleRegisterCancel() {
      this.dialogVisible = false;
      this.$refs['registerForm'].resetFields();
    }
  }

}
</script>

<style scoped>
#background {
  background: url("../assets/R-C.png") center center no-repeat;
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
