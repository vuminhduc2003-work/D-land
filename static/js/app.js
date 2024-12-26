function fetchResidents() {
    fetch('http://127.0.0.1:8000/api/residents/')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#residentTable tbody');
            tableBody.innerHTML = ''; // Clear previous data

            // Add each resident to the table
            data.forEach((resident, index) => {  // Added 'index' parameter to track row numbers
                const row = document.createElement('tr');
                row.classList.add('bg-white', 'border-b', 'dark:bg-gray-800', 'dark:border-gray-700');
                row.innerHTML = `
                    <td class="px-6 py-4 font-medium text-gray-900 dark:text-white">
                       ${index + 1}  <!-- Display row number (index + 1) -->
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
                        <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline" onclick="deleteResidentAPI(${resident.id})">Xoá</a>
                        <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline" onclick="fetchResidentDetails(${resident.id})">Chi tiết</a>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching residents:', error);
        });

    // Add event listener for the add resident form
    document.getElementById('addResidentForm').addEventListener('submit', function (event) {
        event.preventDefault();

        // Get data from the form
        const fullName = document.getElementById('full_name').value;
        const email = document.getElementById('email').value;
        const phoneNumber = document.getElementById('phone_number').value;
        const address = document.getElementById('address').value;
        const birthday = document.getElementById('date_of_birth').value;
        const gender = document.getElementById('gender').value;

        // Data to send in the POST request
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
            body: JSON.stringify(residentData)  // Send resident data
        })
        .then(response => response.json())
        .then(data => {
            if (data) {
                // Show success message
                const successAlert = document.getElementById('successAlertCreateResident');
                successAlert.textContent = 'Cư dân đã được thêm thành công!';
                successAlert.classList.remove('hidden');  // Show success alert
                successAlert.classList.add('bg-green-500', 'text-white');  // Add green background

                // Reload page after 2 seconds
                setTimeout(function () {
                    location.reload(); // Reload the page
                }, 2000);
            } else {
                // Show error message
                const errorAlert = document.getElementById('errorAlert');
                errorAlert.textContent = 'Đã có lỗi xảy ra! Không thể thêm cư dân.';
                errorAlert.classList.remove('hidden');  // Show error alert
                errorAlert.classList.add('bg-red-500', 'text-white');  // Add red background
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}


// Hàm mở modal và hiển thị thông tin chi tiết
function fetchResidentDetails(residentId) {
    const url = `http://127.0.0.1:8000/api/residents/${residentId}/`;

    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error fetching resident details: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('Resident Data:', data); // Kiểm tra dữ liệu trả về

            // Điền thông tin cư dân vào form
            document.getElementById('edit_full_name').value = data.full_name || '';
            document.getElementById('edit_phone_number').value = data.phone_number || '';
            document.getElementById('edit_email').value = data.email || '';
            document.getElementById('edit_date_of_birth').value = data.date_of_birth || '';
            document.getElementById('edit_gender').value = data.gender || 'Male';
            document.getElementById('edit_address').value = data.address || '';

            // Hiển thị modal
            const modal = document.getElementById('detail-modal');
            modal.classList.remove('hidden');
        })
        .catch(error => {
            console.error('Error fetching resident details:', error);

            // Hiển thị thông báo lỗi
            const errorAlert = document.getElementById('errorAlert');
            errorAlert.textContent = error.message;
            errorAlert.classList.remove('hidden');

            // Ẩn thông báo lỗi sau 3 giây
            setTimeout(() => {
                errorAlert.classList.add('hidden');
            }, 3000);
        });
}

function closeModal() {
    const modal = document.getElementById('detail-modal');
    modal.classList.add('hidden');
}

function deleteResidentAPI(residentId) {
    if (confirm('Bạn có muốn xoá cư dân này không ?')) {
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


document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('editResidentForm');
    const residentId = 18;  // Replace with the actual resident ID
    const url = `http://127.0.0.1:8000/api/residents/${residentId}/`;

    form.addEventListener('submit', function (event) {
        event.preventDefault();  // Prevent the default form submission (GET)

        // Collect the data from the form
        const fullName = document.getElementById('edit_full_name').value;
        const phoneNumber = document.getElementById('edit_phone_number').value;
        const email = document.getElementById('edit_email').value;
        const dateOfBirth = document.getElementById('edit_date_of_birth').value;
        const gender = document.getElementById('edit_gender').value;
        const address = document.getElementById('edit_address').value;

        // Prepare the data to send in the body
        const updatedData = {
            full_name: fullName,
            phone_number: phoneNumber,
            email: email,
            date_of_birth: dateOfBirth,
            gender: gender,
            address: address
        };

        // Send the PUT request to update the resident data
        fetch(url, {
            method: 'PUT', // Use PUT to update existing data
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Failed to update the data');
                }
            })
            .then(updatedResident => {
                alert('Cập nhật thông tin thành công!');
                console.log('Updated Resident:', updatedResident);
                location.reload();

            })
            .catch(error => {
                alert('Có lỗi xảy ra khi cập nhật thông tin!');
                console.error('Error updating resident data:', error);
            });
    });
});


    // Function to search residents by name (or other criteria)
    function searchResidents() {
        const searchQuery = document.getElementById('searchInput').value.trim();

        // Make an API request to search residents
        if (searchQuery) {
        fetch(`http://127.0.0.1:8000/api/residents/?search=${searchQuery}`)
        .then(response => response.json())
        .then(residents => {
        displayResidents(residents);  // Display the filtered residents
    })
        .catch(error => {
        console.error('Error fetching residents:', error);
    });
    } else {
        fetch('http://127.0.0.1:8000/api/residents/')
        .then(response => response.json())
        .then(residents => {
        displayResidents(residents);  // Display all residents when search is empty
    })
        .catch(error => {
        console.error('Error fetching residents:', error);
    });
    }
    }

        // Function to display residents in the table
        function displayResidents(residents) {
        const residentList = document.getElementById('residentTable');
        residentList.innerHTML = '';  // Clear existing list

        residents.forEach(resident => {
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
                        <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline" onclick="deleteResidentAPI(${resident.id})">Xoá</a>
                        <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline" onclick="fetchResidentDetails(${resident.id})">Chi tiết</a>
                    </td>
                    
                `;
        residentList.appendChild(row);
    });
    }

    // Initial fetch to populate the residents table
    window.onload = function() {
    searchResidents();  // Fetch and display all residents initially
}


// Gọi hàm khi tải trang
window.onload = fetchResidents;
