<template>
  <el-container>


    <el-main>

      <div>
        <div class="mian">
          <div class="mian2">
            <div>
              <el-divider>楼主</el-divider>
              <div class="item">
                <h3>12321</h3>
                <el-button style="height: 40px" type="primary" size="small">跟帖</el-button>
              </div>
              <el-divider >跟帖</el-divider>
              <div
                v-for="(item1, index) in tableData"
                :key="index"
                class="mian1"
              >
                <el-card class="box-card" >
                  <div class="item">
                    <img sty src="../../assets/logon.jpeg" alt="" />
                    <h3>{{ item1.course_id }}</h3>
                    <el-button style="height: 40px" @click="delete1" type="danger" size="small">删除</el-button>
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
// import * as Quill from 'quill'
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
      content:""
    };
  },

  created() {
    this.$axios.get("/data").then((response) => {

      console.log(response.data);
      this.tableData = response.data.data;

      // var data = response.data.data;
      //
      // for (var i = 0; i < 6; i++) {
      //   this.tableData.push(data[i])
      //   console.log(data[i])
      // }
    });
  },
  methods: {
    delete1(){
      this.$axios.get("http://127.0.0.1:8000/stu/newthemepost/",{
        tp_id:"",
        tp_title:this.title,
        tp_content:this.content
      }).then((response) => {
        this.dialogVisible=false
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
      this.$axios.get("http://127.0.0.1:8000/stu/newthemepost/",{
        tp_id:"",
        tp_title:this.title,
        tp_content:this.content
      }).then((response) => {
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
