function showNotification(message, type) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.style.backgroundColor = type === 'success' ? '#4CAF50' : '#f44336';
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

function sendSignupToken() {
    const email = document.getElementById('email').value.trim();
    const adminId = document.getElementById('admin_id').value;

    const payload = {
        email: email,
        admin_id: parseInt(adminId)
    };

    fetch('https://daycare-management.onrender.com/admins/generate_signup_token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status_code === 200) {
            showNotification('Signup token sent successfully!', 'success');
        } else {
            showNotification('Failed to send signup token: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error sending signup token.', 'error');
    });
}


document.addEventListener('DOMContentLoaded', function() {
    loadContent('babiesform.html');
});

    function loadContent(pageUrl) {
        fetch(pageUrl)
            .then(response => response.text())
            .then(html => {
                const mainContent = document.getElementById('main-content');
                mainContent.innerHTML = html;
                executePageScripts(pageUrl);
            })
            .catch(error => {
                console.error('Error loading the page: ', error);
                const mainContent = document.getElementById('main-content');
                mainContent.innerHTML = '<p>Error loading the content.</p>';
            });
    }

    function executePageScripts(pageUrl) {
        if (pageUrl === 'babiesform.html') {
            registerBabyForm();
        } else if (pageUrl === 'newSitter.html') {
            registerSitterForm();
        } else if (pageUrl === 'allSeaters.html') {
            fetchAllSitters();
        } else if (pageUrl === 'releaseBaby.html') {
            fetchAllData();
        } else if (pageUrl === 'presentSitter.html') {
            fetchSitterBillDetails();
        }
    }
    function fetchAllSitters() {
          console.log("Fetching sitters...");
          fetch('https://daycare-management.onrender.com/sitters/get_all_sitters')
              .then(response => {
                  if (!response.ok) throw new Error('Network response was not ok');
                  return response.json();
              })
              .then(data => {
                  console.log("Data received:", data);
                  populateTable(data.data);
              })
              .catch(error => {
                  console.error('Error fetching sitters:', error);
              });
      }

      function registerBabyForm() {
        const form = document.getElementById('registerBabyForm');
        form.addEventListener('submit', function(event) {
            event.preventDefault();
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
    
            fetch('https://daycare-management.onrender.com/babies/create_baby', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status_code === 200) {
                    showNotification('Baby registered successfully!', 'success');
                    form.reset();
                } else {
                    showNotification('Failed to register baby: ' + data.message, 'error');
                }
            })
            .catch(error => console.error('Error registering baby:', error));
        });
    }

    function registerSitterForm() {
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
             const ninLength = formData.NIN.length;
            if (ninLength !== 13 && ninLength !== 14 && ninLength !== 15) {
                showNotification('Please enter a valid NIN', 'error');
                return;
            }
            fetch('https://daycare-management.onrender.com/auth/sitter_signup', {
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
                if (data.message === 'Sitter created successfully') {
                    showNotification('Sitter registered successfully!', 'success');
                    sitterForm.reset();
                } else {
                    showNotification('Failed to register sitter.', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('Error registering sitter.', 'error');
            });
        });
    }

      function populateTable(sitters) {
        const tableBody = document.getElementById('sittersTableBody');
        tableBody.innerHTML = ''; 
        sitters.forEach(sitter => {
            const statusButton = sitter.status === 'on_duty' ?
                `<button class="btn btn-success" disabled>Present</button>` : 
                `<button class="btn btn-primary" onclick="markPresent(${sitter.id}, this)">${sitter.status}</button>`; 

            const row = `<tr>
                <td>${sitter.name}</td>
                <td>${sitter.location}</td>
                <td>${sitter.contact}</td>
                <td>${statusButton}</td>
            </tr>`;

            tableBody.innerHTML += row; 
        });
    }

    function markPresent(sitterId, element) {
        fetch(`https://daycare-management.onrender.com/sitters/present_sitter/?sitter_id=${sitterId}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.status_code === 200) {
                element.textContent = 'Present';
                element.classList.remove('btn-primary');
                element.classList.add('btn-success');
                element.disabled = true; 
            } else {
                showNotification('Failed to mark as present', 'error');
            }
        })
        .catch(error => {
            console.error('Error marking sitter as present:', error);
            showNotification('Error marking sitter as present', 'error');
        });
    }

    function fetchAllData() {
        console.log("Fetching present babies...");
        fetch('https://daycare-management.onrender.com/babies/get_all_present_babies')
            .then(response => response.json())
            .then(data => {
                console.log("Data received:", data);
                displayPresentBabies(data.data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                showNotification("Failed to fetch data", 'error');
            });
    }

    function displayPresentBabies(presentBabies) {
        const tableBody = document.getElementById('babiesTableBody');
        tableBody.innerHTML = ''; 
        presentBabies.forEach(baby => {
            const row = `
                <tr id="baby-${baby.id}">
                    <td>${baby.name}</td>
                    <td>${baby.location}</td>
                    <td>${baby.time_of_arrival}</td>
                    <td><button class="btn btn-primary" onclick="releaseBaby(${baby.id}, ${baby.sitter_assigned})">Release</button></td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }


    function releaseBaby(babyId, sitterId) {
        const body = { baby_id: babyId, sitter_id: sitterId };
        fetch('https://daycare-management.onrender.com/babies/release_baby', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status_code === 200) {
                showNotification("Baby successfully released", 'success');
                fetchAllData(); // Refreshing the data
            } else {
                showNotification("Failed to release the baby", 'error');
            }
        })
        .catch(error => {
            console.error('Error releasing baby:', error);
            showNotification("Error releasing the baby", 'error');
        });
    }

    function fetchSitterBillDetails() {
        console.log("Fetching sitter bill ...");
        fetch('https://daycare-management.onrender.com/sitters/get_all_sitters_bill')
        .then(response => response.json())
        .then(data => populateTableBill(data.data))
        .catch(error => {
            console.error('Error fetching sitter bills:', error);
        });
    }

    function populateTableBill(data) {
        const tableBody = document.getElementById('paymentTableBody');
        tableBody.innerHTML = '';
        data.forEach(item => {
            const paymentDate = item.is_paid ? item.payment_date : 'Not Paid';
            const actionButton = item.is_paid ? 
                '<button class="btn btn-disabled" disabled>Payment Approved</button>' :
                `<button class="btn" onclick="updatePayment(${item.sitter_id})">Approve Payment</button>`;
            const row = `
                <tr>
                    <td>${item.sitter.name}</td>
                    <td>${item.sitter.contact}</td>
                    <td>${item.total_amount.toFixed(2)}</td>
                    <td>${paymentDate}</td>
                    <td>${actionButton}</td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }
    function updatePayment(sitterId) {
        fetch(`https://daycare-management.onrender.com/sitters/update_payment?sitter_id=${sitterId}`, {
            method: 'PUT'
        }).then(response => response.json())
          .then(data => {
              if (data.status_code === 200) {
                  showNotification('Payment status updated successfully', 'success');
                  fetchSitterBillDetails();  // Refresh the data
              } else {
                  showNotification('Failed to update payment status', 'error');
              }
          }).catch(error => {
              showNotification('Failed to update payment status', 'error');
          });
    }

    function searchBaby() {
        const babyAccess = document.getElementById('babyAccess').value.trim();
        if (babyAccess === '') {
            showNotification('Please enter an access number.', 'error');
            return;
        }
    
        fetch(`https://daycare-management.onrender.com/babies/get_baby_by_access?baby_access=${babyAccess}`)
        .then(response => response.json())
        .then(data => {
            if (data.status_code === 200 && data.data) {
                populateSearchBabyForm(data.data);
                showNotification('Baby found successfully!', 'success');
            } else {
                showNotification('Baby not found.', 'error');
            }
        })
        .catch(error => console.error('Error fetching baby:', error));
    }

    function populateSearchBabyForm(baby) {
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
