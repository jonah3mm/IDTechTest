<script setup>
import StatusBadge from './StatusBadge.vue'
import { useRouter } from 'vue-router'

defineProps({
  assets: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['toggle', 'delete'])
const router = useRouter()

const typeIcon = (type) => {
  const map = {
    workstation: 'bi-pc-display',
    server: 'bi-server',
    network: 'bi-router',
    peripheral: 'bi-printer',
  }
  return map[type] ?? 'bi-device-hdd'
}
</script>

<template>
  <div class="table-responsive">
    <table class="table table-hover align-middle">
      <thead class="table-light">
        <tr>
          <th>Asset</th>
          <th>Type</th>
          <th>Client</th>
          <th>Assigned To</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="assets.length === 0">
          <td colspan="6" class="text-center text-muted py-4">No assets found.</td>
        </tr>
        <tr v-for="asset in assets" :key="asset.id">
          <td>
            <div class="fw-semibold">
              <i :class="`bi ${typeIcon(asset.asset_type)} me-2 text-muted`"></i>
              {{ asset.name }}
            </div>
            <small class="text-muted">{{ asset.serial_number || '—' }}</small>
          </td>
          <td class="text-capitalize">{{ asset.asset_type }}</td>
          <td>{{ asset.client_name }}</td>
          <td>{{ asset.assigned_to || '—' }}</td>
          <td><StatusBadge :status="asset.status" /></td>
          <td>
            <div class="d-flex gap-1">
              <button
                class="btn btn-sm btn-outline-secondary"
                title="View details"
                @click="router.push(`/assets/${asset.id}`)"
              >
                <i class="bi bi-eye"></i>
              </button>
              <button
                v-if="asset.status !== 'retired'"
                class="btn btn-sm btn-outline-warning"
                title="Toggle active/inactive"
                @click="emit('toggle', asset)"
              >
                <i class="bi bi-arrow-repeat"></i>
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                title="Delete asset"
                @click="emit('delete', asset)"
              >
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
