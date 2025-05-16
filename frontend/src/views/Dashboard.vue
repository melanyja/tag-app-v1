<template>
  <div class="max-w-[1000px] mx-auto p-2">
    <div class="max-w-7xl mx-auto p-4 md:p-6 space-y-6">
 
      <section class="bg-white rounded-xl shadow-sm p-6 flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h2 class="text-2xl md:text-3xl font-bold text-gray-800">
            Welcome back, {{ user?.username || 'User' }}
          </h2>
          <p class="text-gray-500 mt-1">{{ user?.email }}</p>
        </div>
        
      </section>
      
      <section class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        <div
          v-for="(card, index) in summaryCards"
          :key="card.title"
          class="bg-white rounded-xl shadow-sm p-5 transition-all hover:shadow-md border-l-4"
          :class="getCardBorderColor(index)"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500 font-medium">{{ card.title }}</p>
              <h3 class="text-2xl font-bold mt-1">{{ card.value }}</h3>
            </div>
            <div class="p-2 rounded-lg" :class="getCardIconBgColor(index)">
            </div>
          </div>
        </div>
      </section>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
  
        
        <section class="bg-white rounded-xl shadow-sm p-6 col-span-1 lg:col-span-2">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold text-gray-800">Recent Documents</h3>
            <RouterLink class="text-sm text-[#04AA6D] font-medium flex items-center" to="/documents">
              View All
              
              <i class="pi pi-angle-right"></i>
            </RouterLink>
          </div>
          
          <div v-if="documents.length === 0" class="flex flex-col items-center justify-center py-10 text-center">
            <div class="p-4 rounded-full bg-gray-100 mb-3">
              <i class="pi pi-file"></i>
            </div>
            <p class="text-gray-500">No documents yet</p>
            <button class="mt-3 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700 transition-colors">
              Create Document
            </button>
          </div>
          
          <ul v-else class="divide-y divide-gray-100">
            <li
              v-for="doc in documents.slice(-3).reverse()"
              :key="doc.id"
              class="py-3 hover:bg-gray-50 px-2 rounded-lg transition-colors"
            >
              <div class="flex justify-between items-center">
                <div class="flex items-center">
                  <div class="p-2 bg-blue-50 rounded-lg mr-3">
                      <i class="pi pi-file"></i>
                  </div>
                  <div>
                    <p class="font-medium text-gray-800">{{ doc.name }}</p>
                    <p class="text-xs text-gray-500">{{ formatDate(doc.updatedAt || new Date()) }}</p>
                  </div>
                </div>
           
              </div>
            </li>
          </ul>
        </section>
        
        <section class="bg-white rounded-xl shadow-sm p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold text-gray-800">Recent Tags</h3>
            <RouterLink class="text-sm gap-2  text-[#04AA6D] font-medium flex items-center" to="/manage-tags">
              Manage
              <i class="pi pi-cog"></i>
            </RouterLink>
          </div>
          
          <div v-if="tags.length === 0" class="flex flex-col items-center justify-center py-10 text-center">
      
            <p class="text-gray-500">No tags created yet</p>
            <button class="mt-3 px-4 py-2 text-[#04AA6D] rounded-lg text-sm  transition-colors">
              Create Tag
            </button>
          </div>
          
          <ul v-else class="space-y-3">
            <li
              v-for="tag in tags.slice(-3).reverse()"
              :key="tag.id"
              class="flex gap-2 items-center p-2 hover:bg-gray-50 rounded-lg transition-colors"
            >
              <i class="pi pi-tags"></i>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-gray-800 truncate">{{ tag.name }}</p>
                <p class="text-xs text-gray-500 truncate">{{ tag.description || 'No description' }}</p>
              </div>
              <div class="ml-2 flex-shrink-0 bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded-full">
                0
              </div>
            </li>
          </ul>
          
         
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/UserStore'
import { apiClient, fetchUserTags } from '../api'
import { RouterLink } from 'vue-router'

const { userState } = useUserStore()
const user = userState.user

const documents = ref([])
const tags = ref([])
const missingTags = ref([])
const gptCount = ref(0)


const summaryCards = computed(() => [
  { title: 'Total Documents', value: documents.value.length,  },
  { title: 'Total Tags', value: tags.value.length },
  { title: 'Missing Tags', value: missingTags.value.length },
  { title: 'AI Generated', value: gptCount.value },
])


const getCardBorderColor = (index) => {
  const colors = [
    'border-blue-500',
    'border-green-500', 
    'border-amber-500',
    'border-purple-500'
  ]
  return colors[index % colors.length]
}

const getCardIconBgColor = (index) => {
  const colors = [
    'bg-blue-100',
    'bg-green-100', 
    'bg-amber-100',
    'bg-purple-100'
  ]
  return colors[index % colors.length]
}



const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const fetchDocuments = async () => {
  try {
    const res = await apiClient.get('/documents')
    documents.value = res.data.documents || []
  } catch (err) {
    console.error('Error loading documents:', err)
  }
}

const fetchTags = async () => {
  try {
    const result = await fetchUserTags()
    tags.value = result
    missingTags.value = result.filter(tag => !tag.value || tag.value.trim() === '')
    
  } catch (err) {
    console.error('Error loading tags:', err)
  }
}

onMounted(() => {
  fetchDocuments()
  fetchTags()
})
</script>