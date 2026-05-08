import { defineConfig } from 'vite';

export default defineConfig(({ mode }) => {
  const isProduction = mode === 'production';
  
  return {
    plugins: [
      require('@vitejs/plugin-react')(),
      require('@tailwindcss/vite')()
    ],
    define: {
      'import.meta.env.VITE_API_BASE_URL': JSON.stringify(
        isProduction ? 'https://naija-oracle.onrender.com/api/v1' : 'http://localhost:8000/api/v1'
      )
    },
    server: {
      port: 3000,
      host: '0.0.0.0'
    }
  };
});
