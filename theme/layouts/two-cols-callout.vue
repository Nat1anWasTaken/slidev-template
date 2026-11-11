<script setup lang="ts">
defineProps<{
  calloutKicker?: string
}>()
</script>

<template>
  <div class="slidev-layout two-cols-callout">
    <div class="google-layout-header">
      <slot />
    </div>
    <div class="google-column-left">
      <slot name="left" />
    </div>
    <div class="google-column-callout">
      <div v-if="calloutKicker" class="google-kicker">
        {{ calloutKicker }}
      </div>
      <slot name="right" />
      <div class="google-mini-rail" aria-hidden="true" />
    </div>
  </div>
</template>
