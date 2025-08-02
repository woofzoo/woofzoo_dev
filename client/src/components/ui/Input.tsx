import { useState } from "react";
import { cva, type VariantProps } from "class-variance-authority";

const inputVariants = cva(
   "w-full border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-pastel",
   {
      variants: {
         size: {
            sm: "px-2 py-1 text-sm",
            md: "px-4 py-2 text-base",
            lg: "px-6 py-3 text-lg",
         },
      },
      defaultVariants: {
         size: "md",
      },
   }
);

interface InputProps
   extends Omit<React.InputHTMLAttributes<HTMLInputElement>, "size">,
   VariantProps<typeof inputVariants> {
   label?: string;
   buttonType: string;
   size?: "sm" | "md" | "lg";
}

export default function Input({ buttonType, label, size, ...props }: InputProps) {
   const [showPassword, setShowPassword] = useState(false);
   const isPassword = buttonType === "password";
   const inputType = isPassword ? (showPassword ? "text" : "password") : buttonType;

   return (
      <div className="flex flex-col gap-1">
         {label && <label className="text-sm font-medium text-gray-700">{label}</label>}
         <div className="relative">
            <input
               type={inputType}
               className={inputVariants({ size })}
               {...props}
            />
            {isPassword && (
               <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-sm text-gray-500"
               >
                  {showPassword ? "Hide" : "Show"}
               </button>
            )}
         </div>
      </div>
   );
}
