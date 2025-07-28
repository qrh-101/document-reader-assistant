import { describe, it, expect, vi } from 'vitest';

vi.mock('axios', () => {
  return {
    default: {
      create: () => ({
        interceptors: { request: { use: vi.fn() }, response: { use: vi.fn() } },
        get: vi.fn().mockResolvedValue({ data: { code: 200, data: 'ok' } }),
        post: vi.fn().mockResolvedValue({ data: { code: 200, data: 'ok' } }),
      }),
    },
  };
});

import request from './request';

describe('request 工具', () => {
  it('封装的 get 方法可用', async () => {
    const res = await request.get('/test');
    expect(res.data.code).toBe(200);
  });

  it('封装的 post 方法可用', async () => {
    const res = await request.post('/test', { foo: 'bar' });
    expect(res.data.code).toBe(200);
  });
}); 