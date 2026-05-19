const btnSmart = document.getElementById('btn-smart');
const btnGoManual = document.getElementById('btn-go-manual');
const resultsSection = document.getElementById('results');
const buildGrid = document.getElementById('build-grid');
const buildTotal = document.getElementById('build-total');
const inputBudget = document.getElementById('budget-input');
const selectUse = document.getElementById('use-select');
const selectRes = document.getElementById('res-select');
const selectGame = document.getElementById('game-select');
const togglePeripherals = document.getElementById('peripherals-toggle');

// === ЛОГІКА ДЛЯ РАМКИ ВІКНА ПЕРИФЕРІЇ (З'являється тільки при увімкненні) ===

// Знаходимо батьківський елемент `.toggle-wrapper`
const toggleWrapperElem = togglePeripherals.closest('.toggle-wrapper');

if (togglePeripherals && toggleWrapperElem) {
    // Слухаємо зміну стану тумблера
    togglePeripherals.addEventListener('change', function() {
        if (this.checked) {
            // Додаємо клас для активації рамки
            toggleWrapperElem.classList.add('active-border');
        } else {
            // Прибираємо клас
            toggleWrapperElem.classList.remove('active-border');
        }
    });

    // Ініціалізуємо стан при завантаженні (якщо тумблер увімкнено за замовчуванням)
    if (togglePeripherals.checked) {
        toggleWrapperElem.classList.add('active-border');
    }
}

// === ЛОГІКА ЗАЛЕЖНИХ СПИСКІВ (Ціль -> Ігри/ПЗ) ===

// Зберігаємо всі оригінальні опції в масив, щоб вони не загубилися при фільтрації
const allGameOptions = Array.from(selectGame.options);

// Слухаємо зміну цілі
selectUse.addEventListener('change', function() {
    const selectedCategory = this.value;

    // 1. Очищаємо другий список
    selectGame.innerHTML = '';

    // 2. Перебираємо збережені опції та повертаємо тільки потрібні
    allGameOptions.forEach(option => {
        // Якщо вибрано "Будь-яка ціль", або опція підходить під обрану категорію, або це універсальна збірка
        if (selectedCategory === 'All' || option.dataset.category === 'All' || option.dataset.category === selectedCategory) {
            // Клонуємо елемент і додаємо його назад у список
            selectGame.appendChild(option.cloneNode(true));
        }
    });
    
    // 3. Скидаємо вибір на першу опцію в списку
    selectGame.selectedIndex = 0;
});

const API_BASE_URL = 'https://cybercraft-3ldd.onrender.com/api';
const BACKEND_URL = 'https://cybercraft-3ldd.onrender.com';
const getCompName = (comp) => {
    if (!comp) return 'Стандартна деталь';
    
    let baseName = comp.name || ((comp.brand || '') + ' ' + (comp.model || '')).trim() || 'Інше';
    
    // Додаємо форм-фактор для материнських плат
    if (comp.form) baseName += ` (${comp.form})`;
    if (comp.form_factor) baseName += ` (${comp.form_factor})`;
    
    // Додаємо тип та інтерфейс для накопичувачів
    if (comp.s_type) baseName += ` ${comp.s_type}`;
    if (comp.interface) baseName += ` ${comp.interface}`;

    // Додаємо об'єм (для RAM та Storage)
    const capacity = comp.cap || comp.capacity;
    if (capacity) baseName += ` ${capacity}GB`;

    return baseName.trim();
};
const getCompBrand = (comp) => {
    if (comp.brand && comp.brand.trim() !== '') return comp.brand.trim();
    if (comp.name && comp.name.trim() !== '') return comp.name.trim().split(' ')[0];
    return 'Інше';
};

function createComponentCard(type, component, delayIndex) {
    if (!component) return '';
    return `
        <div class="component-card" style="animation-delay: ${delayIndex * 0.1}s">
            <div>
                <div class="comp-type">${type}</div>
                <div class="comp-name">${component.name}</div>
            </div>
            <div class="comp-price">${component.price} ₴</div>
        </div>
    `;
}

// === ЛОГІКА КАСТОМНОГО ВІКНА ПОВІДОМЛЕНЬ (Помилка / Успіх) ===
// =========================================================
// === ЛОГІКА КАСТОМНОГО ВІКНА ПОВІДОМЛЕНЬ (Помилка / Успіх) ===
// =========================================================
const errorModal = document.getElementById('error-modal');
const btnCloseError = document.getElementById('btn-close-error');

function showErrorAlert(title, message, type = 'error') {
    document.getElementById('error-title').innerText = title;
    document.getElementById('error-message').innerText = message;
    
    const iconSvg = document.querySelector('.alert-icon svg');
    const iconBox = document.querySelector('.alert-icon');
    const titleText = document.getElementById('error-title');

    if (type === 'success') {
        titleText.style.color = '#4ade80'; // Зелений
        iconBox.style.background = 'rgba(34, 197, 94, 0.1)';
        iconSvg.style.stroke = '#4ade80';
        iconSvg.style.filter = 'drop-shadow(0 0 8px rgba(34, 197, 94, 0.6))';
        // Зелена галочка
        iconSvg.innerHTML = '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>';
    } else {
        titleText.style.color = '#f8fafc'; // Білий/Червоний
        iconBox.style.background = 'rgba(239, 68, 68, 0.1)';
        iconSvg.style.stroke = '#ef4444';
        iconSvg.style.filter = 'drop-shadow(0 0 8px rgba(239, 68, 68, 0.6))';
        // Червоний хрестик
        iconSvg.innerHTML = '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line>';
    }

    errorModal.classList.add('active');
}

// 1. Закриття вікна по кнопці "Зрозуміло"
if (btnCloseError) {
    btnCloseError.addEventListener('click', () => {
        errorModal.classList.remove('active');
    });
}

// 2. Закриття вікна по кліку на темний фон поза ним
if (errorModal) {
    errorModal.addEventListener('click', (e) => {
        if (e.target === errorModal) {
            errorModal.classList.remove('active');
        }
    });
}
// =========================================================

async function fetchSmartBuild() {
    const budgetInputElem = document.getElementById('budget-input');
    const budgetValue = parseFloat(budgetInputElem.value);
    const primaryUse = selectUse.value;
    const resolution = selectRes.value;
    const gameName = selectGame.value;
    const includePeripherals = togglePeripherals.checked;

    // 1. ПРИБРАЛИ ЖОРСТКЕ ОБМЕЖЕННЯ 10 000. 
    // Залишили тільки базову перевірку, щоб користувач хоч щось ввів.
    if (isNaN(budgetValue) || budgetValue <= 0) {
        showErrorAlert("Помилка вводу", "Будь ласка, введіть коректну суму бюджету.");
        return;
    }

    try {
        btnSmart.innerText = "Аналізуємо ринок...";
        btnSmart.disabled = true;

        let endpoint = '/smart/auto-build';
        let requestBody = { target_budget: budgetValue, preference_brand: null };

        if (primaryUse !== "Gaming" || gameName !== "Standard") {
            endpoint = '/smart/purpose-build';
            requestBody = {
                target_budget: budgetValue, 
                primary_use: primaryUse,
                specific_software: gameName,
                performance_level: "Recommended",
                resolution: resolution
            };
        }

        // Запит за ПК
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody)
        });

        // 2. ЧИТАЄМО ВІДПОВІДЬ ВІД СЕРВЕРА
        const data = await response.json();

        // 3. ЯКЩО БЕКЕНД СКАЗАВ, ЩО ГРОШЕЙ МАЛО (Наприклад, статус 400)
        if (!response.ok) {
            // Виводимо наше гарне червоне вікно з текстом помилки від Python-сервера
            const errorMsg = data.error || "На жаль, за цей бюджет неможливо підібрати комплектуючі. Спробуйте збільшити суму.";
            showErrorAlert("Недостатньо коштів", errorMsg);
            
            // Зупиняємо виконання, щоб ПК не малювався
            btnSmart.innerText = "Зібрати автоматично";
            btnSmart.disabled = false;
            return; 
        }

        lastSmartBuild = data;
        
        // 4. ЯКЩО ВСЕ ДОБРЕ - МАЛЮЄМО ЗБІРКУ
        buildGrid.innerHTML = ''; 
        let html = '';
        let finalPrice = data.total_price;

        html += createComponentCard('Процесор', data.cpu, 1);
        html += createComponentCard('Відеокарта', data.gpu, 2);
        html += createComponentCard('Материнська плата', data.motherboard, 3);
        html += createComponentCard('Оперативна пам\'ять', data.ram, 4);
        html += createComponentCard('Накопичувач', data.storage, 5);
        html += createComponentCard('Блок живлення', data.psu, 6);
        html += createComponentCard('Корпус', data.case, 7);
        html += createComponentCard('Охолодження', data.cooler, 1,5);

        // Периферія (якщо увімкнена)
        // Периферія (якщо увімкнена)
        if (includePeripherals) {
            const [miceRes, kbdRes, headRes] = await Promise.all([
                fetch(`${API_BASE_URL}/peripherals/mice`),
                fetch(`${API_BASE_URL}/peripherals/keyboards`),
                fetch(`${API_BASE_URL}/peripherals/headsets`)
            ]);
            
            const mice = await miceRes.json();
            const kbds = await kbdRes.json();
            const heads = await headRes.json();

            if(mice.length > 0) { 
                data.mouse = mice[0]; // Прикріплюємо мишу до об'єкта збірки
                html += createComponentCard('Миша', {name: getCompName(mice[0]), price: mice[0].price}, 8); 
                finalPrice += mice[0].price; 
            }
            if(kbds.length > 0) { 
                data.keyboard = kbds[0]; // Прикріплюємо клавіатуру до об'єкта збірки
                html += createComponentCard('Клавіатура', {name: getCompName(kbds[0]), price: kbds[0].price}, 9); 
                finalPrice += kbds[0].price; 
            }
            if(heads.length > 0) { 
                data.headset = heads[0]; // Прикріплюємо гарнітуру до об'єкта збірки
                html += createComponentCard('Гарнітура', {name: getCompName(heads[0]), price: heads[0].price}, 10); 
                finalPrice += heads[0].price; 
            }
        }

        // Оновлюємо фінальну ціну в об'єкті збірки
        data.total_price = finalPrice;

        // ВАЖЛИВО: Зберігаємо об'єкт для експорту ТІЛЬКИ ТЕПЕР, коли в ньому є периферія і нова ціна!
        lastSmartBuild = data;


        buildGrid.innerHTML = html;
        
       buildTotal.innerHTML = `
            <span class="smart-total-title">Загальна приблизна вартість:</span> <span class="smart-total-price">${finalPrice} ₴</span> 
            <br><span style="font-size: 16px; color: var(--text-muted); display: inline-block; margin-top: 10px;">Оцінка продуктивності: ${data.performance_score || 0} балів</span>
            
            <button class="btn-primary w-100 glow-effect" 
                    onclick="saveBuildToDB('smart')" 
                    style="margin-top: 25px; font-size: 16px;">
                Зберегти збірку
            </button>
            
            <div class="export-section" style="margin-top: 25px; padding-top: 25px; border-top: 1px solid rgba(255,255,255,0.1);">
                <h4 style="font-size: 14px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 15px; letter-spacing: 1px; text-align: center;">Експорт збірки</h4>
                <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
                    <button class="btn-export pdf" onclick="exportBuild('pdf', 'smart')">
                        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                        Чек
                    </button>
                    <button class="btn-export md" onclick="exportBuild('md', 'smart')">
                        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
                        Форум (MD)
                    </button>
                    <button class="btn-export link" onclick="exportBuild('link', 'smart')">
                        <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                        Посилання
                    </button>
                </div>
            </div>
        `;

        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
        console.error(error);
        showErrorAlert("Помилка мережі", "Не вдалося зв'язатися з сервером. Перевірте, чи запущений app.py!");
    } finally {
        btnSmart.innerText = "Зібрати автоматично";
        btnSmart.disabled = false;
    }
}

if (btnSmart) btnSmart.addEventListener('click', fetchSmartBuild);

// --- ЛОГІКА НАВІГАЦІЇ (SPA) ---
const pages = {
    'nav-config': document.getElementById('page-home'),
    'nav-manual': document.getElementById('page-manual'),
    'nav-compare': document.getElementById('page-compare'),
    'nav-bench': document.getElementById('page-bench'),
    'nav-thermal': document.getElementById('page-thermal'),
    'nav-analytics': document.getElementById('page-analytics')
};

