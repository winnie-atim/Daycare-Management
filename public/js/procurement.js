document.addEventListener('DOMContentLoaded', function() {
    fetchProcurementItems();
});

function fetchProcurementItems() {
    fetch('http://127.0.0.1:8014/procurement/items')
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error('Error fetching procurement items:', error));
}

function createProcurementItem() {
    const formData = {
        name: document.getElementById('itemName').value,
        category: document.getElementById('category').value,
        quantity: document.getElementById('quantity').value,
        price: document.getElementById('price').value
    };

    fetch('http://127.0.0.1:8014/procurement/items', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Item added:', data);
        fetchProcurementItems();
    })
    .catch(error => console.error('Error adding item:', error));
}

function createSale() {
    const formData = {
        item_id: document.getElementById('itemId').value,
        quantity_sold: document.getElementById('quantitySold').value,
        total_amount: document.getElementById('totalAmount').value
    };

    fetch('http://127.0.0.1:8014/procurement/sales', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Sale recorded:', data);
        fetchProcurementItems();
    })
    .catch(error => console.error('Error recording sale:', error));
}
