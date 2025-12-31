// if conditnion navbar
document.addEventListener('DOMContentLoaded', () => {
    fetchLocations()
    populateDropdowns().then(() => {
        applyFilters(); // Load card awal setelah dropdown siap
        applyFiltersToMapAndList();
    });
    const userId = sessionStorage.getItem('user_id')
    const role = sessionStorage.getItem('role')
    const liYourOrder = document.getElementById('yourOrder')
    const liTransactnionHistory = document.getElementById('transactionHistory')
    const liLogin = document.getElementById('li-login')
    const liProfile = document.getElementById('li-profile')
    const btnLogin = document.getElementById('btnLogin')
    const btnProfile = document.getElementById('btnProfile')
    const btnLogout = document.getElementById('btnLogout')
    const userName = document.getElementById('user_name')
    userName.textContent = sessionStorage.getItem('name')

    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('nav ul li .menu');

    menuLinks.forEach(link => {
        const href = link.getAttribute('href');

        if (!href || href === '#') return;

        // Cocokkan URL
        if (href === currentPath) {
            link.classList.add(
                'text-accent',
                'font-semibold'
            );

            link.setAttribute('aria-current', 'page');
        } else {
            link.classList.remove(
                'text-accent',
                'font-semibold'
            );
            link.classList.add('text-white')
            link.removeAttribute('aria-current');
        }
    });

    if (userId && role) {
        btnLogin.classList.remove('md:flex')

        btnProfile.classList.remove('hidden')
        btnProfile.classList.add('flex')

        liYourOrder.classList.remove('hidden')
        liTransactnionHistory.classList.remove('hidden')
        liLogin.classList.add('hidden')
        liProfile.classList.remove('hidden')
    } else {
        // LOGOUT
        // btnLogin.classList.remove('hidden')
        btnLogin.classList.add('md:flex')

        btnProfile.classList.remove('md:flex')
        // btnProfile.classList.add('hidden')
        // btnProfile.classList.remove('flex')

        liYourOrder.classList.add('hidden')
        liTransactnionHistory.classList.add('hidden')
        liProfile.classList.add('hidden')
    }

    btnLogout.addEventListener('click', async () => {
        try {
            const res = await fetch('/api/logout', {
                method: 'POST',
                credentials: 'include'
            })

            if (res.ok) {
                sessionStorage.clear()
                localStorage.clear()
                window.location.href = '/'
            } else {
                alert('Logout gagal')
            }
        } catch (err) {
            console.error('Logout error:', err)
        }
    })

    const filters = {
        lokasi: '',
        tipe: ''
    };

    // Ambil data dropdown dari API dan isi dropdown
    async function populateDropdowns() {
        try {
            const lokasiResponse = await fetch('/api/available-city');
            const lokasiData = await lokasiResponse.json();

            // Isi dropdown Lokasi
            const lokasiSelect = document.getElementById('lokasi');
            lokasiSelect.innerHTML = '<option value="">Semua Lokasi</option>';
            lokasiData.data.forEach(item => {
                if (!item.city) return;
                const option = document.createElement('option');
                option.value = item.city;
                option.textContent = item.city;
                lokasiSelect.appendChild(option);
            });

            // Tambahkan event listener setelah dropdown diisi
            attachEventListeners();

        } catch (err) {
            console.error("Gagal mengambil data dropdown:", err);
        }
    }

    // Fungsi untuk mengirim filter dan render card
    async function applyFilters() {
        const params = new URLSearchParams({
            city: filters.lokasi,
            type: filters.tipe
        });
        try {
            const response = await fetch(`/api/food-waste/filter?${params}`);
            const json = await response.json();

            if (json.status === 'success' && json.data) {
                renderCards(json.data); // Panggil fungsi render manual
            } else {
                document.getElementById('foodList').innerHTML = '<p>Data tidak ditemukan.</p>';
            }
        } catch (err) {
            console.error('Error:', err);
            document.getElementById('foodList').innerHTML = '<p>Terjadi kesalahan.</p>';
        }
    }

    function renderCards(foodWastes) {
        const grid = document.getElementById('foodList');
        grid.innerHTML = '';

        if (!foodWastes || foodWastes.length === 0) {
            grid.innerHTML = '<p>Tidak ada data yang ditemukan.</p>';
            return;
        }

        foodWastes.forEach(item => {
            const card = document.createElement('div');
            card.className = 'bg-white rounded-xl overflow-hidden shadow-sm p-3';
            card.innerHTML = `
        <div class="relative">
            <img 
                src="${item.foto_url}" 
                class="w-full h-48 object-cover" 
                alt="${item.name || 'Food Item'}"
            />
            <span class="absolute top-2 right-2 bg-white text-xs font-bold px-2 py-1 rounded-full shadow">
                ${item.city || 'Kota Tidak Diketahui'}
            </span>
        </div>
        <div class="p-3">
            <h2 class="text-lg font-bold text-green-900">${item.name || 'Nama Makanan'}</h2>
            <p class="text-sm text-gray-600 mt-1">${item.city || 'Nama Restoran'}</p>
            <p class="text-xs text-gray-500 mt-1">${item.description || 'Deskripsi tidak tersedia'}</p>
            <div class="mt-2">
                <span class="text-sm font-semibold text-green-900">Rp.${item.price || '0'}</span>
                <span class="text-xs text-gray-500 ml-2">Stok: ${item.stock || 'N/A'}</span>
            </div>
            <button data-food-waste-id="${item.id_food_waste}" class="mt-3 w-full py-1.5 bg-green-900 text-white rounded-full text-sm hover:bg-green-800 transition check-out-btn" >
                Check Out
            </button>
        </div>
        `;
            grid.appendChild(card);
            // Tambahkan event listener ke tombol "Check Out"
            card.querySelector('.check-out-btn').addEventListener('click', (e) => {
                selectedFoodWasteId = e.currentTarget.dataset.foodWasteId
                openFoodDetailModal(item);
            });
        });
    }




    // Fungsi untuk membuka modal detail makanan
    let foodModal = null;
    let selectedFoodWasteId = null;

    function openFoodDetailModal(item) {
        // Isi data
        document.getElementById('modalFoto').src =
            item.foto
                ? `/static/uploads/food_waste/${item.foto}`
                : '/static/images/placeholder.png';

        document.getElementById('modalFoto').src = item.foto_url || '-';
        document.getElementById('modalNamaResto').textContent = item.name || '-';
        document.getElementById('modalJamBuka').textContent =
            `Jam buka: ${item.open || '-'} - ${item.closed || '-'}`;
        document.getElementById('modalLokasi').textContent =
            `Lokasi: ${item.city || '-'}`;
        document.getElementById('modalDescription').textContent =
            item.description || '-';

        function formatRupiah(number) {
            return 'Rp ' + number.toLocaleString('id-ID');
        }


        // Quantity
        let quantity = 1;
        const price = item.price || 0;
        const qtyEl = document.getElementById('quantity');
        const totalEl = document.getElementById('totalPrice')

        function updateTotal() {
            totalEl.textContent = formatRupiah(quantity * price);
            qtyEl.textContent = quantity;
        }

        updateTotal();


        document.getElementById('decreaseQty').onclick = () => {
            if (quantity > 1) {
                quantity--;
                updateTotal();
            }
        };

        document.getElementById('increaseQty').onclick = () => {
            if (quantity < (item.stock || 10)) {
                quantity++;
                updateTotal();
            }
        };

        window.currentOrder = {
            item,
            get quantity() { return quantity; },
            get total() { return quantity * price; }
        };
        // Modal instance (SINGLETON)
        const modalEl = document.getElementById('foodDetailModal');
        if (!foodModal) {
            foodModal = new Modal(modalEl, {
                backdrop: 'static',
                closable: false
            });
        }

        document.getElementById('cancelOrder').onclick = () => foodModal.hide();
        document.getElementById('tutupButton').onclick = () => foodModal.hide();

        document.getElementById('confirmOrder').addEventListener('click', async () => {
            const paymentMethod = document.getElementById('addPaymentMethod').value;
            if (!paymentMethod) {
                alert('Pilih metode pembayaran terlebih dahulu');
                return;
            }

            const payload = {
                qty: currentOrder.quantity,
                price: currentOrder.item.price,
                payment_type: paymentMethod,
                user_id: sessionStorage.getItem('user_id'),     // inject dari Jinja
                food_waste_id: selectedFoodWasteId
            };

            try {
                const res = await fetch('/api/transaction', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const json = await res.json();

                if (json.status === 'success') {
                    alert('Pesanan berhasil dibuat!');
                    foodModal.hide();
                } else {
                    alert(json.message || 'Gagal membuat pesanan');
                }
            } catch (err) {
                console.error(err);
                alert('Terjadi kesalahan');
            }
        })


        foodModal.show();
    }




    // Fungsi untuk menerapkan filter ke peta dan sidebar list (tanpa API)
    function applyFiltersToMapAndList() {
        // Filter data berdasarkan state filter
        let filtered = allLocations;

        if (filters.lokasi) {
            filtered = filtered.filter(loc => loc.city === filters.lokasi);
        }

        if (filters.tipe) {
            filtered = filtered.filter(loc => loc.type === filters.tipe);
        }

        // Kosongkan marker lama
        for (const id in markers) {
            map.removeLayer(markers[id]);
        }
        markers = {};

        // Isi data baru ke peta dan sidebar
        renderList(filtered);
        addMarkersToMap(filtered);
    }



    // Fungsi untuk menambahkan event listener ke dropdown
    function attachEventListeners() {
        // Event listener untuk select lokasi
        document.getElementById('lokasi').addEventListener('change', (e) => {
            filters.lokasi = e.target.value;
            applyFilters();
            applyFiltersToMap();
        });

        // Event listener untuk select tipe
        document.getElementById('type').addEventListener('change', (e) => {
            filters.tipe = e.target.value;
            applyFilters();
            applyFiltersToMap();
        });

    }



    const switchButton = document.getElementById('switch')
    const foodList = document.getElementById('foodList')
    const foodMaps = document.getElementById('foodMaps')

    switchButton.addEventListener('change', () => {
        if (switchButton.checked) {
            // Switch ON
            foodList.classList.remove('hidden')
            foodMaps.classList.add('hidden')
        } else {
            // Switch OFF
            foodList.classList.add('hidden')
            foodMaps.classList.remove('hidden')
        }
    })






    let locations = [];

    // Ambil data dari API
    async function fetchLocations() {
        try {
            const response = await fetch('/api/food-waste/filter');
            const json = await response.json();

            if (json.status === 'success' && json.data) {
                locations = json.data; // Ambil dari json.data
            } else {
                console.error("Gagal mengambil data lokasi:", json);
                locations = []; // Pastikan locations kosong jika gagal
            }

            renderList(locations);
            addMarkersToMap();
        } catch (error) {
            console.error("Gagal mengambil data lokasi:", error);
            locations = []; // Jaga-jaga jika error
        }
    }

    /* =========================
       Init Leaflet map
       ========================= */
    const map = L.map('map').setView([-6.2, 106.85], 11);

    // OSM tiles (gratis)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    const markers = {};

    // custom icon (optional) — simple colored circle icon
    const icon = L.icon({
        iconUrl: 'data:image/svg+xml;utf8,' + encodeURIComponent(
            `<svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" fill="#ffcc00" stroke="#d87a00" stroke-width="1.5"/>
        <text x="12" y="15" font-size="10" text-anchor="middle" fill="#a00" font-family="Arial" font-weight="700">S</text>
        </svg>`
        ),
        iconSize: [36, 36],
        iconAnchor: [18, 36],
        popupAnchor: [0, -36]
    });

    // add markers to map
    function addMarkersToMap() {
        locations.forEach(loc => {

            const popupContent = `
            <div style="
                max-width: 300px;
                padding: 12px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                background: white;
                font-family: sans-serif;
            ">
                <img src="/static/${loc.foto || 'images/placeholder.png'}"
                     alt="${escapeHtml(loc.name)}"
                     style="width:100%; height:100px; object-fit:cover; border-radius:6px">

                <h3 style="font-weight:bold; margin-top:8px;">
                    ${escapeHtml(loc.name)}
                </h3>

                <p style="font-size:13px; color:#555;">
                    ${escapeHtml(loc.address)}
                </p>

                <p style="font-size:13px;">
                    Resto: <b>${escapeHtml(loc.resto_name || '-')}</b>
                </p>

                <p style="font-size:13px;">
                    Harga: <b>Rp${loc.price}</b>
                </p>

                <div style="margin-top:10px; display:flex; gap:6px;">
                    <a href="https://www.google.com/maps/dir/?api=1&destination=-7.746680095458424,110.3542465881601"
                       target="_blank"
                       style="padding:6px 10px; background:#22c55e; color:white; border-radius:4px; font-size:12px;">
                        Petunjuk Arah
                    </a>
                    <button onclick="openFoodDetailModal(${loc.id_food_waste})"
                        style="padding:6px 10px; background:#e5e7eb; border-radius:4px; font-size:12px;">
                        Detail
                    </button>
                </div>
            </div>
        `;

            const marker = L.marker(
                [parseFloat(loc.latitude), parseFloat(loc.longitude)],
                { icon }
            ).addTo(map);

            marker.bindPopup(popupContent, {
                maxWidth: 320
            });

            markers[loc.id_food_waste] = marker;
        });
    }

    /* =========================
       Sidebar list
       ========================= */
    const listEl = document.getElementById('list');

    function renderList(items) {
        listEl.innerHTML = '';

        items.forEach(item => {
            const el = document.createElement('div');
            el.className =
                'p-3 border border-gray-100 rounded-lg mb-2 cursor-pointer hover:bg-blue-50 hover:border-blue-100';

            el.innerHTML = `
            <div class="font-bold text-gray-800">
                ${escapeHtml(item.name)}
            </div>
            <div class="text-sm text-gray-600 mb-2">
                ${escapeHtml(item.address)}
            </div>
            <a class="inline-block px-3 py-1 bg-green-500 text-white rounded-md text-sm">
                Petunjuk Arah
            </a>
        `;

            // klik card → fly ke marker
            el.addEventListener('click', (ev) => {
                if (ev.target.tagName === 'A') return;

                const marker = markers[item.id_food_waste];
                if (marker) {
                    map.flyTo(marker.getLatLng(), 15, { duration: 0.6 });
                    marker.openPopup();
                }
            });

            // klik petunjuk arah
            el.querySelector('a').addEventListener('click', (ev) => {
                ev.stopPropagation();
                window.open(
                    `https://www.google.com/maps/dir/?api=1&destination=${item.latitude},${item.longitude}`,
                    '_blank'
                );
            });

            listEl.appendChild(el);
        });
    }

    /* =========================
       Simple search
       ========================= */
    const q = document.getElementById('q');
    const clear = document.getElementById('clear');

    q.addEventListener('input', () => {
        const v = q.value.trim().toLowerCase();

        if (!v) {
            renderList(locations);
            for (const id in markers) markers[id].addTo(map);
            return;
        }

        const filtered = locations.filter(l =>
            (l.name + ' ' + l.address).toLowerCase().includes(v)
        );

        renderList(filtered);

        for (const id in markers) {
            const show = filtered.some(f => f.id_food_waste == id);
            if (show) {
                markers[id].addTo(map);
            } else {
                map.removeLayer(markers[id]);
            }
        }
    });

    clear.addEventListener('click', () => {
        q.value = '';
        q.dispatchEvent(new Event('input'));
    });

    /* =========================
       User location (watchPosition). Browser will prompt for permission.
       NOTE: geolocation requires https (or localhost).
       ========================= */
    let userMarker = null;
    let userCircle = null;
    // Ganti ID ini agar tidak bentrok
    const locationStatus = document.getElementById('location-status');

    if ('geolocation' in navigator) {
        const opts = { enableHighAccuracy: true, maximumAge: 10000, timeout: 10000 };

        const success = pos => {
            const lat = pos.coords.latitude;
            const lng = pos.coords.longitude;
            const acc = pos.coords.accuracy; // meters

            // Ganti juga di sini
            locationStatus.textContent = `Kamu: ${lat.toFixed(5)}, ${lng.toFixed(5)} (akurat ±${Math.round(acc)} m)`;

            if (!userMarker) {
                userMarker = L.marker([lat, lng], {
                    // simple blue circle marker
                    icon: L.icon({
                        iconUrl: 'data:image/svg+xml;utf8,' + encodeURIComponent(
                            `<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" fill="#2b8cff" stroke="#1a6fe8" stroke-width="1.5"/>
                </svg>`
                        ),
                        iconSize: [28, 28], iconAnchor: [14, 14]
                    })
                }).addTo(map).bindPopup('Kamu di sini');
                userCircle = L.circle([lat, lng], { radius: acc, color: '#2b8cff', weight: 1, fillOpacity: 0.08 }).addTo(map);
                map.setView([lat, lng], 14);
                userMarker.openPopup();
            } else {
                userMarker.setLatLng([lat, lng]);
                userCircle.setLatLng([lat, lng]).setRadius(acc);
            }
        };

        const error = err => {
            // Ganti juga di sini
            locationStatus.textContent = `Gagal ambil lokasi: ${err.message}`;
        };

        // start watching position
        navigator.geolocation.watchPosition(success, error, opts);

    } else {
        // Ganti juga di sini
        locationStatus.textContent = 'Geolocation tidak tersedia di browser ini.';
    }

    /* =========================
       Small helper
       ========================= */
    function escapeHtml(s) {
        return String(s || '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
    }
})
