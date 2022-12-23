<template>
  <el-container>

<el-header>
  <el-menu :default-active="menuActivateIndex" mode="horizontal" @select="handleMenuSelect" router>
    <img src="../../../static/images/school.png" style="width: 15%">
    <el-menu-item index="1" route="/teacher/login"><span @click="logout">退出登录</span></el-menu-item>
    <el-menu-item index="2" route="/teacher/main">个人主页</el-menu-item>
    <el-menu-item index="4" route="/teacher/forum">讨论区</el-menu-item>
    <el-menu-item index="5" >课程广场</el-menu-item>
  </el-menu>
</el-header>
    <el-main>

      <div>
        <div class="mian">
          <div class="mian2">
            <div>
              <el-divider>楼主</el-divider>
              <div class="item">
                <h3>帖子标题：{{  toplist.tp_title }}</h3>
<!--                <h3>{{ toplist.tp_content }}</h3>-->
                <div>
                    <el-button style="height: 40px" @click="addtitle" type="primary" size="small">跟帖</el-button>
                    <el-button style="height: 40px" type="primary" @click="fan" size="small">返回</el-button>
                    </div>
              </div>
              <h3>帖子内容:</h3>
              <div style="margin-left: 80px;font-size: 17px"><span v-html="   toplist.tp_content" style=""></span></div>
              <el-divider >跟帖</el-divider>
              <div
                v-for="(item1, index) in tableData"
                :key="index"
                class="mian1"
              >
                <el-card class="box-card" >
                  <div class="item">
                    <span>
                      <h3 style="float: left">{{ item1.teacher_name }}{{ item1.stu_name }}:</h3>
                      <span v-html="item1.fp_content" style="float: left;margin-top: 3px;margin-left: 10px;font-size: 15px"></span>
                    </span>
                    <el-button style="height: 40px" @click="delete1(item1)" type="danger" size="small">删除</el-button>
                  </div>
                </el-card>


              </div>
            </div>

          </div>
          <div></div>
        </div>
      </div>
    </el-main>
    <el-dialog
      title="跟帖"
      :visible.sync="dialogVisible"
      width="80%"
      :before-close="handleClose"
    >
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
  name: "themepost",

  data() {
    return {
      tableData: [],
      menuActivateIndex: "4",
      input: "",
      title:"",
      dialogVisible:false,
      content:"",
      tp_id:"",
      username:"",
      toplist:[]
    };
  },

  created() {
    this.username=sessionStorage.username;

  },
  watch:{
      $route: {
      handler: function(val, oldVal) {
        console.log(val, oldVal)
         this.tp_id = this.$route.query.tp_id
        this.toplist = this.$route.query
        console.log(this.toplist)
        this.getshowAllFp()
      },
      immediate: true,
       deep:true
    }
  },

  methods: {

    getshowAllFp(){
      this.$axios.post('http://127.0.0.1:8000/showallfp/',JSON.stringify({tp_id:this.tp_id})).then(res=>{
      this.tableData=res.data.data
      console.log(this.tableData)
    })
    },
    fan(){
      this.$router.push("/teacher/forum");
    },
    delete1(item1){
      this.$axios.post("http://127.0.0.1:8000/teacher/deletefollowpost/",JSON.stringify({
        tp_id:this.tp_id,
        teacher_id:this.username,
        fp_id:item1.fp_id
      })).then((response) => {
        this.getshowAllFp()
      });
    },
    sou(){
      this.$axios.get("http://127.0.0.1:8000/searchtp/",{
        tp_title:this.input,
      }).then((response) => {
        this.tableData = response.data.data;
      });

    },
    edit(){

     let data={
        "teacher_id": this.username,
        "tp_id":this.tp_id,
        "fp_content":this.content
      };
      this.$axios.post("http://127.0.0.1:8000/teacher/newfollowpost/",JSON.stringify(data)).then((response) => {
        this.dialogVisible=false
        this.content = ""
        this.getshowAllFp()
      });
    },
    handleMenuSelect(key, keyPath) {
      console.log(key, keyPath);
    },
    logout() {
      sessionStorage.clear();

      this.$router.push("/teacher/login");
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
  margin: 0 10%;
}
.mian2 {
  width: 100%;
}
.mian1 {

}
.el-card__body {
  height: 50px;
}
/* .el-card__body, .el-main {
  display: flex;
} */
.box-card {
  margin: 0 auto;
  text-align: center;
  width: 1000px;
}
.box-card:hover{
  margin-top: 7px;
  background-color: #e8eaec;
}
.titleimg {
  display: flex;
}
.item > img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-right: 20px;
}
.item{
  display: flex;
  justify-content: space-between;
}
</style>
