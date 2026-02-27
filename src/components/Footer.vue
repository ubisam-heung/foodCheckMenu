<template>
  <footer class="footer">
    <span>© (주) 유비샘 조흥재연구원</span>
    <div class="footer-icons">
      <a v-for="item in icons" :key="item.icon" :href="item.url" class="footer-icon-btn" target="_blank" rel="noopener noreferrer">
        <i :class="['mdi', item.icon]"></i>
      </a>
    </div>
  </footer>
</template>

<script setup lang="ts">
const icons = [
  { icon: 'mdi-microphone-message', url: 'https://www.notion.so/3021dd99f25d8056b783d9fa92e2c9b6' },
  { icon: 'mdi-wifi', url: 'https://ubisam.hanbiro.net/ngw/app/#/' },
  { icon: 'mdi-github', url: 'https://github.com/ubisam-heung' },
]
</script>

<style scoped src="../styles/footer.css"></style>
