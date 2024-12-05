// Lấy các phần tử cần thiết
const menuButton = document.getElementById('menuButton');
const menu = document.getElementById('menu');

// Thêm sự kiện click cho nút
menuButton.addEventListener('click', function() {
    // Kiểm tra xem menu đang ẩn hay không
    if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
    } else {
        menu.classList.add('hidden');
    }
});
