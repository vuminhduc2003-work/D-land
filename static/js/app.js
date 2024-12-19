function fetchResidents() {
            fetch('http://127.0.0.1:8000/api/residents/')
                .then(response => response.json())
                .then(data => {
                    const tableBody = document.querySelector('#residentTable tbody');
                    tableBody.innerHTML = ''; // Clear dữ liệu cũ

                    // Thêm từng resident vào bảng
                    data.forEach(resident => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${resident.id}</td>
                            <td>${resident.full_name}</td>
                            <td>${resident.email}</td>
                            <td>${resident.phone_number}</td>
                            <td>${resident.address}</td>
                            <td>
                                <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Edit</a>
                            </td>

                        `;
                        tableBody.appendChild(row);
                    });
                })
                .catch(error => {
                    console.error('Error fetching residents:', error);
                });
        }

        // Gọi hàm để tải dữ liệu ngay khi trang web được tải
        window.onload = fetchResidents;