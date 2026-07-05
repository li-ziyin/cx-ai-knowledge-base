<template>
  <el-container class="app">
    <el-header>
      <el-menu
        :default-active="activeIndex"
        class="nav-menu"
        mode="horizontal"
        router
      >
        <el-menu-item index="/chat">
          <el-icon><chat-line-round /></el-icon>
          <span>智能问答</span>
        </el-menu-item>
        <el-menu-item index="/documents">
          <el-icon><document /></el-icon>
          <span>文档管理</span>
        </el-menu-item>
      </el-menu>
    </el-header>

    <el-main>
      <router-view />
    </el-main>

    <el-footer>
      <div class="footer">
        CX AI Knowledge Base © 2026 | 基于 DeepSeek 大模型
      </div>
    </el-footer>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ChatLineRound, Document } from '@element-plus/icons-vue'

const route = useRoute()
const activeIndex = computed(() => route.path)
</script>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f0f2f5;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f0f2f5;
}
/* 隐藏滚动条但保留滚动 */
body::-webkit-scrollbar {
  width: 0;
  background: transparent;
}
.app {
  min-height: 100vh;
}
.el-header {
  background: linear-gradient(135deg, #409eff 0%, #67c23a 100%);
  padding: 0;
}
.nav-menu {
  justify-content: center;
  background: transparent !important;
  border-bottom: none !important;
}
.nav-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.85) !important;
  font-size: 16px;
  transition: all 0.3s;
}
.nav-menu .el-menu-item:hover {
  color: white !important;
  background: rgba(255, 255, 255, 0.1) !important;
}
.nav-menu .el-menu-item.is-active {
  color: white !important;
  background: rgba(255, 255, 255, 0.2) !important;
  border-bottom: 2px solid white !important;
}
.nav-menu .el-icon {
  margin-right: 6px;
}
.footer {
  text-align: center;
  color: #909399;
  padding: 20px;
  font-size: 14px;
}
</style>