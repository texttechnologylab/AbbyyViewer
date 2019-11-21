const path = require("path")
const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

// const devMode = process.env.NODE_ENV === 'development'
const devMode = true

module.exports =  {
    entry: "./src/javascript/index.ts",
    mode: devMode ? "development" : "production",
    output: {
        path: path.resolve(__dirname, './dist'),
        filename: 'index_bundle.js'
    },

    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: "/lib/",
                
            },
            {
                test: /\.css/,
                loader: 'style-loader!css-loader'
            }
        ]
    },

    resolve: {
        extensions: [ '.tsx', '.ts', '.js' ],
    },
      
    plugins: [  
    ],

    optimization: {
        minimize: true
    },

    
    devServer: {
        contentBase: path.join(__dirname, ''),
        publicPath: "/",
        compress: true,
        port: 9000
      }
      

}