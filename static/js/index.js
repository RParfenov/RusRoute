async function showMapPreview() {
    const cityFrom = document.getElementById('extra-city1').value.trim();
    const cityTo = document.getElementById('extra-city2').value.trim();

    if (!cityFrom || !cityTo) {
        alert('Пожалуйста, выберите оба города.');
        return;
    }

    try {
        const response = await fetch(`/get-map-image?from=${encodeURIComponent(cityFrom)}&to=${encodeURIComponent(cityTo)}`);
        const data = await response.json();

        if (response.ok) {
            document.getElementById('map-image').src = data.map_url;
            document.getElementById('map-preview').style.display = 'block';
        } else {
            alert('Ошибка: ' + data.error);
        }
    } catch (err) {
        console.error(err);
        alert('Не удалось загрузить карту.');
    }
}

function showCityOnMap(which) {
    let cityName;
    if (which === 'from') {
        cityName = document.getElementById('extra-city1').value.trim();
    } else if (which === 'to') {
        cityName = document.getElementById('extra-city2').value.trim();
    } else {
        alert('Некорректный параметр');
        return;
    }

    if (!cityName) {
        alert('Город не указан');
        return;
    }
    const url = `/map/${encodeURIComponent(cityName)}`;
    window.location.href = url;
}