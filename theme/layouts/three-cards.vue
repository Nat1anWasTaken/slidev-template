<script setup lang="ts">
type Accent = 'blue' | 'red' | 'yellow' | 'green'

const props = withDefaults(defineProps<{
  cardColors?: Accent[]
  cardNumbers?: string[]
}>(), {
  cardColors: () => ['blue', 'red', 'green'],
  cardNumbers: () => ['01', '02', '03'],
})
</script>

<template>
  <div class="slidev-layout three-cards">
    <div class="google-layout-header">
      <slot />
    </div>
    <div class="google-card-grid">
      <div class="google-card">
        <div class="google-card-icon" :class="props.cardColors[0] || 'blue'">
          {{ props.cardNumbers[0] || '01' }}
        </div>
        <slot name="card1" />
      </div>
      <div class="google-card">
        <div class="google-card-icon" :class="props.cardColors[1] || 'red'">
          {{ props.cardNumbers[1] || '02' }}
        </div>
        <slot name="card2" />
      </div>
      <div class="google-card">
        <div class="google-card-icon" :class="props.cardColors[2] || 'green'">
          {{ props.cardNumbers[2] || '03' }}
        </div>
        <slot name="card3" />
      </div>
    </div>
  </div>
</template>
