const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const glob = require('glob-all')
const PurgecssPlugin = require('purgecss-webpack-plugin')

class TailwindExtractor {
  static extract(content) {
    return content.match(/[A-Za-z0-9-_:\/]+/g) || [];
  }
}

const PATHS = {
  src: path.join(__dirname)
}

module.exports = {
  entry: './js/app.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'app.js'
  },
  module: {
      rules: [{
        test: /\.scss$/,
        use: ExtractTextPlugin.extract({
            fallback: 'style-loader',
            use: ['css-loader', 'postcss-loader', 'sass-loader']
          })
        }]
  },
  plugins: [ 
    new ExtractTextPlugin('app.css'),
  new PurgecssPlugin({

    // Specify the locations of any files you want to scan for class names.
    paths: glob.sync([path.join(__dirname, "js/*.js"),
          path.join(__dirname, "*.html")]),
    extractors: [
      {
        extractor: TailwindExtractor,

        // Specify the file extensions to include when scanning for
        // class names.
        extensions: ["html", "js"]
      }
    ]
  })
 ]
}

