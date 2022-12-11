<template>
  <el-container>
    <!--    <div style="width: 100%;height: 100%;">-->
    <!--      <el-backtop visibility-height="200"></el-backtop>-->
    <!--    </div>-->

    <el-header>
      <el-menu :default-active="menuActivateIndex" mode="horizontal" @select="handleMenuSelect" router>
        <!--        <img src="src/images/school.png">-->
        <el-menu-item index="1" route="/"><span @click="logout">退出登录</span></el-menu-item>
        <el-menu-item index="2" route="/studentmain">个人主页</el-menu-item>
        <!--        <el-menu-item index="3">已选课程</el-menu-item>-->
        <el-menu-item index="4" route="/forum">讨论区</el-menu-item>
        <el-menu-item index="5" route="/classground">课程广场</el-menu-item>
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
          </div>

          <div style="margin: 20px 10%">
            <el-card shadow="hover" style="margin: 10px 0" v-for="(item,index) in classAll">

              <div style="display: flex;position: relative">
                <div style="position: relative;left: 8%">
                  <img src="../../../static/images/BUAALogo.jpg"
                       style="width: 50px;height: 50px">
                </div>

                <div style="position: relative;left: 18%">
                  <el-link type="primary" :underline="false" @click="classIntroClick(item,index)"
                           style="font-size: 20px;font-weight: bold">
                    {{ item.course_name }}
                  </el-link>
                  <el-rate v-model="item.course_rate" disabled show-score></el-rate>
                  <!--                  <stars v-model="item.course_rate"></stars>-->
                </div>

                <div style="position: absolute;right: 5%;">
                  <el-button type="primary"
                             :disabled="item.course_total >= item.course_capacity"
                             v-show="!ifSelected(item,index)"
                             @click="handleSelectClass(item,index)">选课
                  </el-button>
                  <el-button type="info"
                             :disabled="true"
                             style="margin: 0 0"
                             v-show="ifSelected(item,index)">已选
                  </el-button>
                  <!--                  <el-button type="danger" v-show="true">退课</el-button>-->
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
                <div style="margin: 0 2px">授课老师：{{ classToTeacher(item.content.data.course_id) }}</div>
                <div style="margin: 0 2px;display: flex">
                  <span>课程评分：</span>
                  <el-rate disabled v-model="item.course_rate"></el-rate>
                </div>
                <div style="margin: 0 2px">
                  课程简介：
                  <p style="word-wrap:break-word;">{{ item.content.data.course_intro }}</p>
                </div>
              </div>
            </div>
          </el-card>

          <el-card
            v-show="ifSelected(item.content.data,item.content.index)
            && !classIntroDataList.filter(i => i.id === item.content.data.course_id).at(0).data.ifSubmit"
            shadow="never"
            style="margin: 20px 12%">
            <div slot="header">
              <el-tooltip effect="light" content="给你喜欢的课程投上一票吧！" placement="right-start">
                <span style="font-weight: bold;font-size: large">课程评价</span>
              </el-tooltip>
            </div>

            <div style="display: flex">
              您觉得该课程：
              <el-rate
                v-model="classIntroDataList.filter(i => i.id === item.content.data.course_id).at(0).data.classRate"
                :colors=" ['#99A9BF', '#F7BA2A', '#FF9900']"
                show-text
              ></el-rate>
            </div>
            <div>
              <p>您也可以把您对于该课程的宝贵意见或看法写下来</p>
              <el-input type="textarea"
                        clearable placeholder="请输入您的意见或看法"
                        :autosize="{minRows:3}"
                        v-model="classIntroDataList.filter(i => i.id === item.content.data.course_id).at(0).data.classComment"></el-input>
            </div>
            <el-button type="primary"
                       @click="classCommentSubmit(item.content.data,item.content.index)"
                       style="margin: 15px 46%">提交
            </el-button>
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
                    <span>{{ scope.row.comment_id }}</span>
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

    </el-main>
  </el-container>
</template>

<script>

