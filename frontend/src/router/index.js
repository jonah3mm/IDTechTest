import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AssetsView from '../views/AssetsView.vue'
import AssetCreateView from '../views/AssetCreateView.vue'
import AssetDetailView from '../views/AssetDetailView.vue'
import ClientsView from '../views/ClientsView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/assets', component: AssetsView },
  { path: '/assets/new', component: AssetCreateView },
  { path: '/assets/:id', component: AssetDetailView },
  { path: '/clients', component: ClientsView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
