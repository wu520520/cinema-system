/**
 * Vue 应用入口文件
 * 功能：
 * - 创建 Vue 应用实例
 * - 配置路由
 * - 集成 Element Plus UI 组件库
 * - 挂载到 DOM
 */
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

// 创建应用实例
const app = createApp(App)

// 使用路由插件
app.use(router)

// 使用 Element Plus UI 组件库
app.use(ElementPlus)

// 挂载到 #app 元素
app.mount('#app')
