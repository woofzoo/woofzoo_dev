/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: 'var(--primary-color)',
        secondary: 'var(--secondary-color)',
        accent: 'var(--accent-color)',
        'text-primary': 'var(--text-primary)',
        'bg-light': 'var(--background-light)',
      },
      // You can also extend other properties
      spacing: {
        'custom': 'var(--custom-spacing)',
      },
      fontSize: {
        'dynamic': 'var(--dynamic-font-size)',
      }
    },
  },
  plugins: [],
}