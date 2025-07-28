import { render } from '@testing-library/vue';
import Header from './Header.vue';

describe('Header', () => {
  it('正常渲染', () => {
    const { getByText } = render(Header, {
      global: {
        mocks: {
          $route: { name: 'home' }
        }
      }
    });
    expect(getByText('DeepResearch')).toBeTruthy();
  });

  it('显示标题', () => {
    const { getByText } = render(Header, {
      props: { title: 'DeepResearch' },
      global: {
        mocks: {
          $route: { name: 'home' }
        }
      }
    });
    expect(getByText('DeepResearch')).toBeTruthy();
  });
}); 