module.exports = {
  "presets": [
    [
      "@babel/env",
      {
        "targets": {
          "firefox": "75",
          "chrome": "79",
          "safari": "13",
        },
        "useBuiltIns": "usage",
        "corejs": "3.6.5",
      }
    ]
  ],
  "plugins": [
    ["@babel/plugin-transform-react-jsx", {
      "pragma": "h",
      "pragmaFrag": "Fragment"
    }],
    ["babel-plugin-jsx-pragmatic", {
      "module": "preact",
      "import": "h",
      "export": "h"
    }]
  ]
}
