import { createRouter, createWebHistory } from 'vue-router'
import ChatView from './views/ChatView.vue'
import DocumentsView from './views/DocumentsView.vue'

const routes = [
  { path: '/', redirect: '/chat' },
  { path: '/chat', component: ChatView },
  { path: '/documents', component: DocumentsView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router