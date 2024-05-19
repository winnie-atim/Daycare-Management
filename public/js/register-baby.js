function showNotification(message, type) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.style.backgroundColor = type === 'success' ? '#4CAF50' : '#f44336';
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

function showPopup(message) {
    const popup = document.createElement('div');
    popup.classList.add('popup');
    popup.innerHTML = `
        <div class="popup-content">
            <p>${message}</p>
            <button onclick="closePopup()">Close</button>
        </div>
    `;
    document.body.appendChild(popup);
}

function closePopup() {
    const popup = document.querySelector('.popup');
    if (popup) {
        document.body.removeChild(popup);
    }
}

function generatePDF(baby) {
    if (!window.jspdf) {
        console.error('jsPDF is not loaded');
        return;
    }

    const { jsPDF } = window.jspdf;

    const doc = new jspdf.jsPDF();
    

     const logo = new Image();
     logo.src = '../images/badge.jpg';  
     logo.onload = () => {
         doc.addImage(logo, 'PNG', 10, 10, 50, 20);  
 

         doc.setFontSize(22);
         doc.setTextColor(40);
         doc.text('DAYSTAR DAYCARE ', 70, 20);
 

         doc.setLineWidth(0.5);
         doc.line(10, 35, 200, 35);
 
    
         doc.setFontSize(14);
         doc.setTextColor(0);
         const margin = 10;
         const lineHeight = 10;
         let y = 45;
 
         doc.text(`Baby Name: ${baby.name}`, margin, y);
         y += lineHeight;
         doc.text(`Gender: ${baby.gender}`, margin, y);
         y += lineHeight;
         doc.text(`Age: ${baby.age}`, margin, y);
         y += lineHeight;
         doc.text(`Location: ${baby.location}`, margin, y);
         y += lineHeight;
         doc.text(`Name of Guardian: ${baby.name_of_brought_person}`, margin, y);
         y += lineHeight;
         doc.text(`Time of Arrival: ${baby.time_of_arrival}`, margin, y);
         y += lineHeight;
         doc.text(`Name of Parent: ${baby.name_of_parent}`, margin, y);
         y += lineHeight;
         doc.text(`Fee: ${baby.fee}`, margin, y);
        //  y += lineHeight;
        //  doc.text(`Assigned Sitter: ${baby.sitter_assigned}`, margin, y);
         y += lineHeight;
         doc.text(`Access Number: ${baby.baby_access}`, margin, y);
         y += lineHeight;
    
    doc.save(`${baby.name}'s details.pdf`);
};
}

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
        showNotification('Please enter an access number.', 'error');
        return;
    }

    fetch(`http://127.0.0.1:8014/babies/get_baby_by_access?baby_access=${babyAccess}`)
    .then(response => response.json())
    .then(data => {
        if (data.status_code === 200 && data.data) {
            populateForm(data.data);
            showNotification('Baby found successfully!', 'success');
        } else {
            showNotification('Baby not found.', 'error');
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
            const baby = data.data;
            console.log('Baby registered successfully:', baby);
            showPopup(`Baby registered successfully! Access Number: ${baby.baby_access}`);
            generatePDF(baby);
            form.reset();
            document.getElementById('registerButton').style.display = 'inline-block';
            document.getElementById('updateButton').style.display = 'none';
        } else {
            showNotification('Failed to register baby: ' + data.message, 'error');
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
            showNotification('Baby updated successfully!', 'success');
            form.reset();
            document.getElementById('registerButton').style.display = 'inline-block';
            document.getElementById('updateButton').style.display = 'none';
            loadContent('babiesform.html');
        } else {
            showNotification('Failed to update baby: ' + data.message, 'error');
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
