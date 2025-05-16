<template>
  <div class="p-6 bg-gray-50 min-h-screen max-w-[1000px] mx-auto  ">

    <div class="bg-white p-4">
      <h2 class="text-2xl font-bold">Tag Management</h2>
      <p class="text-[#64748b]">Manage your tags.</p>
    </div>
    <div class="flex flex-col md:flex-row gap-4 mb-6">
      <div class="relative w-full md:w-1/3">
        <input type="text" v-model="searchQuery" placeholder="Search tags..."
          class="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-emerald-500" />
      </div>

      <div class="w-full md:w-1/5">
        <select v-model="filterType"
          class="w-full px-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-emerald-500">
          <option value="">All Tags</option>
          <option value="AI">AI Generated</option>
          <option value="Manual">Manually Created</option>
        </select>
      </div>

      <div class="md:ml-auto">
        <button @click="handleAddTag"
          class="bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2 rounded-lg flex items-center">
          <span class="mr-2">Add Tag +</span>

        </button>
      </div>
    </div>

    <div class="bg-white rounded-lg shadow overflow-hidden">
      <table class="w-full table-fixed divide-y divide-gray-200">
        <thead class="bg-emerald-600">
          <tr>
            <th class="w-[20%] px-6 py-4 text-left text-sm font-bold text-white uppercase tracking-wider">Tag Name</th>
            <th class="w-[15%] px-6 py-4 text-left text-sm font-bold text-white uppercase tracking-wider">Description
            </th>
         
            <th class="w-[15%] px-6 py-4 text-left text-sm font-bold text-white uppercase tracking-wider">Created</th>
            <th class="w-[10%] px-6 py-4 text-right text-sm font-bold text-white uppercase tracking-wider">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="(tag, index) in filteredTags" :key="index" :class="index % 2 === 0 ? 'bg-white' : 'bg-gray-50'">
            <td class="w-[20%] px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{{ tag.name }}</div>
            </td>

            <td class="w-[15%] px-6 py-4">
              <div class="text-sm text-gray-600 truncate">{{ tag.description }}</div>
            </td>

            <td class="w-[15%] px-6 py-4 whitespace-nowrap text-sm text-gray-700">
              {{ formatDate(tag.created_at) }}
            </td>

            <td class="w-[10%] px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="editTag(tag)" class="text-emerald-600 hover:text-emerald-900 p-2 rounded-md mr-2">
                <i class="pi pi-pen-to-square"></i>
              </button>
              <button @click="confirmDeleteTag(tag)" class="text-red-600 hover:text-red-900 p-2 rounded-md">
                <i class="pi pi-trash"></i>
              </button>
            </td>
          </tr>


        </tbody>
      </table>

    </div>


    <Modal :isOpen="showModal" @close="showModal = false" :myClass="'max-w-[450px] w-[90%]'">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">{{ editMode ? 'Edit Tag' : 'Add New Tag' }}</h3>
        </div>
        <div class="p-6">
          <div class="mb-4">
            <label for="tagName" class="block text-sm font-medium text-gray-700 mb-1">Tag Name</label>
            <input id="tagName" type="text" v-model="tagForm.name"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
              placeholder="Enter tag name (e.g. USER_NAME)" />
          </div>
          <div class="mb-4">
            <label for="tagContent" class="block text-sm font-medium text-gray-700 mb-1">Tag Content</label>
            <input id="tagContent" type="text" v-model="tagForm.value"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
              placeholder="Enter tag content" />
          </div>
          <div class="mb-4">
            <label for="tagDescription" class="block text-sm font-medium text-gray-700 mb-1">Description</label>
            <textarea id="tagDescription" v-model="tagForm.description" rows="3"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500"
              placeholder="Enter tag description"></textarea>
          </div>


        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-200 flex justify-end space-x-3 rounded-b-lg">
          <button @click="showModal = false"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
            Cancel
          </button>
          <button @click="updateTag"
            class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700">
            Update
          </button>
        </div>
      </div>
    </Modal>

    <Modal :isOpen="showDeleteModal" @close="showDeleteModal = false">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">Confirm Delete</h3>
        </div>
        <div class="p-6">
          <p class="text-gray-700">
            Are you sure you want to delete the tag <span class="font-bold">{{ tagToDelete.name }}</span>?
          </p>

        </div>
        <div class="px-6 py-4 bg-gray-50 border-t border-gray-200 flex justify-end space-x-3 rounded-b-lg">
          <button @click="closeDeleteModal"
            class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50">
            Cancel
          </button>
          <button @click="handleDeleteTag"
            class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-red-600 hover:bg-red-700">
            Delete
          </button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { fetchUserTags, createTag, deleteTag, getApiUrl, apiClient } from '../api';
import { useRouter } from 'vue-router';
import Modal from '../components/Modal.vue';
import { toast } from "vue3-toastify"

const router = useRouter();
const searchQuery = ref('');
const filterType = ref('');
const showModal = ref(false);
const showDeleteModal = ref(false);
const editMode = ref(false);
const selectedTag = ref(null)

const tagForm = reactive({
  id: null,
  name: '',
  value: "",
  description: '',
  isAIGenerated: false,
  aiPrompt: ''
});

const tagToDelete = reactive({});
const tags = ref([]);
const selectedTagId = ref(null)
const filteredTags = computed(() => {
  console.log(searchQuery.value)
  let result = [...tags.value];

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(tag =>
      tag.name.toLowerCase().includes(query) ||
      tag.description?.toLowerCase().includes(query)
    );
  }
  return result
})
const formatDate = (dateStr) => {
  if (!dateStr) return '-';
  const date = new Date(dateStr);
  return date.toLocaleString(undefined, {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};
const handleAddTag = () => {
  router.push("/tags")
}

const updateTag = async () => {
  const newData = {
    name: tagForm.name,
    value: tagForm.value,
    description: tagForm.description,
  }

  console.log(tagForm.name, tagForm.value, tagForm.description)
  const response = await apiClient.put(`/tags/${selectedTagId.value}`, newData);

  tags.value = await fetchUserTags()
  showModal.value = false
  console.log(response);
  toast.success("Tag updated succesfuly")
};

const editTag = (tag) => {
  editMode.value = true;
  console.log(tag)
  Object.assign(tagForm, { ...tag });
  showModal.value = true;
  selectedTagId.value = tag.id
  console.log(tag.id)
  console.log("Form === ", tagForm)
}


const confirmDeleteTag = (tag) => {
  Object.assign(tagToDelete, tag);
  showDeleteModal.value = true;
}

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  for (const key in tagToDelete) {
    delete tagToDelete[key];
  }
}

const handleDeleteTag = async () => {
  console.log(tagToDelete)
  tags.value = tags.value.filter(tag => tag.id !== tagToDelete.id)
  await deleteTag(tagToDelete.id)

  showDeleteModal.value = false;
}

onMounted(async () => {

  tags.value = await fetchUserTags()

});
</script>