<template>
  <div class="menu-viewer">
    <Header @click="goToday" />
    <main class="main-content">
      <h1 class="title">오늘의 메뉴입니다.</h1>
      <div class="date-nav">
        <button v-if="canGoPrev" class="nav-btn" @click="goPrev">&lt;</button>
        <span class="date">{{ displayDate }}</span>
        <button v-if="canGoNext" class="nav-btn" @click="goNext">&gt;</button>
      </div>
      <div class="img-wrap">
        <img
          v-if="imgExists"
          :alt="`${displayDate} 메뉴 이미지`"
          class="menu-img"
          :src="imgSrc"
        >
        <div v-else class="no-img">이미지가 없습니다.</div>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup lang="ts">

  import { computed, ref, watch } from 'vue'
  import Footer from './Footer.vue'
  import Header from './Header.vue'

  const minDate = new Date('2026-02-27')
  const today = new Date()
  const date = ref(new Date())

  const pad = (n: number) => n.toString().padStart(2, '0')
  const formatDate = (d: Date) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`

  const displayDate = computed(() => formatDate(date.value))
  // github pages는 base 경로가 /foodCheckMenu/ 이므로 BASE_URL 사용
  const imgSrc = computed(() => `${import.meta.env.BASE_URL}${displayDate.value}.jpg`)

  const imgExists = ref(false)
  function checkImgExists () {
    const img = new window.Image()
    img.addEventListener('load', function () {
      imgExists.value = true
    })
    img.addEventListener('error', function () {
      imgExists.value = false
    })
    img.src = imgSrc.value
  }
  watch(imgSrc, () => {
    checkImgExists()
  }, { immediate: true })

  const canGoPrev = computed(() => formatDate(date.value) > formatDate(minDate))
  const canGoNext = computed(() => formatDate(date.value) < formatDate(today))

  function goToday () {
    date.value = new Date()
    // 이미지 존재 여부 즉시 갱신
    checkImgExists()
  }

  function goPrev () {
    if (canGoPrev.value) {
      const d = new Date(date.value)
      d.setDate(d.getDate() - 1)
      date.value = d
    }
  }

  function goNext () {
    if (canGoNext.value) {
      const d = new Date(date.value)
      d.setDate(d.getDate() + 1)
      date.value = d
    }
  }
</script>

<style scoped src="../styles/menu.css"></style>
