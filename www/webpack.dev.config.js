const PreactRefreshPlugin = require('@prefresh/webpack');
const config = require("./webpack.config")
const webpack = require("webpack")
// const path = require("path")


module.exports = (env, options) => {

    let thing = config(env, options);

    thing.plugins.splice(1, 1);  // Remove MiniCSS plugin
    thing.plugins.splice(0, 1); // Remove Clean Webpack plugin
    thing.plugins.push(new webpack.HotModuleReplacementPlugin());
    thing.plugins.push(new PreactRefreshPlugin());
    thing.module.rules[0].use.options.plugins.splice(0, 0, "@prefresh/babel-plugin"); // Add @prefresh/babel-plugin to Babel
    thing.module.rules[2].use.splice(0, 1, "style-loader");   // Replace MiniCSS with style-loader

    return thing;
}