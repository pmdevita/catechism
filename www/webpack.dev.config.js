const PreactRefreshPlugin = require('@prefresh/webpack');
const thing = require("./webpack.config")
const webpack = require("webpack")
const path = require("path")

thing.plugins.splice(1,1)
thing.plugins.push(new webpack.HotModuleReplacementPlugin())
thing.plugins.push(new PreactRefreshPlugin())
thing['devServer'] = {
    hot: true,
    port: 9000,
    contentBase: path.join(__dirname, 'dist'),
}
thing.module.rules[2].use.splice(0,1,"style-loader")
console.log(thing.module.rules[2].use)

console.log(thing)

module.exports = thing;