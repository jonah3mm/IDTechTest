<script setup>
defineProps({
  status: {
    type: String,
    required: true,
  },
})

const badgeClass = (status) => {
  const map = {
    active: 'bg-success',
    inactive: 'bg-warning text-dark',
    retired: 'bg-secondary',
  }
  return map[status] ?? 'bg-light text-dark'
}
</script>

<template>
  <span class="badge" :class="badgeClass(status)">
    {{ status.charAt(0).toUpperCase() + status.slice(1) }}
  </span>
</template>
