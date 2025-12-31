document.addEventListener('DOMContentLoaded', () => {
    const formSubmit = document.getElementById('registerForm')
    sessionStorage.clear()

    formSubmit.addEventListener('submit', async function (e) {
        e.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        if (name === "" || email === "" || password === "") {
            alert("Wajib isi semua inputan")
        } else {
            await fetch('http://127.0.0.1:5000/api/registration-user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                })
            })
                .then(res => res.json())
                .then(result => {
                    if (result.status === 'success') {
                        alert("Daftar Berhasil")
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