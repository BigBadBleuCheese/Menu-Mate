<template>
    <v-app>
        <Main />
    </v-app>
</template>

<script setup>
    import { useTheme } from 'vuetify';

    const theme = useTheme();

    const updateTheme = () => {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        theme.global.name.value = prefersDark ? 'dark' : 'light';
    };

    onMounted(() => {
        updateTheme();
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', updateTheme);
    });

    onUnmounted(() => {
        window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', updateTheme);
    });
</script>
