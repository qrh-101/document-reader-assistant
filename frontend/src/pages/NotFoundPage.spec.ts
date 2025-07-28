import { render } from '@testing-library/vue';
import NotFoundPage from './NotFoundPage.vue';

describe('NotFoundPage', () => {
  it('显示404提示', () => {
    const { getByText } = render(NotFoundPage);
    expect(getByText(/404/)).toBeTruthy();
  });
}); 