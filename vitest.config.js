import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: {
    environment: 'happy-dom',
    include: ['ui/__tests__/**/*.test.js'],
    globals: false,
  },
});
