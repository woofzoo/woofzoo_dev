"use client";

import DashLayout from '@/components/layout/DashLayout'
import { getAllPets } from '@/lib/api/pets';
import React, { useEffect, useState } from 'react';

const page = () => {
   const [allPets, setAllPets] = useState([]);

   useEffect(() => {
      const fetchPets = async () => {
         try {
            const data = await getAllPets({ skip: 0, limit: 10 });
            console.log(data);
         } catch (error) {
            console.error("Failed to fetch pets:", error);
         }
      };

      fetchPets();
   }, []);

   return (
      <DashLayout>page</DashLayout>
   )
}

export default page