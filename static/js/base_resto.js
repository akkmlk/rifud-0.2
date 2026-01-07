if (!sessionStorage.getItem('user_id')) {
    window.location.href = '/'
} else {
    if (sessionStorage.getItem('role') == 'client') {
        window.location.href = '/'
    }
}