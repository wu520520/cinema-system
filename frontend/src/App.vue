<template>
  <!-- 根组件：只有路由视图 -->
  <div id="app">
    <router-view />
  </div>
</template>

<script>
/**
 * 应用根组件
 * 功能：
 * - 作为路由的容器
 * - 提供全局样式
 */
export default {
  name: 'App'
}
</script>

<style>
/* 全局样式重置 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 全局字体和背景 */
body {
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  background: #f5f5f5;
}

/* 应用容器：占满整个视口高度 */
#app {
  min-height: 100vh;
}
</style>