function switchPage(targetId) {
    // Ховаємо всі сторінки і знімаємо active
    Object.keys(pages).forEach(navId => {
        const link = document.getElementById(navId);
        if(link) link.classList.remove('active');
        if(pages[navId]) pages[navId].classList.add('hidden');
    });

    // Активуємо потрібну
    const activeLink = document.getElementById(targetId);
    if(activeLink) activeLink.classList.add('active');
    if(pages[targetId]) pages[targetId].classList.remove('hidden');
}

const navLogo = document.getElementById('nav-logo');
const footerLogo = document.getElementById('footer-logo');

function goHome() {
    switchPage('nav-config'); // Перемикаємо на вкладку "Розумна збірка"
    window.scrollTo({ top: 0, behavior: 'smooth' }); // Плавно скролимо на самий верх сторінки
}

if (navLogo) navLogo.addEventListener('click', goHome);
if (footerLogo) footerLogo.addEventListener('click', goHome);

// Прив'язуємо кліки по меню
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        switchPage(e.target.id);
    });
});

// Кнопка "Зібрати власноруч" на головній перекидає на сторінку ручної збірки
if (btnGoManual) {
    btnGoManual.addEventListener('click', () => {
        switchPage('nav-manual');
    });
}

// ====================================================
// === ЛОГІКА РУЧНОЇ ЗБІРКИ (МОДАЛЬНЕ ВІКНО) ===
// ====================================================

const manualState = { cpu: null, motherboard: null, gpu: null, ram: null, cooler: null, storage: null, psu: null, case: null, mouse: null, keyboard: null, headset: null };
const apiEndpoints = {
    cpu: '/cpus', motherboard: '/motherboards', gpu: '/gpus', ram: '/rams',
    cooler: '/coolers', storage: '/storage', psu: '/psus', case: '/cases',
    mouse: '/peripherals/mice', keyboard: '/peripherals/keyboards', headset: '/peripherals/headsets'
};

const modal = document.getElementById('component-modal');
const btnCloseModal = document.getElementById('close-modal');
const modalItemsList = document.getElementById('modal-items-list');
const modalBrandFilter = document.getElementById('modal-brand-filter');
const modalSearch = document.getElementById('modal-search');

let currentSelectingType = null;
let currentModalData = [];

// 1. Відкриття модального вікна при кліку на кнопку "Обрати"
// 1. Відкриття модального вікна при кліку на кнопку "Обрати"
// 1. Відкриття модального вікна при кліку на кнопку "Обрати"
document.querySelectorAll('.slot-card .btn-secondary').forEach(btn => {
    btn.addEventListener('click', async (e) => {
        const slotCard = e.target.closest('.slot-card');
        currentSelectingType = slotCard.dataset.type;
        
        document.getElementById('modal-title').innerText = slotCard.querySelector('h4').innerText;
        modalItemsList.innerHTML = '<p style="text-align:center; padding: 20px; color: var(--accent-cyan);">Завантаження бази даних...</p>';
        
        // ВАЖЛИВО: Очищаємо масив перед новим запитом, щоб не вилазили старі деталі при помилках!
        currentModalData = []; 
        
      // --- ДИНАМІЧНИЙ ФІЛЬТР (ЗАЛИШИЛИ ТІЛЬКИ ДЛЯ ОЗУ) ---
        const dynamicContainer = document.getElementById('dynamic-filter-container');
        if (dynamicContainer) {
            dynamicContainer.style.display = 'none';
            dynamicContainer.innerHTML = '';

            if (currentSelectingType === 'ram') {
                dynamicContainer.style.display = 'block';
                dynamicContainer.innerHTML = `
                    <select id="modal-dynamic-filter" class="modern-select" style="width: 100%;">
                        <option value="">Будь-який об'єм</option>
                        <option value="8">8 GB</option>
                        <option value="16">16 GB</option>
                        <option value="32">32 GB</option>
                        <option value="64">64 GB</option>
                    </select>
                `;
            }
            const dynFilter = document.getElementById('modal-dynamic-filter');
            if (dynFilter) dynFilter.addEventListener('change', () => renderModalItems(currentModalData));
        }
        // ---------------------------
        // ---------------------------

        // --- Скидаємо сортування на "від дешевшого" при відкритті вікна ---
        const sortBtn = document.getElementById('modal-sort-price');
        if (sortBtn) sortBtn.setAttribute('data-order', 'asc');


        modal.classList.add('active'); 

        try {
            const res = await fetch(`${API_BASE_URL}${apiEndpoints[currentSelectingType]}`);
            if (!res.ok) throw new Error("Помилка мережі");
            currentModalData = await res.json();
            
            populateBrands(currentModalData); 
            renderModalItems(currentModalData); 
        } catch (err) {
            console.error(err);
            modalItemsList.innerHTML = '<p style="color:#ef4444; text-align:center;">Не вдалося завантажити деталі з сервера.</p>';
        }
    });
});

// 2. Закриття вікна
if (btnCloseModal) btnCloseModal.addEventListener('click', () => modal.classList.remove('active'));
if (modal) {
    modal.addEventListener('click', (e) => { 
        if(e.target === modal) modal.classList.remove('active'); 
    });
}

// 3. Заповнення списку брендів (динамічно)
// 3. Заповнення списку брендів (розумний пошук брендів)
// 3. Заповнення списку брендів (розумний пошук брендів)
// 3. Заповнення списку брендів (розумний пошук брендів)
function populateBrands(items) {
    // Використовуємо нашу нову функцію getCompBrand
    const brands = [...new Set(items.map(i => getCompBrand(i)))].sort(); 

    modalBrandFilter.innerHTML = '<option value="">Всі бренди</option>' + 
        brands.map(b => `<option value="${b}">${b}</option>`).join('');
}

// 4. Малювання товарів у вікні (з урахуванням фільтрів)
// 4. Малювання товарів у вікні (з урахуванням фільтрів)
// 4. Малювання товарів у вікні (з урахуванням фільтрів)
// 4. Малювання товарів у вікні (з урахуванням фільтрів)
// 4. Малювання товарів у вікні (УНІВЕРСАЛЬНИЙ ФІЛЬТР)
// 4. Малювання товарів у вікні (УНІВЕРСАЛЬНИЙ ФІЛЬТР)
// 4. Малювання товарів у вікні (ІДЕАЛЬНИЙ ФІЛЬТР ПО БАЗІ ДАНИХ)
// 4. Малювання товарів у вікні (БРОНЕБІЙНИЙ ФІЛЬТР)
// 4. Малювання товарів у вікні
function renderModalItems(items) {
    const filterBrand = modalBrandFilter.value.toLowerCase();
    const filterSearch = modalSearch.value.toLowerCase();
    
    // Читаємо значення динамічного фільтру
    const dynFilterEl = document.getElementById('modal-dynamic-filter');
    const filterDynamic = dynFilterEl ? dynFilterEl.value.toLowerCase() : "";
    
    const filtered = items.filter(item => {
        const itemBrand = getCompBrand(item).toLowerCase();
        const matchBrand = filterBrand ? itemBrand === filterBrand : true;
        
        // Збираємо АБСОЛЮТНО ВСІ значення деталі в один суцільний текст для пошуку
        const allValuesText = Object.values(item).map(v => String(v).toLowerCase()).join(' ');
        
        // Пошук по тексту
        const matchSearch = filterSearch ? allValuesText.includes(filterSearch) : true;
        
        // --- ДИНАМІЧНИЙ ФІЛЬТР (ТІЛЬКИ RAM) ---
        let matchDynamic = true;
        if (filterDynamic && currentSelectingType === 'ram') {
            const cleanText = allValuesText.replace(/[\s-]/g, '');
            const cap = item.capacity || item.cap || null;
            if (cap) {
                matchDynamic = String(cap) === filterDynamic;
            } else {
                matchDynamic = cleanText.includes(filterDynamic + 'gb') || cleanText.includes(filterDynamic + 'гб');
            }
        }

        return matchBrand && matchSearch && matchDynamic;
    });

    const sortBtn = document.getElementById('modal-sort-price');
    const sortOrder = sortBtn ? sortBtn.getAttribute('data-order') : 'asc';

    filtered.sort((a, b) => {
        if (sortOrder === 'asc') {
            return a.price - b.price; // Від дешевшого до дорожчого
        } else {
            return b.price - a.price; // Від дорожчого до дешевшого
        }
    });

    if (filtered.length === 0) {
        modalItemsList.innerHTML = '<p style="text-align:center; padding: 20px; color: var(--text-muted);">Нічого не знайдено за цими фільтрами.</p>';
        return;
    }

    modalItemsList.innerHTML = filtered.map(item => `
        <div class="comp-list-item" onclick='selectComponent(${JSON.stringify(item).replace(/'/g, "&apos;")})'>
            <div class="item-info">
                <div class="item-name">${getCompName(item)}</div>
            </div>
            <div class="item-actions" style="display: flex; align-items: center; gap: 15px;">
                <div class="item-price" style="margin: 0;">${item.price} ₴</div>
                <button class="btn-info" title="Характеристики" onclick='showSpecs(event, ${JSON.stringify(item).replace(/'/g, "&apos;")})' style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); color: var(--accent-cyan); width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.3s;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 18px; height: 18px;">
                        <circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>
                    </svg>
                </button>
            </div>
        </div>
    `).join('');
}

// === ЛОГІКА ВІКНА ХАРАКТЕРИСТИК ===
// === ЛОГІКА ВІКНА ХАРАКТЕРИСТИК ===
// === ЛОГІКА ВІКНА ХАРАКТЕРИСТИК ===
window.showSpecs = function(event, item) {
    event.stopPropagation(); // Зупиняємо клік
    
    document.getElementById('specs-title').innerText = getCompName(item);
    
    let html = '<ul class="specs-list" style="list-style: none; padding: 0;">';
    
    const skipKeys = ['id', 'name', 'brand', 'model', 'price', 'image_url', 'cpu_mark', 'gpu_mark'];
    
    // Словник, який враховує ВСІ можливі назви (і з Dataclass, і з БД)
    const dict = {
        'socket': 'Сокет', 'chipset': 'Чипсет', 
        'form': 'Форм-фактор', 'form_factor': 'Форм-фактор',
        'slots': 'Кількість слотів', 
        'memory_type': 'Підтримка пам\'яті', 
        'cap': 'Об\'єм (ГБ)', 'capacity': 'Об\'єм (ГБ)',
        'r_type': 'Тип пам\'яті', 
        's_type': 'Тип накопичувача', 'storage_type': 'Тип накопичувача', 'type': 'Тип накопичувача',
        'interface': 'Інтерфейс', 
        'core_count': 'Кількість ядер', 'thread_count': 'Кількість потоків',
        'base_clock_ghz': 'Базова частота (ГГц)', 'boost_clock_ghz': 'Turbo частота (ГГц)',
        'tdp': 'Тепловиділення (TDP)', 'integrated_graphics': 'Вбудована графіка',
        'vram_gb': 'Відеопам\'ять (GB)', 'core_clock_mhz': 'Частота ядра (МГц)',
        'length_mm': 'Довжина (мм)', 'speed': 'Швидкість/Частота',
        'modules': 'Кількість модулів', 'wattage': 'Потужність (Вт)', 'efficiency_rating': 'Сертифікат',
        'modular': 'Модульність', 'read_speed_mbps': 'Читання (МБ/с)',
        'write_speed_mbps': 'Запис (МБ/с)', 'size': 'Розмір', 'dpi': 'DPI',
        'switch_type': 'Світчі', 'connection_type': 'Підключення'
    };

    for (const [key, value] of Object.entries(item)) {
        if (!skipKeys.includes(key) && value !== null && value !== '' && value !== false) {
            const displayName = dict[key] || key.replace(/_/g, ' ');
            const displayValue = value === true ? "Так" : value;
            
            html += `
            <li style="padding: 12px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); display: flex; justify-content: space-between; align-items: center;">
                <span class="spec-key" style="color: var(--text-muted); font-size: 13px; text-transform: uppercase; letter-spacing: 1px;">${displayName}</span>
                <span class="spec-val" style="color: var(--text-main); font-weight: 600; font-size: 15px; text-align: right; max-width: 60%;">${displayValue}</span>
            </li>`;
        }
    }
    html += '</ul>';
    
    document.getElementById('specs-content').innerHTML = html;
    const sModal = document.getElementById('specs-modal');
    if (sModal) sModal.classList.add('active');
};

