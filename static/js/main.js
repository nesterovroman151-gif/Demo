document.addEventListener('DOMContentLoaded', function() {
    var slider = document.querySelector('.slider-track');
    if (slider) {
        initSlider(slider);
    }
    var modalTriggers = document.querySelectorAll('[data-modal-target]');
    modalTriggers.forEach(function(trigger) {
        trigger.addEventListener('click', function() {
            var target = document.getElementById(this.dataset.modalTarget);
            if (target) {
                target.classList.add('active');
            }
        });
    });
    var modalClosers = document.querySelectorAll('.modal-close, .modal-overlay');
    modalClosers.forEach(function(el) {
        el.addEventListener('click', function(e) {
            if (e.target === this) {
                document.querySelectorAll('.modal-overlay').forEach(function(m) {
                    m.classList.remove('active');
                });
            }
        });
    });
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.3s';
            alert.style.opacity = '0';
            setTimeout(function() { alert.remove(); }, 300);
        }, 4000);
    });
});

function initSlider(track) {
    var slides = track.querySelectorAll('.slider-slide');
    var dotsContainer = track.parentElement.querySelector('.slider-dots');
    var prevBtn = track.parentElement.querySelector('.slider-prev');
    var nextBtn = track.parentElement.querySelector('.slider-next');
    var current = 0;
    var total = slides.length;
    var interval;

    function goTo(index) {
        if (index < 0) index = total - 1;
        if (index >= total) index = 0;
        current = index;
        track.style.transform = 'translateX(-' + (current * 100) + '%)';
        if (dotsContainer) {
            var dots = dotsContainer.querySelectorAll('.slider-dot');
            dots.forEach(function(d, i) {
                d.classList.toggle('active', i === current);
            });
        }
    }

    function nextSlide() { goTo(current + 1); }
    function prevSlide() { goTo(current - 1); }

    function startAuto() {
        stopAuto();
        interval = setInterval(nextSlide, 3000);
    }

    function stopAuto() {
        if (interval) { clearInterval(interval); interval = null; }
    }

    if (dotsContainer) {
        slides.forEach(function(_, i) {
            var dot = document.createElement('button');
            dot.className = 'slider-dot' + (i === 0 ? ' active' : '');
            dot.type = 'button';
            dot.setAttribute('aria-label', 'Слайд ' + (i + 1));
            dot.addEventListener('click', function() { goTo(i); startAuto(); });
            dotsContainer.appendChild(dot);
        });
    }

    if (prevBtn) prevBtn.addEventListener('click', function() { prevSlide(); startAuto(); });
    if (nextBtn) nextBtn.addEventListener('click', function() { nextSlide(); startAuto(); });

    track.parentElement.addEventListener('mouseenter', stopAuto);
    track.parentElement.addEventListener('mouseleave', startAuto);

    goTo(0);
    startAuto();
}
