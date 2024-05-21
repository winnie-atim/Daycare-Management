document.addEventListener('DOMContentLoaded', function() {
    fetchProcurementItems();
});

function fetchProcurementItems() {
    fetch('https://daycare-management.onrender.com/procurement/items')
    .then(response => response.json())
    .then(data => {
        populateItemSelect(data.data);
        showNotification(data.message, 'success');
    })
    .catch(error => {
        console.error('Error fetching procurement items:', error);
        showNotification('Error fetching procurement items', 'error');
    });
}

function populateItemSelect(items) {
    const itemSelect = document.getElementById('itemSelect');
    itemSelect.innerHTML = '<option value="" disabled selected>Select Item</option>';
    items.forEach(item => {
        const option = document.createElement('option');
        option.value = item.id;
        option.textContent = `${item.name} (${item.category})`;
        itemSelect.appendChild(option);
    });
}

function createProcurementItem() {
    const formData = {
        name: document.getElementById('itemName').value.trim(),
        category: document.getElementById('category').value.trim(),
        quantity: document.getElementById('quantity').value.trim(),
        price: document.getElementById('price').value.trim()
    };

    fetch('https://daycare-management.onrender.com/items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Item added:', data);
        if (data.status_code === 200) {
            showNotification(data.message, 'success');
            document.getElementById('procurementForm').reset();
            fetchProcurementItems();
        } else {
            showNotification('Failed to add item: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error adding item:', error);
        showNotification('Error adding item', 'error');
    });
}

function createSale() {
    const formData = {
        item_id: document.getElementById('itemSelect').value.trim(),
        quantity_sold: document.getElementById('quantitySold').value.trim(),
        total_amount: document.getElementById('totalAmount').value.trim()
    };

    fetch('https://daycare-management.onrender.com/sales', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Sale recorded:', data);
        if (data.status_code === 200) {
            showNotification("Sale created successfully", 'success');
            document.getElementById('salesForm').reset();
            fetchProcurementItems();
        } else {
            showNotification('Failed to record sale: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error recording sale:', error);
        showNotification('Error recording sale', 'error');
    });
}

function showNotification(message, type) {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.style.backgroundColor = type === 'success' ? '#4CAF50' : '#f44336';
    notification.classList.add('show');

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}
