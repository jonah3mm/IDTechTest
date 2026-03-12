<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { createAsset } from '../api/index.js'
import { getClients } from '../api/index.js'

const router = useRouter()
const clients = ref([])
const saving = ref(false)
const error = ref(null)

const form = ref({
  name: '',
  asset_type: '',
  client_id: '',
  serial_number: '',
  assigned_to: '',
  notes: '',
  status: 'active',
})

onMounted(async () => {
  const data = await getClients()
  clients.value = data.clients
})

const handleSubmit = async () => {
  saving.value = true
  error.value = null
  try {
    const payload = { ...form.value }
    if (!payload.name) delete payload.name
    if (!payload.asset_type) delete payload.asset_type
    if (!payload.client_id) delete payload.client_id
    if (!payload.serial_number) delete payload.serial_number
    if (!payload.assigned_to) delete payload.assigned_to
    if (!payload.notes) delete payload.notes
    const asset = await createAsset(payload)
    router.push(`/assets/${asset.id}`)
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to create asset.'
    saving.value = false
  }
}
</script>

<template>
  <div>
    <div class="mb-3">
      <router-link to="/assets" class="text-muted text-decoration-none small">
        <i class="bi bi-arrow-left me-1"></i>Back to Assets
      </router-link>
    </div>

    <h1 class="h3 mb-4">New Asset</h1>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <form @submit.prevent="handleSubmit" style="max-width: 540px">
      <div class="mb-3">
        <label class="form-label fw-semibold">Name <span class="text-danger">*</span></label>
        <input v-model="form.name" type="text" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Type <span class="text-danger">*</span></label>
        <select v-model="form.asset_type" class="form-select">
          <option value="">Select a type…</option>
          <option value="workstation">Workstation</option>
          <option value="server">Server</option>
          <option value="network">Network</option>
          <option value="peripheral">Peripheral</option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Client <span class="text-danger">*</span></label>
        <select v-model="form.client_id" class="form-select">
          <option value="">Select a client…</option>
          <option v-for="c in clients" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Serial Number</label>
        <input v-model="form.serial_number" type="text" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Assigned To</label>
        <input v-model="form.assigned_to" type="text" class="form-control" />
      </div>

      <div class="mb-3">
        <label class="form-label fw-semibold">Notes</label>
        <textarea v-model="form.notes" class="form-control" rows="3"></textarea>
      </div>

      <div class="d-flex gap-2">
        <button type="submit" class="btn btn-primary" :disabled="saving">
          <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
          Create Asset
        </button>
        <router-link to="/assets" class="btn btn-outline-secondary">Cancel</router-link>
      </div>
    </form>
  </div>
</template>
