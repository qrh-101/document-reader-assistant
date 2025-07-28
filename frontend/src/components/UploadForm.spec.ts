import { render, fireEvent } from '@testing-library/vue';
import UploadForm from './UploadForm.vue';

describe('UploadForm', () => {
  it('正常渲染', () => {
    const { getByText, getByRole } = render(UploadForm);
    expect(getByText(/点击或拖拽PDF文件到此处/)).toBeTruthy();
    expect(getByRole('button')).toBeTruthy();
  });

  it('选择文件后触发事件', async () => {
    const { container } = render(UploadForm);
    const fileInput = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = new File(['dummy'], 'test.pdf', { type: 'application/pdf' });
    await fireEvent.change(fileInput, { target: { files: [file] } });
    expect(fileInput.files?.[0].name).toBe('test.pdf');
  });

  it('输入问题并提交', async () => {
    const { getByRole, container } = render(UploadForm);
    const textarea = container.querySelector('textarea') as HTMLTextAreaElement;
    await fireEvent.update(textarea, '测试问题');
    const button = getByRole('button');
    expect(button).toBeTruthy();
  });
}); 