// const name = document.getElementById('name')
// name.textContent = sessionStorage.getItem('name')
const btnLogout = document.getElementById('btnLogout')
btnLogout.addEventListener('click', async (e) => {
    e.preventDefault()

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