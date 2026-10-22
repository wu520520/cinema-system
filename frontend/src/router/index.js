/**
 * 路由配置模块
 */

import { createRouter, createWebHistory } from 'vue-router'
import FilmList from '../views/FilmList.vue'
import FilmDetail from '../views/FilmDetail.vue'
import AddFilm from '../views/AddFilm.vue'
import EditFilm from '../views/EditFilm.vue'

const routes = [
  { path: '/', name: 'FilmList', component: FilmList },
  { path: '/film/:id', name: 'FilmDetail', component: FilmDetail },
  { path: '/add', name: 'AddFilm', component: AddFilm },
  { path: '/edit/:id', name: 'EditFilm', component: EditFilm }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
