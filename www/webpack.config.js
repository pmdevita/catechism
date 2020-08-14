const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
  entry: ['./src/js/main.js', './src/scss/main.scss'],
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        enforce: 'pre',
        use: ['babel-loader', 'source-map-loader'],
      },
      {
        test: /\.html$/,
        use: [{
          loader: "html-loader",
          options: {
          }
        }]
      },
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader?sourceMap",
          "postcss-loader?sourceMap",
          "resolve-url-loader?sourceMap",
          "sass-loader?sourceMap"
        ]

      },
      {
        test: /\.(png|jpe?g|gif|bmp|woff2?)$/i,
        use: ['file-loader'],
      },
    ]
  },
  devtool: 'source-map',
  plugins: [
    new HtmlWebpackPlugin({
      template: path.resolve(__dirname, 'src/index.html'),
      filename: 'index.html'
    }),
    new MiniCssExtractPlugin()
  ]
};