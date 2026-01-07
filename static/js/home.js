document.addEventListener("DOMContentLoaded", async () => {
    const dashboard = document.getElementById('dashboard');
    const leaderbord = document.getElementById('leaderbord');
    const userId = sessionStorage.getItem('user_id');
    let innerLeaderbord = "";

    try {
        const [mostRes, leastRes, sumEdibleRes, sumWasteRes, bestSellingRes] = await Promise.all([
            fetch('http://127.0.0.1:5000/api/most-stock/' + userId),
            fetch('http://127.0.0.1:5000/api/least-stock/' + userId),
            fetch('http://127.0.0.1:5000/api/sum-edible/' + userId),
            fetch('http://127.0.0.1:5000/api/sum-waste/' + userId),
            fetch('http://127.0.0.1:5000/api/best-selling/' + userId),
        ]);

        const mostResult = await mostRes.json();
        const leastResult = await leastRes.json();
        const sumEdibleResult = await sumEdibleRes.json();
        const sumWasteResult = await sumWasteRes.json();
        const bestSellingResult = await bestSellingRes.json();

        dashboard.innerHTML = `
            <div class="bg-[#FBFF6D] w-[150px] h-fit xl:w-[210px] xl:h-[210px] rounded-lg px-4 py-3 xl:px-6 xl:py-5 flex flex-col justify-between items-start gap-3 xl:gap-0">
                <div>
                    <h3 class="self-end font-bold text-sm">Stok Terbanyak</h3>
                    <h3 class="self-end font-bold text-xl xl:text-2xl">${mostResult.data.name}</h3>
                </div>
                <h3 class="self-end font-bold text-5xl">${mostResult.data.stock}</h3>
            </div>

            <div class="bg-[#FFB16D] w-[150px] h-fit xl:w-[210px] xl:h-[210px] rounded-lg px-4 py-3 xl:px-6 xl:py-5 flex flex-col justify-between items-start gap-3 xl:gap-0">
                <div>
                    <h3 class="self-end font-bold text-sm">Stok Menipis</h3>
                    <h3 class="self-end font-bold text-xl xl:text-2xl">${leastResult.data.name}</h3>
                </div>
                <h3 class="self-end font-bold text-5xl">${leastResult.data.stock}</h3>
            </div>

            <div class="bg-[#C2D9FF] w-[150px] h-[150px] xl:w-[210px] xl:h-[210px] rounded-lg px-4 py-3 xl:px-6 xl:py-5 flex flex-col justify-between items-start gap-3 xl:gap-0">
                <div>
                    <h3 class="self-end font-bold text-sm">Total Food</h3>
                    <h3 class="self-end font-bold text-2xl">Edible</h3>
                </div>
                <h3 class="self-end font-bold text-5xl">${sumEdibleResult.data.total_edible}</h3>
            </div>

            <div class="bg-[#FFDC6E] w-[150px] h-[150px] xl:w-[210px] xl:h-[210px] rounded-lg px-4 py-3 xl:px-6 xl:py-5 flex flex-col justify-between items-start gap-3 xl:gap-0">
                <div>
                    <h3 class="self-end font-bold text-sm">Total Food</h3>
                    <h3 class="self-end font-bold text-2xl">Waste</h3>
                </div>
                <h3 class="self-end font-bold text-5xl">${sumWasteResult.data.total_waste}</h3>
            </div>
        `;

        bestSellingResult.data.forEach((item, index) => {
            let bgColor = "#D4D925";

            if (item.no === 1) bgColor = "#EAB308";
            if (item.no === 2) bgColor = "#3B82F6";
            if (item.no === 3) bgColor = "#F97316";

            innerLeaderbord += `
                <div class="px-5 py-2 xl:py-2.5 rounded-[48px] flex justify-between items-center w-full h-fit bg-[${bgColor}]">
                    <h3 class="font-semibold text-lg xl:text-lg w-[90%]">${item.name}</h3>
                    <h3 class="font-bold text-lg xl:text-lg">${item.total_transaction}</h3>
                </div>
            `;
        });

        leaderbord.innerHTML = innerLeaderbord;
    } catch (error) {
        console.error("Gagal mengambil data: ", error);
        dashboard.innerHTML = `<p class="text-red-500">Gagal memuat data</p>`;
    }
})