module.exports = {
  root: true,
  parser: "@typescript-eslint/parser",
  plugins: ["@typescript-eslint", "@angular-eslint"],
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:eslint-plugin-prettier/recommended",
    "plugin:@angular-eslint/recommended",
  ],
  rules: {
    "@typescript-eslint/no-empty-function": "off",
    "@typescript-eslint/no-explicit-any": "off",
    "@angular-eslint/no-empty-lifecycle-method": "off",
    quotes: ["error", "single"],
  },
  overrides: [
    {
      files: "web/src/app/app.module.ts",
      rules: {
        "max-len": "off",
      },
    },
  ],
};
