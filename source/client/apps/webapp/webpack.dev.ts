import { merge } from 'webpack-merge';
import common from './webpack.common'


module.exports = merge(common, {
    mode: 'development',
    devServer: {
        port: 5173,
        liveReload: true,
    },
    output: {
        filename: '[name].js',
    },
    devtool: 'inline-source-map',
})
