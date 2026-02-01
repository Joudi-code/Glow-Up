/* === Navbar === */
const menu = document.querySelector('#glow-menu');
const menuLinks = document.querySelector('.navbar__menu');
if (menu && menuLinks) {
    menu.addEventListener('click', () => {
        menu.classList.toggle('is-active');
        menuLinks.classList.toggle('active');
    });
}

/* === Input Animations === */
function handleInputAnimation() {
    document.querySelectorAll(".auth-input").forEach(input => {
        if (input.value !== "") input.parentNode.parentNode.classList.add("focus");
        input.addEventListener("focus", () => input.parentNode.parentNode.classList.add("focus"));
        input.addEventListener("blur", () => {
            if (input.value == "") input.parentNode.parentNode.classList.remove("focus");
        });
    });
}
document.addEventListener("DOMContentLoaded", handleInputAnimation);

/* === Search === */
const searchInput = document.getElementById('searchBox');
if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase().trim();
        document.querySelectorAll('.products__cards').forEach(card => {
            card.style.display = card.innerText.toLowerCase().includes(term) ? "flex" : "none";
        });
    });
}

/* === Skin Test === */
async function getSkinType() {
    const answers = document.querySelectorAll('input[type="radio"]:checked');
    if (answers.length < 4) { alert("Please answer all questions!"); return; }

    let scores = { dry: 0, oily: 0, combination: 0, sensitive: 0 };
    answers.forEach(a => scores[a.value]++);
    let skinType = Object.keys(scores).reduce((a, b) => scores[a] > scores[b] ? a : b);
    
    const typeMapping = {
        'oily': 'دهنية (Oily)', 'dry': 'جافة (Dry)',
        'combination': 'مختلطة (Combination)', 'sensitive': 'حساسة (Sensitive)'
    };

    localStorage.setItem('userSkinType', skinType.toLowerCase());
    
    const token = localStorage.getItem('token');
    if (token) {
        await fetch('/api/skin-test', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
            body: JSON.stringify({ skin_type: skinType })
        });
    }

    const resDiv = document.getElementById("resultContainer");
    if (resDiv) {
        document.getElementById("result").innerText = `نوع بشرتك: ${typeMapping[skinType]}`;
        resDiv.style.display = "block";
        resDiv.scrollIntoView({ behavior: 'smooth' });
    }
}

