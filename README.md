# Run Our House — Marketing Website

Static marketing site for [Run Our House](https://runourhouse.com), an AI family assistant service for busy parents in Reno, NV.

## Quick Start

```bash
# Install Wrangler (Cloudflare CLI)
npm install

# Local development
npm run dev
# → Opens at http://localhost:8788

# Deploy to Cloudflare Workers
npm run deploy
```

## Project Structure

```
public/
├── index.html           # Homepage — hero, conversation showcases, CTAs
├── how-it-works.html    # Process steps, integrations, timeline
├── pricing.html         # 3 tiers, comparison table, FAQ
├── about.html           # Trust, data handling, bio, testimonial
├── 404.html             # Custom error page
├── style.css            # Single stylesheet (mobile-first)
├── favicon.svg          # Brand icon
├── robots.txt           # Search engine directives
├── sitemap.xml          # Page listing for crawlers
└── images/
    └── og-image.svg     # Social media sharing image
wrangler.toml            # Cloudflare Workers config
package.json             # Wrangler dev dependency
```

## Custom Domain

The site is deployed to Cloudflare Workers. Custom domain (`runourhouse.com`) is configured in the Cloudflare dashboard. `runourhouse.ai` redirects to `runourhouse.com` via Cloudflare redirect rule.

## Updating Content

All content is in static HTML files — edit directly:

- **Pricing**: Edit `public/pricing.html` (pricing cards section)
- **Conversations**: Edit chat bubble HTML in `index.html` and `how-it-works.html`
- **FAQ**: Edit `<details>` elements in `public/pricing.html`
- **Testimonials**: Edit `public/about.html` (testimonial section)
- **Waitlist form**: Update the Formspree form ID in footer forms across all pages

After editing, deploy with `npm run deploy`.

## External Services

- **Formspree**: Waitlist email collection (footer forms on all pages)
- **Calendly**: Discovery call booking (all CTA buttons)
- **Cloudflare**: DNS, hosting, redirect rules

## Brand

- **Colors**: Warm teal (`#2A9D8F`), coral accent (`#E76F51`), cream background (`#FEFAF6`)
- **Fonts**: [Inter](https://fonts.google.com/specimen/Inter) (body), [Nunito](https://fonts.google.com/specimen/Nunito) (headings)
- **Logo**: CSS text wordmark (no image asset)

Built by [Sierra Code Co](https://sierracodeco.com).
