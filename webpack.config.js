var path = require('path')

/* eslint-disable */
module.exports = [
/* eslint-enable */
  {
    entry: {
      main: ['babel-polyfill', './src/dal_select2/npm/index.js'],
    },
    output: {
      path: path.resolve('src/dal_select2/static/autocomplete_light/select2'),
      filename: 'dal_select2.js'
    },
    devtool: 'source-map',
    module: {
      rules: [
        {
          test: /\.js$/,
          //exclude: /(node_modules|bower_components)/,
          use: {
            loader: 'babel-loader',
          }
        }
      ]
    }
  },
  {
    entry: {
      main: ['babel-polyfill', './src/dal_accessible/npm/index.js'],
    },
    output: {
      path: path.resolve('src/dal_accessible/static/dal'),
      filename: 'dist.js'
    },
    devtool: 'source-map',
    module: {
      rules: [
        {
          test: /\.js$/,
          //exclude: /(node_modules|bower_components)/,
          use: {
            loader: 'babel-loader',
          }
        }
      ]
    }
  },
]
