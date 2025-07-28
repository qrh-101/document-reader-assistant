<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <Header />
    <main class="container mx-auto px-4 py-8">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import Header from '@/components/Header.vue'
</script>

<style>
#app {
  font-family: 'Inter', system-ui, sans-serif;
}
</style> 