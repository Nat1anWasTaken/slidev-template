<script setup lang="ts">
defineProps<{
  kicker?: string
}>()
</script>

<template>
  <div class="slidev-layout intro">
    <div class="google-layout-inner">
      <div v-if="kicker" class="google-kicker">
        {{ kicker }}
      </div>
      <slot />
    </div>
  </div>
</template>
