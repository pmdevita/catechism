const PreactRefreshPlugin = require('@prefresh/webpack');
const thing = require("./webpack.config")
const webpack = require("webpack")
const path = require("path")

thing.plugins.splice(1,1);  // Remove MiniCSS plugin
thing.plugins.push(new webpack.HotModuleReplacementPlugin());
thing.plugins.push(new PreactRefreshPlugin());
thing['devServer'] = {
    hot: true,
    port: 9000,
    contentBase: path.join(__dirname, 'dist'),
};
thing.module.rules[0].use[0].options.plugins.splice(0, 0, "@prefresh/babel-plugin"); // Add @prefresh/babel-plugin to Babel
thing.module.rules[2].use.splice(0,1,"style-loader");   // Replace MiniCSS with style-loader

module.exports = thing;