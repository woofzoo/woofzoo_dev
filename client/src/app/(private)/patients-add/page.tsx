"use client";

import DashLayout from '@/components/layout/DashLayout';
import { useRouter } from "next/navigation";

const page = () => {
   const router = useRouter();
   const handleBack = () => {
      if (window.history.length > 1) {
         router.back();
      } else {
         router.push("/owners");
      }
   };
   return (
      <DashLayout>page</DashLayout>
   )
}

export default page