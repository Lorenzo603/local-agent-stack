---
applyTo: "agent-ui/**/*.{ts,tsx}"
description: "TypeScript/React frontend conventions for the agent-ui Next.js app. Use when editing frontend files."
---

# Frontend Conventions (agent-ui)

- Next.js 15 with App Router. Client components require `'use client'` directive.
- React 18. Package manager is pnpm.
- Styling: Tailwind CSS. Use `cn()` from `lib/utils.ts` for class merging.
- State management: Zustand (see `src/store.ts`).
- UI primitives live in `src/components/ui/`. Domain components in `src/components/chat/`.
- Each component folder has a barrel `index.ts` for exports.
- Validation: run `pnpm run validate` from `agent-ui/` (lint + format + typecheck).
- Formatting: Prettier with `prettier-plugin-tailwindcss`.
