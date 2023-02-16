import { merge } from 'webpack-merge';
import common from './webpack.common'


module.exports = merge(common, {
  mode: 'production',
  output: {
    filename: '[name].[contenthash].js',
  },
});