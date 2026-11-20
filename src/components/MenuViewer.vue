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
      <div class="menu-list">
        <div v-for="r in restaurants" :key="r.key" class="menu-col">
          <h2 class="restaurant-name">{{ r.name }}</h2>
          <div class="img-wrap">
            <img
              v-if="imgExists[r.key]"
              :alt="`${displayDate} ${r.name} 메뉴 이미지`"
              class="menu-img"
              :src="imgSrc(r.dir)"
            >
            <div v-else class="no-img">이미지가 없습니다.</div>
          </div>
        </div>
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
  // dir: 식당별 이미지 폴더 (식당 1은 public 루트, 식당 2는 r2/)
  const restaurants = [
    { key: 'r1', name: '지하1층식당', dir: '' },
    { key: 'r2', name: '2층식당', dir: 'r2/' },
  ]
  const imgSrc = (dir: string) => `${import.meta.env.BASE_URL}${dir}${displayDate.value}.jpg`

  const imgExists = ref<Record<string, boolean>>({ r1: false, r2: false })
  function checkImgExists () {
    for (const r of restaurants) {
      const img = new window.Image()
      img.addEventListener('load', () => {
        imgExists.value[r.key] = true
      })
      img.addEventListener('error', () => {
        imgExists.value[r.key] = false
      })
      img.src = imgSrc(r.dir)
    }
  }
  watch(displayDate, () => {
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
