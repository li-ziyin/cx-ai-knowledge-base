<template>
  <div class="app">
    <nav>
      <router-link to="/chat">💬 问答</router-link>
      <router-link to="/documents">📁 文档</router-link>
    </nav>
    <router-view />
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f0f2f5;
}
nav {
  background: #409eff;
  padding: 16px;
  text-align: center;
}
nav a {
  color: white;
  text-decoration: none;
  margin: 0 20px;
  font-size: 16px;
}
nav a.router-link-active {
  font-weight: bold;
  border-bottom: 2px solid white;
}
</style>