export default {
  name: "ClassGround",

  created() {
    this.username = sessionStorage.username;
    this.password = sessionStorage.password;

    this.getData();
  },
  data() {
    return {
      username: '',
      password: '',
      menuActivateIndex: '5',

      //  tabs
      tabsValue: '1',
      mainTab: {title: '所有课程', name: '1'},
      tabs: [],
      tabIndex: 1,

      //  class
      searchClassKeyword: '',
      searchClassDeleteShow: false,
      classAll: [],
      classSelectedId: [],

      //  comments
      classIntroDataList: [],
      // commentSubmitList: [],
      // classRateList: {},
      // classCommentList: {},
      // classCommentsDataList: {},
      // classCommentsData: [],
      //
      // test: [{id: 123, data: {rate: 2, comment: 123}}]
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
      this.$axios.get('http://127.0.0.1:8000/show/').then(response => {
        if (response.data.code === 0) {
          let data = response.data.data
          data.forEach((item, index) => {
            item.course_rate = Number(item.course_rate)
          })
          this.classAll = data;
          // this.$message(response.data.message)
        } else if (response.data.code === 1) {
          this.$message.error(response.data.message)
        }
        console.log(response.data)
      });
      this.$axios.post('http://127.0.0.1:8000/stu/mycourse/', JSON.stringify({"stu_id": this.username})).then(response => {
        console.log(response.data);
        let ids = [];
        let data = response.data.data;
        for (var i = 0; i < data.length; i++) {
          ids.push(data[i].course_id)
        }
        console.log(ids)
        this.classSelectedId = ids
      }).catch(response => {
        console.log(response.error)
      })

    },
    handleSelectClass(item, index) {
      let data = {"username": this.username, 'data': item};
      console.log(item)
      this.$axios.post("http://127.0.0.1:8000/stu/add/", JSON.stringify(data)).then(response => {
        console.log(response.data);

        if (response.data.code === 0) {
          this.$message({
            message: "选课成功",
            type: 'success'
          })
          this.getData();
        } else {
          this.$message({
            message: "选课失败:" + response.data.prompt,
            type: "warning"
          })
        }
      }).catch(response => {
        this.$message({
          message: "服务器内部错误或服务器没有响应",
          type: "error"
        })
        console.log(response.error);
      })
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

        let data = {classRate: 0, classComment: '', classCommentsData: [], ifSubmit: false}
        this.classIntroDataList.push({"id": item.course_id, "data": data})

        this.classGetCommentsData(item.course_id);
      }
    },
    ifSelected(item, index) {
      return this.classSelectedId.includes(item.course_id)
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
    classCommentSubmit(item, index) {
      let comment = this.classIntroDataList.filter(i => i.id === item.course_id).at(0).data;
      // console.log(comment)

      this.$axios.post("http://127.0.0.1:8000/stu/comment/", JSON.stringify({
        "stu_id": this.username,
        "course_id": item.course_id,
        "comment_content": comment.classComment
      })).then(response => {
        console.log(response)

        comment.ifSubmit = true;
        // if success
        this.$alert("我们收到了您的评价，也祝愿您在北航的学习生活越来越顺利，实现自己的人生价值！", "Success", {
            confirmButtonText: "Yes",
            type: 'success',
            center: true,
            callback: action => {
            }
          }
        )

        this.classGetCommentsData(item.course_id)
      }).catch(response => {
          console.log(response)
          this.$message({message: "系统故障，评价失败", type: "error"})
        }
      )
    },
    classToTeacher() {
      return "佚民"
    },
    classGetCommentsData(id) {
      let data = [];
      this.$axios.post("http://127.0.0.1:8000/showcoursecomment/", JSON.stringify({"course_id": id})).then(response => {
        console.log(response)
        data = response.data.data
      }).catch(response => {
        console.log(response)
        this.classCommentsData = []
      })

      this.classIntroDataList.forEach((item, index) => {
        if (item.id === id) {
          item.data.classCommentsData = data;
        }
      })
    }


  }
}
</script>

<style scoped>

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
