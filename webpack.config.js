var path = require('path')

/* eslint-disable */
module.exports = {
/* eslint-enable */
  entry: {
    main: ['babel-polyfill', './src/dal/npm/index.js'],
  },
  output: {
    path: path.resolve('src/dal/static/autocomplete_light/select2'),
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
}
