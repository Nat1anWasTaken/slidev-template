import type { CSSProperties } from 'vue'

export function resolveAssetUrl(url: string) {
  if (url.startsWith('/'))
    return import.meta.env.BASE_URL + url.slice(1)
  return url
}

export function handleBackground(background?: string, dim = true, backgroundSize = 'cover'): CSSProperties {
  if (!background)
    return {}

  const isColor = ['#', 'rgb', 'hsl', 'var('].some(prefix => background.startsWith(prefix))

  if (isColor) {
    return {
      background,
      color: 'white',
    }
  }

  return {
    backgroundImage: dim
      ? `linear-gradient(120deg, rgba(24, 90, 188, 0.88), rgba(32, 33, 36, 0.72)), url("${resolveAssetUrl(background)}")`
      : `url("${resolveAssetUrl(background)}")`,
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    backgroundSize,
    color: dim ? 'white' : undefined,
  }
}
