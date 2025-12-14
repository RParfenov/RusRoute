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