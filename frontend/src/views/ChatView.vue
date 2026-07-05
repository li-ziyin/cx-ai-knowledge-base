<template>
  <div class="chat-container">
    <el-card class="chat-card">
      <template #header>
        <div class="card-header">
          <el-icon :size="24" class="header-icon"><chat-line-round /></el-icon>
          <span>AI 知识库问答</span>
        </div>
      </template>

      <div class="input-area">
        <el-input
          v-model="question"
          type="textarea"
          :rows="3"
          placeholder="输入你的问题，例如：晋景公是怎么死的？"
          @keyup.enter.ctrl="ask"
        />
        <el-button
          type="primary"
          @click="ask"
          :loading="loading"
          class="send-btn"
        >
          {{ loading ? '思考中...' : '发送' }}
        </el-button>
      </div>

      <div v-if="answer" class="answer-area">
        <el-divider content-position="left">回答</el-divider>
        <div class="answer-content" v-html="formattedAnswer"></div>

        <div v-if="sources.length" class="sources-area">
          <el-divider content-position="left">参考来源（{{ sources.length }}条）</el-divider>
          <el-collapse>
            <el-collapse-item
              v-for="(src, i) in sources"
              :key="i"
              :title="`片段 ${i+1}`"
            >
              <div class="source-text">{{ src }}</div>
            </el-collapse-item>
          </el-collapse>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'
import { ChatLineRound } from '@element-plus/icons-vue'

const question = ref('')
const answer = ref('')
const sources = ref([])
const loading = ref(false)

const formattedAnswer = computed(() => {
  return answer.value.replace(/\n/g, '<br>')
})

const ask = async () => {
  if (!question.value.trim()) {
    ElMessage.warning('请输入问题')
    return
  }

  loading.value = true
  answer.value = ''
  sources.value = []

  try {
    const res = await axios.post('/api/chat/', {
      message: question.value,
      system_prompt: '你是企业知识库助手，基于资料回答问题'
    })
    answer.value = res.data.reply
    sources.value = res.data.sources || []

    if (sources.value.length === 0) {
      ElMessage.info('未检索到相关文档，回答基于模型自身知识')
    }
  } catch (err) {
    ElMessage.error('请求失败：' + (err.response?.data?.detail || err.message))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-container {
  max-width: 900px;
  margin: 20px auto;
  padding: 0 20px;
}
.chat-card {
  min-height: 500px;
}
.card-header {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
}
.header-icon {
  margin-right: 10px;
  color: #409eff;
}
.input-area {
  margin-bottom: 20px;
}
.send-btn {
  margin-top: 10px;
  width: 100%;
}
.answer-content {
  line-height: 1.8;
  color: #303133;
  font-size: 15px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 8px;
}
.sources-area {
  margin-top: 20px;
}
.source-text {
  color: #606266;
  line-height: 1.6;
  padding: 10px;
  background: #fafafa;
  border-radius: 4px;
}
</style>