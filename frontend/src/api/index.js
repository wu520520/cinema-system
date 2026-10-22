/**
 * API 接口封装模块
 */

import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const getRegions = () => api.get('/regions')
export const getCategories = () => api.get('/categories')
export const getFilms = (params) => api.get('/films', { params })
export const getFilm = (id) => api.get(`/films/${id}`)

// 文件上传接口
export const uploadFile = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

export const createFilm = (film) => api.post('/films', film)
export const updateFilm = (id, film) => api.put(`/films/${id}`, film)
export const deleteFilm = (id) => api.delete(`/films/${id}`)

export default api
