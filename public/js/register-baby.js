document.addEventListener('DOMContentLoaded', function() {
    fetchSitters();
});

function fetchSitters() {
    fetch('http://127.0.0.1:8014/sitters/get_all_present_sitters')
        .then(response => response.json())
        .then(data => populateSitterDropdown(data.data))
        .catch(error => console.error('Error fetching sitters:', error));
}

function populateSitterDropdown(sitters) {
    const sitterDropdown = document.getElementById('sitterAssigned');
    sitters.forEach(sitter => {
        const option = document.createElement('option');
        option.value = sitter.sitter.id;
        option.textContent = `${sitter.sitter.name} - ${sitter.sitter.location}`;
        sitterDropdown.appendChild(option);
    });
}

function registerBaby() {
    const form = document.getElementById('registerBabyForm');
    const formData = {
        name: form.babyname.value,
        gender: form.gender.value,
        age: parseInt(form.age.value, 10),
        location: form.location.value,
        name_of_brought_person: form.nameofguardian.value,
        time_of_arrival: form.timeOfArrival.value,
        name_of_parent: form.nameofparent.value,
        fee: parseFloat(form.fee.value),
        sitter_assigned: parseInt(form.sitterAssigned.value, 10)
    };

    console.log(formData); 
    
    fetch('http://127.0.0.1:8014/babies/create_baby', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        alert('Baby successfully registered!');
        form.reset();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to register the baby.');
    });
}
