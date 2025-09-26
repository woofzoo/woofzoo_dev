"use client";

import PublicRoute from "@/components/outlets/PublicRoute";

export default function PublicLayout({ children }: { children: React.ReactNode }) {
  return <PublicRoute>{children}</PublicRoute>;
}
