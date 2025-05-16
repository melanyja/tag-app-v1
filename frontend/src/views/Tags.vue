<template>
  <div class="p-6 bg-gray-50 min-h-screen max-w-[1000px] mx-auto  ">
    <div class="bg-white p-4 text-center sm:text-left ">
      <h2 class="text-2xl font-bold">Create New Tag</h2>
      <p class="text-[#64748b]">Create and Manage Tags for automatic document filling</p>
    </div>

    <div class="bg-white  max-w-[1000px]  mx-auto mt-4 p-6 flex flex-col gap-8 sm:gap-2 sm:flex-row">
      <div class="w-full border border-gray-200 rounded-md p-4 space-y-4 [&>div>input]:w-full [&>div>textarea]:w-full">
        <h2 class="text-lg font-semibold">Tag Information</h2>
        <div>
          <label for="">Tag Name</label>
          <input type="text" placeholder="Tag name" v-model="newTag.name">
        </div>
        <div>
          <label for="">Description</label>
          <textarea placeholder="Your description" v-model="newTag.description"></textarea>
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">Tag Content</label>

          <textarea v-if="tagType === 'text'" v-model="newTag.content" placeholder="Write content..."
            class="w-full h-[60px] px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 resize-none text-sm text-gray-800"></textarea>

          <div v-else class="w-full">
            <label v-if="!imageFile"
              class="block w-full px-4 py-3 border border-dashed border-emerald-400 rounded-lg bg-emerald-50 text-sm text-emerald-700 text-center cursor-pointer hover:bg-emerald-100">
              <span>Click to upload Image</span>
              <input type="file" accept="image/*" class="hidden" @change="handleImageUpload" />
            </label>
            <div v-if="imageFile || imagePreview" class="mt-3">
              <div class="relative w-full h-40 rounded-md overflow-hidden border border-gray-200">
                <img v-if="imagePreview" :src="imagePreview" class="w-full h-full object-contain" alt="Image preview" />

                <div v-if="isLoading" class="absolute inset-0 bg-white bg-opacity-70 flex items-center justify-center">
                  <div class="loading-spinner">
                    <i class="pi pi-spin pi-spinner text-emerald-500 text-2xl"></i>
                    <p class="text-sm text-emerald-600 mt-2">Loading...</p>
                  </div>
                </div>

                <button v-if="!isLoading" @click="removeImage"
                  class="absolute top-2 right-2 bg-red-500 text-white p-1 rounded-full w-6 h-6 flex items-center justify-center">
                  <span>×</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="flex">
          <div class="flex gap-2 mr-4">
            <input type="radio" value="text" name="type" checked v-model="tagType">
            <label for="">Text</label>
          </div>
          <div class="flex gap-2">
            <input type="radio" value="image" name="type" v-model="tagType">
            <label for="">Image</label>
          </div>
        </div>
        <button class="primary-btn" @click="saveTag">
          Save Tag
        </button>
      </div>

      <div class="w-full border border-gray-200 rounded-md p-4 space-y-4 [&>div>textarea]:w-full">
        <h2 class="text-lg font-semibold">AI Content Generator</h2>
        <div>
          <label for="">Enter Your Prompt</label>
          <textarea name="" id="" v-model="enteredPrompt"></textarea>
        </div>
        <div>
          <label>Prompt Result</label>
          <textarea class="h-[200px]" v-model="aiText" readonly></textarea>
        </div>

        <div class="flex gap-3">
          <button class="primary-btn" @click="generateContent">Generate Content</button>
          <button class="primary-btn" @click="applyToTag">Apply To Tag</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue"
import { apiClient } from "../api"
import { toast } from "vue3-toastify"

const tagType = ref("text")
const aiText = ref("")
const enteredPrompt = ref("")
const imagePreview = ref(null)
const imageFile = ref(null)
const isLoading = ref(false)

const newTag = reactive({
  name: "",
  description: "",
  content: ""
})

const removeImage = () => {
  imagePreview.value = null
  imageFile.value = null
}

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  isLoading.value = true
  imageFile.value = file

  const reader = new FileReader()
  reader.onload = (e) => {
    setTimeout(() => {
      imagePreview.value = e.target.result
      isLoading.value = false
    }, 800)
  }
  reader.readAsDataURL(file)
}

const applyToTag = () => {
  newTag.content = aiText.value
}

const generateContent = async () => {
  try {
    const res = await apiClient.post("/tags/generate-content", {
      prompt: enteredPrompt.value
    })
    aiText.value = res.data.data
  } catch (error) {
    console.log(error)
  }
}

const saveTag = async () => {
  if (!newTag.name || (tagType.value === 'text' && !newTag.content)) {
    alert("Name and content are required to create tag")
    return
  }

  try {
    const formData = new FormData()
    formData.append("name", newTag.name)
    formData.append("description", newTag.description || "")

    if (tagType.value === "text") {
      formData.append("value", newTag.content)
      await apiClient.post("/tags", formData)
    } else {
      formData.append("file", imageFile.value)
      await apiClient.post("/tags/image", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      })
    }

    newTag.name = ""
    newTag.content = ""
    newTag.description = ""
    imageFile.value = null
    imagePreview.value = null
    toast.success("Tag created successfully!", {
      autoClose: 5000,
      progressStyle: { backgroundColor: "green", height: "6px" },
      theme: "colored"
    })
  } catch (error) {
    toast.error("Error creating tag")
  }
}
</script>