/* === Routines DB (Matching IDs) === */
const routinesDB = {
    oily: {
        name: "الدهنية (Oily)",
        morning: [
            { title: "التنظيف", desc: "غسول رغوي عميق.", product: "Anua Foam", img: "/static/images/Anua heartleaf quercetinol pore deep cleansing foam.jpg", id: 1 },
            { title: "التونر", desc: "موازن للـ pH.", product: "Anua Toner", img: "/static/images/Anua - Heartleaf 77 - Verzachtende toner, 250ml-Geen kleur.jpg", id: 2 },
            { title: "الحماية", desc: "واقي شمس خفيف.", product: "Suncream", img: "/static/images/واقي شمسي بشرة دهنية.jpg", id: 5 }
        ],
        night: [
            { title: "تنظيف مزدوج", desc: "مزيل مكياج زيتي.", product: "Cleansing Oil", img: "/static/images/ANUA Heartleaf Pore Control Cleansing Oil _ K-Beauty Gentle Makeup Remover.jpg", id: 3 },
            { title: "علاج", desc: "سيروم الأزيليك.", product: "Azelaic Serum", img: "/static/images/Anua Azelaic Acid 15+ Intense Calming Serum (Ingredients Explained).jpg", id: 6 },
            { title: "الترطيب", desc: "لوشن خفيف.", product: "Anua Lotion", img: "/static/images/مرطب بشرة دهنية ومختلطة.jpg", id: 4 }
        ]
    },
    dry: {
        name: "الجافة (Dry)",
        morning: [
            { title: "التنظيف", desc: "غسول كريمي.", product: "Centella Foam", img: "/static/images/غسول بشرة حساسة (2).jpg", id: 9 },
            { title: "الترطيب", desc: "كريم غني.", product: "Intense Cream", img: "/static/images/مرطب بشرة جافة.jpg", id: 11 },
            { title: "الحماية", desc: "واقي شمس مرطب.", product: "Silky Sunscreen", img: "/static/images/واقي شمسي للبشرة الجافة.jpg", id: 10 }
        ],
        night: [
            { title: "التنظيف", desc: "منظف زيتي.", product: "Cleansing Oil", img: "/static/images/ANUA Heartleaf Pore Control Cleansing Oil _ K-Beauty Gentle Makeup Remover.jpg", id: 3 },
            { title: "تهدئة", desc: "أمبولة السنتيلا.", product: "Centella Ampoule", img: "/static/images/سيروم بشرة حساسة.jpg", id: 12 },
            { title: "ترطيب عميق", desc: "كريم ليلي.", product: "Intense Cream", img: "/static/images/مرطب بشرة جافة.jpg", id: 11 }
        ]
    },
    combination: {
        name: "المختلطة (Combination)",
        morning: [
            { title: "التنظيف", desc: "غسول متوازن.", product: "Anua Foam", img: "/static/images/Anua heartleaf quercetinol pore deep cleansing foam.jpg", id: 1 },
            { title: "الحماية", desc: "واقي مائي.", product: "Sun Serum", img: "/static/images/واقي شمسي بشرة مختلطة.jpg", id: 13 }
        ],
        night: [
            { title: "ترطيب", desc: "سيروم مائي.", product: "Blue Serum", img: "/static/images/سيروم بشرة مختلطة.jpg", id: 14 },
            { title: "الترطيب", desc: "لوشن يومي.", product: "Anua Lotion", img: "/static/images/مرطب بشرة دهنية ومختلطة.jpg", id: 4 }
        ]
    },
    sensitive: {
        name: "الحساسة (Sensitive)",
        morning: [
            { title: "التنظيف", desc: "غسول لطيف.", product: "Centella Foam", img: "/static/images/غسول بشرة حساسة (2).jpg", id: 9 },
            { title: "تهدئة", desc: "أمبولة مهدئة.", product: "Ampoule", img: "/static/images/سيروم بشرة حساسة.jpg", id: 12 }
        ],
        night: [
            { title: "الترطيب", desc: "كريم مهدئ.", product: "Soothing Cream", img: "/static/images/مرطب بشرة حساسة.jpg", id: 15 }
        ]
    }
};

/* === Routine Rendering === */
const routineContainer = document.getElementById('routineContainer');
if (routineContainer) {
    let type = localStorage.getItem('userSkinType');
    const display = document.getElementById('userSkinTypeDisplay');
    const map = { 'oily': 'الدهنية (Oily)', 'dry': 'الجافة (Dry)', 'combination': 'المختلطة (Combination)', 'sensitive': 'الحساسة (Sensitive)' };

    if (!type || !routinesDB[type]) {
        routineContainer.innerHTML = `<div style="text-align:center; padding:50px;"><h2>لم تقومي بالاختبار!</h2><a href="/skintest" class="main__btn" style="max-width:200px; margin-top:20px;">اذهبي للاختبار</a></div>`;
    } else {
        if (display) display.innerText = map[type];
        renderRoutineSteps(routinesDB[type].morning);
    }
}

function switchRoutine(time) {
    let type = localStorage.getItem('userSkinType');
    if (type && routinesDB[type]) {
        renderRoutineSteps(routinesDB[type][time]);
        document.getElementById('btnMorning').classList.toggle('active', time === 'morning');
        document.getElementById('btnNight').classList.toggle('active', time === 'night');
    }
}

function renderRoutineSteps(steps) {
    const container = document.getElementById('routineContainer');
    if (!container) return;
    container.innerHTML = steps.map((step, i) => `
        <div class="step-card">
            <div class="step-number">${i + 1}</div>
            <h3 class="step-title">${step.title}</h3>
            <p class="step-desc">${step.desc}</p>
            <div class="product-suggestion">
                <img src="${step.img}" onerror="this.src='/static/images/placeholder.jpg'">
                <div class="suggestion-info">
                    <h4>نصيحتنا: استخدمي ${step.product}</h4>
                    <a href="/product-details?id=${step.id}" class="suggestion-link">عرض تفاصيل المنتج <i class="fa-solid fa-arrow-left"></i></a>
                </div>
            </div>
        </div>`).join('');
}

