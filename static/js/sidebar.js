document.addEventListener('DOMContentLoaded', () => {
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('aside ul li a');

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
})