<template>
  <div
    class="w-full min-h-[calc(100vh-3.5rem)] grid items-center gap-4 md:grid-cols-2"
  >
    <div
      class="bg-white rounded-lg w-[95%] py-16 min-w-[300px] max-w-[500px] px-12 text-center mx-auto shadow-md"
    >
      <h2 class="text-3xl mt-2 mb-8 text-left">Log In</h2>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <input
          type="email"
          v-model="email"
          placeholder="Email"
          required
          class="border rounded-lg border-black/30 w-full p-2"
        />

        <div
          class="w-full flex justify-between items-center border rounded-lg border-black/30 mt-4"
        >
          <input
            :type="showPass ? 'text' : 'password'"
            v-model="password"
            placeholder="Password"
            required
            class="block w-[80%] focus:outline-none border-none"
          />
          <div @click="togglePassShow" class="cursor-pointer px-2">
            <i class="pi pi-eye" v-if="!showPass"></i>
            <i v-else class="pi pi-eye-slash"></i>
          </div>
        </div>

        <button
          type="submit"
          class="ml-auto border px-4 py-2 w-full mt-4 rounded-md hover:bg-[#059862] bg-[#04AA6D] text-white font-[500]"
        >
          Log In
        </button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </div>

    <div
      class="hidden md:grid h-[calc(100vh-3.5rem)] rounded-md bg-[url('https://images.unsplash.com/photo-1674027444485-cec3da58eef4?q=80&w=1632&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')] bg-cover"
    ></div>
  </div>
</template>


<script setup>
import { ref, onMounted, watch } from "vue";
import { loginUser } from "../api";
import { useUserStore } from "../stores/UserStore";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");
const error = ref(null);
const { login, userState, fetchUser } = useUserStore();
const router = useRouter();

const showPass = ref(false)

const togglePassShow = () => {
  showPass.value = !showPass.value
}

onMounted(() => {

  if (!userState.user) {
    fetchUser();

  }
});

watch(() => userState.user, (user) => {
  if (user) {
    router.push("/dashboard");
  }
});

const handleLogin = async () => {
  try {
    error.value = null;
    const response = await loginUser(email.value, password.value);

    await login(response.data.access_token);

  } catch (err) {
    error.value = "Invalid email or password";
    console.error(err);
  }
};
</script>

<style scoped>
.error {
  color: red;
}
</style>
