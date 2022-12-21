<template>
  <el-container>
    <el-header>
      <el-menu :default-active="menuActivateIndex" mode="horizontal" @select="handleMenuSelect" router>
        <img src="../../../static/images/school.png" style="width: 15%">
        <el-menu-item index="1" route="/"><span @click="logout">退出登录</span></el-menu-item>
        <el-menu-item index="2">个人主页</el-menu-item>
        <!--        <el-menu-item index="3">已选课程</el-menu-item>-->
        <el-menu-item index="4" route="/forum">讨论区</el-menu-item>
        <el-menu-item index="5" route="/classground">课程广场</el-menu-item>
      </el-menu>
    </el-header>

    <el-main>
      <!--      <img src="@/images/school.png">-->
      <div style="text-align: center">
        <img src="@/assets/dog.jpg" style="border-radius: 50%;width: 100px;height: 100px">
      </div>

      <p style="text-align: center">{{ info.stu_name }}</p>

      <el-tabs v-model="tabsActivateName" @tab-click="handleTabsSelect" stretch>
        <el-tab-pane label="已选课程" name="1">
          <el-table
            :data="classSelect"
            style="width: 100%"
            stripe>
            <el-table-column>
              <template slot-scope="scope">
                <el-button
                  size="mini"
                  type="danger"
                  @click="deleteClass(scope.$index,scope.row)">退选
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

            <!--            <el-table-column-->
            <!--              label="上课时间"-->
            <!--              prop="course_time">-->
            <!--            </el-table-column>-->

          </el-table>

        </el-tab-pane>
        <el-tab-pane label="个人资料" name="2">
          <el-form :model="info" ref="info" label-position="right" label-width="80px" style="width: 50%;margin: 0 auto">
            <el-form-item label="学号">
              <el-input v-model="info.stu_id" :disabled="true"/>
            </el-form-item>
            <el-form-item label="姓名">
              <el-input v-model="info.stu_name" :disabled="!info_edit"/>
            </el-form-item>
            <el-form-item label="密码">
              <el-input v-model="info.stu_password" :disabled="!info_edit" show-password/>
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
              <el-input v-model="info.message" type="textarea" :disabled="!info_edit" rows="2"/>
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
        <el-tab-pane label="我的帖子" name="3"></el-tab-pane>
      </el-tabs>


    </el-main>


  </el-container>
</template>/

<script>
import router from "../../router";

export default {
  name: "StudentMain",
  created() {
    this.username = sessionStorage.username;
    this.password = sessionStorage.password;
    this.initData();
  },
  data() {
    return {
      menuActivateIndex: '2',
      tabsActivateName: '2',
      username: '',
      password: '',

      info: {
        stu_id: '',
        stu_password: '',
        stu_name: '',
        depart: '',
        email: '',
        phone: '',
        message: ''
      },
      info_backup: {},
      info_edit: false,
      info_edit_show: true,

      post: [],

      classSelect: [
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
      this.$axios.post('http://127.0.0.1:8000/stu/modify/', JSON.stringify(this.info)).then(response => {
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
      let data = {'username': this.username, 'course': row}
      this.$axios.post('http://127.0.0.1:8000/stu/rmcourse/', JSON.stringify(data)).then(response => {
        console.log(response.data);

        if (response.data.code === 0) {
          this.classSelect.splice(index, 1);
          this.$msgbox({
            message: '退课成功',
            type: 'success'
          })
        } else {
          this.$msgbox({
            message: '退课失败',
            type: "error"
          })
        }
      }).catch(response => {
        console.log(response.error)
      })
    },
    logout() {
      sessionStorage.clear();

      this.$router.push('/')
    },
    initData() {
      // console.log(this.username,this.password);
      this.$axios.post('http://127.0.0.1:8000/stu/getinfo/', JSON.stringify({"stu_id": this.username})).then(response => {
        console.log(response.data);
        this.info = response.data
      }).catch(response => {
        console.log(response.error)
      });

      this.$axios.post('http://127.0.0.1:8000/stu/mycourse/', JSON.stringify({"stu_id": this.username})).then(response => {
        console.log(response.data);
        this.classSelect = response.data.data
      }).catch(response => {
        console.log(response.error)
      })
    }

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
