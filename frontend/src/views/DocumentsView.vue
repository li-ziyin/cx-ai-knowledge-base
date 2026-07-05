<template>
  <div class="doc-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <el-icon :size="24" class="header-icon"><document /></el-icon>
          <span>文档管理</span>
          <el-tag type="success">已入库 {{ totalChunks }} 个片段</el-tag>
        </div>
      </template>

      <el-upload
        class="upload-area"
        drag
        action="#"
        :auto-upload="false"
        :on-change="handleFile"
        accept=".txt,.pdf,.docx"
      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或 <em>点击上传</em>
        </div>
        <template #tip>
          <div class="el-upload__tip">
            支持 TXT / PDF / DOCX 格式
          </div>
        </template>
      </el-upload>

      <el-button
        type="success"
        @click="upload"
        :loading="uploading"
        :disabled="!file"
        class="upload-btn"
      >
        {{ uploading ? '上传中...' : '开始上传' }}
      </el-button>

      <el-alert
        v-if="message"
        :title="message"
        :type="msgType"
        :closable="false"
        class="msg-alert"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { UploadFilled, Document } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const file = ref(null)
const uploading = ref(false)
const message = ref('')
const msgType = ref('info')
const totalChunks = ref(0)

const handleFile = (uploadFile) => {
  file.value = uploadFile.raw
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
    message.value = `✅ ${res.data.filename} 上传成功！新增 ${res.data.chunks_added} 个片段`
    msgType.value = 'success'
    totalChunks.value += res.data.chunks_added
    ElMessage.success('上传成功')
    file.value = null
  } catch (err) {
    message.value = '❌ 上传失败：' + (err.response?.data?.detail || err.message)
    msgType.value = 'error'
    ElMessage.error('上传失败')
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
  max-width: 900px;
  margin: 20px auto;
  padding: 0 20px;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}
.header-icon {
  margin-right: 10px;
  color: #67c23a;
}
.upload-area {
  margin: 20px 0;
}
.upload-btn {
  width: 100%;
  margin-bottom: 20px;
}
.msg-alert {
  margin-top: 10px;
}
</style>