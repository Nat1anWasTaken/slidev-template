<script setup lang="ts">
defineProps<{
  kicker?: string
}>()
</script>

<template>
  <div class="slidev-layout section">
    <div class="google-layout-inner">
      <div v-if="kicker" class="google-kicker light">
        {{ kicker }}
      </div>
      <slot />
    </div>
  </div>
</template>
