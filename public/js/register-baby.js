document.addEventListener('DOMContentLoaded', function() {
    fetchSitters();
});

function fetchSitters() {
    fetch('http://127.0.0.1:8014/sitters/get_all_present_sitters')
    .then(response => response.json())
    .then(data => {
        const sitterSelect = document.getElementById('sitterAssigned');
        data.data.forEach(sitter => {
            const option = document.createElement('option');
            option.value = sitter.sitter.id;
            option.textContent = sitter.sitter.name;
            sitterSelect.appendChild(option);
        });
    })
    .catch(error => console.error('Error fetching sitters:', error));
}

function searchBaby() {
    const babyAccess = document.getElementById('babyAccess').value.trim();
    if (babyAccess === '') {
        alert('Please enter an access number.');
        return;
    }

    fetch(`http://127.0.0.1:8014/babies/get_baby_by_access?baby_access=${babyAccess}`)
    .then(response => response.json())
    .then(data => {
        if (data.status_code === 200 && data.data) {
            populateForm(data.data);
        } else {
            alert('Baby not found.');
        }
    })
    .catch(error => console.error('Error fetching baby:', error));
}

function populateForm(baby) {
    document.getElementById('babyname').value = baby.name;
    document.getElementById('gender').value = baby.gender;
    document.getElementById('age').value = baby.age;
    document.getElementById('location').value = baby.location;
    document.getElementById('nameofguardian').value = baby.name_of_brought_person;
    document.getElementById('timeOfArrival').value = baby.time_of_arrival;
    document.getElementById('nameofparent').value = baby.name_of_parent;
    document.getElementById('fee').value = baby.fee;
    document.getElementById('sitterAssigned').value = baby.sitter_assigned;

    document.getElementById('updateButton').style.display = 'inline-block';
    document.getElementById('registerButton').style.display = 'none';
    document.getElementById('registerBabyForm').setAttribute('data-baby-access', baby.baby_access);
}

function registerBaby() {
    const form = document.getElementById('registerBabyForm');
    const formData = {
        name: form.babyname.value,
        gender: form.gender.value,
        age: form.age.value,
        location: form.location.value,
        name_of_brought_person: form.nameofguardian.value,
        time_of_arrival: form.timeOfArrival.value,
        name_of_parent: form.nameofparent.value,
        fee: form.fee.value,
        sitter_assigned: form.sitterAssigned.value
    };

    fetch('http://127.0.0.1:8014/babies/create_baby', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status_code === 200) {
            alert('Baby registered successfully!');
            resetForm();
        } else {
            alert('Failed to register baby: ' + data.message);
        }
    })
    .catch(error => console.error('Error registering baby:', error));
}

function updateBaby() {
    const form = document.getElementById('registerBabyForm');
    const babyAccess = form.getAttribute('data-baby-access');
    const formData = {
        baby_access: babyAccess,
        name_of_brought_person: form.nameofguardian.value,
        time_of_arrival: form.timeOfArrival.value,
        fee: form.fee.value,
        sitter_assigned: form.sitterAssigned.value
    };

    fetch('http://127.0.0.1:8014/babies/update_baby', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status_code === 200) {
            alert('Baby updated successfully!');
            resetForm();
        } else {
            alert('Failed to update baby: ' + data.message);
        }
    })
    .catch(error => console.error('Error updating baby:', error));
}

function resetForm() {
    const form = document.getElementById('registerBabyForm');
    form.reset();
    document.getElementById('updateButton').style.display = 'none';
    document.getElementById('registerButton').style.display = 'inline-block';
    form.removeAttribute('data-baby-access');
}
