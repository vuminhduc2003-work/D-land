function fetchResidents() {
    fetch('http://127.0.0.1:8000/api/residents/')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#residentTable tbody');
            tableBody.innerHTML = ''; // Xóa dữ liệu cũ

            // Thêm từng resident vào bảng
            data.forEach(resident => {
                const row = document.createElement('tr');
                row.classList.add('bg-white', 'border-b', 'dark:bg-gray-800', 'dark:border-gray-700');
                row.innerHTML = `
                    <td class="px-6 py-4 font-medium text-gray-900 dark:text-white">
                        ${resident.id}
                    </td>
                    <td class="px-6 py-4">
                        ${resident.full_name}
                    </td>
                    <td class="px-6 py-4">
                        ${resident.email}
                    </td>
                    <td class="px-6 py-4">
                        ${resident.phone_number}
                    </td>
                    <td class="px-6 py-4">
                        ${resident.address}
                    </td>
                    <td class="px-6 py-4">
                        <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline" onclick="deleteResidentAPI(${resident.id})">Xoa</a>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching residents:', error);
        });


    document.getElementById('addResidentForm').addEventListener('submit', function (event) {
    event.preventDefault();

    // Lấy dữ liệu từ form
    const fullName = document.getElementById('full_name').value;
    const email = document.getElementById('email').value;
    const phoneNumber = document.getElementById('phone_number').value;
    const address = document.getElementById('address').value;
    const birthday = document.getElementById('date_of_birth').value;
    const gender = document.getElementById('gender').value;

    // Dữ liệu cần gửi đi trong POST request
    const residentData = {
        full_name: fullName,
        email: email,
        phone_number: phoneNumber,
        address: address,
        date_of_birth: birthday,
        gender: gender
    };

    fetch('http://127.0.0.1:8000/api/residents/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(residentData)  // Gửi trực tiếp đối tượng residentData
    })
    .then(response => response.json())
    .then(data => {
        if (data) {
            // Hiển thị thông báo thành công
            const successAlert = document.getElementById('successAlert');
            successAlert.textContent = 'Cư dân đã được thêm thành công!';
            successAlert.classList.remove('hidden');  // Hiển thị thông báo thành công
            successAlert.classList.add('bg-green-500', 'text-white');  // Thêm màu nền xanh

            // Tải lại trang sau 2 giây
            setTimeout(function() {
                location.reload(); // Tải lại trang
            }, 2000);
        } else {
            // Hiển thị thông báo thất bại
            const errorAlert = document.getElementById('errorAlert');
            errorAlert.textContent = 'Đã có lỗi xảy ra! Không thể thêm cư dân.';
            errorAlert.classList.remove('hidden');  // Hiển thị thông báo lỗi
            errorAlert.classList.add('bg-red-500', 'text-white');  // Thêm màu nền đỏ
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

}
function deleteResidentAPI(residentId) {
    if(confirm('Bạn có muốn xoá cư dân này không ?')) {
        fetch(`http://127.0.0.1:8000/api/residents/${residentId}/`, {
            method: 'DELETE',

        })
        .then(response => {
            if (response.ok) {
                // Hiển thị thông báo thành công
                const successAlert = document.getElementById('successAlert');
                successAlert.classList.remove('hidden');  // Hiển thị alert

                // Tải lại danh sách cư dân sau khi xóa
                fetchResidents();

                // Ẩn thông báo sau 3 giây
                setTimeout(() => {
                    successAlert.classList.add('hidden');
                }, 1000);
            } else {
                alert('Error deleting resident');
            }
        })
        .catch(error => {
            console.error('Error deleting resident:', error);
            alert('Error deleting resident');
        });
    }
}



// Gọi hàm khi tải trang
window.onload = fetchResidents;
