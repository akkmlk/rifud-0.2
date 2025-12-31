document.addEventListener('DOMContentLoaded', () => {
    const formSubmit = document.getElementById('formRegistResto')

    formSubmit.addEventListener('submit', async function (e) {
        e.preventDefault();

        const name = document.getElementById('name').value;
        const address = document.getElementById('address').value;
        const city = document.getElementById('city').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        if (name === "" || address === "" || city === "" || email === "" || password === "") {
            alert("Wajib isi semua inputan")
        } else {
            await fetch('http://127.0.0.1:5000/api/registration-resto', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                    name: name,
                    city: city,
                    address: address
                })
            })
                .then(res => res.json())
                .then(result => {
                    if (result.status === 'success') {
                        const user = result.data;
                        alert("Restoan Berhasil didaftarkan".concat(" ").concat(user.address))
                        window.location.href = '/login'
                    } else {
                        alert(result.message)
                        console.log(result.message)
                    }
                })
                .catch(err => {
                    console.error(err)
                })
        }

    });
})