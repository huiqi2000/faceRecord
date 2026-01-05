<template>
  <div id="app">
    <div>
      <span class="title-text">打卡系统</span>
    </div>
    <div class="clock-container">
      <!-- 打卡按钮区域 -->
      <div class="clock-btn-group">
        <el-button type="primary" size="large" @click="handleClock('上班')">
          上班
        </el-button>
        <el-button type="success" size="large" @click="handleClock('下班')" style="margin-left: 20px;">
          下班
        </el-button>
      </div>

      <!-- Element-UI 日历组件 -->

      <div class="calendar-container" style="margin-top: 30px;">
        <!-- el-calendar：v-model 绑定当前日期，@date-change 绑定点击/切换日期事件 -->
        <el-calendar v-model="currentDate" @input="handleCalendarClick"></el-calendar>
      </div>

      <!-- 1. 下班特殊时间选择弹窗（昨天/今天） -->
      <el-dialog title="请选择打卡日期" :visible.sync="dateSelectDialogVisible" width="30%" :close-on-click-modal="false">
        <div class="dialog-btn-group" style="text-align: center;">
          <el-button type="primary" @click="confirmDate('yesterday')">昨天</el-button>
          <el-button type="success" @click="confirmDate('today')" style="margin-left: 20px;">今天</el-button>
        </div>
      </el-dialog>

      <!-- 2. 每日打卡记录查看弹窗 -->
      <el-dialog :title="`${selectedDate} 打卡记录`" :visible.sync="recordDialogVisible" width="50%">
        <el-table :data="currentDayRecords" border stripe style="width: 100%;">
          <el-table-column prop="id" label="记录ID" align="center" width="80"></el-table-column>
          <el-table-column prop="record_day" label="打卡日期" align="center"></el-table-column>
          <el-table-column prop="record_time" label="打卡时间" align="center"></el-table-column>
          <el-table-column prop="record_type" label="打卡类型" align="center">
            <template #scope="scope">
              <el-tag v-if="scope.row.record_type === '上班'" type="primary">上班</el-tag>
              <el-tag v-else type="success">下班</el-tag>
            </template>
          </el-table-column>
        </el-table>

        <div slot="footer" class="dialog-footer">
          <el-button @click="recordDialogVisible = false">关闭</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      currentDate: new Date(), // 日历当前日期
      dateSelectDialogVisible: false, // 日期选择弹窗状态
      recordDialogVisible: false, // 打卡记录弹窗状态
      selectedDate: '', // 选中的日历日期（YYYY-MM-DD）
      currentDayRecords: [], // 选中日期的打卡记录
      pendingClockType: '', // 待提交的打卡类型（上班/下班）
    }
  },
  methods: {
    /**
     * 处理打卡按钮点击事件
     * @param {String} type 打卡类型（上班/下班）
     */
    handleClock(type) {
      this.pendingClockType = type
      const now = new Date()
      const hours = now.getHours()
      const minutes = now.getMinutes()

      // 判断是否是下班时间且在 00:00 ~ 11:30 之间
      if (type === '下班' && (hours < 11 || (hours === 11 && minutes < 30))) {
        this.dateSelectDialogVisible = true // 显示日期选择弹窗
      } else {
        // 非特殊时间，直接使用今天日期打卡
        const today = this.formatDate(now)
        const currentTime = this.formatTime(now)
        this.submitClockRecord(today, currentTime, type)
      }
    },

    /**
     * 处理日历单元格点击事件
     * @param {Date} date 选中的日期
     * @param {Object} data 日历单元格数据
     */
    handleCalendarClick(date) {
      // console.log('日历单元格点击事件触发', date)
      this.selectedDate = this.formatDate(date)
      this.recordDialogVisible = true
      // 查询该日期的打卡记录
      this.queryClockRecord(this.selectedDate)
    },

    /**
     * 确认日期选择（昨天/今天）
     * @param {String} dateType 日期类型（yesterday/today）
     */
    confirmDate(dateType) {
      this.dateSelectDialogVisible = false
      const now = new Date()
      let targetDate = ''

      if (dateType === 'yesterday') {
        // 计算昨天日期
        const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000)
        targetDate = this.formatDate(yesterday)
      } else {
        // 今天日期
        targetDate = this.formatDate(now)
      }

      // 获取当前时间并提交打卡记录
      const currentTime = this.formatTime(now)
      this.submitClockRecord(targetDate, currentTime, this.pendingClockType)
    },

    /**
     * 提交打卡记录到后端
     * @param {String} recordDay 打卡日期（YYYY-MM-DD）
     * @param {String} recordTime 打卡时间（HH:MM:SS）
     * @param {String} recordType 打卡类型（上班/下班）
     */
    async submitClockRecord(recordDay, recordTime, recordType) {
      // console.log('提交打卡记录：', recordDay, recordTime, recordType)
      try {
        const res = await this.$axios.post(`${this.$baseApi}/clock/add`, {
          record_day: recordDay,
          record_time: recordTime,
          record_type: recordType
        })

        if (res.data.code === 200) {
          this.$message.success(res.data.msg)
          // 若当前日历选中的是打卡日期，刷新记录
          if (this.selectedDate === recordDay) {
            this.queryClockRecord(recordDay)
          }
        } else {
          this.$message.error(res.data.msg)
        }
      } catch (error) {
        console.error('打卡失败：', error)
        this.$message.error('网络异常，打卡失败')
      }
    },

    /**
     * 查询指定日期的打卡记录
     * @param {String} targetDate 目标日期（YYYY-MM-DD）
     */
    async queryClockRecord(targetDate) {
      try {
        const res = await this.$axios.get(`${this.$baseApi}/clock/query`, {
          params: { date: targetDate }
        })

        if (res.data.code === 200) {
          this.currentDayRecords = res.data.data
        } else {
          this.$message.error(res.data.msg)
          this.currentDayRecords = []
        }
      } catch (error) {
        console.error('查询打卡记录失败：', error)
        this.$message.error('网络异常，查询失败')
        this.currentDayRecords = []
      }
    },

    /**
     * 格式化日期为 YYYY-MM-DD
     * @param {Date} date 日期对象
     * @returns {String} 格式化后的日期
     */
    formatDate(date) {
      const year = date.getFullYear()
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      const day = date.getDate().toString().padStart(2, '0')
      return `${year}-${month}-${day}`
    },

    /**
     * 格式化时间为 HH:MM:SS
     * @param {Date} date 日期对象
     * @returns {String} 格式化后的时间
     */
    formatTime(date) {
      // 先判断传入的是否为有效Date对象，避免报错
      if (!(date instanceof Date) || isNaN(date.getTime())) {
        console.error('传入的参数不是有效Date对象');
        return ''; // 无效参数返回空字符串或自定义提示
      }

      // 获取年、月、日（日期部分）
      const year = date.getFullYear();
      // 月份是0-11，需要+1
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');

      // 你的原有时间部分逻辑（保留并复用）
      const hours = date.getHours().toString().padStart(2, '0');
      const minutes = date.getMinutes().toString().padStart(2, '0');
      const seconds = date.getSeconds().toString().padStart(2, '0');

      // 拼接为 yyyy-MM-dd HH:mm:ss 格式并返回
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }
  }
}
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.title-text {
  font-size: 30px;
  font-weight: bold;
}

