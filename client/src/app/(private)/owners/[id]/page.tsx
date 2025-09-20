"use client";

import DashLayout from "@/components/layout/DashLayout";
import { ChevronLeft } from "lucide-react";
import React from "react";
import { useRouter } from "next/navigation";

const Page = () => {
   const router = useRouter();

   const handleBack = () => {
      if (window.history.length > 1) {
         router.back();
      } else {
         router.push("/owners");
      }
   };

   return (
      <DashLayout>
         <button
            onClick={handleBack}
            className="flex items-center gap-2 text-gray-700 hover:text-gray-900"
         >
            <ChevronLeft size={24} />
            <span>Back</span>
         </button>
      </DashLayout>
   );
};

export default Page;
