---
description: "Add a new React UI component to the agent-ui frontend. Use when asked to create a new component, page, or UI feature."
---

# New UI Component

Create a new component for the agent-ui frontend.

## Steps

1. **Create the component file** at the appropriate location:
   - Domain components: `agent-ui/src/components/chat/{{ComponentName}}/{{ComponentName}}.tsx`
   - UI primitives: `agent-ui/src/components/ui/{{component-name}}.tsx`

2. **Use the standard patterns**:
   ```tsx
   'use client'
   import { cn } from '@/lib/utils'

   interface {{ComponentName}}Props {
     className?: string
   }

   export function {{ComponentName}}({ className }: {{ComponentName}}Props) {
     return <div className={cn('', className)}></div>
   }
   ```

3. **Add barrel export** — create or update the `index.ts` in the component folder:
   ```ts
   export { {{ComponentName}} } from './{{ComponentName}}'
   ```

4. **Validate**: `cd agent-ui && pnpm run validate`
