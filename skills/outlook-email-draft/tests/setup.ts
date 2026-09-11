import { vi } from 'vitest';

vi.stubGlobal('fetch', vi.fn(() => {
  throw new Error('Live network access is disabled in tests. Inject a mock transport.');
}));