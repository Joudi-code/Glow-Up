let allProducts = []; 
let currentEditProductId = null; 

function showSection(sectionId) {
    document.querySelectorAll('main > div').forEach(div => div.style.display = 'none');
    document.getElementById(`${sectionId}-section`).style.display = 'block';
    
    document.querySelectorAll('aside .sidebar a').forEach(a => a.classList.remove('active'));
    // تفعيل الزر المناسب 
    if(sectionId === 'dashboard') document.querySelector('aside a:nth-child(1)').classList.add('active');
    if(sectionId === 'users') { fetchUsers(); document.querySelector('aside a:nth-child(2)').classList.add('active'); }
    if(sectionId === 'products') { fetchAdminProducts(); document.querySelector('aside a:nth-child(3)').classList.add('active'); }
}

async function fetchAdminProducts() {
    const res = await fetch('/api/products');
    allProducts = await res.json();
    document.getElementById('products-table-body').innerHTML = allProducts.map(p => `
        <tr>
            <td><img src="${p.image}" class="product-thumbnail"></td>
            <td>${p.name}</td>
            <td>${p.category}</td>
            <td>$${p.price}</td>
            <td>
                <a href="javascript:void(0)" class="primary" onclick="openEditModal(${p.id})">Edit</a> | 
                <a href="javascript:void(0)" class="danger" onclick="deleteProduct(${p.id})">Delete</a>
            </td>
        </tr>`).join('');
}

async function fetchUsers() {
    const token = localStorage.getItem('token');
    const res = await fetch('/api/admin/users', { headers: { 'Authorization': `Bearer ${token}` } });
    const users = await res.json();
    document.getElementById('users-table-body').innerHTML = users.map(u => `
        <tr>
            <td>${u.name}</td><td>${u.email}</td>
            <td class="warning">${u.skin_type}</td><td>${u.join_date}</td>
            <td><button onclick="deleteUser('${u.email}')" style="color:red; cursor:pointer;">Delete</button></td>
        </tr>`).join('');
}

/* Modals & Actions */
function openEditModal(id) {
    const p = allProducts.find(x => x.id === id);
    currentEditProductId = id;
    document.getElementById("modal-title").innerText = "Edit Product";
    const f = document.getElementById("product-form");
    f.elements['name'].value = p.name;
    f.elements['category'].value = p.category;
    f.elements['price'].value = p.price;
    f.elements['description'].value = p.description;
    document.getElementById("product-modal").style.display = "block";
}

document.getElementById("add-product-btn").onclick = () => {
    currentEditProductId = null;
    document.getElementById("modal-title").innerText = "Add New Product";
    document.getElementById("product-form").reset();
    document.getElementById("product-modal").style.display = "block";
};

document.querySelector(".close-modal").onclick = () => document.getElementById("product-modal").style.display = "none";

document.getElementById("product-form").onsubmit = async function(e) {
    e.preventDefault();
    const token = localStorage.getItem('token');
    const payload = {
        name: this.elements['name'].value, category: this.elements['category'].value,
        price: this.elements['price'].value, description: this.elements['description'].value,
        image: "/static/images/placeholder.jpg"
    };
    
    let url = currentEditProductId ? `/api/admin/products/${currentEditProductId}` : '/api/admin/products';
    let method = currentEditProductId ? 'PUT' : 'POST';

    const res = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
        body: JSON.stringify(payload)
    });
    if(res.ok) { alert("Success!"); document.getElementById("product-modal").style.display = "none"; fetchAdminProducts(); }
};

async function deleteProduct(id) {
    if(!confirm("Delete?")) return;
    const token = localStorage.getItem('token');
    await fetch(`/api/products/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } });
    fetchAdminProducts();
}

async function deleteUser(email) {
    if(!confirm("Delete User?")) return;
    const token = localStorage.getItem('token');
    await fetch(`/api/admin/users/${email}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } });
    fetchUsers();
}

document.addEventListener('DOMContentLoaded', () => showSection('dashboard'));