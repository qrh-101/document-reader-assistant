import { render } from '@testing-library/vue';
import HomePage from './HomePage.vue';

describe('HomePage', () => {
  it('正常渲染', () => {
    const { getByText } = render(HomePage);
    expect(getByText(/上传PDF/i)).toBeTruthy();
  });
}); 