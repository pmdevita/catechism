const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const babel = require("./babel.config");
const TerserPlugin = require("terser-webpack-plugin");
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = (env, options) => {
  const isDevelopment = options.mode !== 'production';
  return {
    entry: {
      js: './src/js/main.js',
      css: './src/scss/main.scss',
      tw: './src/scss/tailwind.scss'
    },
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: '[name].[contenthash].js',
      publicPath: "",
      assetModuleFilename: "images/[name].[hash][ext][query]"
    },
    module: {
      rules: [
        {
          test: /\.jsx?$/,
          // resolve: {
          //   fullySpecified: false
          // },
          use: [
            'babel-loader',
            // 'source-map-loader'
          ],
        },
        {
          test: /\.html$/,
          use: [{
            loader: "html-loader",
            options: {}
          }]
        },
        {
          test: /\.scss$/,
          exclude: /tailwind.scss$/,
          use: [
            isDevelopment ? 'style-loader' : MiniCssExtractPlugin.loader,
            {
              loader: 'css-loader',
              options: {
                modules: {
                  localIdentName: '[path][name]__[local]'
                }
              }
            },
            {
              loader: "postcss-loader",
              options: {
                sourceMap: true
              }
            },
            "resolve-url-loader?sourceMap",
            "sass-loader?sourceMap"
          ]

        },
        {
          test: /tailwind.scss$/,
          use: [
            isDevelopment ? 'style-loader' : MiniCssExtractPlugin.loader,
            'css-loader',
            {
              loader: "postcss-loader",
              options: {
                sourceMap: true
              }
            },
            "resolve-url-loader?sourceMap",
            "sass-loader?sourceMap"
          ]

        },
        {
          test: /\.(png|jpe?g|gif|bmp|woff2?)$/i,
          type: "asset/resource"
        },
      ]
    },
    devtool: 'source-map',
    plugins: [
      new CleanWebpackPlugin(),
      new HtmlWebpackPlugin({
        template: path.resolve(__dirname, 'src/index.html'),
        filename: 'index.html'
      }),
      new MiniCssExtractPlugin({
        filename: "[name].[contenthash].css"
      })
    ],
    optimization: {
      minimize: !isDevelopment,
      minimizer: [
        new TerserPlugin(),
        new CssMinimizerPlugin(),
      ],
      splitChunks: {
        cacheGroups: {
          commons: {
            test: /[\\/]node_modules[\\/](?!lazysizes)/,
            name: 'vendor',
            chunks: 'all',
          },
        },
      },
    },
    devServer: {
      contentBase: path.join(__dirname, 'dist'),
      host: '0.0.0.0',
      port: 9000,
      // historyApiFallback: true,
      hot: true,
      inline: true,
      // publicPath: '/',
      // clientLogLevel: 'none',
      open: false,
      overlay: true,
    }
  }
}
