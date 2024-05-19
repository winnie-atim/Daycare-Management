function showNotification(message, type) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.style.backgroundColor = type === 'success' ? '#4CAF50' : '#f44336';
    notification.classList.add('show');
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

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
              showNotification('Payment status updated successfully', 'success');

              fetchSitterBillDetails();  
          } else {
              showNotification('Failed to update payment status', 'error');
          }
      }).catch(error => {
          console.error('Error updating payment status:', error);
          showNotification('Failed to update payment status', 'error');
      });
}
