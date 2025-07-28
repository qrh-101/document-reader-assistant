import { render } from '@testing-library/vue';
import ProgressBar from './ProgressBar.vue';

describe('ProgressBar', () => {
  const baseProps = { progress: 50, message: '测试', status: 'waiting' };

  it('正常渲染', () => {
    const { getByText } = render(ProgressBar, { props: baseProps });
    expect(getByText('50%')).toBeTruthy();
  });

  it('显示正确的进度', () => {
    const { getByText } = render(ProgressBar, { props: { ...baseProps, progress: 75 } });
    expect(getByText('75%')).toBeTruthy();
  });

  it('进度为0时显示0%', () => {
    const { getByText } = render(ProgressBar, { props: { ...baseProps, progress: 0 } });
    expect(getByText('0%')).toBeTruthy();
  });
}); 