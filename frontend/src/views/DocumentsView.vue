<template>
  <div class="doc-container">
    <h2>📁 文档管理</h2>

    <div class="upload-box">
      <input type="file" @change="handleFile" accept=".txt,.pdf,.docx" />
      <button @click="upload" :disabled="!file || uploading">
        {{ uploading ? '上传中...' : '上传文档' }}
      </button>
    </div>

    <p v-if="message" :class="msgType">{{ message }}</p>

    <div class="stats">
      <h3>知识库状态</h3>
      <p>已入库文本片段：{{ totalChunks }} 个</p>
      <button @click="refresh">刷新</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const file = ref(null)
const uploading = ref(false)
const message = ref('')
const msgType = ref('')
const totalChunks = ref(0)

const handleFile = (e) => {
  file.value = e.target.files[0]
  message.value = ''
}

const upload = async () => {
  if (!file.value) return
  uploading.value = true
  message.value = ''

  const form = new FormData()
  form.append('file', file.value)

  try {
    const res = await axios.post('/api/documents/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    message.value = `✅ 上传成功！新增 ${res.data.chunks_added} 个文本片段`
    msgType.value = 'success'
    totalChunks.value += res.data.chunks_added
  } catch (err) {
    message.value = '❌ 上传失败：' + (err.response?.data?.detail || err.message)
    msgType.value = 'error'
  } finally {
    uploading.value = false
  }
}

const refresh = async () => {
  try {
    const res = await axios.get('/api/documents/list')
    totalChunks.value = res.data.total_chunks
  } catch (err) {
    console.error(err)
  }
}

onMounted(refresh)
</script>

<style scoped>
.doc-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.upload-box {
  margin: 20px 0;
  padding: 20px;
  border: 2px dashed #ddd;
  border-radius: 8px;
  text-align: center;
}
input[type="file"] {
  margin-bottom: 10px;
}
button {
  margin-top: 10px;
  padding: 8px 20px;
  background: #67c23a;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background: #a0cfff;
}
.success { color: #67c23a; font-weight: bold; }
.error { color: #f56c6c; font-weight: bold; }
.stats {
  margin-top: 30px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}
</style>