.clock-container {
  width: 80%;
  margin: 0 auto;
}

.clock-btn-group {
  margin-top: 20px;
}

.calendar-container {
  margin-top: 30px;
}

.calendar-cell {
  padding: 10px;
  cursor: pointer;
  border-radius: 4px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.calendar-cell:hover {
  background-color: #f5f7fa;
}

.dialog-btn-group {
  padding: 20px 0;
}



/* 圆圈 样式 */
/* 日期单元格样式：保证布局合理 */
.calendar-date-cell {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 10px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 原有日期文字样式（可选，可自定义） */
.calendar-date-text {
  font-size: 14px;
  color: #333;
  margin-bottom: 8px;
  /* 与圆圈保持间距 */
  z-index: 1;
  /* 确保日期文字在圆圈上方 */
}

/* 两个圆圈的容器：横向排列 */
.calendar-circle-group {
  display: flex;
  gap: 6px;
  /* 两个圆圈之间的间距 */
  z-index: 1;
}

/* 圆圈基础样式 */
.circle {
  display: inline-block;
  width: 8px;
  /* 圆圈大小 */
  height: 8px;
  border-radius: 50%;
  /* 圆形 */
  background-color: #dcdfe6;
  /* 默认灰色 */
}

/* 第一个圆圈自定义样式（可按需修改颜色、大小） */
.circle-1 {
  background-color: #409eff;
  /* 蓝色 */
}

/* 第二个圆圈自定义样式（可按需修改颜色、大小） */
.circle-2 {
  background-color: #f56c6c;
  /* 红色 */
}
</style>