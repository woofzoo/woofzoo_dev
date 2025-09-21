import React, { useState, useRef, useEffect } from 'react';

interface Option {
   value: string;
   label: string;
}

interface CustomDropdownProps {
   label: string;
   name: string;
   value: string;
   onChange: (name: string, value: string) => void;
   options: Option[];
   placeholder?: string;
   className?: string;
   required?: boolean;
}

const CustomDropdown: React.FC<CustomDropdownProps> = ({
   label,
   name,
   value,
   onChange,
   options,
   placeholder = "Select an option",
   className = "",
   required = false
}) => {
   const [isOpen, setIsOpen] = useState(false);
   const [searchTerm, setSearchTerm] = useState('');
   const dropdownRef = useRef<HTMLDivElement>(null);

   // Filter options based on search term
   const filteredOptions = options.filter(option =>
      option.label.toLowerCase().includes(searchTerm.toLowerCase())
   );

   // Handle click outside to close dropdown
   useEffect(() => {
      const handleClickOutside = (event: MouseEvent) => {
         if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
            setIsOpen(false);
            setSearchTerm('');
         }
      };

      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
   }, []);

   const handleSelect = (option: Option) => {
      onChange(name, option.value);
      setIsOpen(false);
      setSearchTerm('');
   };

   const handleToggle = () => {
      setIsOpen(!isOpen);
      setSearchTerm('');
   };

   const selectedOption = options.find(option => option.value === value);

   return (
      <div className="relative" ref={dropdownRef}>
         {/* Label */}
         <label className="block text-base font-medium text-text-primary mb-2">
            {label} {required && <span className="text-danger">*</span>}
         </label>

         {/* Dropdown Button */}
         <button
            type="button"
            onClick={handleToggle}
            className={`w-full border border-border-primary rounded-xl px-4 py-3 text-left focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-primary-pastel transition-all bg-background-primary hover:bg-background-secondary ${className}`}
         >
            <div className="flex items-center justify-between">
               <span className={selectedOption ? 'text-text-primary' : 'text-text-secondary'}>
                  {selectedOption ? selectedOption.label : placeholder}
               </span>
               <svg
                  className={`w-5 h-5 text-text-secondary transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
               >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
               </svg>
            </div>
         </button>

         {/* Dropdown Menu */}
         {isOpen && (
            <div className="absolute z-50 w-full mt-2 bg-background-primary border border-border-primary rounded-xl shadow-2xl max-h-60 overflow-hidden">
               {/* Search Input (for options with many items) */}
               {options.length > 5 && (
                  <div className="p-3 border-b border-border-primary">
                     <input
                        type="text"
                        placeholder="Search..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full px-3 py-2 text-sm border border-border-primary rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-pastel focus:border-primary-pastel"
                        onClick={(e) => e.stopPropagation()}
                     />
                  </div>
               )}

               {/* Options List */}
               <div className="max-h-48 overflow-y-auto">
                  {filteredOptions.length > 0 ? (
                     filteredOptions.map((option) => (
                        <button
                           key={option.value}
                           type="button"
                           onClick={() => handleSelect(option)}
                           className={`w-full px-4 py-3 text-left hover:bg-background-secondary transition-colors focus:outline-none focus:bg-background-secondary ${value === option.value
                                 ? 'bg-primary-pastel/20 text-primary border-r-4 border-primary font-medium'
                                 : 'text-text-primary'
                              }`}
                        >
                           <div className="flex items-center justify-between">
                              <span>{option.label}</span>
                              {value === option.value && (
                                 <svg className="w-4 h-4 text-primary" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                 </svg>
                              )}
                           </div>
                        </button>
                     ))
                  ) : (
                     <div className="px-4 py-3 text-text-secondary text-sm">
                        No options found
                     </div>
                  )}
               </div>
            </div>
         )}
      </div>
   );
};

export default CustomDropdown;