// Simple vanilla JS for additional animations
document.addEventListener('DOMContentLoaded', function() {
    // Add animation delays to feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.setProperty('--i', index);
    });

    // Add animation delays to API cards
    const apiCards = document.querySelectorAll('.api-card');
    apiCards.forEach((card, index) => {
        card.style.setProperty('--i', index);
    });

    // Smooth scroll for CTA button
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton) {
        ctaButton.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector('#api');
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // Add subtle parallax effect to background blobs
    window.addEventListener('mousemove', function(e) {
        const blobs = document.querySelectorAll('.glow-blob');
        const mouseX = e.clientX / window.innerWidth;
        const mouseY = e.clientY / window.innerHeight;

        blobs.forEach((blob, index) => {
            const speed = (index + 1) * 0.5;
            const x = (mouseX - 0.5) * speed;
            const y = (mouseY - 0.5) * speed;
            blob.style.transform = `translate(${x}px, ${y}px)`;
        });
    });
});