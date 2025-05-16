<template>
  <div class="p-6 bg-gray-50 min-h-screen max-w-[1000px] mx-auto  ">
    <div class="">
      <div>
        <div class="bg-white p-4">
          <h2 class="text-2xl font-bold">Document Templates</h2>
          <p class="text-[#64748b]">Manage and download modified document</p>
        </div>

        <div class="bg-white  max-w-[1200px]  mx-auto mt-4 p-6 gap-2">
          <div class="flex justify-between">
            <input type="text" placeholder="Search document..." class="w-[400px]" v-model="filterInput">
          </div>
        </div>

        <div class="bg-white  max-w-[1000px]  mx-auto mt-4 gap-2">
          <div class="overflow-hidden rounded-md border border-gray-300">
            <table class="w-full border-collapse">
              <thead class="bg-emerald-600 text-white border-b border-gray-300">
                <tr class="[&>th]:py-3 [&>th]:px-4 [&>th]:font-[600] text-left">
                  <th>Document Name</th>
                  <th>Size</th>
                  <th>Uploaded</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="document in filtered" :key="document.filename"
                  class="border-b border-gray-300 [&>td]:py-3 [&>td]:px-4 hover:bg-gray-100 transition cursor-pointer">
                  <td class="flex items-center gap-3">
                    <i class="pi pi-file-word text-blue-500"></i>
                    <div>
                      <p>{{ document.name }}</p>
                      <p class="text-sm text-gray-400">{{ document.description }}</p>
                    </div>
                  </td>
                  <td> 1MB </td>
                  <td>{{ formatDate(document.created_at) }}</td>

                  <td class="space-x-3">
                    <i class="pi pi-download text-blue-500 cursor-pointer "
                      @click="handleDownload(document.id)"></i>
                    <i class="pi pi-trash text-red-500 cursor-pointer"></i>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>

      </div>
    </div>
  </div>


  <Modal :isOpen="showUploadModal" @close="showUploadModal = false" :showCross="true"
    :myClass="'max-w-[600px] w-[80vw] p-8'">
    <div class="space-y-4">
      <h2 class="text-xl font-semibold">Upload New File</h2>


      <label
        class="flex items-center justify-center w-full h-32 border-2 border-dashed border-gray-400 rounded-lg cursor-pointer hover:bg-gray-100 transition"
        @dragover.prevent>
        <input type="file" class="hidden" @change="handleFileChange" accept=".doc,.docx" />
        <span class="text-sm text-gray-500" v-if="!fileToUpload">Click or Drag a file here</span>
        <span class="text-sm text-gray-700" v-else>{{ fileToUpload.name }}</span>
      </label>


      <div>
        <label class="text-sm font-medium text-gray-700">File Name</label>
        <input v-model="uploadFilename" type="text" class="w-full p-2 border rounded bg-gray-100" />
      </div>


      <div class="flex justify-end gap-2">
        <button @click="showUploadModal = false" class="px-4 py-2 border rounded">Cancel</button>
        <button class="primary-btn" @click="handleUpload" :disabled="!fileToUpload">
          Upload
        </button>
      </div>
    </div>
  </Modal>
</template>




<script setup>

import { computed, onMounted, ref } from 'vue';
import { apiClient } from '../api';
import Modal from '../components/Modal.vue';

const showUploadModal = ref(false)
const uploadFilename = ref(false)
const documents = ref([])
const fileToUpload = ref(null)
const filterInput = ref("")

const filtered = computed(() => {
  if (!filterInput.value) return documents.value;
  return documents.value.filter(doc =>
    doc.name.toLowerCase().includes(filterInput.value.toLowerCase())
  )
})

onMounted(async () => {
  await fetchDocuments()
})

const fetchDocuments = async () => {
  const res = await apiClient.get("/documents")
  documents.value = res.data.documents
  documents.value.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
}

const formatDate = (date) => {
  const createdAt = new Date(date);
  return createdAt.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  });
}
const handleFileChange = (event) => {
  const selectedFile = event.target.files[0];
  if (selectedFile) {
    fileToUpload.value = selectedFile;
    uploadFilename.value = selectedFile.name;
  }
};

const handleUpload = async () => {
  const allowedExtensions = [".doc", ".docx"];
  const fileName = fileToUpload.value.name.toLowerCase();
  const fileExtension = fileName.slice(fileName.lastIndexOf("."));

  if (!allowedExtensions.includes(fileExtension)) {
    alert("Only .doc and .docx files are allowed!");
    return;
  }

  try {
    const formData = new FormData()
    formData.append('file', fileToUpload.value)
    formData.append('name', uploadFilename.value)

    console.log("trying to add file")

    const response = await apiClient.post(
      `/documents`, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    })

    fileToUpload.value = null
    uploadFilename.value = ""
    showUploadModal.value = false
    await fetchDocuments()
  } catch (error) {
    console.error("Error uploading file:", error)
  }
}

const handleDownload = async (documentId) => {
  try {
    console.log(` Download request for: ${documentId}`);

    const response = await apiClient.get(`/documents/back/${documentId}`, {
      responseType: "blob",
    });

    console.log("File received from backend", response);


    const contentDisposition = response.headers["content-disposition"];
    let filename = documentId + ".docx";

    if (contentDisposition) {
      const match = contentDisposition.match(/filename="(.+)"/);
      if (match) {
        filename = match[1];
      }
    } else {
      console.warn(" Content-Disposition header missing. Using default filename.");
    }

    console.log(` Saving file as: ${filename}`);


    const url = window.URL.createObjectURL(new Blob([response.data]));
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    console.log(" File download triggered");
  } catch (error) {
    console.error(" Error downloading file:", error);
  }
};
</script>