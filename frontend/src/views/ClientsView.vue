<script setup>
import { ref, onMounted } from 'vue'
import { getClients, deleteClient } from '../api/index.js'
import ClientCard from '../components/ClientCard.vue'

const clients = ref([])
const loading = ref(true)
const error = ref(null)

const fetchClients = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await getClients()
    clients.value = data.clients
  } catch (err) {
    error.value = 'Failed to load clients.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleDelete = async (client) => {
  if (!confirm(`Delete "${client.name}"?`)) return
  try {
    await deleteClient(client.id)
    fetchClients()
  } catch (err) {
    const msg = err.response?.data?.error || 'Could not delete client.'
    alert(msg)
  }
}

onMounted(fetchClients)
</script>

<template>
  <div>
    <div class="d-flex align-items-center mb-4">
      <div>
        <h1 class="h3 mb-0">Clients</h1>
        <p class="text-muted mb-0">{{ clients.length }} client{{ clients.length !== 1 ? 's' : '' }}</p>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <div v-if="loading" class="text-center py-5 text-muted">
      <div class="spinner-border spinner-border-sm me-2"></div>
      Loading…
    </div>

    <div v-else class="row g-3">
      <div v-if="clients.length === 0" class="col-12 text-center text-muted py-5">
        No clients found.
      </div>
      <div v-for="client in clients" :key="client.id" class="col-md-6 col-lg-4">
        <ClientCard :client="client" @delete="handleDelete" />
      </div>
    </div>
  </div>
</template>
