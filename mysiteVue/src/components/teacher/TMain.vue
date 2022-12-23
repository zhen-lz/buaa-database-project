<template>
  <el-container>
    <el-header>
      <el-menu :default-active="menuActivateIndex" mode="horizontal" @select="handleMenuSelect" router>
        <img src="../../../static/images/school.png" style="width: 15%">
        <el-menu-item index="1" route="/teacher/login"><span @click="logout">退出登录</span></el-menu-item>
        <el-menu-item index="2">个人主页</el-menu-item>
        <el-menu-item index="4" route="/teacher/forum">讨论区</el-menu-item>
        <el-menu-item index="5" route="/teacher/classground">课程广场</el-menu-item>
      </el-menu>
    </el-header>

    <el-main>
      <!--      <img src="@/images/school.png">-->
      <div style="text-align: center">
        <img src="../../../static/images/logon.jpeg" style="border-radius: 50%;width: 100px;height: 100px">
      </div>

      <p style="text-align: center">{{ info.teacher_name }}</p>

      <el-tabs v-model="tabsActivateName" @tab-click="handleTabsSelect" stretch>
        <el-tab-pane label="我开设的课程" name="1">
          <el-table
            :data="classMine"
            style="width: 100%"
            stripe>
            <el-table-column>
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="danger"
                  @click="deleteClass(scope.$index,scope.row)">删除课程
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
              label="课程评分"
              prop="course_rate">
              <!--              <el-rate ></el-rate>-->
            </el-table-column>

            <el-table-column
              label="选课人数/课程容量"
              prop="course_total/course_capacity">
            </el-table-column>

            <el-table-column>
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="primary"
                  @click="addCourseMaterial(scope.$index,scope.row)">添加课程资料
                </el-button>
              </template>
            </el-table-column>

            <!--            <el-table-column-->
            <!--              label="上课时间"-->
            <!--              prop="course_time">-->
            <!--            </el-table-column>-->

          </el-table>

        </el-tab-pane>
        <el-tab-pane label="个人资料" name="2">
          <el-form :model="info" ref="info" label-position="right" label-width="80px" style="width: 40%;margin: 0 auto">
            <el-form-item label="教工号">
              <el-input v-model="info.teacher_id" :disabled="true"/>
            </el-form-item>
            <el-form-item label="姓名">
              <el-input v-model="info.teacher_name" :disabled="!info_edit"/>
            </el-form-item>
            <el-form-item label="密码">
              <el-input v-model="info.teacher_password" :disabled="!info_edit" show-password/>
            </el-form-item>
            <el-form-item label="学院">
              <el-input v-model="info.depart" :disabled="!info_edit"/>
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="info.email" :disabled="!info_edit"/>
            </el-form-item>
            <el-form-item label="电话">
              <el-input v-model="info.phone" :disabled="!info_edit"/>
            </el-form-item>
            <el-form-item label="个人简介">
              <el-input v-model="info.message"
                        type="textarea"
                        :disabled="!info_edit"
                        autosize
                        :autosize="{ minRows: 2 }"/>
            </el-form-item>

            <el-form-item size="large" v-show="info_edit_show" style="text-align: center">
              <el-button type="primary" @click="changeInfo">修改资料</el-button>
            </el-form-item>

            <el-form-item size="large" v-show="!info_edit_show" style="text-align: center">
              <el-button type="primary" @click="changeInfoSubmit">确定</el-button>
              <el-button type="primary" @click="changeInfoCancel">取消</el-button>
            </el-form-item>

          </el-form>
        </el-tab-pane>
        <el-tab-pane label="我发布的帖子" name="3"></el-tab-pane>
      </el-tabs>

      <el-dialog title="添加课程资料"
                 center
                 :visible.sync="dialogVisible"
                 width="40%"
                 :before-close="closeDialog"
                 append-to-body
                 top="16vh"
      >
        <el-form ref="classMaterial" v-model="classMaterial" label-width="100px"
        >
          <el-form-item v-for="(material,index) in classMaterial.material"
                        :label="'课程资料' + Number(index+1)"
                        :key="material.key"
                        :prop="'material.' + index + '.value'">
            <div style="display: flex ">
              <el-input v-model="material.material_name"></el-input>
              <p/>
              <el-button @click.prevent="removeMaterial(material)">删除</el-button>
            </div>
          </el-form-item>

          <div style="text-align: center">
            <el-button type="primary" @click="courseMaterialSubmit()">提交</el-button>
            <el-button @click="addMaterial">新增课程资料</el-button>
            <el-button @click="closeDialog">取消</el-button>
          </div>

        </el-form>


      </el-dialog>


    </el-main>


  </el-container>
</template>/

<script>
import router from "../../router";

