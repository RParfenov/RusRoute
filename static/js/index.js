document.addEventListener('DOMContentLoaded', function() {
    // Параллельное переключение стикеров (любое количество может быть активно)
    document.querySelectorAll('.sticker-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            this.classList.toggle('active');
        });
    });
});