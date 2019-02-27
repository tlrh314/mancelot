const path = require('path');

const ExtractTextPlugin = require("extract-text-webpack-plugin");
const HtmlWebpackPlugin = require('html-webpack-plugin');


module.exports = {
    entry : './src/index.js',
    output : {
        filename : 'bundle.js',
        path : path.resolve(__dirname, 'dist')
    },
    /*devServer : {
     contentBase : './dist'
     },*/
    module : {
        rules : [
            {
                test : /\.(js|jsx)$/,
                exclude : /(node_modules|bower_components)/,
                use : {
                    loader : 'babel-loader',
                    options : {
                        presets : [ 'env', 'react', 'stage-2' ]
                    }
                }
            },
            {
                test : /\.scss$/,
                use : ExtractTextPlugin.extract({
                                                    use : [ {
                                                        loader : "css-loader"
                                                    }, {
                                                        loader : "sass-loader"
                                                    } ],
                                                    // use style-loader in
                                                    // development
                                                    fallback : "style-loader"
                                                })
            }
        ]
    },
    plugins : [
        new ExtractTextPlugin("styles.css"),
        new HtmlWebpackPlugin({
            template : path.join(path.resolve(__dirname, 'dist'), 'index.html')
        })
    ],
    resolve : {
        extensions : [ '.js', '.jsx' ]
    }
};