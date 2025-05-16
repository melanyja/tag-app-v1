<template>
  <div class="min-h-screen ">
    <Navbar />
    <Sidebar v-if="userState.user && sidebarActive" />
    <div>
      <router-view />
    </div>

  </div>
</template>

<script setup>

import Navbar from "./components/Navbar.vue";
import Sidebar from "./components/Sidebar.vue";

import { useUserStore } from "./stores/UserStore";
import { ref, provide } from "vue";

const { userState } = useUserStore();

const sidebarActive = ref(true)
provide("sidebarActive", sidebarActive)


</script>
