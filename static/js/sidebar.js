document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('aside ul li a');
    const btnLogoutSidebar = document.getElementById('btnLogoutSidebar')

    menuLinks.forEach(link => {
        const href = link.getAttribute('href');

        if (!href || href === '#') return;

        // Cocokkan URL
        if (href === currentPath) {
            link.classList.add(
                'bg-green-800'
            );

            link.setAttribute('aria-current', 'page');
        } else {
            link.classList.remove(
                'hover:bg-green-800'
            );
            link.classList.add('text-white')
            link.removeAttribute('aria-current');
        }
    });

    btnLogoutSidebar.addEventListener('click', async (e) => {
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
})