<template>
  <!-- 编辑电影页面模板 -->
  <div class="edit-film">
    <button class="back-btn" @click="$router.back()">← 返回</button>
    <h1>编辑电影</h1>
    
    <!-- 电影信息编辑表单（只有数据加载完成后才显示） -->
    <form @submit.prevent="handleSubmit" v-if="form.title">
      <!-- 电影标题 -->
      <div class="form-group">
        <label>电影标题 *</label>
        <input v-model="form.title" required />
      </div>
      
      <!-- 剧情简介 -->
      <div class="form-group">
        <label>剧情简介</label>
        <textarea v-model="form.synopsis" rows="4"></textarea>
      </div>
      
      <!-- 封面图片编辑（支持预览原图或新图） -->
      <div class="form-group">
        <label>封面图片</label>
        <input type="file" @change="handleFileChange" accept="image/*" />
        <img v-if="previewUrl" :src="previewUrl" :alt="form.title" class="preview-img" />
        <img v-else-if="form.pic" :src="`/uploads/${form.pic}`" :alt="form.title" class="preview-img" />
      </div>
      
      <!-- 地区和类型选择 -->
      <div class="form-row">
        <div class="form-group">
          <label>地区</label>
          <select v-model="form.region">
            <option value="">请选择</option>
            <option v-for="r in regions" :key="r.id" :value="r.id">{{ r.name }}</option>
          </select>
        </div>
        
        <div class="form-group">
          <label>类型 *</label>
          <select v-model="form.category" required>
            <option value="">请选择</option>
            <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
      </div>
      
      <!-- 导演 -->
      <div class="form-group">
        <label>导演</label>
        <input v-model="form.director" />
      </div>
      
      <!-- 上映日期和时长 -->
      <div class="form-row">
        <div class="form-group">
          <label>上映日期</label>
          <input type="date" v-model="form.release_date" />
        </div>
        
        <div class="form-group">
          <label>时长（分钟）*</label>
          <input type="number" v-model.number="form.times" required />
        </div>
      </div>
      
      <!-- IMDb评分和分级 -->
      <div class="form-row">
        <div class="form-group">
          <label>IMDb评分</label>
          <input type="number" step="0.1" min="0" max="10" v-model.number="form.score" />
        </div>
        
        <div class="form-group">
          <label>分级 *</label>
          <select v-model="form.grade" required>
            <option v-for="g in grades" :key="g" :value="g">{{ g }}</option>
          </select>
        </div>
      </div>
      
      <!-- 票房和制作机构 -->
      <div class="form-row">
        <div class="form-group">
          <label>票房（万元）</label>
          <input type="number" v-model.number="form.profit" />
        </div>
        
        <div class="form-group">
          <label>制作/发行机构</label>
          <input v-model="form.organization" />
        </div>
      </div>
      
      <!-- 提交按钮 -->
      <div class="form-actions">
        <button type="submit" class="submit-btn">保存修改</button>
      </div>
    </form>
  </div>
</template>

<script>
/**
 * 编辑电影页面组件
 * 功能：
 * - 加载并显示现有电影数据
 * - 支持修改所有字段
 * - 支持重新上传图片
 * - 时长单位转换（秒 <-> 分钟）
 */
import { getFilm, getRegions, getCategories, uploadFile, updateFilm } from '../api'

export default {
  name: 'EditFilm',
  data() {
    return {
      form: {},            // 表单数据（会从API加载）
      regions: [],         // 地区下拉选项
      categories: [],      // 分类下拉选项
      grades: ['G', 'PG', 'PG-13', 'R', 'NC-17', 'NR'],  // 分级选项
      file: null,          // 新选择的待上传文件
      previewUrl: '',      // 新图片预览URL
      originalPic: ''      // 原始图片文件名
    }
  },
  /**
   * 组件挂载时：
   * 1. 获取地区和分类数据
   * 2. 获取电影详情并填充表单
   * 3. 转换时长单位（秒 -> 分钟）
   */
  async mounted() {
    const [regionsRes, categoriesRes] = await Promise.all([// 同时发送请求获取地区和分类数据
      getRegions(),
      getCategories()
    ])
    this.regions = regionsRes.data
    this.categories = categoriesRes.data
    
    const id = this.$route.params.id
    const res = await getFilm(id)
    this.form = res.data
    this.originalPic = this.form.pic
    if (this.form.times) {
      this.form.times = Math.floor(this.form.times / 60)
    }
  },
  methods: {
    /**
     * 处理文件选择变化，生成新图预览
     */
    handleFileChange(e) {
      this.file = e.target.files[0]
      if (this.file) {
        this.previewUrl = URL.createObjectURL(this.file)
      }
    },
    /**
     * 处理表单提交
     * 1. 上传新图片（如果有）
     * 2. 转换时长单位（分钟 -> 秒）
     * 3. 提交更新到后端
     */
    async handleSubmit() {
      try {
        // 1. 如果用户选了新图片，先上传图片
        if (this.file) {
          const uploadRes = await uploadFile(this.file)
          this.form.pic = uploadRes.data.filename
        }

        // 2. 复制表单数据，避免直接修改原对象
        const submitData = { ...this.form }

        // 3. 时长单位转换：用户输入的分钟 → 后端需要的秒
        if (submitData.times) submitData.times = submitData.times * 60
        
        // 4. 提交更新到后端
        await updateFilm(this.form.id, submitData)
        alert('修改成功')
        this.$router.push('/')
      } catch (error) {
        alert('修改失败')
      }
    }
  }
}
</script>

<style scoped>
.edit-film {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.back-btn {
  padding: 10px 20px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 20px;
}

h1 {
  margin-bottom: 30px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}

.form-group input,
.form-group textarea,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.preview-img {
  width: 200px;
  margin-top: 10px;
  border-radius: 4px;
}

.form-actions {
  margin-top: 30px;
}

.submit-btn {
  width: 100%;
  padding: 15px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}
</style>
