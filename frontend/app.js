const services = [
    { id: 'auth', endpoint: '/api/auth/' },
    { id: 'user', endpoint: '/api/users/' },
    { id: 'product', endpoint: '/api/products/' },
    { id: 'chat', endpoint: '/api/chat/' },
    { id: 'order', endpoint: '/api/orders/' }
];

async function checkStatus() {
    for (const service of services) {
        const badge = document.getElementById(`${service.id}-status`);
        try {
            const res = await fetch(service.endpoint);
            // Some endpoints might not return JSON, so we check res.ok first
            if (res.ok) {
                updateBadge(badge, 'online');
            } else {
                updateBadge(badge, 'offline');
            }
        } catch (e) {
            updateBadge(badge, 'offline');
        }
    }
}

function updateBadge(element, status) {
    element.className = `status-badge ${status}`;
    element.innerText = status;
}

async function placeOrder() {
    const msg = document.getElementById('order-msg');
    msg.style.color = 'var(--text-secondary)';
    msg.innerText = "Processing order...";
    
    try {
        const res = await fetch('/api/orders/');
        
        if (!res.ok) {
            msg.style.color = 'var(--error)';
            msg.innerText = "Order Failed: Service returned an error";
        } else {
            msg.style.color = 'var(--success)';
            msg.innerText = "Order Placed Successfully!";
        }
    } catch (e) {
        msg.style.color = 'var(--error)';
        msg.innerText = "Order Failed: Service unreachable";
    }
    
    // Refresh statuses immediately after placing an order
    checkStatus();
}

// Initial status check
checkStatus();

// Poll every 5 seconds to keep dashboard live
setInterval(checkStatus, 5000);
