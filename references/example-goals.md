# Example Goals — Complete Example Set

## Example 1: Feature Development

**User input (vague):**
> "Add a shopping cart feature to my e-commerce site"

**Structured output:**
```xml
<task>
Implement a shopping cart feature for the e-commerce website.
Allow users to add products, update quantities, remove items,
and proceed to checkout. Cart state must persist across page refreshes
and across browser sessions (logged-in users).
</task>

<context>
## Project Background
The project is a Next.js e-commerce site using TypeScript and Tailwind CSS.
It currently has product listing and detail pages, but no cart or checkout flow.
Database: PostgreSQL with Prisma ORM. Auth: NextAuth.js.

## Related Code
- `src/app/products/` — product listing and detail pages
- `src/lib/db.ts` — Prisma client instance
- `src/types/` — TypeScript type definitions
- `prisma/schema.prisma` — database schema (currently no Cart model)

## History
- Initial product catalog implemented 2 weeks ago
- User expressed need for cart in last sprint planning

## Known Constraints
- Tech stack: Next.js 14, TypeScript, Prisma, PostgreSQL
- Must work for both guest users (localStorage) and logged-in users (database)
- Mobile-responsive (Tailwind CSS already in use)

## Related References
- Shopify cart API design (for reference)
- Next.js App Router patterns for server/client components
</context>

<constraints>
## Must Do
- Cart must persist across page refreshes (guest: localStorage; logged-in: database)
- Add-to-cart button on all product detail pages
- Cart icon in header with item count badge
- Cart page with quantity update and remove functionality
- "Proceed to checkout" button (links to future checkout page)

## Must NOT Do
- Do not implement checkout/payment (separate task)
- Do not require user registration just to add items to cart (guest cart)
- Do not use external cart services; keep it self-contained

## Technical Constraints
- Use existing Prisma schema; add Cart and CartItem models
- API routes must follow Next.js 14 App Router conventions
- State management: React context for client-side cart state

## Resource Constraints
- Should be completable within 1-2 days of focused work
- Prefer simple implementation over over-engineering
</constraints>

<output>
## Definition of Done
- [ ] Guest user can add items to cart, refresh page, cart still has items
- [ ] Logged-in user's cart persists in database; accessible from any device
- [ ] Cart page displays correct items, quantities, and subtotal
- [ ] User can update quantity (1-99) and remove items
- [ ] Cart icon badge shows correct item count
- [ ] "Proceed to checkout" button navigates to /checkout (placeholder OK)

## Verification Method
- Manual test: add item as guest → refresh → verify cart
- Manual test: sign up → add item → sign out → sign in → verify cart persists
- Unit test: cart API routes (GET/POST/PUT/DELETE /api/cart)
- Visual check: cart page matches design intent (Tailwind CSS)

## Termination Condition
- All above acceptance criteria met, OR
- Execution exceeds 15 rounds without completion, OR
- Blocker encountered (e.g., Prisma schema migration fails repeatedly)
</output>
```

---

## Example 2: Optimization Task

**User input (vague):**
> "Optimize the API response time"

