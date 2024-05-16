function loadContent(pageUrl) {
    fetch(pageUrl)
        .then(response => response.text())
        .then(html => {
            const mainContent = document.getElementById('main-content');
            mainContent.innerHTML = html;
           
            if (pageUrl === 'allSeaters.html') {
                fetchSitters();
            }
            else if (pageUrl === 'releaseBaby.html') {
                fetchAllData();
            }
        })
        .catch(error => {
            console.error('Error loading the page: ', error);
            mainContent.innerHTML = '<p>Error loading the content.</p>';
        });
      }
      function fetchSitters() {
          console.log("Fetching sitters...");
          fetch('http://127.0.0.1:8014/sitters/get_all_sitters')
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
        fetch(`http://127.0.0.1:8014/sitters/present_sitter/?sitter_id=${sitterId}`, {
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
                alert('Failed to mark as present');
            }
        })
        .catch(error => {
            console.error('Error marking sitter as present:', error);
            alert('Error marking sitter as present');
        });
    }

    function fetchAllData() {
        Promise.all([
            fetch('http://127.0.0.1:8014/babies/get_all_present_babies').then(response => response.json()),
            fetch('http://127.0.0.1:8014/babies/get_release_baby').then(response => response.json())
        ])
        .then(([presentData, releasedData]) => {
            const releasedIds = new Set(releasedData.data.map(baby => baby.baby_id));
            displayPresentBabies(presentData.data.filter(baby => !releasedIds.has(baby.id)));
        })
        .catch(error => {
            console.error('Error fetching data:', error);
            alert('Failed to fetch data.');
        });
    }

    function displayPresentBabies(presentBabies) {
        const tableBody = document.getElementById('babiesTableBody');
        tableBody.innerHTML = ''; // Clear existing entries
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
        fetch('http://127.0.0.1:8014/babies/release_baby', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status_code === 200) {
                alert('Baby successfully released!');
                fetchAllData(); // Refresh data
            } else {
                alert('Failed to release the baby: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error releasing baby:', error);
            alert('Error releasing the baby.');
        });
    }

    