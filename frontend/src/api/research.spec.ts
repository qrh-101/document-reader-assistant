import { describe, it, expect, vi } from 'vitest';
import * as api from './research';

vi.mock('@/utils/request', () => ({
  __esModule: true,
  default: {
    post: vi.fn().mockResolvedValue({ data: { report_id: 'test', markdown_report: '# 测试', report_metadata: {} } }),
    get: vi.fn().mockResolvedValue({ data: { report_id: 'test', markdown_report: '# 测试', report_metadata: {} } }),
  },
  upload: vi.fn().mockResolvedValue({ data: { report_id: 'test', markdown_report: '# 测试', report_metadata: {} } }),
}));

describe('research API', () => {
  it('generateReport 返回报告数据', async () => {
    const file = new File(['dummy'], 'test.pdf', { type: 'application/pdf' });
    const res = await api.generateReport(file, '问题');
    expect(res.data.report_id).toBe('test');
  });
}); 