**Structured output:**
```xml
<task>
Optimize the REST API's average response time for the product listing endpoint.
Current baseline: ~800ms for 100 products.
Target: reduce to <200ms for same payload.
Focus on database query optimization and response caching.
</task>

<context>
## Project Background
Node.js REST API with Express. Database: MongoDB with Mongoose ODM.
The `/api/products` endpoint serves product listings with pagination.
Currently fetches all fields, including large `description` and `reviews` sub-documents.

## Related Code
- `src/routes/products.js` — product routes
- `src/models/Product.js` — Mongoose schema (has `description`, `reviews`, `category` sub-doc)
- `src/controllers/productController.js` — controller with pagination logic
- `src/middleware/cache.js` — existing Redis cache middleware (not used for products)

## History
- Product schema has grown over time; originally only had `name`, `price`, `image`
- Reviews were embedded (should be separate collection or referenced)
- No indexing on `category` or `price` fields currently

## Known Constraints
- MongoDB Atlas (M0 free tier) — limited performance
- Cannot change client contract (response shape must stay the same)
- Redis available for caching

## Related References
- MongoDB indexing best practices
- Mongoose `select()` for field projection
- Redis cache patterns for REST APIs
</context>

<constraints>
## Must Do
- Reduce `/api/products?page=1&limit=100` response time to <200ms
- Maintain same JSON response shape (backward compatible)
- Add appropriate MongoDB indexes
- Implement Redis caching for product listings (TTL: 5 min)

## Must NOT Do
- Do not change the response JSON structure (breaking change for clients)
- Do not paginate differently (keep `page` and `limit` params)
- Do not upgrade MongoDB tier (optimization task, not infrastructure task)

## Technical Constraints
- Mongoose ODM (not raw MongoDB driver)
- Redis for caching (already set up in `src/middleware/cache.js`)
- Node.js 18+

## Resource Constraints
- Test on local environment first; do not run benchmarks on production
- Prefer changes that don't require data migration
</constraints>

<output>
## Definition of Done
- [ ] `GET /api/products?page=1&limit=100` responds in <200ms (local, warm cache)
- [ ] MongoDB indexes created on `category`, `price`, and query filter fields
- [ ] Product queries use field projection (exclude `description`, `reviews` from listing)
- [ ] Redis cache middleware applied to product listing route (TTL configurable)
- [ ] Cache invalidation on product create/update/delete
- [ ] Provide before/after benchmark report

## Verification Method
- Run: `ab -n 100 -c 10 http://localhost:3000/api/products?page=1&limit=100`
- Check MongoDB indexes: `db.products.getIndexes()`
- Verify cache: check Redis for `cache:products:page:1:limit:100` key after first request
- Code review: ensure field projection is applied in Mongoose query

## Termination Condition
- All above acceptance criteria met, OR
- Execution exceeds 20 rounds without completion, OR
- Optimization yields <20% improvement (may need different approach)
</output>
```

---

## Example 3: Content Creation / Research

**User input (vague):**
> "Help me write a technical blog post about API security"

**Structured output:**
```xml
<task>
Write a technical blog post about API security best practices for developers.
Target audience: junior to mid-level backend developers.
Topic focus: the top 5 most common API security mistakes and how to fix them.
Output: a complete draft (1500-2000 words) ready for review and publishing.
</task>

<context>
## Project Background
The user maintains a developer blog focused on backend engineering topics.
Previous posts covered REST API design, database optimization, and testing strategies.
The blog uses Markdown and is hosted on a static site generator (e.g., Astro or Hugo).

## Audience
- Junior to mid-level backend developers
- Familiar with REST basics but may not know security best practices
- Prefer practical examples over theoretical explanations

## Related References
- OWASP API Security Top 10 (2023)
- Previous blog post: "REST API Design Best Practices" (for tone/style reference)
- Common vulnerabilities: broken auth, excessive data exposure, lack of rate limiting
</context>

<constraints>
## Must Do
- Cover exactly 5 security mistakes (practical, common ones)
- Each mistake: explanation + code example (vulnerable vs. fixed)
- Include actionable checklist at the end
- Use the same tone/style as previous blog posts

## Must NOT Do
- Do not cover theoretical cryptography (too advanced for target audience)
- Do not make it a listicle without depth (each item needs substance)
- Do not skip code examples (developers need to see real code)

## Content Constraints
- Length: 1500-2000 words
- Language: clear, conversational, no jargon without explanation
- Code examples: prefer Node.js/Express (matches audience's likely stack)

## Resource Constraints
- Draft due for review within 1 day
- Research should use freely available OWASP/docs (no paywalled sources)
</constraints>

<output>
## Definition of Done
- [ ] Draft covers exactly 5 API security mistakes
- [ ] Each mistake has: plain-English explanation + vulnerable code example + fixed code example
- [ ] Includes an actionable checklist (10-15 items) at the end
- [ ] Word count: 1500-2000 words
- [ ] Tone matches previous posts (conversational, developer-to-developer)
- [ ] Markdown format, ready to copy into blog CMS

## Verification Method
- Read through: is each mistake clearly explained with code?
- Word count check (any Markdown word counter)
- Checklist: can a junior developer follow it?
- Style check: compare with previous published post

## Termination Condition
- All above acceptance criteria met, OR
- Execution exceeds 10 rounds without completion, OR
- User provides feedback requiring major restructuring (handle as new task)
</output>
```
