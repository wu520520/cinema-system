<template>
  <!-- 电影详情页模板 -->
  <div class="film-detail">
    <!-- 操作按钮：返回列表 + 编辑 -->
    <div class="back-btn">
      <button @click="$router.back()">← 返回列表</button>
      <button @click="$router.push(`/edit/${film.id}`)">编辑</button>
    </div>
    
    <!-- 详情内容（只有数据加载完成后才显示） -->
    <div class="detail-container" v-if="film">
      <!-- 左侧：电影封面 -->
      <div class="detail-left">
        <img :src="film.pic ? `/uploads/${film.pic}` : 'https://via.placeholder.com/400x600?text=No+Image'" :alt="film.title" />
      </div>
      
      <!-- 右侧：电影信息 -->
      <div class="detail-right">
        <h1>{{ film.title }}</h1>
        <!-- 信息网格：显示各种元数据 -->
        <div class="info-grid">
          <div class="info-item">
            <span class="label">地区：</span>
            <span>{{ film.region_name || '未知' }}</span>
          </div>
          <div class="info-item">
            <span class="label">类型：</span>
            <span>{{ film.category_name || '未知' }}</span>
          </div>
          <div class="info-item">
            <span class="label">导演：</span>
            <span>{{ film.director || '未知' }}</span>
          </div>
          <div class="info-item">
            <span class="label">分级：</span>
            <span>{{ film.grade }}</span>
          </div>
          <div class="info-item">
            <span class="label">上映日期：</span>
            <span>{{ film.release_date || '未知' }}</span>
          </div>
          <div class="info-item">
            <span class="label">时长：</span>
            <span>{{ formatTime(film.times) }}</span>
          </div>
          <div class="info-item">
            <span class="label">IMDb评分：</span>
            <span>{{ film.score ? film.score + '分' : '暂无评分' }}</span>
          </div>
          <div class="info-item">
            <span class="label">票房：</span>
            <span>{{ film.profit ? film.profit + '万元' : '暂无数据' }}</span>
          </div>
          <div class="info-item">
            <span class="label">制作/发行：</span>
            <span>{{ film.organization || '未知' }}</span>
          </div>
        </div>
        
        <!-- 剧情简介 -->
        <div class="synopsis">
          <h3>剧情简介</h3>
          <p>{{ film.synopsis || '暂无简介' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * 电影详情页面组件
 * 功能：
 * - 显示电影的完整信息
 * - 时长自动格式化
 * - 提供编辑入口
 */
import { getFilm } from '../api'
import { formatTime } from '../utils'

export default {
  name: 'FilmDetail',
  data() {
    return {
      film: null  // 电影详情数据
    }
  },
  /**
   * 组件挂载时获取电影详情
   */
  async mounted() {
    const id = this.$route.params.id
    const res = await getFilm(id)
    this.film = res.data
  },
  methods: {
    formatTime  // 复用工具函数格式化时长
  }
}
</script>

<style scoped>
.film-detail {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.back-btn {
  margin-bottom: 20px;
}

.back-btn button {
  padding: 10px 20px;
  margin-right: 10px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.back-btn button:first-child {
  background: #409eff;
  color: white;
  border-color: #409eff;
}

.detail-container {
  display: flex;
  gap: 30px;
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.detail-left img {
  width: 300px;
  height: 450px;
  object-fit: cover;
  border-radius: 8px;
}

.detail-right {
  flex: 1;
}

.detail-right h1 {
  font-size: 28px;
  margin-bottom: 20px;
  color: #333;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 30px;
}

.info-item {
  display: flex;
  font-size: 14px;
}

.info-item .label {
  color: #999;
  min-width: 80px;
}

.synopsis h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #333;
}

.synopsis p {
  line-height: 1.8;
  color: #666;
}
</style>
