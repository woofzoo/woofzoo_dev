"use client";

import { useAuth } from "@/context/AuthContext";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function PublicRoute({ children }: { children: React.ReactNode }) {
   const { user } = useAuth();
   const router = useRouter();
   
   useEffect(() => {
      if (user) router.replace(`/dashboard/${user.id}`);
   }, [user, router]);

   return <>{children}</>;
}

