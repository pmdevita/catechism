module.exports = (api, options, dirname) => {
  api.cache.using(() => process.env.NODE_ENV)
  const isHot = process.env.HOT_RELOAD === 'true';
  const config = {
    "presets": [
      [
        "@babel/preset-env",
        {
          "targets": {
            "firefox": "79",
            "chrome": "80",
            "safari": "13",
          }
        }
      ]
    ],
    "plugins":
        [
          ["@babel/plugin-transform-react-jsx", {
            "pragma": "h",
            "pragmaFrag": "Fragment"
          }],
          ["babel-plugin-jsx-pragmatic", {
            "module": "preact",
            "import": "h",
            "export": "h"
          }],
          "@babel/plugin-proposal-class-properties"
        ]
  }
  if (isHot) {
    config['plugins'].splice(0, 0, '@prefresh/babel-plugin');
  }
  return config;
}