// Закриття вікна характеристик (через делегування)
document.addEventListener('click', (e) => {
    const sModal = document.getElementById('specs-modal');
    if (!sModal) return;
    if (e.target.id === 'btn-close-specs' || e.target === sModal) {
        sModal.classList.remove('active');
    }
});

// 5. Події фільтрації
// 5. Події фільтрації та сортування
if (modalBrandFilter) modalBrandFilter.addEventListener('change', () => renderModalItems(currentModalData));
if (modalSearch) modalSearch.addEventListener('input', () => renderModalItems(currentModalData));

// Логіка кліку на кнопку сортування
const modalSortPrice = document.getElementById('modal-sort-price');
if (modalSortPrice) {
    modalSortPrice.addEventListener('click', () => {
        const currentOrder = modalSortPrice.getAttribute('data-order');
        const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
        modalSortPrice.setAttribute('data-order', newOrder);
        renderModalItems(currentModalData); // Перемальовуємо список
    });
}

// 6. Вибір компонента користувачем
window.selectComponent = function(item) {
    manualState[currentSelectingType] = item; // Зберігаємо в стан
    
    // Оновлюємо UI слота на сторінці
    const slotCard = document.querySelector(`.slot-card[data-type="${currentSelectingType}"]`);
    const nameEl = slotCard.querySelector('.selected-name');
    nameEl.innerText = getCompName(item);
    nameEl.style.color = 'var(--accent-cyan)';
    slotCard.style.borderColor = 'var(--accent-cyan)';
    
    modal.classList.remove('active'); // Ховаємо вікно
    updateManualSummary(); // Перераховуємо ціну та сумісність
};

// 7. Оновлення панелі "Підсумок збірки"
// 7. Оновлення панелі "Підсумок збірки"
async function updateManualSummary() {
    // Рахуємо ціну
    let total = 0;
    Object.values(manualState).forEach(item => { if(item) total += item.price; });
    document.querySelector('.summary-price').innerText = `${total} ₴`;

    // Рахуємо потужність
    let watts = 50; 
    if (manualState.cpu) watts += manualState.cpu.tdp || 65;
    if (manualState.gpu) watts += manualState.gpu.tdp || 200;
    document.querySelector('.summary-watts').innerText = `Орієнтовна потужність: ~${watts} W`;

    const compBox = document.querySelector('.compatibility-box');
    
    // ПЕРЕВІРКА №1: Чи обрані мінімально необхідні компоненти
    if (!manualState.cpu || !manualState.motherboard || !manualState.psu) {
        compBox.className = 'compatibility-box warning';
        compBox.innerText = 'Оберіть процесор, материнську плату та блок живлення для базової перевірки сумісності.';
        return;
    }

    try {
        compBox.className = 'compatibility-box warning';
        compBox.innerText = 'Перевірка всіх компонентів...';

        const res = await fetch(`${API_BASE_URL}/build/validate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                cpu_id: manualState.cpu.id,
                motherboard_id: manualState.motherboard.id,
                gpu_id: manualState.gpu ? manualState.gpu.id : 0,
                ram_id: manualState.ram ? manualState.ram.id : 0,
                psu_id: manualState.psu ? manualState.psu.id : 0
            })
        });
        
        const valid = await res.json();
        let isCompatible = valid.is_compatible;
        let errors = valid.errors ? [...valid.errors] : [];

        // --- ФРОНТЕНД ПЕРЕВІРКА ГАБАРИТІВ ТА ЖИВЛЕННЯ ---
        const caseItem = manualState.case;
        const gpuItem = manualState.gpu;
        const coolerItem = manualState.cooler;
        const psuItem = manualState.psu;

        // 1. Перевірка БЖ
        if (psuItem && psuItem.wattage) {
            if (psuItem.wattage < watts + 50) {
                isCompatible = false;
                errors.push(`Слабкий блок живлення! Система споживатиме ~${watts} Вт. БЖ на ${psuItem.wattage} Вт не має безпечного запасу.`);
            }
        }

        // 2. Перевірка Корпусу (якщо обраний)
        if (caseItem) {
            if (gpuItem && gpuItem.length_mm && caseItem.max_gpu_length_mm) {
                if (gpuItem.length_mm > caseItem.max_gpu_length_mm) {
                    isCompatible = false;
                    errors.push(`Відеокарта занадто довга (${gpuItem.length_mm} мм). Корпус вміщує макс. ${caseItem.max_gpu_length_mm} мм.`);
                }
            }
            const coolerH = coolerItem ? (coolerItem.height_mm || coolerItem.size) : null;
            if (coolerH && caseItem.max_cooler_height_mm) {
                if (coolerH > caseItem.max_cooler_height_mm) {
                    isCompatible = false;
                    errors.push(`Кулер занадто високий (${coolerH} мм). Кришка корпусу закриється макс. при ${caseItem.max_cooler_height_mm} мм.`);
                }
            }
        }
        // ----------------------------------------------

        // ПЕРЕВІРКА №2: Аналіз статусу
        if (isCompatible && errors.length === 0) {
            // Якщо обрані ВСІ габаритні деталі
            if (manualState.case && manualState.gpu && manualState.cooler) {
                compBox.className = 'compatibility-box success';
                compBox.innerText = '✅ Ваша збірка повністю сумісна, а всі деталі ідеально вміщуються в корпус!';
            } else {
                // Якщо є тільки база
                compBox.className = 'compatibility-box success';
                compBox.innerText = '✅ Базові деталі сумісні! Додайте корпус, відеокарту та кулер, щоб перевірити їхні розміри.';
            }
        } else {
            // Якщо є помилки
            compBox.className = 'compatibility-box error';
            compBox.innerHTML = '❌ Знайдено конфлікти:<br>' + errors.map(e => `- ${e}`).join('<br>');
        }
    } catch (e) {
        console.error("Помилка сумісності:", e);
        compBox.className = 'compatibility-box error';
        compBox.innerText = 'Не вдалося перевірити сумісність. Сервер не відповідає.';
    }
}

// ====================================================
// === БОКОВА ПАНЕЛЬ СЕРВІСІВ (SIDEBAR) ===
// ====================================================
const btnOpenSidebar = document.getElementById('btn-open-sidebar');
const btnCloseSidebar = document.getElementById('btn-close-sidebar');
const cyberSidebar = document.getElementById('cyber-sidebar');
const sidebarOverlay = document.getElementById('sidebar-overlay');

// Функція для відкриття
function openSidebar() {
    cyberSidebar.classList.add('active');
    sidebarOverlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Забороняємо скрол фону
}

// Функція для закриття (використовується також в HTML onClick)
window.closeSidebar = function() {
    cyberSidebar.classList.remove('active');
    sidebarOverlay.classList.remove('active');
    document.body.style.overflow = ''; // Повертаємо скрол
}

// Обробники подій
if (btnOpenSidebar) btnOpenSidebar.addEventListener('click', openSidebar);
if (btnCloseSidebar) btnCloseSidebar.addEventListener('click', closeSidebar);
if (sidebarOverlay) sidebarOverlay.addEventListener('click', closeSidebar); // Закриття по кліку на темний фон

// ====================================================
// === ЛОГІКА БЕНЧМАРКІВ (BOTTLENECK АНАЛІЗАТОР) ===
// ====================================================
const benchCpuSelect = document.getElementById('bench-cpu-select');
const benchGpuSelect = document.getElementById('bench-gpu-select');
const benchResSelect = document.getElementById('bench-res-select');
const benchGameSelect = document.getElementById('bench-game-select'); // НОВЕ
const btnRunBench = document.getElementById('btn-run-bench');
const benchResultsPanel = document.getElementById('bench-results-panel');
const benchValue = document.getElementById('bench-value');
const benchDesc = document.getElementById('bench-desc');
const benchFps = document.getElementById('bench-fps'); // НОВЕ
const benchGameNameDisplay = document.getElementById('bench-game-name'); // НОВЕ
const benchProgress = document.getElementById('bench-progress');

// Завантаження доступних CPU та GPU при старті
async function loadBenchmarkOptions() {
    if (!benchCpuSelect || !benchGpuSelect) return;
    
    try {
        const [cpuRes, gpuRes] = await Promise.all([
            fetch(`${API_BASE_URL}/cpus`),
            fetch(`${API_BASE_URL}/gpus`)
        ]);
        
        const cpus = await cpuRes.json();
        const gpus = await gpuRes.json();
        
        // Функція сортування за назвою для зручності
        const sortByName = (a, b) => getCompName(a).localeCompare(getCompName(b));
        
        benchCpuSelect.innerHTML = '<option value="">-- Оберіть процесор --</option>' + 
            cpus.sort(sortByName).map(c => `<option value="${c.id}">${getCompName(c)}</option>`).join('');
            
        benchGpuSelect.innerHTML = '<option value="">-- Оберіть відеокарту --</option>' + 
            gpus.sort(sortByName).map(g => `<option value="${g.id}">${getCompName(g)}</option>`).join('');
            
    } catch (e) {
        console.error("Помилка завантаження деталей для бенчмарку:", e);
        benchCpuSelect.innerHTML = '<option value="">Помилка сервера</option>';
    }
}

// Запускаємо завантаження
loadBenchmarkOptions();

// Обробка натискання кнопки "Проаналізувати"
// Обробка натискання кнопки "Проаналізувати"
if (btnRunBench) {
    btnRunBench.addEventListener('click', async () => {
        const cpuId = benchCpuSelect.value;
        const gpuId = benchGpuSelect.value;
        const res = benchResSelect.value;
        const game = benchGameSelect.value; // Витягуємо назву гри

        if (!cpuId || !gpuId) {
            showErrorAlert("Помилка", "Будь ласка, оберіть і процесор, і відеокарту для аналізу.");
            return;
        }

        btnRunBench.innerText = "Аналізуємо систему...";
        btnRunBench.disabled = true;

        try {
            // Звертаємося до НОВОГО Python-маршруту через POST
            const response = await fetch(`${API_BASE_URL}/benchmarks/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    cpu_id: cpuId,
                    gpu_id: gpuId,
                    resolution: res,
                    game_name: game
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) throw new Error(data.error || "Помилка сервера");
            
            const percent = data.bottleneck_percent;
            
            // Визначаємо колір
            let color = "var(--accent-cyan)";
            if (percent > 10 && percent <= 20) color = "#facc15"; 
            else if (percent > 20) color = "#ef4444"; 

            // Заповнюємо дані Bottleneck
            benchValue.innerText = `${percent}%`;
            benchDesc.innerText = data.bottleneck_desc;
            benchValue.style.color = color;
            benchValue.style.textShadow = `0 0 30px ${color}80`;
            benchProgress.style.background = `linear-gradient(90deg, ${color}, var(--accent-purple))`;
            document.querySelector('.result-card').style.borderColor = color;

            // Заповнюємо дані FPS
            benchGameNameDisplay.innerText = `У грі ${game}`;
            benchResultsPanel.classList.remove('hidden');
            
            // Крута анімація лічильника FPS (швидко накручує цифри)
            let currentFps = 0;
            const targetFps = data.fps;
            const step = Math.ceil(targetFps / 30) || 1; 
            const timer = setInterval(() => {
                currentFps += step;
                if (currentFps >= targetFps) {
                    currentFps = targetFps;
                    clearInterval(timer);
                }
                benchFps.innerText = currentFps;
            }, 30);

            // Анімація прогрес-бару
            benchProgress.style.width = '0%';
            setTimeout(() => {
                benchProgress.style.width = `${Math.min(percent, 100)}%`;
            }, 100);

        } catch (err) {
            console.error(err);
            showErrorAlert("Помилка тестування", "Не вдалося розрахувати параметри. Перевірте підключення до сервера.");
        } finally {
            btnRunBench.innerText = "Проаналізувати систему";
            btnRunBench.disabled = false;
        }
    });
}