export default {
  name: "TMain",
  created() {
    this.username = sessionStorage.username;
    this.initData();
  },
  data() {
    return {
      menuActivateIndex: '2',
      tabsActivateName: '2',
      username: '',
      password: '',

      dialogVisible: false,
      classMaterial: {
        course_id: '',
        teacher_id: '',
        material: [{
          material_name: '',
          material_intro: ''
        }],
      },

      info: {
        teacher_id: '',
        teacher_password: '',
        teacher_name: '',
        depart: '',
        email: '',
        phone: '',
        message: ''
      },
      info_backup: {},
      info_edit: false,
      info_edit_show: true,

      post: [],

      classMine: [
        {
          course_id: '',
          course_name: '',
          course_teacher_name: '',
          course_info: '',
          course_time: '',
        },
      ],
    }
  },
  methods: {
    handleMenuSelect(key, keyPath) {
      console.log(key, keyPath)
    },
    handleTabsSelect(key, keyPath) {
      console.log(key, keyPath)
    },
    changeInfo() {
      this.info_edit_show = false;
      this.info_edit = true;

      this.info_backup = {...this.info}
    },
    changeInfoSubmit() {
      this.$axios.post('http://127.0.0.1:8000/teacher/modify/', JSON.stringify(this.info)).then(response => {
        console.log(response.data);

        if (response.data.code === 210) {

          this.$msgbox({
            message: '修改成功',
            type: 'success'
          })

          this.info_edit = false;
          this.info_edit_show = true;
        } else {
          this.$msgbox({
            message: '修改失败',
            type: "error"
          })
        }

      }).catch(response => {
        console.log(response.error)
      })
    },
    changeInfoCancel() {
      this.info_edit_show = true;
      this.info_edit = false;
      this.info = this.info_backup;
    },
    deleteClass(index, row) {
      this.$confirm("此操作将会删除该课程，并造成不可逆转的后果,是否继续？", "提示", {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let data = {'teacher_id': this.username, 'course': row}
        this.$axios.post('http://127.0.0.1:8000/teacher/rmcourse/', JSON.stringify(data)).then(response => {
          console.log(response.data);

          if (response.data.code === 0) {
            this.classSelect.splice(index, 1);
            this.$msgbox({
              message: '删除课程成功',
              type: 'success'
            })
          } else {
            this.$msgbox({
              message: '删除课程失败',
              type: "error"
            })
          }
        }).catch(response => {
          console.log(response.error)
        })

        this.classMine = this.classMine.filter(item => item.course_id !== row.course_id);
      })

    },
    addCourseMaterial(index, row) {
      this.classMaterial.course_id = row.course_id;
      this.classMaterial.teacher_id = this.username;

      this.dialogVisible = true;
    },
    courseMaterialSubmit() {
      this.$axios.post('http://127.0.0.1:8000/teacher/addmaterial/', JSON.stringify(this.classMaterial)).then(response => {
        console.log(response);

        if (response.data.code === 0) {
          this.$message({
            message: "添加成功",
            type: 'success',
          });

          this.closeDialog();

        } else {
          this.$alert(response.data.prompt, {
            type: 'error',
            confirmButtonText: "确定",
            callback: action => {
              this.$refs["classMaterial"].resetFields();
              this.classMaterial.material = [{
                material_name: '',
                material_intro: ''
              }];
            }
          })
        }
      }).catch(error => {
        console.log(error);

        this.$message({
          message: "服务器错误或响应超时",
          type: 'error'
        })
      })

    },
    closeDialog() {
      this.$refs["classMaterial"].resetFields();
      this.classMaterial.material = [{
        material_name: '',
        material_intro: ''
      }];
      this.dialogVisible = false;
    },
    removeMaterial(item) {
      var index = this.classMaterial.material.indexOf(item)
      if (index !== -1) {
        this.classMaterial.material.splice(index, 1)
      }
    },
    addMaterial() {
      this.classMaterial.material.push({
        material_name: '',
        material_intro: '',
        key: Date.now()
      });
    },

    logout() {
      sessionStorage.clear();

      this.$router.push('/')
    },
    initData() {
      let wrong = false;

      this.$axios.post('http://127.0.0.1:8000/teacher/getinfo/', JSON.stringify({"teacher_id": this.username})).then(response => {
        console.log(response.data);
        this.info = response.data
      }).catch(response => {
        console.log(response.error)
        wrong = true;
      });

      this.$axios.post('http://127.0.0.1:8000/teacher/mycourse/', JSON.stringify({"teacher_id": this.username})).then(response => {
        console.log(response.data);
        this.classMine = response.data.data
      }).catch(response => {
        console.log(response.error)
        wrong = true;
      })

      if (wrong) {
        this.$message({
          message: "服务器错误或响应超时",
          type: 'error'
        })
      }
    },


  }

}
</script>

<style scoped>
.el-menu-item {
  float: right;
}

/*.el-tabs {*/
/*  width: 50%;*/
/*  margin: 0 auto;*/
/*}*/
v-deep .el-tabs__header {
  width: 50%;
  margin: 0 auto;
}
</style>
