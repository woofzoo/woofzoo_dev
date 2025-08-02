import { useState } from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
   label?: string;
   buttonType: string;
}

export default function Input({ buttonType, label, ...props }: InputProps) {
   const [showPassword, setShowPassword] = useState(false);
   const isPassword = buttonType === "password";
   const inputType = isPassword ? (showPassword ? "text" : "password") : buttonType;
   return (
      <div className="flex flex-col gap-1">
         {label && <label className="text-sm font-medium text-gray-700">{label}</label>}
         <div className="relative">
            <input
               type={inputType}
               className="w-full border px-4 py-2 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-pastel"
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