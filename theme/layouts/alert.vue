<script setup lang="ts">
defineProps<{
  kicker?: string
}>()
</script>

<template>
  <div class="slidev-layout alert">
    <div class="google-layout-inner">
      <div v-if="kicker" class="google-kicker">
        {{ kicker }}
      </div>
      <slot />
      <div class="google-mini-rail" aria-hidden="true" />
    </div>
  </div>
</template>
