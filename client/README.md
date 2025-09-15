This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.


<!-- my-nextjs-app/
├── .env.local
├── .env.example
├── next.config.js
├── middleware.ts
├── package.json
├── tsconfig.json
│
├── public/
│   ├── images/
│   └── icons/
│
└── src/
    ├── app/                     # App Router
    │   ├── globals.css
    │   ├── layout.tsx
    │   ├── page.tsx
    │   ├── loading.tsx
    │   ├── error.tsx
    │   │
    │   ├── (auth)/              # Route groups
    │   │   ├── login/page.tsx
    │   │   └── register/page.tsx
    │   │
    │   ├── dashboard/
    │   │   ├── layout.tsx
    │   │   ├── page.tsx
    │   │   └── [id]/page.tsx
    │   │
    │   └── api/                 # API routes
    │       ├── auth/route.ts
    │       └── users/route.ts
    │
    ├── components/              # UI components
    │   ├── ui/                  # Basic components
    │   ├── forms/
    │   └── layout/
    │
    ├── lib/                     # Utilities & config
    │   ├── auth.ts
    │   ├── db.ts
    │   ├── utils.ts
    │   └── validations.ts
    │
    ├── hooks/                   # Custom hooks
    │   └── use-auth.ts
    │
    ├── store/                   # State management
    │   └── auth-store.ts
    │
    └── types/                   # TypeScript types
        ├── auth.ts
        └── global.d.ts -->

my-nextjs-app/
├── .env.local
├── .env.example
├── next.config.js
├── middleware.ts            # (optional) server-side route protection
├── package.json
├── tsconfig.json
│
├── public/
│   ├── images/
│   └── icons/
│
└── src/
    ├── app/
    │   ├── globals.css
    │   ├── layout.tsx
    │   ├── loading.tsx
    │   ├── error.tsx
    │   │
    │   ├── (public)/             # 👈 Public-only routes
    │   │   ├── layout.tsx        # wraps children with <PublicRoute>
    │   │   ├── login/page.tsx
    │   │   └── register/page.tsx
    │   │
    │   ├── (private)/            # 👈 Authenticated-only routes
    │   │   ├── layout.tsx        # wraps children with <PrivateRoute>
    │   │   └── dashboard/
    │   │       ├── layout.tsx
    │   │       ├── page.tsx
    │   │       └── [id]/page.tsx
    │   │
    │   └── api/                  # API routes (unaffected)
    │       ├── auth/route.ts
    │       └── users/route.ts
    │
    ├── components/
    │   ├── ui/
    │   ├── forms/
    │   └── layout/
    │
    ├── lib/
    │   ├── auth.ts               # token helpers, getUserFromToken
    │   ├── db.ts
    │   ├── utils.ts
    │   └── validations.ts
    │
    ├── hooks/
    │   └── use-auth.ts           # useAuth hook
    │
    ├── store/
    │   └── auth-store.ts         # Zustand or Redux auth store
    │
    └── types/
        ├── auth.ts
        └── global.d.ts
