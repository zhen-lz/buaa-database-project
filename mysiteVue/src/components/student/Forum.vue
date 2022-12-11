<template>
  <el-container>
    <el-header>
      <el-menu
        :default-active="menuActivateIndex"
        mode="horizontal"
        @select="handleMenuSelect"
        router
      >
        <!--        <img src="src/assets/school.png">-->
        <el-menu-item index="1" route="/"
        ><span @click="logout">退出登录</span></el-menu-item
        >
        <el-menu-item index="2" route="/studentmain">个人主页</el-menu-item>
        <!--        <el-menu-item index="3">已选课程</el-menu-item>-->
        <el-menu-item index="4" route="/forum">讨论区</el-menu-item>
        <el-menu-item index="5" route="/classground">课程广场</el-menu-item>
      </el-menu>
    </el-header>

    <el-main>
      <div>
        <div class="mian">
          <div class="mian2">
            <div>
              <el-input v-model="input" placeholder="请输入内容"></el-input>
              <div
                v-for="(item, index) in tableData"
                :key="index"
                class="mian1"
              >
                <el-card class="box-card"  route="/edit">
                  <div class="text item">
                    <div class="main21">
                      <h3>{{ item.course_id }}</h3>
                      <span @click="mainedit">进入帖子</span>
                    </div>
                    {{ item.tp_title }}
                    {{ item.tp_content }}
                    {{ item.tp_time }}
                  </div>
                </el-card>
              </div>
            </div>
            <el-button @click="sou" style="height: 40px" type="primary" round
            >搜索</el-button
            >
          </div>
          <div></div>
          <div>
            <el-card class="box-card1">
              <div class="titleimg">
                <img src="../../assets/logon.jpeg" alt="" />
                <div>
                  <p>用户名:154</p>
                  <p>学号:154</p>
                  <p>已发帖子:4</p>
                </div>
              </div>
              <el-button style="width: 360px" @click="addtitle" type="primary"
              >新增主题贴</el-button
              >
            </el-card>
          </div>
        </div>
      </div>
    </el-main>
    <el-dialog
      title="新增主题贴"
      :visible.sync="dialogVisible"
      width="80%"
      :before-close="handleClose"
    >
      <el-input style="margin-bottom:20px" v-model="title" placeholder="请输入标题"></el-input>
      <quill-editor  class="editor"  v-model="content" ref="customQuillEditor"  >
      </quill-editor>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="edit"
        >确 定</el-button
        >
      </span>
    </el-dialog>
  </el-container>
</template>

<script>
import * as Quill from 'quill'
// 这里引入修改过的video模块并注册
export default {
  name: "forum",

  data() {
    return {
      tableData: [],
      menuActivateIndex: "4",
      input: "",
      title:"",
      dialogVisible:false,
      content:""
    };
  },

  created() {
    this.$axios.post('http://127.0.0.1:8000/showalltp/',JSON.stringify({stu_id:sessionStorage.username})).then(res=>{
      this.tableData=res.data.data
    })
    //
    // this.$axios.get("/data").then((response) => {
    //
    //   console.log(response.data);
    //   this.tableData = response.data.data;
    //
    //   // var data = response.data.data;
    //   //
    //   // for (var i = 0; i < 6; i++) {
    //   //   this.tableData.push(data[i])
    //   //   console.log(data[i])
    //   // }
    // });
  },
  methods: {
    mainedit(){
      this.$router.push({path:'/themepost'})
    },
    sou(){
      this.$axios.get("http://127.0.0.1:8000/searchtp/",{
        tp_title:this.input,
      }).then((response) => {
        this.tableData = response.data.data;
      });
    },

    edit(){
      this.$axios.post("http://127.0.0.1:8000/stu/newthemepost/",JSON.stringify({
        stu_id:sessionStorage.username,
        themepost: {
          tp_title: this.title,
          tp_content: this.content
        }
      })).then((response) => {
        this.dialogVisible=false
      });
    },
    handleMenuSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    logout() {
      sessionStorage.clear();

      this.$router.push("/");
    },
    addtitle() {
      this.dialogVisible = true;
    },
    handleEdit(index, row) {
      console.log(index, row);

      this.dialogVisibleEdit = true;
      this.editFrom = { ...row };
      this.editInfo = new Array({ index: index, row: row });
      console.log(this.editInfo);
    },
    handleDelete(index, row) {
      console.log(index, row);

      this.$axios
        .post("/delete", { msg: "delete", data: row })
        .then((response) => {
          console.log(response.data);

          if (response.data.error === 0) {
            this.tableData.splice(index, 1);
            this.$msgbox({
              message: "删除成功",
              type: "success",
            });
          } else {
            this.$message({ message: "删除失败", type: "error" });
          }
        });
    },
    handleAdd() {
      this.$axios
        .post("/add", { msg: "add", data: this.addFrom })
        .then((response) => {
          console.log(response.data);

          if (response.data.error === 0) {
            this.$msgbox({
              message: "添加成功",
              type: "success",
            });

            this.tableData.push(this.addFrom);
            console.log(this.tableData);
            this.dialogVisible = false;
          } else {
            this.$message({ message: "添加失败", type: "error" });
          }
        });
    },
    handleClose(done) {
      this.$confirm("确认关闭？")
        .then((_) => {
          done();
        })
        .catch((_) => {});
    },
    handleEditSubmit() {
      this.$axios
        .post("/edit", {
          msg: "edit",
          data: this.editFrom,
          info: this.editInfo,
        })
        .then((response) => {
          console.log(response.data);

          if (response.data.error === 0) {
            this.tableData.splice(this.editInfo.at(0).index, 1, this.editFrom);
            console.log(this.editInfo);

            this.$msgbox({
              message: "修改成功",
              type: "success",
            });

            this.dialogVisibleEdit = false;
          } else {
            this.$message({ message: "添加失败", type: "error" });
          }
        });
    },
  },
};
</script>


<style scoped>
.el-menu-item {
  float: right;
}
.mian {
  display: flex;
  margin: 0 10%;
}
.mian2 {
  display: flex;
  width: 45%;
}
.mian1 {
  margin: 20px 12%;
}
.el-card__body {
  height: 50px;
}
/* .el-card__body, .el-main {
  display: flex;
} */
.box-card1 {
  margin-left: 100px;
  width: 400px;
}
.titleimg {
  display: flex;
}
.titleimg > img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
}
.main21{
  display: flex;
  justify-content: space-between;
}
.main21>span{
  color: rgb(81, 136, 209);
}
h3{
  margin: 0 0;
}
</style>
