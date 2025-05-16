<template>
  <div class="p-6 bg-gray-50 min-h-screen max-w-[1000px] mx-auto  ">

    <div class="bg-white p-4">
      <h2 class="text-2xl font-bold">Account Settings</h2>
    </div>
    <form @submit.prevent="saveChanges" class="bg-white p-4  ">
      <div class="space-y-6">

        <div class="flex flex-col">
          <label for="username" class="text-sm font-medium text-gray-700 mb-1">Username</label>
          <div class="flex">

            <input type="text" id="username" v-model="formData.username" class="flex-grow ">
          </div>
        </div>

        <div class="flex flex-col">
          <label for="email" class="text-sm font-medium text-gray-700 mb-1">Email Address</label>
          <div class="flex">

            <input type="email" id="email" v-model="formData.email" class="flex-grow ">
          </div>
        </div>

        <div class="flex flex-col">
          <label for="password" class="text-sm font-medium mb-1">Password</label>
          <div class="flex">

            <input type="password" id="password" v-model="formData.password" class="flex-grow ">
            <button type="button" @click="changePassword"
              class="ml-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500">
              Change
            </button>
          </div>
        </div>


        <div class="flex pt-4 border-t border-gray-200">
          <button type="submit"
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500">
            Save Changes
          </button>
          <button type="button" @click="resetForm"
            class="ml-2 px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500">
            Cancel
          </button>
        </div>
      </div>
    </form>
    <div class="mt-10 pt-6 border-t border-gray-200 bg-white p-4">
      <h3 class="text-lg font-medium text-red-600 flex items-center">

        Danger Zone
      </h3>
      <div class="mt-3">
        <button type="button" @click="deleteAccount"
          class="px-4 py-2 bg-red-100 text-red-600 rounded-md hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-red-500">
          Delete Account
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

const formData = reactive({
  username: '',
  email: '',
  password: ""
});


const saveChanges = () => {
  console.log('Saving changes:', formData);
};

const resetForm = () => {

};

const changePassword = () => {
  console.log('Changing password');
};


const deleteAccount = () => {
  if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
    console.log('Deleting account');
  }
};
</script>