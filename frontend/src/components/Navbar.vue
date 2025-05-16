<template>
  <nav class="bg-white
       h-14 shadow-lg sticky top-0 left-0 z-50 ">

    <button class="absolute top-1 left-6 text-xl" @click="handleBurger" v-if="userState.user">
      <i class="pi pi-bars  hover:bg-gray-100 rounded-full p-3"></i>
    </button>
    <div class="mb-8 h-full  flex items-center pl-16 
        
        gap-8 max-w-[1000px] mx-auto text-black font-semibold px-4">

    
      <router-link to="/" :class="route.path === '/' ? '' : 'text-gray-500'"
      class=" h-14 px-4 grid place-items-center text-lg">Home</router-link>
      <router-link to="/dashboard" v-if="userState.user" :class="route.path === '/dashboard' ? '' : 'text-gray-500'"
        class=" h-14 px-4 grid place-items-center">Dashboard</router-link>




      <div class="w-[170px] h-[40px] border relative rounded-full ml-auto" v-if="!userState.user">
        <router-link to="/login" v-if="!userState.user" class="top-0 bottom-0 left-0 right-0 pr-6
          bg-[#E3EEFF] text-[#1A1A1A]
          text-right absolute hover:bg-[#059862] rounded-full pt-1 hover:text-white font-[500]">Log In</router-link>
        <router-link to="/signup" v-if="!userState.user" class="top-0 pt-1 bottom-0 w-[90px] bg-[#04AA6D] absolute text-white font-[500] text-center
          px-4 hover:bg-[#059862] rounded-full">Sign Up</router-link>

      </div>

      <button v-if="userState.user" @click="handleLogout" class="ml-auto border px-4 py-2 rounded-md hover:bg-[#059862]   bg-[#04AA6D]
      text-white font-[500]">Logout</button>
      <!-- <button v-if="userState.user" @click="handleLogout">Logout ({{ userState.user.email }})</button> -->
    </div>
  </nav>

</template>

<script setup>
import { useUserStore } from "../stores/UserStore";
import { useRouter, useRoute } from "vue-router";
import { inject } from "vue";
const { userState, logout } = useUserStore();
const router = useRouter();
const route = useRoute()
const sidebarActive = inject("sidebarActive")
const handleLogout = async () => {
  await logout();
  router.push("/login");
};

const handleBurger = () => {
  sidebarActive.value = !sidebarActive.value;
}
</script>