function fetchResidents() {
    const urlAPIResident = 'http://127.0.0.1:8000/api/residents/'
    fetch(urlAPIResident)
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#residentTable tbody');
            tableBody.innerHTML = ''; // Clear previous data

            // Add each resident to the table
            data.forEach((resident, index) => {
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
                        <button class="btn btn-warning btn-sm" onclick="fetchResidentDetails(${resident.id})">Chi tiết</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteResidentAPI(${resident.id})">Xóa</button>
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

        // Check if all fields are filled
        if (!fullName || !email || !phoneNumber || !address || !birthday || !gender) {
            const errorAlert = document.getElementById('errorAlert');
            errorAlert.textContent = 'Tất cả các trường đều phải được điền!';
            errorAlert.classList.remove('hidden');
            errorAlert.classList.add('bg-red-500', 'text-white');
            return; // Stop if any field is empty
        }

        // Data to send in the POST request
        const residentData = {
            full_name: fullName,
            email: email,
            phone_number: phoneNumber,
            address: address,
            date_of_birth: birthday,
            gender: gender
        };

        // Send data via POST request
        fetch('http://127.0.0.1:8000/api/residents/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(residentData)  // Send the resident data as JSON
        })
        .then(response => {
            if (!response.ok) {
                // Log the error response if not OK
                return response.text().then(text => {
                    throw new Error('Error: ' + text);
                });
            }
            return response.json();
        })
        .then(data => {
            if (data) {
                // Show success message
                const successAlert = document.getElementById('successAlertCreateResident');
                successAlert.textContent = 'Cư dân đã được thêm thành công!';
                successAlert.classList.remove('hidden');
                successAlert.classList.add('bg-green-500', 'text-white');

                // Optionally, reload the table after adding a resident
                fetchResidents(); // Refresh the resident list
            } else {
                // Show error message
                const errorAlert = document.getElementById('errorAlert');
                errorAlert.textContent = 'Đã có lỗi xảy ra! Không thể thêm cư dân.';
                errorAlert.classList.remove('hidden');
                errorAlert.classList.add('bg-red-500', 'text-white');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            // Display error alert
            const errorAlert = document.getElementById('errorAlert');
            errorAlert.textContent = 'Đã có lỗi xảy ra! Không thể thêm cư dân.';
            errorAlert.classList.remove('hidden');
            errorAlert.classList.add('bg-red-500', 'text-white');
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
document.getElementById('editResidentForm').addEventListener('submit', function (event) {
    event.preventDefault();  // Prevent default form submission

    const url = `http://127.0.0.1:8000/api/residents/${residentId}/`;

    // Collect data from the form
    const fullName = document.getElementById('edit_full_name').value;
    const phoneNumber = document.getElementById('edit_phone_number').value;
    const email = document.getElementById('edit_email').value;
    const dateOfBirth = document.getElementById('edit_date_of_birth').value;
    const gender = document.getElementById('edit_gender').value;
    const address = document.getElementById('edit_address').value;

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
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedData)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update the data');
            }
            return response.json();
        })
        .then(updatedResident => {
            alert('Cập nhật thông tin thành công!');
            console.log('Updated Resident:', updatedResident);

            // Close the modal after successful update
            closeModal();

            // Optionally, reload the resident list to show updated data
            fetchResidents();
        })
        .catch(error => {
            alert('Có lỗi xảy ra khi cập nhật thông tin!');
            console.error('Error updating resident data:', error);
        });
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




    window.onload = function() {
}


const apiUrlApartment = 'http://127.0.0.1:8000/api/apartments/';

// Hàm tải danh sách căn hộ
async function fetchApartments() {
    const apartmentTable = document.querySelector('#apartmentTable tbody');
    apartmentTable.innerHTML = ''; // Xóa dữ liệu cũ

    try {
        const response = await fetch(apiUrlApartment);

        if (!response.ok) {
            throw new Error(`Lỗi khi gọi API: ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();

        data.forEach((apartment, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${apartment.apartment_code}</td>
                <td>${apartment.building}</td>
                <td>${apartment.floor_number}</td>
                <td>${apartment.area} m²</td>
                <td>${apartment.status}</td>
                <td>
                    <button class="btn btn-info btn-sm" onclick="viewApartmentDetails(${apartment.id})">Xem Chi Tiết</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteApartment(${apartment.id})">Xóa</button>
                </td>
            `;
            apartmentTable.appendChild(row);
        });
    } catch (error) {
        console.error('Lỗi khi tải danh sách căn hộ:', error);
        alert('Không thể tải danh sách căn hộ. Vui lòng thử lại sau.');
    }
}
async function viewApartmentDetails(apartmentId) {
    const apiUrlApartmentDetail = `http://127.0.0.1:8000/api/apartments/${apartmentId}/`;

    try {
        const response = await fetch(apiUrlApartmentDetail);

        if (!response.ok) {
            throw new Error('Không thể tải thông tin căn hộ');
        }

        const apartment = await response.json();

        // Cập nhật thông tin chi tiết căn hộ vào modal
        document.getElementById('apartmentCodeDetail').textContent = apartment.apartment_code;
        document.getElementById('buildingDetail').textContent = apartment.building;
        document.getElementById('floorNumberDetail').textContent = apartment.floor_number;
        document.getElementById('areaDetail').textContent = apartment.area;
        document.getElementById('apartmentOrientationDetail').textContent = apartment.apartment_orientation;
        document.getElementById('statusDetail').textContent = apartment.status;

        // Mở modal
        const modal = new bootstrap.Modal(document.getElementById('viewApartmentModal'));
        modal.show();
    } catch (error) {
        console.error('Lỗi:', error);
        alert('Có lỗi xảy ra khi tải thông tin căn hộ.');
    }
}
// Hàm xử lý khi gửi biểu mẫu trong modal
async function addApartment(event) {
    event.preventDefault(); // Ngăn chặn reload trang

    // Lấy dữ liệu từ modal
    const apartmentData = {
        apartment_code: document.getElementById('apartmentCode').value,
        building: document.getElementById('building').value,
        floor_number: parseInt(document.getElementById('floorNumber').value),
        area: parseFloat(document.getElementById('area').value),
        apartment_orientation: document.getElementById('apartmentOrientation').value,
        status: document.getElementById('status').value,
    };

    try {
        const response = await fetch(apiUrlApartment, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(apartmentData),
        });

        if (!response.ok) {
            throw new Error(`Lỗi khi thêm căn hộ: ${response.status}`);
        }

        alert('Thêm căn hộ thành công!');
        document.getElementById('apartmentForm').reset(); // Xóa dữ liệu form
        fetchApartments(); // Tải lại danh sách căn hộ

        // Ẩn modal
        const modalElement = document.querySelector('#addApartmentModal');
        const modal = bootstrap.Modal.getInstance(modalElement);
        modal.hide();
    } catch (error) {
        console.error('Lỗi khi thêm căn hộ:', error);
        alert('Không thể thêm căn hộ. Vui lòng thử lại sau.');
    }
}

// Gắn sự kiện vào biểu mẫu
document.getElementById('apartmentForm').addEventListener('submit', addApartment);


// Gắn sự kiện vào biểu mẫu
document.getElementById('apartmentForm').addEventListener('submit', addApartment);
async function deleteApartment(apartmentId) {
    if (!confirm('Bạn có chắc chắn muốn xóa căn hộ này?')) {
        return;
    }

    try {
        const response = await fetch(`${apiUrlApartment}${apartmentId}/`, {
            method: 'DELETE',
        });

        if (!response.ok) {
            throw new Error(`Không thể xóa căn hộ: ${response.status}`);
        }

        alert('Căn hộ đã được xóa thành công!');
        fetchApartments(); // Tải lại danh sách
    } catch (error) {
        console.error('Lỗi khi xóa căn hộ:', error);
        alert('Không thể xóa căn hộ. Vui lòng thử lại sau.');
    }
}

document.addEventListener('DOMContentLoaded', fetchApartments);

// Gọi hàm khi tải trang
window.onload = fetchResidents;
