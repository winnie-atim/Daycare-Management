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

        fetch('http://127.0.0.1:8014/sitters/create_sitter', {
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
                alert('Sitter registered successfully!');
                sitterForm.reset();
            } else {
                alert('Failed to register sitter.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error registering sitter.');
        });
    });
});