// ====================================================
// === ЛОГІКА АНАЛІЗАТОРА ОХОЛОДЖЕННЯ (THERMALS) ===
// ====================================================
const thermCpuSelect = document.getElementById('therm-cpu-select');
const thermCoolerSelect = document.getElementById('therm-cooler-select');
const thermCaseSelect = document.getElementById('therm-case-select');
const thermAmbientInput = document.getElementById('therm-ambient-input');
const btnRunThermal = document.getElementById('btn-run-thermal');
const thermResultsPanel = document.getElementById('therm-results-panel');
const thermTempValue = document.getElementById('therm-temp-value');
const thermThrottleValue = document.getElementById('therm-throttle-value');
const thermFansValue = document.getElementById('therm-fans-value');

// Завантаження бази для охолодження
async function loadThermalOptions() {
    if (!thermCpuSelect) return;
    try {
        const [cpuRes, coolerRes, caseRes] = await Promise.all([
            fetch(`${API_BASE_URL}/cpus`),
            fetch(`${API_BASE_URL}/coolers`),
            fetch(`${API_BASE_URL}/cases`)
        ]);
        
        const cpus = await cpuRes.json();
        const coolers = await coolerRes.json();
        const cases = await caseRes.json();
        
        const sortByName = (a, b) => getCompName(a).localeCompare(getCompName(b));
        
        thermCpuSelect.innerHTML = '<option value="">-- Оберіть процесор --</option>' + 
            cpus.sort(sortByName).map(c => `<option value="${c.id}">${getCompName(c)}</option>`).join('');
            
        thermCoolerSelect.innerHTML = '<option value="">-- Оберіть охолодження --</option>' + 
            coolers.sort(sortByName).map(c => `<option value="${c.id}">${getCompName(c)}</option>`).join('');
            
        thermCaseSelect.innerHTML = '<option value="">-- Оберіть корпус --</option>' + 
            cases.sort(sortByName).map(c => `<option value="${c.id}">${getCompName(c)}</option>`).join('');
            
    } catch (e) {
        console.error("Помилка завантаження деталей для Thermal:", e);
    }
}
loadThermalOptions();

