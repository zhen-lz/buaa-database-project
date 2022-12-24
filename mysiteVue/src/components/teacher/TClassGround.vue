<template>
  <el-container>
    <!--    <div style="width: 100%;height: 100%;">-->
    <!--      <el-backtop visibility-height="200"></el-backtop>-->
    <!--    </div>-->

    <el-header>
      <el-menu :default-active="menuActivateIndex" mode="horizontal" @select="handleMenuSelect" router>
        <img src="../../../static/images/school.png" style="width: 15%">
        <el-menu-item index="1" route="/teacher/login"><span @click="logout">退出登录</span></el-menu-item>
        <el-menu-item index="2" route="/teacher/main">个人主页</el-menu-item>
        <el-menu-item index="4" route="/teacher/forum">讨论区</el-menu-item>
        <el-menu-item index="5" route="/teacher/classground">课程广场</el-menu-item>
      </el-menu>
    </el-header>

    <el-main>
      <el-tabs v-model="tabsValue" type="card" @tab-remove="removeTab">

        <el-tab-pane
          :key="mainTab.name"
          :label="mainTab.title"
          :name="mainTab.name">

          <div style="display: flex;margin: 0 8%;">
            <el-input v-model="searchClassKeyword"
                      placeholder="输入您想查找的课程名称"
                      prefix-icon="el-icon-search"/>
            &nbsp;&nbsp;&nbsp;
            <el-button type="primary" circle icon="el-icon-search" plain @click="searchClassClick"/>
            <el-button type="danger" round @click="searchClassDelete" v-show="searchClassDeleteShow">
              清除搜索
            </el-button>
            <el-button type="primary" round @click="dialogVisible=true" v-show="!searchClassDeleteShow">
              开设课程
            </el-button>
          </div>

          <div style="margin: 20px 10%">
            <el-card shadow="hover" style="margin: 10px 0" v-for="(item,index) in classAll">

              <div style="display: flex;position: relative">
                <div style="position: relative;left: 8%">
                  <img src="../../../static/images/BUAALogo.jpg"
                       style="width: 50px;height: 50px">
                </div>

                <div style="position: relative;left: 18%">
                  <el-tooltip effect="light" placement="right" content="点击查看课程详情" :open-delay="1000">
                    <el-link type="primary" :underline="false" @click="classIntroClick(item,index)"
                             style="font-size: 20px;font-weight: bold">
                      {{ item.course_name }}
                    </el-link>
                  </el-tooltip>

                  <el-rate v-model="item.course_rate" disabled show-score></el-rate>
                  <!--                  <stars v-model="item.course_rate"></stars>-->
                </div>

                <div style="position: absolute;right: 5%;">
                  选课人数/课程容量
                  <div class="text-box">{{ item.course_total }}/{{ item.course_capacity }}</div>

                </div>

              </div>
            </el-card>

          </div>
        </el-tab-pane>

        <el-tab-pane
          v-for="(item,index) in tabs"
          :key="item.name"
          :label="item.title"
          :name="item.name"
          closable>
          <el-card shadow="never" style="margin: 20px 12%">
            <div style="display: flex">
              <div>
                <img src="../../../static/images/BUAALogo.jpg" style="width: 200px;height: 200px">
              </div>
              <div style="width: 80%">
                <div class="text-box-title" style="text-align: left">课程名称：{{ item.content.data.course_name }}</div>
                <div class="text-box" style="font-size: small;padding: 4px;display: inline-block;">
                  课程代码：{{ item.content.data.course_id }}
                </div>
                <el-divider></el-divider>
                <div style="margin: 0 2px">授课老师：{{ item.content.data.teacher_name }}</div>
                <div style="margin: 0 2px;display: flex">
                  <span>课程评分：</span>
                  <el-rate disabled v-model="item.course_rate"></el-rate>
                </div>
                <div style="margin: 0 2px">
                  课程资料：
                  <span v-for="(i,ind) in item.course_material">
                    {{ i.material_name }}
                  </span>

                </div>

                <div style="margin: 0 2px">
                  课程简介：
                  <p style="word-wrap:break-word;">{{ item.content.data.course_intro }}</p>
                </div>
              </div>
            </div>
          </el-card>

          <div style="margin: 10px 12%;">
            <el-table empty-text="该课程还没有评价"
                      :data="classIntroDataList.filter(i => i.id === item.content.data.course_id).at(0).data.classCommentsData">
              <el-table-column width="100">
                <img src="../../../static/images/BUAALogo.jpg" style="width: 50px;height: 50px;border-radius: 50%">
              </el-table-column>

              <el-table-column
                width="160">
                <template slot-scope="scope">
                  <div slot="reference"
                       style="width: 80px;font-size: large;color: #409EFF;font-weight: bold;text-align: center">
                    <span>{{ scope.row.stu_name }}</span>
                  </div>
                  <div style="color: lightslategray">
                    <i class="el-icon-time"></i>
                    <span style="margin-left: 5px">{{ scope.row.comment_time }}</span>
                  </div>

                </template>
              </el-table-column>

              <el-table-column
                prop="comment_content">
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

      </el-tabs>

      <el-dialog
        title="开设课程"
        center
        :visible.sync="dialogVisible"
        width="38%"
        :before-close="closeDialog"
        append-to-body
        top="16vh">

        <el-form ref="newClass" :model="newClass" label-width="80px">
          <el-form-item label="课程代码" prop="course_id"
                        :rules="[
      { required: true, message: '课程代码不能为空'}]">
            <el-input v-model="newClass.course_id"></el-input>
          </el-form-item>

          <el-form-item label="课程名称" prop="course_name"
                        :rules="[
      { required: true, message: '课程名称不能为空'}]">
            <el-input v-model="newClass.course_name"></el-input>
          </el-form-item>

          <el-form-item label="课程容量" prop="course_capacity"
                        :rules="[
      { required: true, message: '课程容量不能为空'},
      { type: 'number', message: '课程容量必须为数字值'}
    ]">
            <el-input v-model.number="newClass.course_capacity"></el-input>
          </el-form-item>

          <el-form-item label="课程简介" prop="course_intro">
            <el-input v-model="newClass.course_intro"
                      type="textarea"
                      autosize
                      :autosize="{ minRows: 2 }"></el-input>
          </el-form-item>

          <div style="text-align: center">
            <el-button type="primary" @click="addNewClass">确定</el-button>
            <el-button @click="closeDialog">取消</el-button>
          </div>
        </el-form>

      </el-dialog>

    </el-main>
  </el-container>
