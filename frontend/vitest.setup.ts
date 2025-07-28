import '@testing-library/jest-dom';
import { config } from '@vue/test-utils';
import ElementPlus from 'element-plus';
import { createPinia, setActivePinia } from 'pinia';

// 全局注册 Element Plus
config.global.plugins = [ElementPlus];

// 全局注册 Pinia
const pinia = createPinia();
setActivePinia(pinia);
config.global.plugins.push(pinia); 