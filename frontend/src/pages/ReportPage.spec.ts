import { render } from '@testing-library/vue';
import ReportPage from './ReportPage.vue';
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

describe('ReportPage', () => {
  it('正常渲染', () => {
    const { container } = render(ReportPage);
    expect(container.innerHTML).toContain('报告');
  });
}); 