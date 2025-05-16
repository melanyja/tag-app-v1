<template>
  <teleport to="body">
    <div v-if="isOpen" class="modal-overlay">
      <div class="modal" :class="[myClass]">
        <button @click="closeModal" class="text-gray-500 hover:text-gray-800 close">
          <i class="pi pi-times text-lg"></i>
        </button>
        <slot></slot>
      </div>
    </div>
  </teleport>
</template>

<script setup>


const props = defineProps({
  isOpen: Boolean,
  myClass: {
    type: String,
    default: ""
  },
  showCross: {
    type: Boolean,
    default: true
  }
});
const emit = defineEmits(['close']);

function closeModal() {
  emit('close');
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal {
  background: white;

  border-radius: 8px;

  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  position: relative;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
}
</style>