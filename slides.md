---
theme: ./theme
title: 簡報標題
colorSchema: light
aspectRatio: 16/9
canvasWidth: 980
exportFilename: slides
layout: cover
kicker: 課程名稱 · 第 X 週
team: 第 X 組
members:
  - 組員一
  - 組員二
meta: 2026.11.11
---

# 簡報標題

一句話說明這份簡報要回答的問題

<!--
這份 slides.md 是版面範例，每一頁示範一種 layout。開新簡報時整份換掉即可。
-->

---
layout: section
kicker: Part 1
---

# 章節標題

章節的一句話摘要

---

# 一般內容頁

標題下的第一段會變成副標

- 重點一，搭配 `inline code`
- 重點二，[連結](https://sli.dev)
- 重點三

> 結論或補充說明放在引用區塊，會變成細線下的灰字

---
layout: three-cards
cardColors: [blue, red, green]
cardNumbers: ['01', '02', '03']
---

# 三個重點

::card1::

### 第一點

一兩句說明

::card2::

### 第二點

一兩句說明

::card3::

### 第三點

一兩句說明

---
layout: two-cols-callout
calloutKicker: Takeaway
---

# 左邊內容，右邊結論

::left::

- 左欄放論述或條列
- 第二點
- 第三點

::right::

## 右欄放一句結論

---
layout: figure
kicker: Part 1 · 章節標題
---

# 圖表頁

圖表放在 `::figure::`，資料來源放在 `::source::`

::figure::

<img src="/images/placeholder.svg" class="h-64" alt="">

圖說文字

::source::

資料來源：作者（年份）《出處》

---
layout: figure-side
figureWidth: 50%
---

# 左文右圖

- 文字放左邊
- 圖放在 `::figure::`

::figure::

<img src="/images/placeholder.svg" class="h-80" alt="">

---
layout: image-right
image: /images/placeholder.svg
kicker: Image
---

# 半版圖片

右半邊是 `image`，左半邊是內容

::callout::

### Callout

補充說明卡片

---
layout: fact
kicker: 關鍵數字
---

# 42%

一句話說明這個數字

---
layout: statement
---

# 一句主張，
*重點用斜體標成藍色*

---
layout: quote
---

# 引言放在這裡，最多兩三行。

作者，《出處》

---
layout: alert
kicker: Warning
---

# 注意事項

需要特別提醒的內容

---
layout: end
kicker: Thanks
---

# 謝謝聆聽

<div class="google-qr-row">
  <QrCode url="https://sli.dev/" label="Slidev" size="9rem" />
</div>
