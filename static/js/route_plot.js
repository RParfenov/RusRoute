document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const zoomed = document.querySelector('.plot-container.zoomed');
        if (zoomed) toggleZoom();
    }
});

function switchPlot(type) {
    const costSlide = document.getElementById('slide-cost');
    const timeSlide = document.getElementById('slide-time');

    if (type === 'cost') {
        costSlide.classList.add('active');
        timeSlide.classList.remove('active');
    } else if (type === 'time') {
        timeSlide.classList.add('active');
        costSlide.classList.remove('active');
    }
}

function toggleZoom() {
    const container = document.querySelector('.plot-container')
    const parent = document.querySelector('.image-container')

    if (container.classList.contains('zoomed')) {
        container.classList.remove('zoomed');
        parent.classList.remove('zoomed');
    } else {
        container.classList.add('zoomed');
        parent.classList.add('zoomed');
    }
}

// --- Маршруты ---
let routePool = [];
let currentRouteIndex = 0;

const routes = {
    'plane': 'card-plane',
    'train': 'card-train',
    'free_trails': 'card-free_trails',
    'toll_trails': 'card-toll_trails'
};

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', function () {
    if (!window.ROUTE_DATA) {
        console.error('ROUTE_DATA not found in window');
        return;
    }

    let sortByCost = false;
    const activeFilters = new Set();

    const transportBtns = document.querySelectorAll('.transport-btn[data-type]');
    const moneyBtn = document.querySelector('.transport-btn[data-type="money"]');

    // Обновление пула и отображение маршрута
    function updateRoutePool() {
        const showAll = (activeFilters.size === 0 || activeFilters.size === 3);
        let pool = [];

        for (let type of ['plane', 'train', 'free_trails', 'toll_trails']) {
            let isInPool = false;
            if (showAll) {
                isInPool = true;
            } else if (type === 'free_trails' || type === 'toll_trails') {
                isInPool = activeFilters.has('car');
            } else {
                isInPool = activeFilters.has(type);
            }
            if (isInPool) {
                pool.push(type);
            }
        }

        // Сортировка
        pool.sort((a, b) => {
            if (sortByCost) {
                return window.ROUTE_DATA[a].cost - window.ROUTE_DATA[b].cost;
            } else {
                return window.ROUTE_DATA[a].time - window.ROUTE_DATA[b].time;
            }
        });

        routePool = pool;
        currentRouteIndex = 0;
        renderCurrentRoute();
    }

    function renderCurrentRoute() {
        // Скрыть все карточки
        Object.values(routes).forEach(id => {
            document.getElementById(id).style.display = 'none';
        });

        // Показать текущую
        if (routePool.length > 0) {
            const type = routePool[currentRouteIndex];
            document.getElementById(routes[type]).style.display = 'block';
        }

        // Обновить счётчик
        const counter = document.getElementById('route-counter');
        if (counter) {
            counter.textContent = routePool.length > 0
                ? `${currentRouteIndex + 1} / ${routePool.length}`
                : '0 / 0';
        }

        // Скрыть/показать навигацию
        const nav = document.querySelector('.route-nav');
        if (nav) {
            nav.style.display = routePool.length > 1 ? 'flex' : 'none';
        }
    }

    function switchRoute(direction) {
        if (routePool.length <= 1) return;
        if (direction === 'prev' && currentRouteIndex > 0) {
            currentRouteIndex--;
        } else if (direction === 'next' && currentRouteIndex < routePool.length - 1) {
            currentRouteIndex++;
        }
        renderCurrentRoute();
    }

    // Экспорт функции в глобальную область (для onclick)
    window.switchRoute = switchRoute;

    // Обработчики кнопок
    transportBtns.forEach(btn => {
        if (btn.dataset.type !== 'money') {
            btn.addEventListener('click', () => {
                const type = btn.dataset.type;
                btn.classList.toggle('active');
                if (btn.classList.contains('active')) {
                    activeFilters.add(type);
                } else {
                    activeFilters.delete(type);
                }
                updateRoutePool();
            });
        }
    });

    if (moneyBtn) {
        moneyBtn.addEventListener('click', () => {
            moneyBtn.classList.toggle('active');
            sortByCost = moneyBtn.classList.contains('active');
            updateRoutePool();
        });
    }

    updateRoutePool();
});