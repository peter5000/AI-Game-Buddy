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
    {
        ignores: [
            "node_modules/",
            ".next/",
            ".venv/",
            "next-env.d.ts",
            "out/",
            "build/",
            "dist/",
        ],
    },

    eslint.configs.recommended,
    ...tseslint.configs.recommended,

    // 👇 Explicit Next.js config block (this makes Next.js detection happy)
    {
        plugins: {
            "@next/next": nextPlugin,
        },
        rules: {
            ...nextPlugin.configs["core-web-vitals"].rules,
        },
    },

    {
        files: ["**/*.{js,jsx,ts,tsx}"],
        plugins: {
            react: reactPlugin,
            "react-hooks": hooksPlugin,
            "jsx-a11y": jsxA11yPlugin,
            "simple-import-sort": importSortPlugin,
            // 👇 keep Next here too so rules work inside this block
            "@next/next": nextPlugin,
        },
        languageOptions: {
            parser: tseslint.parser,
            parserOptions: {
                ecmaVersion: "latest",
                sourceType: "module",
                ecmaFeatures: { jsx: true },
                project: "./tsconfig.json",
            },
            globals: {
                ...globals.browser,
                ...globals.node,
                ...globals.es2021,
            },
        },
        rules: {
            // your custom rules (no need to duplicate next/core-web-vitals here)
            "no-console": ["warn", { allow: ["warn", "error"] }],
            "prefer-const": "error",
            "no-unused-vars": "off",
            "@typescript-eslint/no-unused-vars": [
                "error",
                { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
            ],

            "react/react-in-jsx-scope": "off",
            "react/prop-types": "off",
            "react/jsx-uses-react": "off",
            "react/jsx-uses-vars": "error",
            "react/jsx-key": "error",
            "react/no-unescaped-entities": "error",

            "react-hooks/rules-of-hooks": "error",
            "react-hooks/exhaustive-deps": "warn",

            "simple-import-sort/imports": [
                "error",
                {
                    groups: [
                        ["^\\u0000"],
                        ["^react", "^next", "^@?\\w"],
                        ["^(@|components|lib|app)(/.*|$)"],
                        ["^\\.\\.(?!/?$)", "^\\.\\./?$"],
                        ["^\\./(?=.*/)(?!/?$)", "^\\.(?!/?$)", "^\\./?$"],
                        ["^.+\\.s?css$"],
                    ],
                },
            ],
            "simple-import-sort/exports": "error",

            "@typescript-eslint/no-explicit-any": "warn",
            "@typescript-eslint/explicit-function-return-type": "off",
            "@typescript-eslint/explicit-module-boundary-types": "off",
            "@typescript-eslint/no-non-null-assertion": "warn",
        },
        settings: {
            react: { version: "detect" },
        },
    },

    {
        files: ["**/*.config.{js,ts,mjs}"],
        rules: {
            "no-console": "off",
            "@typescript-eslint/no-require-imports": "off",
        },
    },
    {
        files: ["**/*.d.ts"],
        rules: {
            "@typescript-eslint/no-unused-vars": "off",
        },
    },

    prettierConfig,
];