// Обробка натискання кнопки розрахунку
if (btnRunThermal) {
    btnRunThermal.addEventListener('click', async () => {
        const cpuId = thermCpuSelect.value;
        const coolerId = thermCoolerSelect.value;
        const caseId = thermCaseSelect.value;
        const ambient = parseInt(thermAmbientInput.value) || 22;

        if (!cpuId || !coolerId || !caseId) {
            showErrorAlert("Помилка", "Будь ласка, оберіть процесор, кулер та корпус.");
            return;
        }

        btnRunThermal.innerText = "Симуляція навантаження...";
        btnRunThermal.disabled = true;

        try {
            const response = await fetch(`${API_BASE_URL}/thermal/estimate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    cpu_id: parseInt(cpuId), cooler_id: parseInt(coolerId),
                    case_id: parseInt(caseId), ambient_temp_c: ambient
                })
            });
            const data = await response.json();
            if (!response.ok) throw new Error("Помилка сервера");

            thermResultsPanel.classList.remove('hidden');

            const temp = data.estimated_load_temp_c;
            let color = "var(--accent-cyan)"; 
            let shadow = "rgba(6, 182, 212, 0.5)";
            if (temp > 75 && temp <= 85) { color = "#facc15"; shadow = "rgba(250, 204, 21, 0.5)"; }
            else if (temp > 85) { color = "#ef4444"; shadow = "rgba(239, 68, 68, 0.5)"; }

            // АНІМАЦІЯ ТЕМПЕРАТУРИ
            let currentTemp = 0;
            const stepT = Math.ceil(temp / 25) || 1;
            const timerT = setInterval(() => {
                currentTemp += stepT;
                if (currentTemp >= temp) { currentTemp = temp; clearInterval(timerT); }
                thermTempValue.innerText = `${currentTemp}°C`;
            }, 30);

            thermTempValue.style.color = color;
            thermTempValue.style.textShadow = `0 0 20px ${shadow}`;
            document.querySelector('#therm-results-panel').style.borderColor = color;

            if (data.will_throttle) {
                thermThrottleValue.innerText = "ТАК ⚠️";
                thermThrottleValue.style.color = "#ef4444";
                thermThrottleValue.style.textShadow = "0 0 15px rgba(239, 68, 68, 0.5)";
            } else {
                thermThrottleValue.innerText = "НІ ✅";
                thermThrottleValue.style.color = "#4ade80";
                thermThrottleValue.style.textShadow = "0 0 15px rgba(34, 197, 94, 0.5)";
            }

            // АНІМАЦІЯ ВЕНТИЛЯТОРІВ
            let currentFans = 0;
            const targetFans = data.suggested_case_fans;
            if (targetFans > 0) {
                const timerF = setInterval(() => {
                    currentFans++;
                    thermFansValue.innerText = `+${currentFans}`;
                    if (currentFans >= targetFans) clearInterval(timerF);
                }, 150);
            } else {
                thermFansValue.innerText = "+0";
            }

        } catch (err) {

            console.error(err);
            showErrorAlert("Помилка розрахунку", "Не вдалося розрахувати температури. Перевірте сервер.");
        } finally {
            btnRunThermal.innerText = "Розрахувати температури";
            btnRunThermal.disabled = false;
        }
    });
}

// ====================================================
// === СЕРВІС ЕКСПОРТУ (TXT, Markdown, Link) ===
// ====================================================

// Глобальна змінна для збереження останньої "Розумної збірки"
let lastSmartBuild = null; 

window.exportBuild = function(format, source) {
    let build = null;
    let totalPrice = 0;

    // 1. Отримуємо дані залежно від типу збірки
    if (source === 'manual') {
        build = manualState;
        Object.values(manualState).forEach(item => { if(item) totalPrice += item.price; });
        if (!build.cpu && !build.gpu && !build.motherboard) {
            showErrorAlert("Увага", "Ваша збірка порожня. Оберіть деталі для експорту.");
            return;
        }
    } else if (source === 'smart') {
        if (!lastSmartBuild) {
            showErrorAlert("Увага", "Згенеруйте розумну збірку перед експортом.");
            return;
        }
        build = lastSmartBuild;
        totalPrice = lastSmartBuild.total_price || 0;
    }

    const labels = {
        cpu: "Процесор (CPU)", motherboard: "Материнська плата", gpu: "Відеокарта (GPU)", 
        ram: "Оперативна пам'ять", storage: "Накопичувач", cooler: "Охолодження", 
        psu: "Блок живлення", case: "Корпус", mouse: "Миша", keyboard: "Клавіатура", headset: "Гарнітура"
    };

    // 2. Генерація текстового ЧЕКА (Завантаження TXT)
    // 2. Генерація PDF-документа (Замість TXT)
    // 2. Генерація PDF-документа (БЕЗ милиць зі схованими блоками)
    // 2. Генерація PDF-документа (З ФІКСОМ ПУСТОГО ЕКРАНУ)
    if (format === 'pdf') {
        let pdfHtml = `
            <div style="padding: 40px; font-family: 'Arial', sans-serif; color: #1f2937; background: #ffffff; width: 800px; box-sizing: border-box;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #06b6d4; margin: 0; font-size: 32px; font-weight: bold;">CyberCraft</h1>
                    <h3 style="color: #6b7280; margin: 5px 0; font-size: 18px;">Офіційна специфікація ПК</h3>
                    <hr style="border: 0; border-top: 2px solid #e5e7eb; margin-top: 20px;">
                </div>
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 30px;">
                    <thead>
                        <tr style="background: #f3f4f6;">
                            <th style="padding: 15px; text-align: left; border-bottom: 2px solid #d1d5db; width: 30%;">Компонент</th>
                            <th style="padding: 15px; text-align: left; border-bottom: 2px solid #d1d5db; width: 50%;">Модель</th>
                            <th style="padding: 15px; text-align: right; border-bottom: 2px solid #d1d5db; width: 20%;">Ціна (₴)</th>
                        </tr>
                    </thead>
                    <tbody>
        `;

        for (let key in labels) {
            if (build[key]) {
                pdfHtml += `
                        <tr>
                            <td style="padding: 15px; border-bottom: 1px solid #e5e7eb;"><strong>${labels[key]}</strong></td>
                            <td style="padding: 15px; border-bottom: 1px solid #e5e7eb;">${getCompName(build[key])}</td>
                            <td style="padding: 15px; border-bottom: 1px solid #e5e7eb; text-align: right; color: #06b6d4; font-weight: bold;">${build[key].price}</td>
                        </tr>`;
            }
        }

        pdfHtml += `
                    </tbody>
                </table>
                <div style="text-align: right; padding: 20px; background: #f8fafc; border-radius: 8px;">
                    <h2 style="margin: 0; color: #111827;">Загальна вартість: <span style="color: #8b5cf6;">${totalPrice} ₴</span></h2>
                </div>
                <div style="margin-top: 50px; text-align: center; color: #9ca3af; font-size: 12px;">
                    <p>Згенеровано платформою CyberCraft OS | Збирай як професіонал</p>
                    <p>${new Date().toLocaleString('uk-UA')}</p>
                </div>
            </div>
        `;

        // Створюємо реальний DOM-елемент у пам'яті (надійніше, ніж просто рядок)
        const element = document.createElement('div');
        element.innerHTML = pdfHtml;

        // Налаштування для конвертації (З ФІКСОМ СТРИБКА scrollY)
        const opt = {
            margin:       0, 
            filename:     `CyberCraft_Build_${new Date().getTime()}.pdf`,
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true, scrollY: 0, windowY: 0 }, // <- ФІКС ТУТ!
            jsPDF:        { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };

        // Запускаємо генерацію
        html2pdf().set(opt).from(element).save().then(() => {
            showErrorAlert("Готово!", "PDF-специфікацію успішно завантажено на ваш пристрій.", "success");
        });
    }
    
    // 3. Генерація MARKDOWN для Reddit/Форумів (Копіювання)
    else if (format === 'md') {
        let md = `### Моя збірка в CyberCraft 🚀\n\n`;
        md += `| Деталь | Модель | Ціна |\n|---|---|---|\n`;
        
        for (let key in labels) {
            if (build[key]) {
                md += `| **${labels[key]}** | ${getCompName(build[key])} | ${build[key].price} ₴ |\n`;
            }
        }
        md += `| **Всього** | | **${totalPrice} ₴** |\n`;

        navigator.clipboard.writeText(md).then(() => {
            showErrorAlert("Успішно!", "Markdown-код скопійовано!\n\nТепер ви можете вставити його на Reddit чи інший форум.", "success");
        });
    } 
    
    // 4. Генерація КОРОТКОГО ПОСИЛАННЯ (Копіювання)
    // 4. Генерація ПОСИЛАННЯ (Для збережених і незбережених збірок)
    else if (format === 'link') {
        let shortLink = 'https://cybercraft-app.onrender.com/';
        
        // Якщо це просто генерація на екрані, зашиваємо ID деталей в URL
        if (build) {
            const params = new URLSearchParams();
            if (build.cpu) params.append('cpu', build.cpu.id);
            if (build.gpu) params.append('gpu', build.gpu.id);
            if (build.motherboard) params.append('mb', build.motherboard.id);
            if (build.ram) params.append('ram', build.ram.id);
            if (build.storage) params.append('st', build.storage.id);
            if (build.cooler) params.append('col', build.cooler.id);
            if (build.psu) params.append('psu', build.psu.id);
            if (build.case) params.append('cas', build.case.id);
            // --- ДОДАНА ПЕРИФЕРІЯ ---
            if (build.mouse) params.append('ms', build.mouse.id);
            if (build.keyboard) params.append('kb', build.keyboard.id);
            if (build.headset) params.append('hs', build.headset.id);
            // ------------------------
            
            // Якщо є хоча б одна деталь, додаємо параметри до посилання
            if (params.toString()) {
                shortLink += '?' + params.toString();
            }
        }
        
        navigator.clipboard.writeText(shortLink).then(() => {
            showErrorAlert("Посилання створено!", `Ваше унікальне посилання:\n\n${shortLink}\n\n(Вже скопійовано в буфер обміну)`, "success");
        });
    }
};

// ====================================================
// === ЛОГІКА СТОРІНКИ ПОРІВНЯННЯ ===
// ====================================================

// 1. Перемикання вкладок
// 1. Перемикання вкладок
// 1. Перемикання вкладок
document.querySelectorAll('.compare-tab').forEach(tab => {
    tab.addEventListener('click', (e) => {
        document.querySelectorAll('.compare-tab').forEach(t => t.classList.remove('active'));
        
        document.querySelectorAll('.compare-content').forEach(c => {
            c.classList.remove('active');
            c.classList.add('hidden');
        });
        
        e.target.classList.add('active');
        
        const targetId = e.target.dataset.target;
        const targetContent = document.getElementById(targetId);
        if (targetContent) {
            targetContent.classList.add('active');
            targetContent.classList.remove('hidden');
        }

        // НОВЕ: Завантажуємо збережені збірки для вибору, якщо відкрили вкладку збірок
        if (targetId === 'compare-builds') {
            loadSavedBuildsForComparison();
        }
    });
});

// 2. Логіка завантаження деталей (для вкладки "Окремі деталі")
const compTypeSelect = document.getElementById('compare-type-select');
const compItem1 = document.getElementById('compare-item-1');
const compItem2 = document.getElementById('compare-item-2');

async function loadCompareItems() {
    const type = compTypeSelect.value;
    const endpoints = {
        'cpu': '/cpus', 'gpu': '/gpus', 'motherboard': '/motherboards',
        'ram': '/rams', 'storage': '/storage', 'cooler': '/coolers',
        'psu': '/psus', 'case': '/cases'
    };
    
    compItem1.innerHTML = '<option value="">Завантаження...</option>';
    compItem2.innerHTML = '<option value="">Завантаження...</option>';
    
    try {
        const res = await fetch(`${API_BASE_URL}${endpoints[type]}`);
        const items = await res.json();
        const sortByName = (a, b) => getCompName(a).localeCompare(getCompName(b));
        
        const options = '<option value="">-- Оберіть деталь --</option>' + 
            items.sort(sortByName).map(i => `<option value="${i.id}">${getCompName(i)}</option>`).join('');
            
        compItem1.innerHTML = options;
        compItem2.innerHTML = options;
    } catch(e) {
        console.error(e);
    }
}
if (compTypeSelect) compTypeSelect.addEventListener('change', loadCompareItems);
loadCompareItems();

// 2.5 Логіка завантаження бази для вкладки "Баланс"
async function loadBalanceItems() {
    const cpuSelect = document.getElementById('balance-cpu');
    const gpuSelect = document.getElementById('balance-gpu');
    if (!cpuSelect || !gpuSelect) return;
    
    try {
        const [cpuRes, gpuRes] = await Promise.all([ fetch(`${API_BASE_URL}/cpus`), fetch(`${API_BASE_URL}/gpus`) ]);
        const cpus = await cpuRes.json();
        const gpus = await gpuRes.json();
        const sortByName = (a, b) => getCompName(a).localeCompare(getCompName(b));

        cpuSelect.innerHTML = '<option value="">-- Оберіть процесор --</option>' + cpus.sort(sortByName).map(i => `<option value="${i.id}">${getCompName(i)}</option>`).join('');
        gpuSelect.innerHTML = '<option value="">-- Оберіть відеокарту --</option>' + gpus.sort(sortByName).map(i => `<option value="${i.id}">${getCompName(i)}</option>`).join('');
    } catch (e) {
        console.error("Помилка завантаження балансу:", e);
    }
}
loadBalanceItems();

// 3. Обробка кліку "Порівняти деталі"
const btnCompareItems = document.getElementById('btn-run-compare-items');
if (btnCompareItems) {
    btnCompareItems.addEventListener('click', async () => {
        const type = compTypeSelect.value;
        const id1 = compItem1.value;
        const id2 = compItem2.value;

        if (!id1 || !id2) { showErrorAlert("Увага", "Оберіть обидві деталі для порівняння."); return; }
        if (id1 === id2) { showErrorAlert("Увага", "Ви обрали однакові деталі. Немає сенсу порівнювати."); return; }

        btnCompareItems.innerText = "Аналіз...";
        const resultBox = document.getElementById('compare-items-result');
        const listObj = document.getElementById('adv-list');

        try {
            const res = await fetch(`${API_BASE_URL}/comparison/components`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ component_type: type, item_id_1: parseInt(id1), item_id_2: parseInt(id2) })
            });
            const data = await res.json();
            const checkIcon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>`;
            
            let html = '';
            if (data.advantages && data.advantages.length > 0) {
                // Використовуємо innerHTML, щоб теги <strong> з Python нормально відмалювалися
                data.advantages.forEach(adv => { html += `<li class="adv-item">${checkIcon} <span>${adv}</span></li>`; });
            }
            listObj.innerHTML = html;
            resultBox.classList.remove('hidden');
        } catch(e) {
            console.error(e); showErrorAlert("Помилка", "Не вдалося отримати дані з сервера.");
        } finally {
            btnCompareItems.innerText = "Порівняти деталі";
        }
    });
}

// 3.5 Обробка кліку "Перевірити баланс"
const btnRunBalance = document.getElementById('btn-run-balance');
if (btnRunBalance) {
    btnRunBalance.addEventListener('click', async () => {
        const cpuId = document.getElementById('balance-cpu').value;
        const gpuId = document.getElementById('balance-gpu').value;

        if (!cpuId || !gpuId) { showErrorAlert("Увага", "Оберіть процесор та відеокарту."); return; }

        btnRunBalance.innerText = "Аналіз...";
        const resultBox = document.getElementById('compare-balance-result');
        const listObj = document.getElementById('balance-adv-list');

        try {
            const res = await fetch(`${API_BASE_URL}/comparison/balance`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cpu_id: parseInt(cpuId), gpu_id: parseInt(gpuId) })
            });
            const data = await res.json();
            
            let color = data.advice.includes("Увага") ? "#facc15" : "#4ade80";
            listObj.innerHTML = `
                <li class="adv-item" style="border-color: ${color};">
                    <svg style="color: ${color};" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line>
                    </svg>
                    <span style="color: ${color}; font-weight: 600;">${data.advice}</span>
                </li>`;
            resultBox.style.borderColor = color;
            resultBox.classList.remove('hidden');
        } catch(e) {
            showErrorAlert("Помилка", "Не вдалося перевірити баланс.");
        } finally {
            btnRunBalance.innerText = "Перевірити баланс";
        }
    });
}

// 4. Тимчасова логіка "Порівняти збірки" (Смарт vs Ручна)
// 4. ЗАВАНТАЖЕННЯ ТА ПОРІВНЯННЯ ЗБЕРЕЖЕНИХ ЗБІРОК
async function loadSavedBuildsForComparison() {
    const s1 = document.getElementById('compare-build-1');
    const s2 = document.getElementById('compare-build-2');
    
    if (!currentUserId) {
        const msg = '<option value="">Увійдіть в аккаунт</option>';
        s1.innerHTML = msg; s2.innerHTML = msg; return;
    }

    try {
        const res = await fetch(`${API_BASE_URL}/profile/${currentUserId}/favorites`);
        const builds = await res.json();
        
        // Зберігаємо для швидкого доступу до ID деталей
        window.userBuildsCache = builds;

        if (builds.length === 0) {
            const msg = '<option value="">Немає збережених збірок</option>';
            s1.innerHTML = msg; s2.innerHTML = msg; return;
        }

        let opt = '<option value="">-- Оберіть збірку --</option>';
        builds.forEach(b => { opt += `<option value="${b.id}">${b.name}</option>`; });
        s1.innerHTML = opt; s2.innerHTML = opt;
    } catch (e) { console.error("Помилка завантаження", e); }
}

const btnCompareBuilds = document.getElementById('btn-run-compare-builds');
if (btnCompareBuilds) {
    btnCompareBuilds.addEventListener('click', async () => {
        const id1 = document.getElementById('compare-build-1').value;
        const id2 = document.getElementById('compare-build-2').value;

        if (!id1 || !id2) { showErrorAlert("Увага", "Оберіть дві збірки."); return; }
        if (id1 === id2) { showErrorAlert("Увага", "Оберіть різні збірки."); return; }

        const b1 = window.userBuildsCache.find(b => b.id == id1);
        const b2 = window.userBuildsCache.find(b => b.id == id2);

        btnCompareBuilds.innerText = "Глибокий аналіз...";
        btnCompareBuilds.disabled = true;

        try {
            const res = await fetch(`${API_BASE_URL}/compare/builds`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    build_1: { cpu_id: b1.cpu_id, gpu_id: b1.gpu_id, motherboard_id: b1.motherboard_id, ram_id: b1.ram_id, psu_id: b1.psu_id, storage_id: b1.storage_id, cooler_id: b1.cooler_id, case_id: b1.case_id },
                    build_2: { cpu_id: b2.cpu_id, gpu_id: b2.gpu_id, motherboard_id: b2.motherboard_id, ram_id: b2.ram_id, psu_id: b2.psu_id, storage_id: b2.storage_id, cooler_id: b2.cooler_id, case_id: b2.case_id }
                })
            });
            const data = await res.json();

            const resBox = document.getElementById('compare-builds-result');
            const winnerObj = document.getElementById('compare-builds-winner');
            const expObj = document.getElementById('compare-builds-explanation');

            const wColor = data.winner_build === 1 ? "var(--accent-cyan)" : "var(--accent-purple)";
            const winnerName = data.winner_build === 1 ? b1.name : b2.name;

            // ОСЬ ТУТ: Застосовуємо нову іконку-медаль та градієнтний клас
            // ОСЬ ТУТ: Застосовуємо нову іконку-медаль та обидва градієнтні класи
            winnerObj.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="${wColor}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="win-medallion">
                        <circle cx="12" cy="8" r="7"/>
                        <polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>
                    </svg>
                    <span class="winner-prefix-text">Перемагає:</span> 
                    <span class="success-gradient-text" style="font-size: 26px;">${winnerName}</span>
                </div>
            `;
            
            // Очищаємо старий inline-стиль кольору, бо тепер у нас градієнт
            winnerObj.style.color = ''; 
            resBox.style.borderColor = wColor;

            let html = `<p style="margin-bottom: 25px; text-align: center; font-size: 16px; color: #e2e8f0;">${data.explanation_text}</p><div style="display: flex; flex-direction: column; gap: 20px; text-align: left;">`;

            // Виводимо покомпонентний аналіз, який прийшов з Python
            for (const [comp, advantages] of Object.entries(data.detailed_analysis)) {
                if (advantages && advantages.length > 0) {
                    html += `
                        <div>
                            <h4 style="color: var(--accent-cyan); font-size: 13px; text-transform: uppercase; margin-bottom: 8px;">${comp}</h4>
                            <ul class="adv-list" style="gap: 5px;">
                                ${advantages.map(a => `<li class="adv-item" style="padding: 8px 15px; font-size: 14px; border-left-width: 2px;">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px; height:16px;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
                                    <span>${a}</span>
                                </li>`).join('')}
                            </ul>
                        </div>`;
                }
            }
            expObj.innerHTML = html + `</div>`;
            resBox.classList.remove('hidden');
        } catch (e) { showErrorAlert("Помилка", "Не вдалося отримати аналіз."); } 
        finally { btnCompareBuilds.innerText = "Порівняти конфігурації"; btnCompareBuilds.disabled = false; }
    });
}

// ====================================================
// === ЛОГІКА АНАЛІТИКИ РИНКУ (MARKET ANALYTICS) ===
// ====================================================
const analyticsTypeSelect = document.getElementById('analytics-type-select');
const analyticsItemSelect = document.getElementById('analytics-item-select');
const btnRunAnalytics = document.getElementById('btn-run-analytics');
const analyticsResultsPanel = document.getElementById('analytics-results-panel');

// Завантаження деталей при зміні категорії
async function loadAnalyticsItems() {
    if (!analyticsTypeSelect || !analyticsItemSelect) return;
    
    const type = analyticsTypeSelect.value;
    analyticsItemSelect.innerHTML = '<option value="">Завантаження...</option>';
    
    // Словник ендпоінтів для різних типів (запозичили з порівняння)
    // Словник ендпоінтів для різних типів
    const endpoints = {
        'cpu': '/cpus', 'gpu': '/gpus', 'motherboard': '/motherboards',
        'ram': '/rams', 'storage': '/storage', 'psu': '/psus',
        'cooler': '/coolers', 'case': '/cases',
        'mouse': '/peripherals/mice', 'keyboard': '/peripherals/keyboards', 'headset': '/peripherals/headsets'
    };

    try {
        const res = await fetch(`${API_BASE_URL}${endpoints[type]}`);
        const items = await res.json();
        const sortByName = (a, b) => getCompName(a).localeCompare(getCompName(b));
        
        analyticsItemSelect.innerHTML = '<option value="">-- Оберіть модель --</option>' + 
            items.sort(sortByName).map(i => `<option value="${i.id}">${getCompName(i)}</option>`).join('');
    } catch (e) {
        console.error("Помилка завантаження для аналітики:", e);
        analyticsItemSelect.innerHTML = '<option value="">Помилка завантаження</option>';
    }
}

