document.addEventListener('DOMContentLoaded', function() {
    loadUsers();

    // Add User Modal
    const modal = document.getElementById('addUserModal');
    const addUserBtn = document.getElementById('addUserBtn');
    const closeBtn = document.getElementsByClassName('close')[0];
    const addUserForm = document.getElementById('addUserForm');
    const logoutBtn = document.getElementById('logoutBtn');

    addUserBtn.onclick = function() {
        modal.style.display = "block";
    }

    closeBtn.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Form submission
    addUserForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            first_name: document.getElementById('firstName').value,
            last_name: document.getElementById('lastName').value,
            gender: document.getElementById('gender').value,
            username: document.getElementById('newUsername').value,
            password: document.getElementById('newPassword').value
        };

        try {
            const response = await fetch('http://localhost:8000/users', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                alert('User created successfully!');
                modal.style.display = "none";
                addUserForm.reset();
                loadUsers();  // Refresh the users list
            } else {
                const data = await response.json();
                alert('Error creating user: ' + data.detail);
            }
        } catch (error) {
            alert('Error creating user: ' + error);
        }
    });

    // Logout functionality
    logoutBtn.addEventListener('click', () => {
        window.location.href = '/login';
    });

    // Edit User Modal
    const editModal = document.getElementById('editUserModal');
    const editCloseBtn = editModal.getElementsByClassName('close')[0];
    const editUserForm = document.getElementById('editUserForm');

    editCloseBtn.onclick = function() {
        editModal.style.display = "none";
    }

    // Edit form submission
    editUserForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const userId = document.getElementById('editUserId').value;
        const formData = {
            first_name: document.getElementById('editFirstName').value,
            last_name: document.getElementById('editLastName').value,
            gender: document.getElementById('editGender').value
        };

        try {
            const response = await fetch(`http://localhost:8000/users/${userId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                alert('User updated successfully!');
                editModal.style.display = "none";
                loadUsers();  // Refresh the users list
            } else {
                const data = await response.json();
                alert('Error updating user: ' + data.detail);
            }
        } catch (error) {
            alert('Error updating user: ' + error);
        }
    });
});

async function loadUsers() {
    try {
        const response = await fetch('http://localhost:8000/users');
        const users = await response.json();
        
        const tableBody = document.getElementById('usersTableBody');
        tableBody.innerHTML = '';  // Clear existing rows
        
        users.forEach(user => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${user.id}</td>
                <td>${user.first_name}</td>
                <td>${user.last_name}</td>
                <td>${user.gender}</td>
                <td>${user.username}</td>
                <td>
                    <button onclick="editUser(${user.id})" class="btn-primary btn-edit">Edit</button>
                    <button onclick="deleteUser(${user.id})" class="btn-primary btn-delete">Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading users:', error);
        alert('Error loading users');
    }
}

async function deleteUser(userId) {
    if (confirm('Are you sure you want to delete this user?')) {
        try {
            const response = await fetch(`http://localhost:8000/users/${userId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                alert('User deleted successfully!');
                loadUsers();  // Refresh the users list
            } else {
                const data = await response.json();
                alert('Error deleting user: ' + data.detail);
            }
        } catch (error) {
            alert('Error deleting user: ' + error);
        }
    }
}

async function editUser(userId) {
    try {
        const response = await fetch(`http://localhost:8000/users/${userId}`);
        const user = await response.json();
        
        // Populate the edit form
        document.getElementById('editUserId').value = user.id;
        document.getElementById('editFirstName').value = user.first_name;
        document.getElementById('editLastName').value = user.last_name;
        document.getElementById('editGender').value = user.gender;
        
        // Show the edit modal
        const editModal = document.getElementById('editUserModal');
        editModal.style.display = "block";
    } catch (error) {
        alert('Error loading user data: ' + error);
    }
} 
