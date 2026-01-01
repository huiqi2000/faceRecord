import Vue from 'vue'
import App from './App.vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from 'axios'

Vue.config.productionTip = false
// 全局注册 Element-UI
Vue.use(ElementUI)
// 全局配置 axios
Vue.prototype.$axios = axios
// 后端 API 基础路径
Vue.prototype.$baseApi = 'http://localhost:5000/api'

new Vue({
  render: h => h(App),
}).$mount('#app')