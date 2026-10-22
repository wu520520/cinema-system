<template>
  <!-- 添加电影页面模板 -->
  <div class="add-film">
    <button class="back-btn" @click="$router.back()">← 返回</button>
    <h1>添加电影</h1>
    
    <!-- 电影信息表单 -->
    <form @submit.prevent="handleSubmit">
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
      
      <!-- 封面图片上传 -->
      <div class="form-group">
        <label>封面图片</label>
        <input type="file" @change="handleFileChange" accept="image/*" />
        <img v-if="previewUrl" :src="previewUrl" alt="预览" class="preview-img" />
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
            <option value="">请选择</option>
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
        <button type="submit" class="submit-btn">保存</button>
      </div>
    </form>
  </div>
</template>

<script>
/**
 * 添加电影页面组件
 * 功能：
 * - 表单输入电影信息
 * - 图片上传和预览
 * - 表单验证
 */
import { getRegions, getCategories, uploadFile, createFilm } from '../api'

export default {
  name: 'AddFilm',
  data() {
    return {
      // 表单数据
      form: {
        title: '',
        synopsis: '',
        region: '',
        director: '',
        release_date: '',
        times: '',
        score: '',
        grade: '',
        category: '',
        profit: '',
        organization: '',
        pic: ''
      },
      regions: [],        // 地区下拉选项
      categories: [],     // 分类下拉选项
      grades: ['G', 'PG', 'PG-13', 'R', 'NC-17', 'NR'],  // 分级选项
      file: null,         // 待上传的文件
      previewUrl: ''      // 图片预览URL
    }
  },
  /**
   * 组件挂载时获取地区和分类数据
   */
  async mounted() {
    const [regionsRes, categoriesRes] = await Promise.all([// 同时发送请求获取地区和分类数据
      getRegions(),
      getCategories()
    ])
    this.regions = regionsRes.data
    this.categories = categoriesRes.data
  },
  methods: {
   
    handleFileChange(e) {
      // 处理文件选择变化，生成预览
      this.file = e.target.files[0]
      if (this.file) {
        // 生成一个临时的预览 URL
        this.previewUrl = URL.createObjectURL(this.file)
      }
    },
    // 提交表单
    async handleSubmit() {
      try {

        // 上传图片（如果有），并获取文件名
        if (this.file) {
          const uploadRes = await uploadFile(this.file)
          this.form.pic = uploadRes.data.filename
        }

        // 复制表单数据，避免直接修改原始数据
        const submitData = { ...this.form }

        // 单位转换：将时长从分钟转换为秒
        if (submitData.times) submitData.times = submitData.times * 60

        // 提交数据到后端创建电影
        await createFilm(submitData)
        alert('添加成功')
        this.$router.push('/')
      } catch (error) {
        alert('添加失败')
      }
    }
  }
}
</script>

<style scoped>
.add-film {
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
