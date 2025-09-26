"use client"

import { X } from "lucide-react"
import React from "react"

interface ModalProps {
   title: string
   children: React.ReactNode
   onClose: () => void
}

const Modal: React.FC<ModalProps> = ({ title, children, onClose }) => {
   return (
      <div className="fixed inset-0 z-50 flex items-center justify-center transition-opacity duration-300">
         <div
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
            onClick={onClose}
         />

         <div className="relative w-full max-w-md bg-background-secondary rounded-xl shadow-xl border border-border-primary p-6 z-10 m-4">
            <div className="flex justify-between items-center mb-6">
               <h2 className="text-xl font-semibold text-text-primary">{title}</h2>
               <button
                  onClick={onClose}
                  className="p-1 rounded-full text-text-muted hover:bg-background-muted hover:text-text-primary transition-colors"
               >
                  <X size={16} />
               </button>
            </div>
            {children}
         </div>
      </div>
   )
}

export default Modal
