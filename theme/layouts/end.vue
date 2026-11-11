<script setup lang="ts">
defineProps<{
  kicker?: string
  meta?: string
}>()
</script>

<template>
  <div class="slidev-layout end">
    <div class="google-layout-inner">
      <div v-if="kicker" class="google-kicker light">
        {{ kicker }}
      </div>
      <slot />
      <div v-if="meta" class="google-meta light">
        {{ meta }}
      </div>
    </div>
  </div>
</template>
