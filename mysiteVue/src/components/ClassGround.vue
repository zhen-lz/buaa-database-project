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
          <el-button type="primary" round>搜索</el-button>
        </div>

        <el-table
          :data="tableData"
          style="width: 90%;margin: 0 auto">

          <el-table-column>
            <template slot-scope="scope">
              <el-button
                size="mini"
                type="primary"
                @click="handleSelectClass(scope.$index, scope.row)">选课
              </el-button>
            </template>
          </el-table-column>

          <el-table-column
            label="课程代号"
            prop="course_id">
          </el-table-column>

          <el-table-column
            label="课程名称"
            prop="course_name">
          </el-table-column>

          <el-table-column
            label="授课老师"
            prop="course_teacher_name">
          </el-table-column>

          <el-table-column
            label="课程信息"
            prop="course_intro">
          </el-table-column>

          <el-table-column
            label="已选人数"
            prop="course_total">
          </el-table-column>

          <el-table-column
            label="课程容量"
            prop="course_capacity">
          </el-table-column>

        </el-table>

<!--        <div v-for="(item,index) in tableData" :key="index" class="mian1">-->
<!--          <el-card class="box-card">-->
<!--            <div class="text item">-->
<!--              {{item.course_id}}-->
<!--              {{item.course_name}}-->
<!--              {{item.course_info}}-->
<!--              {{item.course_capacity}}-->
<!--            </div>-->
<!--          </el-card>-->
<!--        </div>-->
      </div>
    </el-main>

  </el-container>
</template>

<script>
export default {
  name: "ClassGround",
  created() {
    this.username=sessionStorage.username;
    this.password=sessionStorage.password;

    this.getData();
  },
  data() {
    return {
        username:'',
        password:'',
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
        if(response.data.code === 0){
          this.tableData=response.data.data
          this.$message(response.data.message)
        }else if(response.data.code === 1){
          this.$message.error(response.data.message)
        }
        console.log(response.data)

      })
    },
    handleSelectClass(index,row){
      let data = {"username":this.username,'data':row};
      console.log(row)
      this.$axios.post("http://127.0.0.1:8000/stu/add/",JSON.stringify(data)).then(response=>{
        console.log(response.data);

        if(response.data.code===0){
          this.$message({
            message:"选课成功",
            type:'success'
          })
          this.getData();
        }else{
          this.$message({
            message:"选课失败",
            type: "warning"
          })
        }
      }).catch(response=>{
        console.log(response.error);
      })
    }
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
