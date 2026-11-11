<script setup lang="ts">
import { computed } from 'vue'
import { encode } from 'uqr'

const props = withDefaults(defineProps<{
  /** URL (or any text) to encode. */
  url: string
  /** Bold title under the code, e.g. "GitHub Repo". */
  label?: string
  /** Optional small text under the label (e.g. a short URL). Hidden by default. */
  caption?: string
  /** Rendered edge length of the code, any CSS length. */
  size?: string
  /** Error correction level; M survives a slightly blurry projector photo. */
  ecc?: 'L' | 'M' | 'Q' | 'H'
  /** Wrap the code in a link so it is clickable in the web build. */
  link?: boolean
}>(), {
  size: '9rem',
  ecc: 'M',
  link: true,
})

// Quiet zone of 2 modules; the card's own white padding adds the rest.
const qr = computed(() => encode(props.url, { ecc: props.ecc, border: 2 }))

// One <path> of 1×1 squares, merged per row run, keeps the SVG tiny and crisp.
const path = computed(() => {
  const { data, size } = qr.value
  let d = ''
  for (let y = 0; y < size; y++) {
    let x = 0
    while (x < size) {
      if (!data[y][x]) { x++; continue }
      const start = x
      while (x < size && data[y][x]) x++
      d += `M${start} ${y}h${x - start}v1h${start - x}z`
    }
  }
  return d
})
</script>

<template>
  <figure class="deck-qr">
    <component
      :is="props.link ? 'a' : 'div'"
      class="deck-qr-code"
      :href="props.link ? props.url : undefined"
      :target="props.link ? '_blank' : undefined"
      :rel="props.link ? 'noopener' : undefined"
      :style="{ width: props.size, height: props.size }"
    >
      <svg
        :viewBox="`0 0 ${qr.size} ${qr.size}`"
        shape-rendering="crispEdges"
        role="img"
        :aria-label="`QR code：${props.url}`"
      >
        <rect :width="qr.size" :height="qr.size" fill="#fff" />
        <path :d="path" fill="currentColor" />
      </svg>
    </component>
    <figcaption v-if="props.label || props.caption">
      <b v-if="props.label" class="deck-qr-label">{{ props.label }}</b>
      <span v-if="props.caption" class="deck-qr-caption">{{ props.caption }}</span>
    </figcaption>
  </figure>
</template>
