import { createGlobalState, useStorage } from '@vueuse/core';

export const usePersistedState = createGlobalState(() => useStorage('menu-mate', {
}, localStorage));
