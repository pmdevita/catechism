const defaultTheme = require('tailwindcss/defaultTheme');

module.exports = {
  mode: 'jit',
  purge: [
    './src/**/*.html',
    './src/**/*.js',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    fontFamily: {
      sans: ["Roboto", "Arial", "Helvetica Neue", "Helvetica", ...defaultTheme.fontFamily.sans],
      display: ["Merriweather", "Times New Roman", "Times", ...defaultTheme.fontFamily.sans]
    },
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
