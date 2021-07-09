const PreactRefreshPlugin = require('@prefresh/webpack');
const config = require("./webpack.config")
const webpack = require("webpack")
const path = require("path")


module.exports = (env, options) => {

    let thing = config(env, options);

    thing.module.rules[0]['include'] = [path.resolve(__dirname, 'src')]  // Prefresh freaks the heck out without this
    thing.plugins.splice(2, 1);  // Remove MiniCSS plugin
    thing.plugins.splice(0, 1); // Remove Clean Webpack plugin
    thing.plugins.push(new webpack.HotModuleReplacementPlugin());
    thing.plugins.push(new PreactRefreshPlugin());

    return thing;
}