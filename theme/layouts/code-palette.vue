<script setup lang="ts">
type Accent = 'blue' | 'red' | 'yellow' | 'green'

interface PaletteEntry {
  label?: string
  value: string
  color?: Accent
}

defineProps<{
  palette?: PaletteEntry[]
}>()
</script>

<template>
  <div class="slidev-layout code-palette">
    <slot />
    <div v-if="palette?.length" class="google-color-chips" aria-label="Color palette">
      <span
        v-for="entry in palette"
        :key="entry.value"
        :class="entry.color || 'blue'"
      >{{ entry.label || entry.value }}</span>
    </div>
  </div>
</template>
