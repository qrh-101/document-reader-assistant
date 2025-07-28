import { render, fireEvent, waitFor } from '@testing-library/vue';
import HomePage from '@/pages/HomePage.vue';
import ReportPage from '@/pages/ReportPage.vue';
import { createRouter, createWebHistory } from 'vue-router';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ref } from 'vue';

// mock useReportStore，只保证主流程，metadata 可为空对象
vi.mock('@/stores/reportStore', () => {
  return {
    useReportStore: () => ({
      createReport: vi.fn().mockResolvedValue({ report_id: 'test-id' }),
      fetchReportDetail: vi.fn().mockResolvedValue({
        id: 'test-id',
        title: '测试报告',
        content: '# 测试报告\n\n内容',
        metadata: {},
        created_at: '',
        updated_at: ''
      }),
      currentReport: {
        value: {
          id: 'test-id',
          title: '测试报告',
          content: '# 测试报告\n\n内容',
          metadata: {},
          created_at: '',
          updated_at: ''
        }
      }
    }),
  };
});

const pushMock = vi.fn();
// Mock vue-router's useRoute and useRouter
vi.mock('vue-router', async (importOriginal) => {
  const actual = await importOriginal();
  return {
    ...actual,
    useRoute: () => ({
      params: { id: 'test-id' },
      name: 'report'
    }),
    useRouter: () => ({
      push: pushMock
    })
  };
});

// Mock API
vi.mock('@/api/research', () => ({
  generateReport: vi.fn().mockResolvedValue({
    data: {
      report_id: 'test-id',
      markdown_report: '# 测试报告\n\n内容',
      report_metadata: { total_chunks: 1, processed_chunks: 1, token_per_chunk: 500 }
    }
  }),
  getReportDetail: vi.fn().mockResolvedValue({
    data: {
      report_id: 'test-id',
      markdown_report: '# 测试报告\n\n内容',
      report_metadata: { total_chunks: 1, processed_chunks: 1, token_per_chunk: 500 }
    }
  })
}));

// Minimal router setup for integration tests
const routes = [
  { path: '/', component: HomePage },
  { path: '/report/:id', component: ReportPage }
];

describe('App 集成流程', () => {
  let router: ReturnType<typeof createRouter>;

  beforeEach(() => {
    router = createRouter({
      history: createWebHistory(),
      routes,
    });
    pushMock.mockClear();
  });

  it('用户上传PDF、输入问题并查看报告', async () => {
    const { getByText, getAllByRole, container } = render(HomePage, {
      global: { plugins: [router] }
    });

    // 模拟选择文件
    const fileInput = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(['dummy'], 'test.pdf', { type: 'application/pdf' });
    await fireEvent.change(fileInput, { target: { files: [file] } });
    expect(fileInput.files?.[0].name).toBe('test.pdf');

    // 输入问题
    const textarea = container.querySelector('textarea') as HTMLTextAreaElement;
    await fireEvent.update(textarea, '集成测试问题');

    // 提交表单，查找“开始生成报告”按钮
    const buttons = getAllByRole('button');
    const submitBtn = buttons.find(btn => btn.textContent?.includes('开始生成报告'));
    await fireEvent.click(submitBtn!);

    // 等待API响应并跳转到报告页面
    await waitFor(() => {
      expect(pushMock).toHaveBeenCalledWith(expect.stringContaining('/report/test-id'));
    });

    // 渲染报告页面并断言主内容
    const { container: reportContainer } = render(ReportPage, {
      global: { plugins: [router], mocks: { $route: { params: { id: 'test-id' } } } }
    });
    await waitFor(() => {
      expect(reportContainer.innerHTML).toContain('测试报告');
      expect(reportContainer.innerHTML).toContain('内容');
    });
  });
}); 