// Слухаємо зміну типу
if (analyticsTypeSelect) {
    analyticsTypeSelect.addEventListener('change', loadAnalyticsItems);
    loadAnalyticsItems(); // Перше завантаження при старті
}

// Запуск аналітики
if (btnRunAnalytics) {
    btnRunAnalytics.addEventListener('click', async () => {
        const type = analyticsTypeSelect.value;
        const itemId = analyticsItemSelect.value;

        if (!itemId) {
            showErrorAlert("Увага", "Будь ласка, оберіть конкретну модель для аналізу.");
            return;
        }

        btnRunAnalytics.innerText = "Збираємо дані з магазинів...";
        btnRunAnalytics.disabled = true;

        try {
            // Робимо 3 паралельні запити до бекенду
            const [trendRes, storesRes, historyRes] = await Promise.all([
                fetch(`${API_BASE_URL}/market/trend?type=${type}&id=${itemId}`),
                fetch(`${API_BASE_URL}/market/stores?type=${type}&id=${itemId}`),
                fetch(`${API_BASE_URL}/market/history?type=${type}&id=${itemId}`)
            ]);

            const trendData = await trendRes.json();
            const storesData = await storesRes.json();
            const historyData = await historyRes.json();

            // 1. ВІДМАЛЬОВУЄМО ВЕРДИКТ
            const verdictTextObj = document.getElementById('analytics-verdict-text');
            const verdictCardObj = document.getElementById('analytics-verdict-card');
            
            const verdictText = trendData.trend_analysis;
            verdictTextObj.innerText = verdictText;
            
            // Розмальовуємо рамку залежно від вигоди
            let color = "var(--accent-cyan)";
            let shadow = "rgba(6, 182, 212, 0.3)";
            if (verdictText.includes("на піку")) { color = "#ef4444"; shadow = "rgba(239, 68, 68, 0.3)"; } // Червоний
            else if (verdictText.includes("вигідною")) { color = "#4ade80"; shadow = "rgba(34, 197, 94, 0.3)"; } // Зелений
            else if (verdictText.includes("стабільна")) { color = "#facc15"; shadow = "rgba(250, 204, 21, 0.3)"; } // Жовтий
            
            verdictCardObj.style.borderColor = color;
            verdictCardObj.style.boxShadow = `0 0 20px ${shadow}`;

            // 2. ВІДМАЛЬОВУЄМО МАГАЗИНИ
            // 2. ВІДМАЛЬОВУЄМО МАГАЗИНИ (KTC, CompX, ITbox)
            // 2. ВІДМАЛЬОВУЄМО МАГАЗИНИ (З БРЕНДОВИМИ КОЛЬОРАМИ ТА ЛОГІКОЮ НАЯВНОСТІ)
            // 2. ВІДМАЛЬОВУЄМО МАГАЗИНИ (З ЛОГОТИПАМИ ТА БРЕНДОВИМИ КОЛЬОРАМИ)
            // 2. ВІДМАЛЬОВУЄМО МАГАЗИНИ (ЛОГОТИПИ, КОЛЬОРИ ТА РОЗУМНИЙ FALLBACK)
            const storesListObj = document.getElementById('analytics-stores-list');
            storesListObj.innerHTML = storesData.map((store, index) => {
                
                // 1. Універсальна перевірка: якщо є "(БД)" або "(Орієнтовно)" - це не LIVE
                const isLive = !store.store_name.includes('(БД)') && !store.store_name.includes('(Орієнтовно)');
                
                // 2. Витягуємо чисту назву (видаляємо помітки)
                let cleanName = store.store_name.replace(' (БД)', '').replace(' (Орієнтовно)', '').replace('\n', '').trim();

                // 3. Брендові кольори та домени для логотипів (Блакитний, Синій, Жовтий)
                // 3. Брендові кольори та домени для логотипів
                // 3. Брендові кольори та домени для логотипів
                // 3. Брендові кольори та домени для логотипів
                // 3. Брендові кольори та домени для логотипів
                let themeColor = "var(--accent-cyan)";
                let domain = "";

                if (cleanName.includes("KTC")) { cleanName = "KTC"; themeColor = "#38bdf8"; domain = "ktc.ua"; }
                else if (cleanName.includes("Moyo")) { cleanName = "Moyo"; themeColor = "#4b9af9"; domain = "moyo.ua"; } // Зелений колір Moyo
                else if (cleanName.includes("LuckyLink")) { cleanName = "LuckyLink"; themeColor = "#facc15"; domain = "luckylink.kiev.ua"; }
                // 4. Логіка плашки LIVE
                const liveBadge = isLive 
                    ? `<span style="font-size: 10px; color: #4ade80; border: 1px solid #4ade80; padding: 2px 5px; border-radius: 4px; margin-left: 10px; vertical-align: middle; box-shadow: 0 0 5px #4ade80;">LIVE</span>` 
                    : '';

                // 5. Повідомлення, якщо ціна з БД
                const warningMsg = !isLive 
                    ? `<div style="font-size: 12px; color: #ef4444; margin-top: 8px; font-weight: 500;">Немає в наявності. Орієнтовна ціна.</div>` 
                    : `<div style="font-size: 12px; opacity: 0; margin-top: 8px;">&nbsp;</div>`;

                // Отримуємо фавіконку з Google
                const logoUrl = domain ? `https://www.google.com/s2/favicons?domain=${domain}&sz=32` : '';
                const logoImg = logoUrl ? `<img src="${logoUrl}" alt="logo" style="width: 20px; height: 20px; border-radius: 4px; filter: drop-shadow(0 0 5px ${themeColor}80);">` : '';

                return `
                <div class="store-card" style="animation-delay: ${index * 0.1}s; border: 1px solid ${themeColor}40; background: rgba(0,0,0,0.2);">
                    <div class="store-name" style="color: ${themeColor}; display: flex; align-items: center; justify-content: center; gap: 8px;">
                        ${logoImg}
                        ${cleanName} ${liveBadge}
                    </div>
                    <div class="store-price" style="text-shadow: 0 0 15px ${themeColor}40; color: ${themeColor}; margin: 10px 0 0;">${store.current_price} ₴</div>
                    ${warningMsg}
                    <a href="${store.url}" target="_blank" class="btn-store" 
                       style="border-color: ${themeColor}; color: ${themeColor}; margin-top: 15px;"
                       onmouseover="this.style.background='${themeColor}'; this.style.color='#000'; this.style.boxShadow='0 0 20px ${themeColor}80'"
                       onmouseout="this.style.background='transparent'; this.style.color='${themeColor}'; this.style.boxShadow='none'">
                       Перейти в магазин
                    </a>
                </div>
                `;
            }).join('');

            // 3. ВІДМАЛЬОВУЄМО CSS ГРАФІК
            const chartObj = document.getElementById('analytics-chart');
            if (historyData.length > 0) {
                // Знаходимо максимальну ціну, щоб розрахувати 100% висоти стовпчика
                const maxPrice = Math.max(...historyData.map(h => h.average_price));
                
                chartObj.innerHTML = historyData.map((point) => {
                    const heightPercent = (point.average_price / maxPrice) * 100;
                    return `
                        <div class="chart-bar-wrapper">
                            <div class="chart-bar" style="height: ${heightPercent}%;">
                                <span class="chart-tooltip">${point.average_price} ₴</span>
                            </div>
                            <span class="chart-label">${point.date}</span>
                        </div>
                    `;
                }).join('');
            } else {
                chartObj.innerHTML = '<p style="color: var(--text-muted); width: 100%; text-align: center;">Немає даних для графіка</p>';
            }

            // Показуємо панель з плавною анімацією
            analyticsResultsPanel.classList.remove('hidden');

        } catch (e) {
            console.error("Помилка аналітики:", e);
            showErrorAlert("Помилка мережі", "Не вдалося отримати дані про ціни. Перевірте підключення до сервера.");
        } finally {
            btnRunAnalytics.innerText = "Проаналізувати ринок";
            btnRunAnalytics.disabled = false;
        }
    });
}

// ====================================================
// === ЛОГІКА АВТОРИЗАЦІЇ ТА ПРОФІЛЮ ===
// ====================================================

const authModal = document.getElementById('auth-modal');
const btnOpenAuth = document.getElementById('btn-profile'); 
const btnCloseAuth = document.getElementById('btn-close-auth');
const tabLogin = document.getElementById('tab-login');
const tabRegister = document.getElementById('tab-register');
const formLogin = document.getElementById('form-login');
const formRegister = document.getElementById('form-register');

let currentToken = localStorage.getItem('cyber_token');
let currentUserId = localStorage.getItem('cyber_user_id');

function extractUserId(token) {
    if(!token) return null;
    const match = token.match(/payload_user_id_(\d+)/);
    return match ? parseInt(match[1]) : null;
}

function toggleAuthTabs(isLogin) {
    if (isLogin) {
        tabLogin.classList.add('active'); tabRegister.classList.remove('active');
        formLogin.classList.remove('hidden'); formRegister.classList.add('hidden');
    } else {
        tabRegister.classList.add('active'); tabLogin.classList.remove('active');
        formRegister.classList.remove('hidden'); formLogin.classList.add('hidden');
    }
}
if(tabLogin) tabLogin.addEventListener('click', () => toggleAuthTabs(true));
if(tabRegister) tabRegister.addEventListener('click', () => toggleAuthTabs(false));

if(btnOpenAuth) {
    btnOpenAuth.addEventListener('click', () => {
        if (currentToken && currentUserId) {
            switchPage('nav-profile');
            loadUserProfile();
        } else {
            authModal.classList.add('active');
        }
    });
}
if(btnCloseAuth) btnCloseAuth.addEventListener('click', () => authModal.classList.remove('active'));

// Логін (З гарними помилками)
// ====================================================
// === ЛОГІКА ШВИДКОГО ВХОДУ (ЗБЕРЕЖЕНІ АКАУНТИ) ===
// ====================================================

function getSavedAccounts() {
    return JSON.parse(localStorage.getItem('cyber_saved_accounts')) || [];
}

function saveAccountLocally(email, pass) {
    let accounts = getSavedAccounts();
    // Перевіряємо, чи немає вже такого email
    if (!accounts.find(acc => acc.email === email)) {
        accounts.push({ email: email, pass: pass });
        localStorage.setItem('cyber_saved_accounts', JSON.stringify(accounts));
    } else {
        // Якщо є, оновлюємо пароль (на випадок якщо він змінився)
        const accIndex = accounts.findIndex(acc => acc.email === email);
        accounts[accIndex].pass = pass;
        localStorage.setItem('cyber_saved_accounts', JSON.stringify(accounts));
    }
    renderSavedAccounts();
}

window.removeSavedAccount = function(event, email) {
    event.stopPropagation(); // Щоб клік на хрестик не викликав "Швидкий вхід"
    let accounts = getSavedAccounts();
    accounts = accounts.filter(acc => acc.email !== email);
    localStorage.setItem('cyber_saved_accounts', JSON.stringify(accounts));
    renderSavedAccounts();
}

window.quickLogin = function(email, pass) {
    // Підставляємо дані в поля і автоматично натискаємо кнопку "Увійти"
    document.getElementById('auth-login-email').value = email;
    document.getElementById('auth-login-pass').value = pass;
    document.getElementById('btn-submit-login').click();
}

