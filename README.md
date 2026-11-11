# Slidev template

Starting point for a new [Slidev](https://sli.dev) deck with the Google-inspired theme. The theme lives in [`theme/`](theme) and is copied into every deck made from this template, so each deck can change its own copy freely.

## Start a new deck

```sh
gh repo create Nat1anWasTaken/<name> --public --template Nat1anWasTaken/slidev-template --clone
cd <name>
pnpm install
pnpm dev
```

Then:

1. Rename `name` in `package.json` and replace `slides.md` (it is a gallery of every layout).
2. In the repo settings, set **Pages → Source** to **GitHub Actions**.
3. Make sure the [Renovate app](https://github.com/apps/renovate) has access to the new repo.

## Commands

```sh
pnpm dev           # preview slides.md
pnpm build         # build to dist/
pnpm export        # export a PDF (needs playwright-chromium)
pnpm fonts         # rebuild the CJK font subsets (needs uv)
pnpm fonts:check   # list characters missing from the subsets
```

## CI

[`.github/workflows/ci.yml`](.github/workflows/ci.yml) runs on every push to `main` and on every pull request:

- **build:** checks the font subsets cover the slides, then builds the site with `--base /<repo>/`.
- **export:** exports the PDF and uploads it as the `slides-pdf` artifact.
- **deploy:** on `main` only, publishes the build to GitHub Pages.

Node comes from `.node-version` and pnpm from `packageManager` in `package.json`.

## Renovate

[`renovate.json`](renovate.json) runs weekly (Asia/Taipei). It bumps ranges in `package.json`, keeps the lockfile fresh, and groups the Slidev and Vue packages and the GitHub Actions. Minor and patch updates merge automatically once CI passes; major updates wait for review. Each new npm release must be 3 days old before Renovate picks it up. Node follows LTS releases only.

## Theme

Every slide uses Google's four colours (`--google-blue`, `--google-red`, `--google-yellow` and `--google-green`) and Google Sans, with a fixed 980px 16:9 canvas. All tokens are in [`theme/styles/theme.css`](theme/styles/theme.css).

| Layout | Use | Props and slots |
|---|---|---|
| `cover` | Title slide | `kicker`, `team`, `members`, `meta`, `topics`, `background`, `qr`, `qrLabel` |
| `section` | Blue section divider | `kicker` |
| `default` | Title plus content | |
| `three-cards` | Three numbered cards | `cardColors`, `cardNumbers`, `::card1::` to `::card3::` |
| `two-cols-callout` | Content on the left, a takeaway on the right | `calloutKicker`, `::left::`, `::right::` |
| `figure` | Chart or image with a source line | `kicker`, `::figure::`, `::source::` |
| `figure-side` | Text on the left, figure on the right | `kicker`, `figureWidth`, `::figure::`, `::source::` |
| `image-left` / `image-right` | Half-slide image | `image`, `backgroundSize`, `kicker`, `::callout::` |
| `intro`, `statement`, `fact`, `alert`, `quote` | One big line | `kicker` (except `quote`) |
| `end` | Blue closing slide | `kicker`, `meta` |
| `code-palette` | Code with colour chips | `palette` |

Components: `<QrCode url label caption size />`. Put several in a `<div class="google-qr-row">`.

### Chinese text

Google Sans has no CJK glyphs, so the theme self-hosts subsets of Noto Sans TC and Noto Serif TC that contain only the characters the deck uses. After changing on-slide text, run `pnpm fonts` and commit the updated `theme/assets/fonts/`. If you forget, CI fails at `fonts:check` and lists the missing characters. Missing characters fall back to PingFang TC or Microsoft JhengHei, never to blank boxes.

## License

[MIT](LICENSE). See [`theme/assets/fonts/SOURCE.md`](theme/assets/fonts/SOURCE.md) for the font licences.