</template>

<script>

export default {
  name: "TClassGround",

  created() {
    this.username = sessionStorage.username;

    this.getData();
  },
  data() {
    return {
      username: '',
      password: '',
      menuActivateIndex: '5',

      dialogVisible: false,
      // new class
      newClass: {
        course_id: '',
        course_name: '',
        course_capacity: '',
        course_intro: '',
      },

      //  tabs
      tabsValue: '1',
      mainTab: {title: '所有课程', name: '1'},
      tabs: [],
      tabIndex: 1,

      //  class
      searchClassKeyword: '',
      searchClassDeleteShow: false,
      classAll: [],

      //  comments
      classIntroDataList: [],
    }
  },
  methods: {
    logout() {
      sessionStorage.clear();

      this.$router.push('/teacher/login')
    },
    handleMenuSelect(key, keyPath) {
      console.log(key, keyPath)
    },
    getData() {
      this.$axios.get('http://127.0.0.1:8000/show/').then(response => {
        if (response.data.code === 0) {
          let data = response.data.data
          data.forEach((item, index) => {

            item.course_rate = Number(item.course_rate)
            item.course_material = this.classToMaterial(item.course_id)
          })
          this.classAll = data;
          // this.$message(response.data.message)
        } else if (response.data.code === 1) {
          this.$message.error(response.data.message)
        }
        console.log(response.data)
      });
    },
    removeTab(targetName) {
      let tabs = this.tabs;
      let activeName = this.tabsValue;
      let id = '';
      if (activeName === targetName) {
        tabs.forEach((tab, index) => {
          if (tab.name === targetName) {
            id = tab.content.data.course_id;
            let nextTab = tabs[index + 1] || tabs[index - 1];
            if (nextTab) {
              activeName = nextTab.name;
            } else {
              activeName = this.mainTab.name;
            }
          }
        });
      }

      this.tabsValue = activeName;
      this.tabs = tabs.filter(tab => tab.name !== targetName);

      this.classIntroDataList = this.classIntroDataList.filter(item => item.id !== id)
    },
    classIntroClick(item, index) {
      let ifExist = false;
      let tabName = '';
      this.tabs.forEach(i => {
        if (i.content.data.course_id === item.course_id) {
          ifExist = true;
          tabName = i.name;
        }
      })

      if (ifExist) {
        this.tabsValue = tabName;
      } else {
        let newTabName = ++this.tabIndex + '';
        this.tabs.push({
          title: item.course_name,
          name: newTabName,
          content: {index: index, data: item}
        });
        this.tabsValue = newTabName;

        let data = {classCommentsData: []}
        this.classIntroDataList.push({"id": item.course_id, "data": data})

        this.classGetCommentsData(item.course_id);
      }
    },
    searchClassClick() {
      // this.$axios.post("http://127.0.0.1:8000/search/"
      let data = this.classAll;
      let words = this.searchClassKeyword;
      data = data.filter(d => d.course_name.includes(words))
      this.classAll = data;
      this.searchClassDeleteShow = true

    },
    searchClassDelete() {
      this.searchClassKeyword = '';
      this.searchClassDeleteShow = false;
      this.getData();
    },
    classGetCommentsData(id) {
      let comment = this.classIntroDataList.filter(i => i.id === id).at(0).data;
      this.$axios.post("http://127.0.0.1:8000/showcoursecomment/", JSON.stringify({"course_id": id})).then(response => {
        console.log(response)
        comment.classCommentsData = response.data.data
      }).catch(response => {
        console.log(response)
      })
    },
    closeDialog() {
      this.dialogVisible = false;
      this.$refs["newClass"].resetFields()
    },
    addNewClass() {
      this.$refs['newClass'].validate((valid) => {
        if (valid) {
          this.$axios.post("http://127.0.0.1:8000/teacher/add/", JSON.stringify({
            "teacher_id": this.username,
            "course": this.newClass
          })).then(response => {
            console.log(response);

            if (response.data.code === 0) {
              this.$message({
                message: "添加课程成功",
                type: 'success',
              });

              this.getData();

              this.closeDialog()
            } else {
              this.$alert(response.data.prompt, {
                type: 'error',
                confirmButtonText: "确定",
                callback: action => {
                  this.$refs["newClass"].resetFields();
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

        } else {
          console.log("error submit");
          return false;
        }
      })

    },
    classToMaterial(id) {
      let data = [];
      this.$axios.post("http://127.0.0.1:8000/showcoursematerial/", JSON.stringify({"course_id": id}
      )).then(response => {
        data = response.data.data.data;
      })
      return data;
    },


  }
}
</script>

<style scoped>
.el-menu-item {
  float: right;
}

.el-card__body {
  height: 50px;
}

.el-divider--horizontal {
  margin: 8px 0;
  background: 0 0;
  border-top: 1px solid #e8eaec;
}

.text-box {
  margin: 5px 3px;
  background: #EBEEF5;
  border-radius: 4px;
  text-align: center;
  font-size: small;

}

.text-box-title {
  margin: 5px 2px;
  text-align: center;
  font-weight: bold;
  font-size: larger;
  color: #409EFF;
}
</style>
