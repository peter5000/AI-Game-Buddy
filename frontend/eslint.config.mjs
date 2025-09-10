import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import nextPlugin from "@next/eslint-plugin-next";
import reactPlugin from "eslint-plugin-react";
import hooksPlugin from "eslint-plugin-react-hooks";
import jsxA11yPlugin from "eslint-plugin-jsx-a11y";
import importSortPlugin from "eslint-plugin-simple-import-sort";
import prettierConfig from "eslint-config-prettier";
import globals from "globals";

export default [
    // Global ignores
    {
        ignores: ["node_modules/", ".next/", ".venv/"],
    },

    // Base configurations for all files
    eslint.configs.recommended,
    ...tseslint.configs.recommended,

    // Configurations for React/Next files
    {
        files: ["**/*.{js,jsx,ts,tsx}"],
        plugins: {
            react: reactPlugin,
            "react-hooks": hooksPlugin,
            "@next/next": nextPlugin,
            "jsx-a11y": jsxA11yPlugin,
            "simple-import-sort": importSortPlugin,
        },
        languageOptions: {
            parserOptions: {
                ecmaFeatures: {
                    jsx: true,
                },
            },
            globals: {
                ...globals.browser,
                ...globals.node,
            },
        },
        rules: {
            // General rules
            "no-console": ["warn", { allow: ["warn", "error"] }],

            // React and Hooks rules
            ...reactPlugin.configs.recommended.rules,
            ...hooksPlugin.configs.recommended.rules,
            "react/react-in-jsx-scope": "off", // Not needed with Next.js/new JSX transform
            "react/prop-types": "off", // Not needed with TypeScript

            // Next.js specific rules
            ...nextPlugin.configs.recommended.rules,
            ...nextPlugin.configs["core-web-vitals"].rules,

            // Accessibility rules
            ...jsxA11yPlugin.configs.recommended.rules,

            // Import sorting
            "simple-import-sort/imports": "error",
            "simple-import-sort/exports": "error",
        },
        settings: {
            react: {
                version: "detect", // Automatically detect the React version
            },
        },
    },

    // Prettier configuration must be last
    prettierConfig,
];
