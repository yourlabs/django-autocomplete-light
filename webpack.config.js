var path = require('path')

/* eslint-disable */
module.exports = {
/* eslint-enable */
  entry: {
    main: ['babel-polyfill', './src/dal/js/index.js'],
  },
  output: {
    path: path.resolve('src/dal/static/dal'),
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
}
