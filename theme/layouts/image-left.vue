<script setup lang="ts">
import { computed } from 'vue'
import { handleBackground } from '../layoutHelper'

const props = withDefaults(defineProps<{
  image?: string
  backgroundSize?: string
  kicker?: string
}>(), {
  backgroundSize: 'cover',
})

const style = computed(() => handleBackground(props.image, false, props.backgroundSize))
</script>

<template>
  <div class="google-image-split">
    <div class="google-image-pane" :style="style" />
    <div class="slidev-layout default image-left">
      <div v-if="props.kicker" class="google-kicker">
        {{ props.kicker }}
      </div>
      <slot />
      <div v-if="$slots.callout" class="google-card compact google-image-callout">
        <slot name="callout" />
      </div>
    </div>
  </div>
</template>