/* === Display Products === */
async function displayProducts() {
    const container = document.getElementById('products-container');
    if (!container) return;
    try {
        const res = await fetch('/api/products');
        const products = await res.json();
        container.innerHTML = products.map(p => `
            <div class="products__cards">
                <h3>${p.category}</h3>
                <img src="${p.image}" alt="${p.name}" onerror="this.src='/static/images/placeholder.jpg'">
                <p class="product__name">${p.name}</p>
                <p class="product__price">Price: $${p.price}</p>
                <a href="/product-details?id=${p.id}" class="main__btn">عرض التفاصيل</a>
            </div>`).join('');
    } catch (e) { console.error(e); }
}

/* === Product Details === */
document.addEventListener('DOMContentLoaded', async () => {
    displayProducts();
    const container = document.getElementById('detailsContainer');
    if (!container) return;
    const id = new URLSearchParams(window.location.search).get('id');
    if (!id) return;

    try {
        const res = await fetch(`/api/products/${id}`);
        const p = await res.json();
        container.innerHTML = `
            <div class="details-wrapper">
                <div class="details-image"><img src="${p.image}"></div>
                <div class="details-info">
                    <h1>${p.name}</h1>
                    <p class="details-price">$${p.price}</p>
                    <div class="category-badge">${p.category}</div>
                    <p class="details-desc">${p.description}</p>
                    <div class="ingredients-box"><h4>🌿 المكونات الفعالة:</h4><ul><li>${p.ingredients || 'غير متوفر'}</li></ul></div>
                    <a href="/products" class="back-btn">عودة للمنتجات</a>
                </div>
            </div>`;
    } catch (e) { container.innerHTML = "<h2>المنتج غير موجود</h2>"; }
});

/* === Login Logic === */
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        
        try {
            const res = await fetch('/api/login', {
                method: 'POST', 
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();
            
            if (data.status === "success") {
                // حفظ البيانات الأساسية
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('userRole', data.role);
                localStorage.setItem('username', data.username);

                if (data.skin_type) {
                    localStorage.setItem('userSkinType', data.skin_type);
                } else {
                    // إذا كان المستخدم جديداً ولم يحدد بشرته، نمسح القديم
                    localStorage.removeItem('userSkinType');
                }
                // ---------------------------------------------

                alert(`مرحباً ${data.username}!`);
                window.location.href = data.role === 'admin' ? '/admin' : '/';
            } else { 
                alert(data.message); 
            }
        } catch (e) { 
            console.error(e);
            alert("حدث خطأ في الاتصال بالسيرفر"); 
        }
    });
}

/* === Signup Logic === */
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            name: document.getElementById('signupName').value,
            email: document.getElementById('signupEmail').value,
            password: document.getElementById('signupPassword').value,
            skin_type: document.getElementById('signupSkin').value
        };
        try {
            const res = await fetch('/api/signup', {
                method: 'POST', headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) { alert("Account created!"); window.location.href = '/login'; }
            else { const d = await res.json(); alert(d.message); }
        } catch (e) { alert("Error"); }
    });
}
/* =========================================
   9. كود إدارة زر الخروج (Logout Logic)
   ========================================= */
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    const logoutLi = document.getElementById('logoutLi');
    const loginBtn = document.querySelector('a[href="/login"]'); // زر الدخول الموجود أصلاً
    const signupBtn = document.querySelector('a[href="/signup"]'); // زر التسجيل الموجود أصلاً

    // 1. التحكم في ظهور الأزرار
    if (token) {
        // إذا كان المستخدم مسجلاً: أظهر الخروج وأخفِ الدخول والتسجيل
        if (logoutLi) logoutLi.style.display = 'flex';
        if (loginBtn) loginBtn.parentElement.style.display = 'none';
        if (signupBtn) signupBtn.parentElement.style.display = 'none';
    } else {
        // إذا لم يكن مسجلاً: العكس
        if (logoutLi) logoutLi.style.display = 'none';
        if (loginBtn) loginBtn.parentElement.style.display = 'flex';
        if (signupBtn) signupBtn.parentElement.style.display = 'flex';
    }

    // 2. برمجة عملية الخروج
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            
            localStorage.clear(); 
            // -----------------------------

            alert("تم تسجيل الخروج بنجاح");
            window.location.href = '/login';
        });
    }
});