<template>
  <el-container>
    <el-header>
      <el-menu :default-active="menuActivateIndex" mode="horizontal" @select="handleMenuSelect" router>
        <!--        <img src="src/assets/school.png">-->
        <el-menu-item index="1" route="/"><span @click="logout">退出登录</span></el-menu-item>
        <el-menu-item index="2" route="/studentmain">个人主页</el-menu-item>
        <!--        <el-menu-item index="3">已选课程</el-menu-item>-->
        <el-menu-item index="4" route="/main">讨论区</el-menu-item>
        <el-menu-item index="5" route="/classground">课程广场</el-menu-item>
      </el-menu>
    </el-header>

    <el-main>
      <div>
        <div class="mian">
          <el-input v-model="input" placeholder="请输入内容"></el-input>
          <el-button type="primary" round>主要按钮</el-button>
        </div>

        <div v-for="o in 5" :key="o" class="mian1">
          <el-card class="box-card">
            <div class="text item">
              {{ "列表内容 " + o }}
            </div>
          </el-card>
        </div>
      </div>
    </el-main>

  </el-container>
</template>

<script>
export default {
  name: "ClassGround",
  created() {
    this.getData();
  },
  data() {
    return {
      menuActivateIndex: '5',
      tableData: [],
    }
  },
  methods: {
    logout() {
      sessionStorage.clear();

      this.$router.push('/')
    },
    handleMenuSelect(key, keyPath) {
      console.log(key, keyPath)
    },
    getData() {
      this.$axios.get('http://127.0.0.1:8000/show/').then(response=>{
        console.log(response.data)

        this.tableData=response.data.data
      })
    },
  }

}
</script>

<style scoped>
.el-menu-item {
  float: right;
}
.mian {
  display: flex;
  margin: 0 10%;
}
.mian1 {
  margin: 20px 12%;
}
.el-card__body{
  height: 50px;
}
</style>
