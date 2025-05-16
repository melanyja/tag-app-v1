<template>
  <div class="w-full min-h-[calc(100vh-3.5rem)] grid items-center gap-4 md:grid-cols-2">
    <div class="bg-white rounded-lg w-[95%] py-16 min-w-[300px] max-w-[500px] px-12 text-center mx-auto shadow-md">
      <h2 class="text-3xl mt-2 mb-8 text-left">Sign Up</h2>
      <form @submit.prevent="handleRegister" class="space-y-4 [&>div>input]:w-full">
        <div>
          <input type="text" v-model="username" placeholder="Username" required
            class="p-2 border rounded-lg border-black/30" />
          <p v-if="errors.username" class=" error-box">{{ errors.username }}</p>
        </div>
        <div>
          <input type="email" v-model="email" placeholder="Email" required
            class="p-2 border rounded-lg border-black/30" />
          <p v-if="errors.email" class=" error-box">{{ errors.email }}</p>
        </div>


        <div>
          <div class="w-full  flex justify-between items-center outline-none
      border rounded-lg border-black/30  ">
            <input :type="showPass ? 'text' : 'password'" v-model="password" placeholder="Password" required
              class="block w-[80%] focus:outline-none border-none " />

            <div @click="togglePassShow" class="cursor-pointer px-2">
              <i class="pi pi-eye" v-if="!showPass"></i>
              <i v-else class="pi pi-eye-slash">
              </i>
            </div>
          </div>
          <p v-if="errors.password" class=" error-box">{{ errors.password }}</p>
        </div>

        <div>
          <div class="w-full  flex justify-between items-center outline-none
      border rounded-lg border-black/30  ">
            <input type="password" v-model="repassword" placeholder="Password " required
              class="block w-[80%] focus:outline-none border-none " />

            <div @click="" class="cursor-pointer px-2">
              <i class="pi pi-eye" v-if="!showPass"></i>
              <i v-else class="pi pi-eye-slash">
              </i>
            </div>
          </div>
          <p v-if="errors.repass" class=" error-box">
            {{ errors.repass }}
          </p>
        </div>


        <button type="submit" class="w-full ml-auto border px-4 py-2 mt-4 rounded-md hover:bg-[#059862]   bg-[#04AA6D]
        text-white font-[500]">Sign Up</button>
      </form>
      <p v-if="message" class="success-box">{{ message }}</p>
      <p v-if="error" class="error-box">{{ error }}</p>
    </div>
    <div
      class="hidden md:grid h-[calc(100vh-3.5rem)] rounded-md bg-[url('https://images.unsplash.com/photo-1674027444485-cec3da58eef4?q=80&w=1632&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')] bg-cover">
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { registerUser } from "../api";
import { useRouter } from "vue-router";
import { toast } from "vue3-toastify"


const email = ref("");
const username = ref("")
const password = ref("");
const repassword = ref("");
const message = ref(null);
const error = ref(null);
const router = useRouter();
const showPass = ref(false)

const errors = reactive({
  username: "",
  password: "",
  repass: "",
  email: ""
})

const clearErrors = () => Object.keys(errors).forEach(k => errors[k] = "");

const checkFormData = () => {
  let isValid = true;
  clearErrors();

  if (username.value.trim().length < 3) {
    console.log("Bad username")
    errors.username = "Username must be at least 3 characters";
    isValid = false;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/;

  if (!emailRegex.test(email.value)) {
    errors.email = "Please enter a valid email address";
    isValid = false;
  }

  if (!passwordRegex.test(password.value)) {
    errors.password = "Password must be at least 8 characters and include at least one letter and one number";
    isValid = false;
  }

  if (password.value !== repassword.value) {
    errors.repass = "Passwords do not match";
    isValid = false;
  }

  return isValid;
}

const togglePassShow = () => {
  showPass.value = !showPass.value
}

const handleRegister = async () => {
  if (!checkFormData()) {
    console.log("Bad form")
    return;
  }
  try {
    error.value = null;
    message.value = null;
    console.log(email.value, username.value, password.value)
    await registerUser(email.value, username.value, password.value);
    message.value = "Registration successful! Redirecting to login...";

    toast("Registration succesfull!", {
      autoClose: 5000,
      progressStyle: { backgroundColor: "green", height: "6px" }, theme: "colored"
    })

    setTimeout(() => {
      router.push("/login");
    }, 6000);
  } catch (err) {
    error.value = "Registration failed";
    console.error(err);
  }
};
</script>
