<template>
  <div id="background">
    <!--  <img src="../assets/loginimg.png"/>-->

    <div class="auth-form" style="margin-top: 280px">
      <h1 style="margin-bottom: 16px;text-align: center">欢迎回来！</h1>
      <div class="auth-form-body">
        <el-form ref="form" label-width="80">
          <label>用户名</label>
          <el-input class="input-info" v-model="username" placeholder="请输入用户名" prefix-icon="el-icon-user"
                    @blur="check(username)"></el-input>
          <div style="padding: 16px 0;position: relative">
            <label>密码</label>
            <el-link type="primary" style="position: absolute; top: 16px;right: 0;font-size: 14px"
                     @click="forgotpassword">忘记密码？
            </el-link>
            <el-input class="input-info" show-password v-model="password" placeholder="请输入密码"
                      prefix-icon="el-icon-lock" @blur="check(password)"></el-input>

            <el-button type="success" style="width: 100% ;margin-top: 16px" @click="loginhander">登录</el-button>
          </div>
        </el-form>
      </div>

      <div class="auth-form-body" style="margin-top: 16px;text-align: center;position: relative">
        <label>还没有账号？尝试去</label>
        <el-link type="primary" style="font-size: 14px;position: absolute;top: 16px" @click="gotoregister">注册
        </el-link>
      </div>


    </div>

  </div>
</template>

<script>
export default {
  name: "Login",

  data() {
    return {
      username: "",
      password: "",
    };
  },

  methods: {
    loginhander() {
      this.$axios.post("http://localhost:8080/api/mock",{'username':this.username,'password':this.password}).then(response => {
        this.result = response.data
        console.log(response.data)
      }).catch(error => {
        console.log(error)
      })

      if (this.result === 1) {
        this.$alert("密码不对", {
          type: "error",
          confirmButtonText: "确定",
          callback: action => {
            this.password = "";
          }
        })
      }

      if (this.result === 2) {
        this.$alert("用户不存在", {
          type: "error",
          confirmButtonText: "确定",
          callback: action => {
            this.password = "";
            this.username = "";
          }
        })
      }

      if (this.result === 0) {
        this.$message({
            message: "登录成功！",
            type: "success"
          }
        );

        setTimeout(() => {
          this.$router.push("/hello-world");
        }, 1000);
      }

    },

    // forgotpassword() {
    // },
    // TODO: 忘记密码处理

    // gotoregister() {
    // },
    // TODO: 注册信息

    check(value) {
      if (value === '') {
        this.$message({message: '请输入字符', type: 'warning'})
      }
    },

  }

}
</script>

<style scoped>
#background {
  background: url("../assets/loginimg.png") center center no-repeat;
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
