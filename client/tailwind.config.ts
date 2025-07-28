import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        // Custom color palette
        'orange-primary': '#ff6933',
        'teal-primary': '#21a0a0',
        'yellow-accent': '#FEB041',
        'red-accent': '#E63E01',
        
        // Semantic colors
        primary: {
          DEFAULT: '#ff6933',
          50: '#fff7f4',
          100: '#ffede6',
          200: '#ffd9cc',
          300: '#ffbfa3',
          400: '#ff9966',
          500: '#ff6933',
          600: '#e6501a',
          700: '#cc4717',
          800: '#b33d14',
          900: '#993311',
        },
        secondary: {
          DEFAULT: '#21a0a0',
          50: '#f0fafa',
          100: '#ccf2f2',
          200: '#99e6e6',
          300: '#66d9d9',
          400: '#33cccc',
          500: '#21a0a0',
          600: '#1a8080',
          700: '#146666',
          800: '#0d4d4d',
          900: '#073333',
        },
        accent: {
          DEFAULT: '#FEB041',
          50: '#fffbf0',
          100: '#fef3d9',
          200: '#fee7b3',
          300: '#fedb8c',
          400: '#fecf66',
          500: '#feb041',
          600: '#e59d3a',
          700: '#cc8a33',
          800: '#b3772c',
          900: '#996424',
        },
        danger: {
          DEFAULT: '#E63E01',
          50: '#fdf4f0',
          100: '#f9e1d9',
          200: '#f3c3b3',
          300: '#eda58c',
          400: '#e78766',
          500: '#e63e01',
          600: '#cf3801',
          700: '#b83201',
          800: '#a12c01',
          900: '#8a2601',
        },
      },
      backgroundColor: {
        'orange-primary': 'var(--color-orange-primary)',
        'teal-primary': 'var(--color-teal-primary)',
        'yellow-accent': 'var(--color-yellow-accent)',
        'red-accent': 'var(--color-red-accent)',
      },
      textColor: {
        'orange-primary': 'var(--color-orange-primary)',
        'teal-primary': 'var(--color-teal-primary)',
        'yellow-accent': 'var(--color-yellow-accent)',
        'red-accent': 'var(--color-red-accent)',
      },
      borderColor: {
        'orange-primary': 'var(--color-orange-primary)',
        'teal-primary': 'var(--color-teal-primary)',
        'yellow-accent': 'var(--color-yellow-accent)',
        'red-accent': 'var(--color-red-accent)',
      },
    },
  },
  plugins: [],
}

export default config