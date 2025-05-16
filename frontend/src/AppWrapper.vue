<template>
  <App />
</template>

<script setup>
import { provide } from 'vue';
import { provideUserStore } from './stores/UserStore';

import App from './App.vue';

provideUserStore();

</script>