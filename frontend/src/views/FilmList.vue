<template>
  <!-- 电影列表页模板 -->
  <div class="film-list">
    <!-- 页面头部：标题 + 添加按钮 -->
    <div class="header">
      <h1>宝莱坞影视系统</h1>
      <button class="add-btn" @click="$router.push('/add')">添加电影</button>
    </div>
    
    <!-- 筛选和排序区域 -->
    <div class="filters">
      <!-- 按类型筛选 -->
      <div class="filter-group">
        <span>按类型：</span>
        <button 
          v-for="cat in categories" :key="cat.id"
          :class="{ active: selectedCategory === cat.id }"
          @click="selectedCategory = cat.id"
        >{{ cat.name }}</button>
        <button :class="{ active: !selectedCategory }" @click="selectedCategory = null">全部</button>
      </div>
      
      <!-- 按地区筛选 -->
      <div class="filter-group">
        <span>按地区：</span>
        <button 
          v-for="reg in regions" :key="reg.id"
          :class="{ active: selectedRegion === reg.id }"
          @click="selectedRegion = reg.id"
        >{{ reg.name }}</button>
        <button :class="{ active: !selectedRegion }" @click="selectedRegion = null">全部</button>
      </div>
      
      <!-- 按等级筛选 -->
      <div class="filter-group">
        <span>按等级：</span>
        <button 
          v-for="g in grades" :key="g"
          :class="{ active: selectedGrade === g }"
          @click="selectedGrade = g"
        >{{ g }}</button>
        <button :class="{ active: !selectedGrade }" @click="selectedGrade = null">全部</button>
      </div>
      
      <!-- 排序选项 -->
      <div class="sort-group">
        <span>排序：</span>
        <button 
          v-for="s in sortOptions" :key="s.value"
          :class="{ active: sortBy === s.value }"
          @click="sortBy = s.value"
        >{{ s.label }}</button>
      </div>
    </div>
    
    <!-- 电影卡片网格 -->
    <div class="films">
      <div 
        v-for="film in films" :key="film.id" 
        class="film-card"
        @click="$router.push(`/film/${film.id}`)"
      >
        <!-- 电影封面 -->
        <div class="film-pic">
          <img :src="film.pic ? `/uploads/${film.pic}` : 'https://via.placeholder.com/300x400?text=No+Image'" :alt="film.title" />
        </div>
        <!-- 电影基本信息 -->
        <div class="film-info">
          <h3>{{ film.title }}</h3>
          <div class="film-meta">
            <span>{{ film.region_name || '未知' }}</span>
            <span>{{ film.category_name || '未知' }}</span>
            <span v-if="film.score">{{ film.score }}分</span>
          </div>
        </div>
        <!-- 操作按钮：编辑和删除 -->
        <div class="film-actions">
          <button class="edit-btn" @click.stop="$router.push(`/edit/${film.id}`)">编辑</button>
          <button class="delete-btn" @click.stop="handleDelete(film)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/**
 * 电影列表页面组件
 * 功能：
 * - 显示所有电影卡片
 * - 支持按类型、地区、等级筛选
 * - 支持按票房、评分、时间排序
 * - 支持删除和编辑操作
 */
import { getRegions, getCategories, getFilms, deleteFilm } from '../api'

export default {
  name: 'FilmList',
  data() {
    return {
      films: [],          // 电影列表数据
      regions: [],        // 地区列表
      categories: [],     // 分类列表
      grades: ['G', 'PG', 'PG-13', 'R', 'NC-17', 'NR'],  // 电影分级选项
      selectedCategory: null,  // 当前选中的分类筛选
      selectedRegion: null,    // 当前选中的地区筛选
      selectedGrade: null,     // 当前选中的分级筛选
      sortBy: 'created',       // 当前排序方式
      sortOptions: [           // 排序选项配置
        { label: '按票房', value: 'profit' },
        { label: '按IMDb评分', value: 'score' },
        { label: '按最新上映', value: 'created' }
      ]
    }
  },
  /**
   * 组件挂载时初始化数据
   */
  async mounted() {
    await this.fetchRegions()       // 获取地区数据
    await this.fetchCategories()    // 获取分类数据
    await this.fetchFilms()         // 获取电影列表
  },
  /**
   * 监听筛选和排序条件变化，自动刷新电影列表
   */
  watch: {
    selectedCategory() { this.fetchFilms() },
    selectedRegion() { this.fetchFilms() },
    selectedGrade() { this.fetchFilms() },
    sortBy() { this.fetchFilms() }
  },
  methods: {
    /**
     * 获取地区列表
     */
    async fetchRegions() {
      const res = await getRegions()
      this.regions = res.data
    },
    /**
     * 获取分类列表
     */
    async fetchCategories() {
      const res = await getCategories()
      this.categories = res.data
    },
    /**
     * 获取电影列表（带筛选和排序参数）
     */
    async fetchFilms() {
      const params = {}
      if (this.selectedCategory) params.category = this.selectedCategory
      if (this.selectedRegion) params.region = this.selectedRegion
      if (this.selectedGrade) params.grade = this.selectedGrade
      if (this.sortBy) params.sort_by = this.sortBy
      
      const res = await getFilms(params)
      this.films = res.data
    },
    /**
     * 删除电影（带确认提示）
     */
    async handleDelete(film) {
      if (confirm(`确定要删除《${film.title}》吗？`)) {
        await deleteFilm(film.id)
        await this.fetchFilms()  // 删除后刷新列表
        alert('删除成功')
      }
    }
  }
}
</script>

<style scoped>
.film-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header h1 {
  color: #333;
}

.add-btn {
  padding: 10px 20px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.filters {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.filter-group, .sort-group {
  margin-bottom: 15px;
}

.filter-group span, .sort-group span {
  font-weight: bold;
  margin-right: 10px;
  color: #666;
}

.filter-group button, .sort-group button {
  padding: 5px 12px;
  margin: 0 5px 5px 0;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
}

.filter-group button.active, .sort-group button.active {
  background: #409eff;
  color: white;
  border-color: #409eff;
}

.films {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.film-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  position: relative;
}

.film-pic {
  height: 350px;
  overflow: hidden;
}

.film-pic img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.film-info {
  padding: 15px;
}

.film-info h3 {
  font-size: 16px;
  margin-bottom: 10px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.film-meta {
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: #999;
}

.film-actions {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  gap: 8px;
}

.edit-btn, .delete-btn {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.edit-btn {
  background: #409eff;
  color: white;
}

.delete-btn {
  background: #f56c6c;
  color: white;
}
</style>
