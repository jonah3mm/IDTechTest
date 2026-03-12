<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  client: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['delete'])
const router = useRouter()
</script>

<template>
  <div class="card h-100">
    <div class="card-body">
      <h5 class="card-title">
        <i class="bi bi-building me-2 text-muted"></i>{{ client.name }}
      </h5>
      <ul class="list-unstyled small text-muted mb-3">
        <li v-if="client.contact_email">
          <i class="bi bi-envelope me-1"></i>{{ client.contact_email }}
        </li>
        <li v-if="client.phone">
          <i class="bi bi-telephone me-1"></i>{{ client.phone }}
        </li>
      </ul>
      <span class="badge bg-primary">{{ client.asset_count }} asset{{ client.asset_count !== 1 ? 's' : '' }}</span>
    </div>
    <div class="card-footer d-flex gap-2">
      <button class="btn btn-sm btn-outline-primary" @click="router.push(`/clients/${client.id}`)">
        <i class="bi bi-eye me-1"></i>View
      </button>
      <button class="btn btn-sm btn-outline-danger ms-auto" @click="emit('delete', client)">
        <i class="bi bi-trash me-1"></i>Delete
      </button>
    </div>
  </div>
</template>
