
document.addEventListener('DOMContentLoaded', () => {
    // simple greeting animation
    const greeting = document.querySelector('h2');
    if (greeting) {
        greeting.style.opacity = 0;
        let opacity = 0;
        const fadeIn = setInterval(() => {
            if (opacity >= 1) clearInterval(fadeIn);
            greeting.style.opacity = opacity;
            opacity += 0.05;
        }, 30);
    }

    //role-specific button highlights
    const buttons = document.querySelectorAll('.card a.btn');
    buttons.forEach((btn) => {
        btn.addEventListener('mouseenter', () => {
            btn.classList.add('shadow-lg');
        });
        btn.addEventListener('mouseleave', () => {
            btn.classList.remove('shadow-lg');
        });
    });
});
