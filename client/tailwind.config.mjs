/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Brand Colors
        'primary': 'var(--primary-color)',
        'secondary': 'var(--secondary-color)',
        'accent': 'var(--accent-color)',
        'danger': 'var(--danger-color)',

        // Pastel Versions
        'primary-pastel': 'var(--primary-color-pastel)',
        'secondary-pastel': 'var(--secondary-color-pastel)',
        'accent-pastel': 'var(--accent-color-pastel)',
        'danger-pastel': 'var(--danger-color-pastel)',

        // Text Colors
        'text-primary': 'var(--text-primary)',
        'text-secondary': 'var(--text-secondary)',
        'text-muted': 'var(--text-muted)',
        'text-inverse': 'var(--text-inverse)',

        // Background Colors
        'background-primary': 'var(--background-primary)',
        'background-secondary': 'var(--background-secondary)',
        'background-muted': 'var(--background-muted)',

        // Border Colors
        'border-primary': 'var(--border-primary)',
        'border-secondary': 'var(--border-secondary)',
        'border-focus': 'var(--border-focus)',

        // Status Colors
        'success': 'var(--success-color)',
        'warning': 'var(--warning-color)',
        'error': 'var(--error-color)',
        'info': 'var(--info-color)',
      },
      borderRadius: {
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
        xl: 'var(--radius-xl)',
        '2xl': 'var(--radius-2xl)',
      },
      boxShadow: {
        sm: 'var(--shadow-sm)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
        xl: 'var(--shadow-xl)',
        teal: 'var(--shadow-teal)',
        red: 'var(--shadow-red)',
      },
    },
  },
  plugins: [],
};
