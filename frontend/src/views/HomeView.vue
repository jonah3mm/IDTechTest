<script setup>
import { ref, onMounted } from 'vue'
import { getAssets, getClients } from '../api/index.js'

const stats = ref({
  totalAssets: 0,
  activeAssets: 0,
  inactiveAssets: 0,
  retiredAssets: 0,
  totalClients: 0,
})

const loading = ref(true)

onMounted(async () => {
  const [assetsData, clientsData] = await Promise.all([
    getAssets({ page: 1 }),
    getClients(),
  ])

  stats.value.totalAssets = assetsData.total
  stats.value.totalClients = clientsData.clients.length

  // Count by status — fetch all pages to tally (simplified: count from first page sample)
  const statusCounts = { active: 0, inactive: 0, retired: 0 }
  assetsData.assets.forEach((a) => {
    if (statusCounts[a.status] !== undefined) statusCounts[a.status]++
  })
  stats.value.activeAssets = statusCounts.active
  stats.value.inactiveAssets = statusCounts.inactive
  stats.value.retiredAssets = statusCounts.retired

  loading.value = false
})
</script>

<template>
  <div>
    <div class="d-flex align-items-center mb-4">
      <div>
        <h1 class="h3 mb-0">Dashboard</h1>
        <p class="text-muted mb-0">IT Asset Overview</p>
      </div>
    </div>

    <div v-if="loading" class="text-center py-5 text-muted">
      <div class="spinner-border spinner-border-sm me-2"></div>
      Loading…
    </div>

    <div v-else>
      <div class="row g-3 mb-4">
        <div class="col-sm-6 col-lg-3">
          <div class="card border-0 bg-primary text-white h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <div class="fs-2 fw-bold">{{ stats.totalAssets }}</div>
                  <div class="opacity-75">Total Assets</div>
                </div>
                <i class="bi bi-hdd-stack fs-2 opacity-50"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-sm-6 col-lg-3">
          <div class="card border-0 bg-success text-white h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <div class="fs-2 fw-bold">{{ stats.activeAssets }}</div>
                  <div class="opacity-75">Active</div>
                </div>
                <i class="bi bi-check-circle fs-2 opacity-50"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-sm-6 col-lg-3">
          <div class="card border-0 bg-warning text-dark h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <div class="fs-2 fw-bold">{{ stats.inactiveAssets }}</div>
                  <div class="opacity-75">Inactive</div>
                </div>
                <i class="bi bi-pause-circle fs-2 opacity-50"></i>
              </div>
            </div>
          </div>
        </div>
        <div class="col-sm-6 col-lg-3">
          <div class="card border-0 bg-secondary text-white h-100">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start">
                <div>
                  <div class="fs-2 fw-bold">{{ stats.totalClients }}</div>
                  <div class="opacity-75">Clients</div>
                </div>
                <i class="bi bi-building fs-2 opacity-50"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-3">
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-body text-center py-5">
              <i class="bi bi-hdd-network display-4 text-primary mb-3 d-block"></i>
              <h5>Manage Assets</h5>
              <p class="text-muted">View, search, and update tracked devices across all clients.</p>
              <router-link to="/assets" class="btn btn-primary">
                <i class="bi bi-arrow-right me-1"></i>Go to Assets
              </router-link>
            </div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card h-100">
            <div class="card-body text-center py-5">
              <i class="bi bi-building display-4 text-secondary mb-3 d-block"></i>
              <h5>Manage Clients</h5>
              <p class="text-muted">Browse client organizations and their associated assets.</p>
              <router-link to="/clients" class="btn btn-outline-secondary">
                <i class="bi bi-arrow-right me-1"></i>Go to Clients
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
