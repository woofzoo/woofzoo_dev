"use client";

import PrivateRoute from "@/components/outlets/PrivateRoute";

export default function PrivateLayout({ children }: { children: React.ReactNode }) {
   return <PrivateRoute>{children}</PrivateRoute>;
}
