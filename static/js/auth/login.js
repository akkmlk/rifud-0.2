document.addEventListener('DOMContentLoaded', () => {
    const user_id = sessionStorage.getItem('user_id')

    if (user_id) {
        window.location.href = '/'
    }
    const formSubmit = document.getElementById('loginForm')

    formSubmit.addEventListener('submit', async function (e) {
        e.preventDefault();

        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        if (email === "" || password === "") {
            alert("Wajib isi semua inputan")
        } else {
            await fetch('http://127.0.0.1:5000/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            })
                .then(res => res.json())
                .then(result => {
                    if (result.status === 'success') {
                        const user = result.data;
                        sessionStorage.setItem('user_id', user.id)
                        sessionStorage.setItem('role', user.role)
                        sessionStorage.setItem('name', user.name)

                        if (user.role === 'client') {
                            window.location.href = '/'
                        } else {
                            window.location.href = '/home-resto'
                        }

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