function renderSavedAccounts() {
    const container = document.getElementById('saved-accounts-container');
    const list = document.getElementById('saved-accounts-list');
    
    if (!container || !list) return; 

    const accounts = getSavedAccounts();

    if (accounts.length === 0) {
        container.classList.add('hidden');
        return;
    }

    container.classList.remove('hidden');
    list.innerHTML = accounts.map(acc => {
        const letter = acc.email.charAt(0).toUpperCase();
        
        // === НОВЕ: Перевірка наявності аватарки ===
        const avatarContent = acc.avatar_url 
            ? `<img src="${BACKEND_URL}${acc.avatar_url}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">` 
            : letter;

        return `
            <div class="saved-account-card" onclick="quickLogin('${acc.email}', '${acc.pass}')">
                <div class="saved-avatar" style="overflow: hidden;">${avatarContent}</div>
                <div class="saved-info">
                    <div class="saved-email">${acc.email}</div>
                    <div class="saved-hint">Натисніть для входу</div>
                </div>
                <button class="btn-remove-account" onclick="removeSavedAccount(event, '${acc.email}')" title="Видалити">
                    <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>
            </div>
        `;
    }).join('');
}

// Викликаємо відмальовку карток при завантаженні сторінки
renderSavedAccounts();

// ====================================================
// === ОНОВЛЕНИЙ ЛОГІН ===
// ====================================================

// --- НОВА ФУНКЦІЯ: Жорстка перевірка формату Email ---
function isValidEmail(email) {
    const re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,10}$/;
    return re.test(String(email).toLowerCase());
}

document.getElementById('btn-submit-login').addEventListener('click', async () => {
    const email = document.getElementById('auth-login-email').value;
    const pass = document.getElementById('auth-login-pass').value;
    const btnSubmit = document.getElementById('btn-submit-login');

    if(!email || !pass) { showErrorAlert("Увага", "Заповніть всі поля."); return; }
    
    // === НОВЕ: Перевірка формату email ===
    if(!isValidEmail(email)) { 
        showErrorAlert("Помилка формату", "Будь ласка, введіть коректний email (наприклад, name@gmail.com)."); 
        return; 
    }

    btnSubmit.innerText = "Вхід...";
    btnSubmit.disabled = true;

    try {
        const res = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: pass })
        });
        const data = await res.json();
        
        if (res.ok) {
            currentToken = data.access_token;
            currentUserId = extractUserId(currentToken);
            localStorage.setItem('cyber_token', currentToken);
            localStorage.setItem('cyber_user_id', currentUserId);
            
            saveAccountLocally(email, pass);
            
            // === НОВЕ: Одразу підтягуємо аватарку для швидкого входу ===
            try {
                const profRes = await fetch(`${API_BASE_URL}/profile/${currentUserId}`);
                const profData = await profRes.json();
                let accounts = getSavedAccounts();
                let accIdx = accounts.findIndex(a => a.email === email);
                if (accIdx !== -1) {
                    accounts[accIdx].avatar_url = profData.avatar_url;
                    localStorage.setItem('cyber_saved_accounts', JSON.stringify(accounts));
                    renderSavedAccounts();
                }
            } catch(e) { console.error("Не вдалося завантажити аватарку", e); }
            
            authModal.classList.remove('active');
            checkAuthState();
            
            document.getElementById('auth-login-email').value = '';
            document.getElementById('auth-login-pass').value = '';

            showErrorAlert("Успіх", "Ви успішно увійшли в систему!", "success");
        } else {
            showErrorAlert("Помилка входу", data.error || "Невірний email або пароль. Перевірте введені дані.");
        }
    } catch(e) { 
        showErrorAlert("Помилка", "Сервер не відповідає."); 
    } finally {
        btnSubmit.innerText = "Увійти";
        btnSubmit.disabled = false;
    }
});

// Реєстрація (З перевіркою Email)
document.getElementById('btn-submit-register').addEventListener('click', async () => {
    const email = document.getElementById('auth-reg-email').value;
    const pass = document.getElementById('auth-reg-pass').value;
    const passConf = document.getElementById('auth-reg-pass-confirm').value;
    
    if(!email || !pass) { showErrorAlert("Увага", "Заповніть всі поля."); return; }
    
    // === НОВЕ: Перевірка формату email ===
    if(!isValidEmail(email)) { 
        showErrorAlert("Помилка формату", "Будь ласка, введіть коректний email для реєстрації."); 
        return; 
    }
    
    if(pass !== passConf) { showErrorAlert("Увага", "Паролі не співпадають."); return; }
    if(pass.length < 6) { showErrorAlert("Увага", "Пароль має бути від 6 символів."); return; }

    try {
        const res = await fetch(`${API_BASE_URL}/auth/register`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: pass })
        });
        const data = await res.json();
        
        if (res.ok) {
            showErrorAlert("Успіх", "Аккаунт створено! Тепер увійдіть.", "success");
            toggleAuthTabs(true);
            document.getElementById('auth-login-email').value = email;
        } else {
            showErrorAlert("Помилка", data.error || "Такий email вже існує або дані некоректні.");
        }
    } catch(e) { showErrorAlert("Помилка", "Сервер не відповідає."); }
});

function checkAuthState() {
    if (currentToken && currentUserId) {
        btnOpenAuth.innerHTML = `<span style="color:#fff; font-weight: 600;">Мій Кабінет</span>`;
        pages['nav-profile'] = document.getElementById('page-profile');
    } else {
        btnOpenAuth.innerHTML = `<span style="color:#fff; font-weight: 600;">Увійти</span>`;
    }
}
checkAuthState();

document.getElementById('btn-logout').addEventListener('click', () => {
    currentToken = null; currentUserId = null;
    localStorage.removeItem('cyber_token'); localStorage.removeItem('cyber_user_id');
    checkAuthState(); goHome();
    showErrorAlert("Вихід", "Ви вийшли з системи.", "success");
});

// === ЛОГІКА ВИДАЛЕННЯ АКАУНТА ===
const btnDeleteAccount = document.getElementById('btn-delete-account');
if (btnDeleteAccount) {
    btnDeleteAccount.addEventListener('click', async () => {
        const confirmDelete = confirm("УВАГА!\nВи впевнені, що хочете назавжди видалити свій аккаунт та всі збережені збірки? Цю дію неможливо скасувати!");
        
        if (confirmDelete) {
            try {
                const res = await fetch(`${API_BASE_URL}/profile/${currentUserId}`, {
                    method: 'DELETE'
                });
                
                if (res.ok) {
                    // Видаляємо акаунт також з меню "Швидкого входу"
                    const email = document.getElementById('profile-email').value;
                    let accounts = getSavedAccounts();
                    accounts = accounts.filter(acc => acc.email !== email);
                    localStorage.setItem('cyber_saved_accounts', JSON.stringify(accounts));
                    renderSavedAccounts(); 
                    
                    // Очищаємо сесію
                    currentToken = null; 
                    currentUserId = null;
                    localStorage.removeItem('cyber_token'); 
                    localStorage.removeItem('cyber_user_id');
                    
                    checkAuthState(); 
                    goHome(); // Повертаємо на головну
                    showErrorAlert("Аккаунт видалено", "Ваш профіль та всі дані було назавжди видалено.", "success");
                } else {
                    showErrorAlert("Помилка", "Не вдалося видалити аккаунт. Спробуйте пізніше.");
                }
            } catch (e) {
                showErrorAlert("Помилка", "Сервер не відповідає.");
            }
        }
    });
}

// ====================================================
// === РОБОТА З ПРОФІЛЕМ ТА АКОРДЕОНОМ ЗБІРОК ===
// ====================================================

// Кеш для швидкого перекладу ID в Назву деталі
let componentCache = {};
async function preloadComponentCache() {
    if (Object.keys(componentCache).length > 0) return; 
    try {
        const endpoints = [
            '/cpus', '/gpus', '/motherboards', '/rams', '/storage', '/psus', '/coolers', '/cases',
            '/peripherals/mice', '/peripherals/keyboards', '/peripherals/headsets'
        ];
        const names = [
            'cpu', 'gpu', 'motherboard', 'ram', 'storage', 'psu', 'cooler', 'case',
            'mouse', 'keyboard', 'headset'
        ];
        for (let i=0; i<endpoints.length; i++) {
            const res = await fetch(`${API_BASE_URL}${endpoints[i]}`);
            const data = await res.json();
            componentCache[names[i]] = {};
            data.forEach(item => { componentCache[names[i]][item.id] = getCompName(item); });
        }
    } catch(e) { console.error("Cache load error", e); }
}

