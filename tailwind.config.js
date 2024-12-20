/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',               // Đảm bảo rằng các tệp HTML của bạn được bao gồm
    './node_modules/flowbite/**/*.js',     // Bao gồm các file JS của Flowbite
    './styles/**/*.js'                     // Nếu bạn có các file JS trong thư mục styles
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin'),  // Đảm bảo Flowbite plugin được cài đặt và sử dụng
  ],
}
