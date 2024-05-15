function loadContent(pageUrl) {
    fetch(pageUrl)
        .then(response => response.text())
        .then(html => {
            const mainContent = document.getElementById('main-content');
            mainContent.innerHTML = html;
            // Initialize or re-run JavaScript if necessary
            if (pageUrl === 'allSeaters.html') {
                fetchSitters(); // Assuming this function populates the table
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