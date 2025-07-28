import { render } from '@testing-library/vue';
import ReportViewer from './ReportViewer.vue';
import { vi } from 'vitest';

vi.mock('vue-router', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    useRoute: () => ({
      params: { id: 'test-id' },
      name: 'report'
    }),
    useRouter: () => ({})
  };
});

describe('ReportViewer', () => {
  it('正常渲染', () => {
    const { getByTestId } = render(ReportViewer, {
      props: { content: '# 标题' }
    });
    expect(getByTestId('report-viewer')).toBeTruthy();
  });

  it('渲染markdown内容', () => {
    const { container } = render(ReportViewer, {
      props: { content: '# 测试报告' }
    });
    expect(container.innerHTML).toContain('测试报告');
  });
}); 