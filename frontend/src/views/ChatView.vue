<template>
  <div class="chat-container">
    <h2>🤖 AI 知识库问答</h2>

    <div class="input-box">
      <textarea
        v-model="question"
        placeholder="输入你的问题，例如：长鑫存储是做什么的？"
        rows="3"
      ></textarea>
      <button @click="ask" :disabled="loading">
        {{ loading ? '思考中...' : '发送' }}
      </button>
    </div>

    <div v-if="answer" class="answer-box">
      <h3>回答：</h3>
      <div class="content">{{ answer }}</div>

      <div v-if="sources.length" class="sources">
        <h4>📚 参考来源：</h4>
        <div v-for="(src, i) in sources" :key="i" class="source-item">
          <span class="tag">片段{{ i+1 }}</span>
          <p>{{ src }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const question = ref('')
const answer = ref('')
const sources = ref([])
const loading = ref(false)

const ask = async () => {
  if (!question.value.trim()) return
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
  } catch (err) {
    answer.value = '请求失败：' + (err.response?.data?.detail || err.message)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.chat-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
.input-box textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  font-size: 14px;
}
button {
  margin-top: 10px;
  padding: 10px 24px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}
button:disabled {
  background: #a0cfff;
}
.answer-box {
  margin-top: 20px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}
.content {
  line-height: 1.6;
  color: #333;
}
.sources {
  margin-top: 16px;
}
.source-item {
  margin: 8px 0;
  padding: 10px;
  background: white;
  border-left: 4px solid #409eff;
  border-radius: 4px;
}
.tag {
  font-size: 12px;
  color: #409eff;
  font-weight: bold;
}
</style>