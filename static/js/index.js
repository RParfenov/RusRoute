document.addEventListener('DOMContentLoaded', function() {
    // Инициализация карты OpenLayers
    const map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([37.6156, 55.7522]), // Москва
            zoom: 7
        })
    });

    // Источник для маркеров
    const vectorSource = new ol.source.Vector();

    // Слой для маркеров
    const vectorLayer = new ol.layer.Vector({
        source: vectorSource
    });

    map.addLayer(vectorLayer);

    // Функция для получения координат города через API
    async function getCityCoordinates(cityName) {
        if (!cityName) return null;

        try {
            const response = await fetch(`/api/city-coordinates/${encodeURIComponent(cityName)}`);
            if (!response.ok) throw new Error('Город не найден');

            const data = await response.json();
            return {
                lat: data.lat,
                lon: data.lon,
                name: data.name
            };
        } catch (error) {
            console.error(`Ошибка при получении координат для "${cityName}":`, error);
            return null;
        }
    }

    // Функция для добавления маркера
    function addMarker(lat, lon, color, label) {
        const feature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat]))
        });

        // Стиль маркера
        feature.setStyle(
            new ol.style.Style({
                image: new ol.style.Circle({
                    radius: 8,
                    fill: new ol.style.Fill({ color: color }),
                    stroke: new ol.style.Stroke({ color: 'black', width: 2 })
                }),
                text: new ol.style.Text({
                    text: label,
                    font: '12px Arial',
                    offsetY: -15,
                    fill: new ol.style.Fill({ color: 'black' })
                })
            })
        );

        vectorSource.addFeature(feature);
    }

    // Функция для обновления маркеров
    async function updateMarkers() {
        // Очищаем предыдущие маркеры
        vectorSource.clear();

        const fromInput = document.getElementById('extra-city1').value.trim();
        const toInput = document.getElementById('extra-city2').value.trim();

        // Получаем координаты
        const fromCoords = await getCityCoordinates(fromInput);
        const toCoords = await getCityCoordinates(toInput);

        // Добавляем маркеры
        if (fromCoords) {
            addMarker(fromCoords.lat, fromCoords.lon, '#ff6633', 'Откуда');
        }

        if (toCoords) {
            addMarker(toCoords.lat, toCoords.lon, '#10ff04', 'Куда');
        }

        // Центрируем карту на маркерах
        if (fromCoords && toCoords) {
            const extent = vectorSource.getExtent();
            if (!ol.extent.isEmpty(extent)) {
                map.getView().fit(extent, { padding: [50, 50], maxZoom: 10 });
            }
        } else if (fromCoords) {
            map.getView().setCenter(ol.proj.fromLonLat([fromCoords.lon, fromCoords.lat]));
            map.getView().setZoom(7);
        } else if (toCoords) {
            map.getView().setCenter(ol.proj.fromLonLat([toCoords.lon, toCoords.lat]));
            map.getView().setZoom(7);
        } else {
            // Если ни один город не найден — возвращаемся к центру Москвы
            map.getView().setCenter(ol.proj.fromLonLat([37.6156, 55.7522]));
            map.getView().setZoom(7);
        }
    }

    // Навешиваем обработчики на поля ввода
    document.getElementById('extra-city1').addEventListener('input', updateMarkers);
    document.getElementById('extra-city2').addEventListener('input', updateMarkers);

    // Первичная загрузка
    updateMarkers();
});