// function loadContent(pageUrl) {
//     fetch(pageUrl)
//         .then(response => response.text())
//         .then(html => {
//             const mainContent = document.getElementById('main-content');
//             mainContent.innerHTML = html;
            
//             Array.from(mainContent.querySelectorAll("script")).forEach(oldScript => {
//                 const newScript = document.createElement("script");
//                 newScript.text = oldScript.text;
//                 oldScript.parentNode.replaceChild(newScript, oldScript);
//             });
            
//             if(pageUrl === 'presentSitter.html') {
//                 fetchSitterBillDetails();
//             }
//         })
//         .catch(error => {
//             console.error('Error loading the page: ', error);
//             mainContent.innerHTML = '<p>Error loading the content.</p>';
//         });
// }

function populateTable(data) {
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
    fetch(`http://127.0.0.1:8014/sitters/update_payment?sitter_id=${sitterId}`, {
        method: 'PUT'
    }).then(response => response.json())
      .then(data => {
          if (data.status_code === 200) {
              alert('Payment status updated successfully!');
              fetchSitterBillDetails();  // Refresh the data
          } else {
              alert('Failed to update payment status: ' + data.message);
          }
      }).catch(error => {
          console.error('Error updating payment status:', error);
          alert('Failed to update payment status.');
      });
}
