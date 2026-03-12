<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        <router-link class="navbar-brand fw-bold" to="/">
          <i class="bi bi-hdd-network me-2"></i>NetTrack
        </router-link>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navMenu"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navMenu">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/">Dashboard</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/assets">Assets</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/clients">Clients</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="container py-4">
      <router-view />
    </main>

    <footer class="border-top mt-5 py-3 text-center text-muted small">
      NetTrack &mdash; Internal Asset Management
    </footer>
  </div>
</template>
