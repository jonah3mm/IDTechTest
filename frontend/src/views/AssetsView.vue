<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getAssets, toggleAsset, deleteAsset, downloadAssetsCsv } from '../api/index.js'
import AssetTable from '../components/AssetTable.vue'

const route = useRoute()
const router = useRouter()
const parsePage = (value) => {
  const parsed = Number.parseInt(value, 10)
  return Number.isFinite(parsed) && parsed > 0 ? parsed : 1
}
const queryValue = (value) => typeof value === 'string' ? value : ''
const assetTypeOptions = ['workstation', 'server', 'network', 'peripheral']
const statusOptions = ['active', 'inactive', 'retired']

const assets = ref([])
const total = ref(0)
const currentPage = ref(parsePage(route.query.page))
const totalPages = ref(1)
const search = ref(queryValue(route.query.search))
const assetType = ref(queryValue(route.query.type))
const statusFilter = ref(queryValue(route.query.status))
const loading = ref(false)
const error = ref(null)
let searchDebounceId = null

const formatDate = (dateStr) => dateStr ? dateStr.split('T')[0] : 'Never'

const syncRoute = () => {
  const query = {}
  if (search.value) query.search = search.value
  if (assetType.value) query.type = assetType.value
  if (statusFilter.value) query.status = statusFilter.value
  if (currentPage.value > 1) query.page = String(currentPage.value)
  router.replace({ query })
}

const fetchAssets = async () => {
  loading.value = true
  error.value = null
  try {
    const data = await getAssets({
      search: search.value,
      type: assetType.value,
      status: statusFilter.value,
      page: currentPage.value,
    })
    assets.value = data.assets.map((a) => ({
      ...a,
      last_seen_formatted: formatDate(a.last_seen),
    }))
    total.value = data.total
    totalPages.value = data.pages
  } catch (err) {
    error.value = 'Failed to load assets. Is the backend running?'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const handleToggle = async (asset) => {
  await toggleAsset(asset.id)
  fetchAssets()
}

const handleDelete = async (asset) => {
  if (!confirm(`Delete "${asset.name}"? This cannot be undone.`)) return
  await deleteAsset(asset.id)
  fetchAssets()
}

const handleExport = () => {
  downloadAssetsCsv({
    search: search.value,
    type: assetType.value,
    status: statusFilter.value,
  })
}

const goToPage = (page) => {
  if (page < 1 || page > totalPages.value || page === currentPage.value) return
  currentPage.value = page
  syncRoute()
  fetchAssets()
}

watch(search, () => {
  currentPage.value = 1
  if (searchDebounceId) clearTimeout(searchDebounceId)
  searchDebounceId = window.setTimeout(() => {
    syncRoute()
    fetchAssets()
  }, 300)
})

watch(assetType, () => {
  currentPage.value = 1
  syncRoute()
  fetchAssets()
})

watch(statusFilter, () => {
  currentPage.value = 1
  syncRoute()
  fetchAssets()
})

onMounted(fetchAssets)

onBeforeUnmount(() => {
  if (searchDebounceId) clearTimeout(searchDebounceId)
})
</script>

<template>
  <div>
    <div class="d-flex align-items-center mb-4">
      <div>
        <h1 class="h3 mb-0">Assets</h1>
        <p class="text-muted mb-0">{{ total }} total asset{{ total !== 1 ? 's' : '' }}</p>
      </div>
      <button class="btn btn-outline-secondary ms-auto me-2" @click="handleExport">
        <i class="bi bi-download me-1"></i>Export CSV
      </button>
      <router-link to="/assets/new" class="btn btn-primary ms-auto">
        <i class="bi bi-plus-lg me-1"></i>Add Asset
      </router-link>
    </div>

    <!-- Search -->
    <div class="card mb-3">
      <div class="card-body py-2">
        <div class="row g-2 align-items-center">
          <div class="col">
            <div class="input-group">
              <span class="input-group-text bg-transparent border-end-0">
                <i class="bi bi-search text-muted"></i>
              </span>
              <input
                v-model="search"
                type="text"
                class="form-control border-start-0 ps-0"
                placeholder="Search assets…"
              />
            </div>
          </div>
          <div class="col-sm-4 col-lg-3">
            <select v-model="assetType" class="form-select">
              <option value="">All Types</option>
              <option v-for="type in assetTypeOptions" :key="type" :value="type" class="text-capitalize">
                {{ type }}
              </option>
            </select>
          </div>
          <div class="col-sm-4 col-lg-3">
            <select v-model="statusFilter" class="form-select">
              <option value="">All Statuses</option>
              <option v-for="status in statusOptions" :key="status" :value="status" class="text-capitalize">
                {{ status }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-5 text-muted">
      <div class="spinner-border spinner-border-sm me-2"></div>
      Loading…
    </div>

    <!-- Table -->
    <div v-else class="card">
      <div class="card-body p-0">
        <AssetTable
          :assets="assets"
          @toggle="handleToggle"
          @delete="handleDelete"
        />
      </div>
    </div>

    <!-- Pagination -->
    <nav v-if="totalPages > 1" class="mt-3" aria-label="Asset pages">
      <ul class="pagination justify-content-center mb-0">
        <li class="page-item" :class="{ disabled: currentPage === 1 }">
          <button class="page-link" @click="goToPage(currentPage - 1)">
            <i class="bi bi-chevron-left"></i>
          </button>
        </li>
        <li
          v-for="p in totalPages"
          :key="p"
          class="page-item"
          :class="{ active: p === currentPage }"
        >
          <button class="page-link" @click="goToPage(p)">{{ p }}</button>
        </li>
        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
          <button class="page-link" @click="goToPage(currentPage + 1)">
            <i class="bi bi-chevron-right"></i>
          </button>
        </li>
      </ul>
    </nav>
  </div>
</template>
