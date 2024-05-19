function showNotification(message, type) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.style.backgroundColor = type === 'success' ? '#4CAF50' : '#f44336';
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

document.addEventListener('DOMContentLoaded', function() {
    const sitterForm = document.getElementById('sitterForm');

    sitterForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = {
            name: document.getElementById('name').value.trim(),
            location: document.getElementById('location').value.trim(),
            date_of_birth: document.getElementById('date_of_birth').value,
            contact: document.getElementById('contact').value.trim(),
            gender: document.getElementById('gender').value,
            next_of_kin: document.getElementById('next_of_kin').value.trim(),
            NIN: document.getElementById('NIN').value.trim(),
            recommended_by: document.getElementById('recommended_by').value.trim(),
            religion: document.getElementById('religion').value.trim(),
            level_of_education: document.getElementById('level_of_education').value.trim()
        };

        console.log(formData);

        fetch('https://daycare-management.onrender.com/sitters/create_sitter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to register sitter: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            if (data.message === 'Sitter created successfully') {
                showNotification('Sitter registered successfully', 'success');
                sitterForm.reset();
            } else {
                showNotification('Failed to register sitter', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error registering sitter', 'error');

        });
    });
});