async function loadUserProfile() {
    if(!currentUserId) return;
    try {
        await preloadComponentCache(); 
        
        const [profileRes, buildsRes] = await Promise.all([
            fetch(`${API_BASE_URL}/profile/${currentUserId}`),
            fetch(`${API_BASE_URL}/profile/${currentUserId}/favorites`)
        ]);
        
        const profile = await profileRes.json();
        const builds = await buildsRes.json();

        document.getElementById('profile-username').value = profile.username;
        document.getElementById('profile-email').value = profile.email;
        const displayName = profile.username || "User";
        document.getElementById('profile-display-name').innerText = displayName;
        
        // --- НОВА ЛОГІКА ВІДОБРАЖЕННЯ АВАТАРКИ ---
        const avatarLetter = document.getElementById('profile-avatar-letter');
        const avatarImg = document.getElementById('profile-avatar-img');

        if (profile.avatar_url) {
            avatarImg.src = `${BACKEND_URL}${profile.avatar_url}`;
            avatarImg.classList.remove('hidden');
            avatarLetter.classList.add('hidden');
        } else {
            avatarLetter.innerText = displayName.charAt(0).toUpperCase();
            avatarLetter.classList.remove('hidden');
            avatarImg.classList.add('hidden');
        }

        // === НОВЕ: Оновлюємо кеш аватарки у збережених акаунтах ===
        let accounts = getSavedAccounts();
        let accIndex = accounts.findIndex(acc => acc.email === profile.email);
        if (accIndex !== -1) {
            accounts[accIndex].avatar_url = profile.avatar_url;
            localStorage.setItem('cyber_saved_accounts', JSON.stringify(accounts));
            renderSavedAccounts();
        }

        const buildsList = document.getElementById('saved-builds-list');
        if (builds.length === 0) {
            // Додали анімований клас
            buildsList.innerHTML = `<p class="empty-builds-text">У вас ще немає збережених збірок.</p>`;
        } else {
            buildsList.innerHTML = builds.map(b => {
                const c_cpu = b.cpu_id ? (componentCache['cpu'][b.cpu_id] || `CPU #${b.cpu_id}`) : 'Не обрано';
                const c_gpu = b.gpu_id ? (componentCache['gpu'][b.gpu_id] || `GPU #${b.gpu_id}`) : 'Не обрано';
                const c_mb = b.motherboard_id ? (componentCache['motherboard'][b.motherboard_id] || `MB #${b.motherboard_id}`) : 'Не обрано';
                const c_ram = b.ram_id ? (componentCache['ram'][b.ram_id] || `RAM #${b.ram_id}`) : 'Не обрано';
                const c_psu = b.psu_id ? (componentCache['psu'][b.psu_id] || `PSU #${b.psu_id}`) : 'Не обрано';
                const c_case = b.case_id ? (componentCache['case'][b.case_id] || `Case #${b.case_id}`) : 'Не обрано';
                
                // Периферія
                const c_mouse = b.mouse_id ? (componentCache['mouse'][b.mouse_id] || `Mouse #${b.mouse_id}`) : 'Не обрано';
                const c_kbd = b.keyboard_id ? (componentCache['keyboard'][b.keyboard_id] || `Kbd #${b.keyboard_id}`) : 'Не обрано';
                const c_head = b.headset_id ? (componentCache['headset'][b.headset_id] || `Headset #${b.headset_id}`) : 'Не обрано';
                
                return `
                    <div class="saved-build-item" id="build-item-${b.id}">
                        <div class="saved-build-header" onclick="this.parentElement.classList.toggle('expanded')">
                            <div>
                                <div class="saved-build-name" id="build-name-${b.id}">${b.name}</div>
                            </div>
                            <div class="build-actions">
                                <button class="btn-edit-build" onclick="renameBuild(event, ${b.id}, '${b.name}')" title="Перейменувати">
                                    <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                                </button>
                                <button class="btn-info" style="width: 32px; height: 32px; pointer-events: none;">
                                    <svg class="expand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width: 14px; transition: 0.3s;"><path d="M6 9l6 6 6-6"></path></svg>
                                </button>
                            </div>
                        </div>
                        <div class="saved-build-details">
                            <div class="build-component-row"><span class="comp-label">Процесор</span><span class="comp-val">${c_cpu}</span></div>
                            <div class="build-component-row"><span class="comp-label">Відеокарта</span><span class="comp-val">${c_gpu}</span></div>
                            <div class="build-component-row"><span class="comp-label">Мат. плата</span><span class="comp-val">${c_mb}</span></div>
                            <div class="build-component-row"><span class="comp-label">Пам'ять</span><span class="comp-val">${c_ram}</span></div>
                            <div class="build-component-row"><span class="comp-label">Блок жив.</span><span class="comp-val">${c_psu}</span></div>
                            <div class="build-component-row"><span class="comp-label">Корпус</span><span class="comp-val">${c_case}</span></div>
                            
                            <div class="build-component-row" style="margin-top: 10px; border-top: 1px dashed rgba(255,255,255,0.05); padding-top: 10px;">
                                <span class="comp-label" style="color: var(--accent-purple);">Миша</span><span class="comp-val">${c_mouse}</span>
                            </div>
                            <div class="build-component-row"><span class="comp-label" style="color: var(--accent-purple);">Клавіатура</span><span class="comp-val">${c_kbd}</span></div>
                            <div class="build-component-row"><span class="comp-label" style="color: var(--accent-purple);">Гарнітура</span><span class="comp-val">${c_head}</span></div>
                            
                            <div style="display: flex; gap: 10px; justify-content: center; margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.05);">
                                <button class="btn-export pdf" onclick="exportSavedBuild(event, 'pdf', ${b.id})">
                                    <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
                                    Чек
                                </button>
                                <button class="btn-export md" onclick="exportSavedBuild(event, 'md', ${b.id})">
                                    <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"></circle><circle cx="6" cy="12" r="3"></circle><circle cx="18" cy="19" r="3"></circle><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line></svg>
                                    Форум
                                </button>
                                <button class="btn-export link" onclick="exportSavedBuild(event, 'link', ${b.id})">
                                    <svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                                    Лінк
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        }
    } catch(e) { console.error("Помилка профілю", e); }
}

// Перейменування збірки
window.renameBuild = async function(event, buildId, oldName) {
    event.stopPropagation(); // Зупиняємо клік, щоб список не згортався
    const newName = prompt("Введіть нову назву для збірки:", oldName);
    if (!newName || newName === oldName) return;
    
    try {
        const res = await fetch(`${API_BASE_URL}/profile/${currentUserId}/favorites/${buildId}`, {
            method: 'PUT', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ build_name: newName })
        });
        const data = await res.json();
        if (data.success) {
            document.getElementById(`build-name-${buildId}`).innerText = newName;
            showErrorAlert("Успіх", "Назву збірки оновлено!", "success");
        } else {
            showErrorAlert("Помилка", "Не вдалося перейменувати.");
        }
    } catch(e) { showErrorAlert("Помилка", "Сервер не відповідає."); }
}

document.getElementById('btn-update-profile').addEventListener('click', async () => {
    const uname = document.getElementById('profile-username').value;
    const email = document.getElementById('profile-email').value;
    
    // === НОВЕ: Перевірка формату email при оновленні профілю ===
    if(email && !isValidEmail(email)) {
        showErrorAlert("Помилка формату", "Будь ласка, введіть коректний email."); 
        return; 
    }

    try {
        await fetch(`${API_BASE_URL}/profile/${currentUserId}`, {
            method: 'PUT', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: uname, email: email })
        });
        showErrorAlert("Успіх", "Дані профілю оновлено!", "success");
        loadUserProfile(); // Оновлюємо аватарку
    } catch(e) { showErrorAlert("Помилка", "Не вдалося оновити дані."); }
});

document.getElementById('btn-change-pass').addEventListener('click', async () => {
    const oldP = document.getElementById('profile-old-pass').value;
    const newP = document.getElementById('profile-new-pass').value;
    if(!oldP || !newP) { showErrorAlert("Увага", "Заповніть обидва поля пароля."); return; }
    try {
        const res = await fetch(`${API_BASE_URL}/profile/${currentUserId}/password`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ old_password: oldP, new_password: newP })
        });
        const data = await res.json();
        if(data.success) {
            showErrorAlert("Успіх", "Пароль змінено!", "success");
            document.getElementById('profile-old-pass').value = '';
            document.getElementById('profile-new-pass').value = '';
        } else { showErrorAlert("Помилка", "Невірний старий пароль."); }
    } catch(e) { showErrorAlert("Помилка", "Помилка сервера."); }
});

window.saveBuildToDB = async function(source) {
    if (!currentToken || !currentUserId) {
        showErrorAlert("Авторизація", "Для збереження збірок потрібно увійти в аккаунт.");
        authModal.classList.add('active');
        return;
    }

    let buildObj = {};
    let buildName = "";

    if (source === 'smart') {
        if (!lastSmartBuild) return;
        buildObj = lastSmartBuild;
        buildName = `Розумна збірка (${new Date().toLocaleDateString('uk-UA')})`;
    } else if (source === 'manual') {
        buildObj = manualState;
        if (!buildObj.cpu || !buildObj.motherboard) {
            showErrorAlert("Увага", "Оберіть хоча б базові комплектуючі (CPU, MB)."); return;
        }
        buildName = `Моя кастомна збірка (${new Date().toLocaleDateString('uk-UA')})`;
    }

    // ВАЖЛИВО: Замість || 0 ми тепер передаємо || null, щоб БД не падала
    const payload = {
        build_name: buildName,
        cpu_id: buildObj.cpu?.id || null, gpu_id: buildObj.gpu?.id || null,
        motherboard_id: buildObj.motherboard?.id || null, ram_id: buildObj.ram?.id || null,
        storage_id: buildObj.storage?.id || null, psu_id: buildObj.psu?.id || null,
        cooler_id: buildObj.cooler?.id || null, case_id: buildObj.case?.id || null,
        mouse_id: buildObj.mouse?.id || null, keyboard_id: buildObj.keyboard?.id || null,
        headset_id: buildObj.headset?.id || null
    };

    try {
        const res = await fetch(`${API_BASE_URL}/profile/${currentUserId}/favorites`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            showErrorAlert("Успіх!", "Збірку успішно збережено у вашому кабінеті.", "success");
        } else {
            showErrorAlert("Помилка", "Не вдалося зберегти збірку.");
        }
    } catch(e) { showErrorAlert("Помилка", "Помилка зв'язку з сервером."); }
};

// НОВА ФУНКЦІЯ: Експорт збереженої збірки через Python API (з реальним завантаженням)
window.exportSavedBuild = async function(event, format, buildId) {
    event.stopPropagation(); // Забороняємо акордеону згортатися при кліку на кнопку
    
    try {
        let res;
        if (format === 'pdf') {
            res = await fetch(`${API_BASE_URL}/export/pdf/${buildId}`);
        } else if (format === 'md') {
            res = await fetch(`${API_BASE_URL}/export/markdown/${buildId}`);
        } else if (format === 'link') {
            res = await fetch(`${API_BASE_URL}/export/share/${buildId}`);
        }

        const data = await res.json();

        if (!res.ok) {
            throw new Error(data.error || "Внутрішня помилка сервера");
        }

        if (format === 'pdf') {
            // 1. Формуємо повний шлях до файлу на нашому Flask-сервері
            // Flask автоматично роздає файли з папки static
            const fileUrl = `${BACKEND_URL}${data.pdf_download_url}`;
            
            // 2. Завантажуємо файл у пам'ять браузера як Blob (бінарні дані)
            const pdfRes = await fetch(fileUrl);
            const blob = await pdfRes.blob();
            
            // 3. Створюємо тимчасове посилання та примусово "клікаємо" по ньому для скачування
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `CyberCraft_Build_${buildId}_Spec.pdf`; // Назва файлу при скачуванні
            document.body.appendChild(a);
            a.click();
            
            // 4. Прибираємо за собою сміття
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            showErrorAlert("Готово!", "PDF-специфікацію успішно завантажено на ваш пристрій.", "success");
        } 
        else if (format === 'md') {
            navigator.clipboard.writeText(data.markdown_text);
            showErrorAlert("Успіх", "Код для Reddit/Форумів скопійовано в буфер обміну!", "success");
        } 
        else if (format === 'link') {
            navigator.clipboard.writeText(data.short_url);
            showErrorAlert("Посилання створено!", `Ваше унікальне посилання скопійовано:\n\n${data.short_url}`, "success");
        }
    } catch (e) {
        showErrorAlert("Помилка експорту", e.message || "Не вдалося зв'язатися з сервером.");
    }
}

// ====================================================
// === ЗАВАНТАЖЕННЯ ВЛАСНОЇ АВАТАРКИ ===
// ====================================================
const avatarUpload = document.getElementById('avatar-upload');
if (avatarUpload) {
    avatarUpload.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('avatar', file);

        try {
            const res = await fetch(`${API_BASE_URL}/profile/${currentUserId}/avatar`, {
                method: 'POST',
                body: formData 
            });
            const data = await res.json();
            
            if (res.ok) {
                showErrorAlert("Успіх", "Вашу аватарку оновлено!", "success");
                loadUserProfile(); 
            } else {
                showErrorAlert("Помилка", data.error || "Не вдалося завантажити фото.");
            }
        } catch (err) {
            showErrorAlert("Помилка", "Сервер не відповідає.");
        }
    });
}

// ====================================================
// === ЛОГІКА ІМПОРТУ ЗБІРКИ ЗА ПОСИЛАННЯМ ===
// ====================================================
async function checkSharedBuildInURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const buildId = urlParams.get('build');
    
    let buildData = null;

    try {
        if (buildId) {
            // Варіант 1: Лінк із Кабінету (?build=15)
            const res = await fetch(`${API_BASE_URL}/build/${buildId}`);
            if (res.ok) buildData = await res.json();
        } else if (urlParams.has('cpu') || urlParams.has('mb') || urlParams.has('gpu')) {
            // Варіант 2: Лінк з Конструктора (?cpu=1&gpu=2...)
            buildData = {
                name: "Імпортована конфігурація",
                cpu_id: parseInt(urlParams.get('cpu')) || null,
                gpu_id: parseInt(urlParams.get('gpu')) || null,
                motherboard_id: parseInt(urlParams.get('mb')) || null,
                ram_id: parseInt(urlParams.get('ram')) || null,
                storage_id: parseInt(urlParams.get('st')) || null,
                cooler_id: parseInt(urlParams.get('col')) || null,
                psu_id: parseInt(urlParams.get('psu')) || null,
                case_id: parseInt(urlParams.get('cas')) || null
            };
        }

        if (buildData) {
            // Розставляємо деталі по слотах у "Ручній збірці"
            const typeMap = {
                'cpu': 'cpu_id', 'gpu': 'gpu_id', 'motherboard': 'motherboard_id', 
                'ram': 'ram_id', 'storage': 'storage_id', 'cooler': 'cooler_id', 
                'psu': 'psu_id', 'case': 'case_id'
            };
            
            for (const [type, idKey] of Object.entries(typeMap)) {
                const componentId = buildData[idKey];
                if (componentId) {
                    const itemsRes = await fetch(`${API_BASE_URL}${apiEndpoints[type]}`);
                    const items = await itemsRes.json();
                    const fullComponent = items.find(i => i.id === componentId);
                    
                    if (fullComponent) {
                        manualState[type] = fullComponent;
                        const slotCard = document.querySelector(`.slot-card[data-type="${type}"]`);
                        if (slotCard) {
                            const nameEl = slotCard.querySelector('.selected-name');
                            nameEl.innerText = getCompName(fullComponent);
                            nameEl.style.color = 'var(--accent-cyan)';
                            slotCard.style.borderColor = 'var(--accent-cyan)';
                        }
                    }
                }
            }
            
            // Оновлюємо підсумок, перемикаємо сторінку і чистимо URL
            updateManualSummary();
            switchPage('nav-manual');
            window.scrollTo({ top: 0, behavior: 'smooth' });
            showErrorAlert("Збірку імпортовано! 🚀", `Конфігурацію "${buildData.name}" завантажено. Тепер ви можете її редагувати!`, "success");
            
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    } catch (err) {
        console.error("Помилка імпорту:", err);
    }
}

// Запускаємо перевірку одразу після завантаження сторінки
checkSharedBuildInURL();