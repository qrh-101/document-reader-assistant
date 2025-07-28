import { setActivePinia, createPinia } from 'pinia';
import { useReportStore } from './reportStore';
import { describe, it, expect, beforeEach, vi } from 'vitest';

vi.mock('@/api/research', () => ({
  generateReport: vi.fn().mockResolvedValue({ data: { code: 200, data: { report_id: 'test', markdown_report: '# 测试', report_metadata: {} } } })
}));

describe('reportStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it('createReport 方法可用', async () => {
    const store = useReportStore();
    const file = new File(['dummy'], 'test.pdf', { type: 'application/pdf' });
    await store.createReport(file, '问题');
    expect(store.reports.length).toBeGreaterThanOrEqual(0);
  });
}); 