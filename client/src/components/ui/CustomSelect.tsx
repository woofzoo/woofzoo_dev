import React, { useState, useRef, useEffect } from 'react';

type Option = {
   value: string;
   label: string;
};

type SelectProps = {
   label: string;
   name: string;
   value: string;
   options: Option[];
   onChange: (event: { target: { name: string; value: string } }) => void;
   placeholder?: string;
   className?: string;
};

export const CustomSelect: React.FC<SelectProps> = ({
   label,
   name,
   value,
   options,
   onChange,
   placeholder = 'Select an option',
   className = ''
}) => {
   const [isOpen, setIsOpen] = useState(false);
   const selectRef = useRef<HTMLDivElement>(null);

   const selectedLabel = options.find(option => option.value === value)?.label || placeholder;

   useEffect(() => {
      const handleClickOutside = (event: MouseEvent) => {
         if (selectRef.current && !selectRef.current.contains(event.target as Node)) {
            setIsOpen(false);
         }
      };

      document.addEventListener('mousedown', handleClickOutside);
      return () => {
         document.removeEventListener('mousedown', handleClickOutside);
      };
   }, []);

   const handleSelect = (optionValue: string) => {
      onChange({ target: { name, value: optionValue } });
      setIsOpen(false);
   };

   return (
      <div className="relative w-full font-sans" ref={selectRef}>
         <label className="block text-sm font-medium text-text-primary mb-1">{label}</label>
         <div className="relative">
            <button
               type="button"
               onClick={() => setIsOpen(!isOpen)}
               className={`
            w-full bg-background-primary border border-border-primary rounded-xl px-4 py-3 text-left
            focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-border-focus
            transition-all flex items-center justify-between
            ${className}
          `}
               aria-haspopup="listbox"
               aria-expanded={isOpen}
            >
               <span className={value ? 'text-text-primary' : 'text-text-muted'}>{selectedLabel}</span>
               <svg
                  className={`w-5 h-5 text-text-secondary transform transition-transform duration-200 ${isOpen ? '-rotate-180' : 'rotate-0'
                     }`}
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
               >
                  <path
                     fillRule="evenodd"
                     d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                     clipRule="evenodd"
                  />
               </svg>
            </button>

            {isOpen && (
               <ul
                  className="
              absolute z-10 w-full mt-1 bg-background-primary border border-border-secondary rounded-xl
              shadow-lg max-h-60 overflow-y-auto
            "
                  role="listbox"
               >
                  {options.map((option) => (
                     <li
                        key={option.value}
                        onClick={() => handleSelect(option.value)}
                        className={`
                  px-4 py-3 text-text-secondary cursor-pointer hover:bg-background-secondary
                  transition-colors duration-150
                  ${value === option.value ? 'bg-primary-pastel text-primary font-semibold' : ''}
                `}
                        role="option"
                        aria-selected={value === option.value}
                     >
                        {option.label}
                     </li>
                  ))}
               </ul>
            )}
         </div>
      </div>
   );
};
