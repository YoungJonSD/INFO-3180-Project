<script setup>
import { RouterLink, RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
</script>

<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App"
}
</script>
