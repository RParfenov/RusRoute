document.addEventListener('DOMContentLoaded', function() {
    const fromInput = document.getElementById('extra-city1')
    const toInput = document.getElementById('extra-city2')
    const link = document.getElementById('show-route-btn')

    if (!fromInput || !toInput || !link) return;

    function updateRouteLink() {
        const from_city = fromInput.value.trim() || 'Москва';
        const to_city = toInput.value.trim() || 'Казань';

        const url = `/route?city_from=${encodeURIComponent(from_city)}&city_to=${encodeURIComponent(to_city)}`;
        link.href = url;
    }

    fromInput.addEventListener('input', updateRouteLink)
    toInput.addEventListener('input', updateRouteLink)

    updateRouteLink();
})