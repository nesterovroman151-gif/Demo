document.addEventListener('DOMContentLoaded', function() {
    var slider = document.querySelector('.slider-track');
    if (slider) initSlider(slider);

    var modalTriggers = document.querySelectorAll('[data-modal-target]');
    modalTriggers.forEach(function(trigger) {
        trigger.addEventListener('click', function() {
            var target = document.getElementById(this.dataset.modalTarget);
            if (target) target.classList.add('active');
        });
    });

    var modalClosers = document.querySelectorAll('.modal-close, .modal-overlay');
    modalClosers.forEach(function(el) {
        el.addEventListener('click', function(e) {
            if (e.target === this) {
                document.querySelectorAll('.modal-overlay.active').forEach(function(m) {
                    m.classList.remove('active');
                });
            }
        });
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay.active').forEach(function(m) {
                m.classList.remove('active');
            });
        }
    });

    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.4s, transform 0.4s';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(function() { alert.remove(); }, 400);
        }, 4500);
    });

    var inputs = document.querySelectorAll('.form-input');
    inputs.forEach(function(input) {
        input.addEventListener('invalid', function(e) {
            e.preventDefault();
            this.classList.add('error');
            var error = this.parentElement.querySelector('.error-text');
            if (!error) {
                error = document.createElement('span');
                error.className = 'error-text';
                this.parentElement.appendChild(error);
            }
            if (this.validationMessage) {
                error.textContent = this.validationMessage;
            }
        });

        input.addEventListener('input', function() {
            if (this.classList.contains('error')) {
                this.classList.remove('error');
                var error = this.parentElement.querySelector('.error-text');
                if (error) error.remove();
            }
        });
    });

    var cards = document.querySelectorAll('.application-card, .card');
    cards.forEach(function(card, i) {
        card.style.animationDelay = (i * 0.05) + 's';
        card.classList.add('fade-in');
    });
});

function initSlider(track) {
    var container = track.parentElement;
    var slides = track.querySelectorAll('.slider-slide');
    var dotsContainer = container.querySelector('.slider-dots');
    var prevBtn = container.querySelector('.slider-prev');
    var nextBtn = container.querySelector('.slider-next');
    var progressBar = container.querySelector('.slider-progress');

    var current = 0;
    var total = slides.length;
    var isAnimating = false;
    var interval;
    var progressTimer;
    var INTERVAL_MS = 3000;

    function goTo(index, skipAnimation) {
        if (isAnimating && !skipAnimation) return;
        if (index < 0) index = total - 1;
        if (index >= total) index = 0;
        current = index;

        if (skipAnimation) {
            track.style.transition = 'none';
        } else {
            track.style.transition = 'transform 0.45s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
            isAnimating = true;
            setTimeout(function() { isAnimating = false; }, 450);
        }
        track.style.transform = 'translateX(-' + (current * 100) + '%)';

        if (dotsContainer) {
            dotsContainer.querySelectorAll('.slider-dot').forEach(function(d, i) {
                d.classList.toggle('active', i === current);
            });
        }

        resetProgress();
    }

    function nextSlide() { goTo(current + 1); }
    function prevSlide() { goTo(current - 1); }

    function startProgress() {
        stopProgress();
        if (!progressBar) return;
        progressBar.style.transition = 'none';
        progressBar.style.width = '0%';
        requestAnimationFrame(function() {
            progressBar.style.transition = 'width ' + INTERVAL_MS + 'ms linear';
            progressBar.style.width = '100%';
        });
    }

    function stopProgress() {
        if (progressBar) {
            var computed = window.getComputedStyle(progressBar);
            progressBar.style.transition = 'none';
            progressBar.style.width = computed.width;
        }
    }

    function startAuto() {
        stopAuto();
        interval = setInterval(nextSlide, INTERVAL_MS);
        startProgress();
    }

    function stopAuto() {
        if (interval) { clearInterval(interval); interval = null; }
        stopProgress();
    }

    if (dotsContainer) {
        dotsContainer.innerHTML = '';
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

    var touchStartX = 0;
    var touchEndX = 0;

    container.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
        stopAuto();
    }, { passive: true });

    container.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        var diff = touchStartX - touchEndX;
        if (Math.abs(diff) > 50) {
            if (diff > 0) nextSlide();
            else prevSlide();
        }
        startAuto();
    }, { passive: true });

    goTo(0, true);
    startAuto();
}

function showToast(message, type) {
    type = type || 'info';
    var container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }
    var toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(function() {
        toast.style.transition = 'opacity 0.3s, transform 0.3s';
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(20px)';
        setTimeout(function() { toast.remove(); }, 300);
    }, 3500);
}