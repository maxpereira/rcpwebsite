/* =========================================
   VOLUNTEER PAGE — Script
   ========================================= */

// Volunteer form submit
const volForm = document.getElementById('volForm');
const volFormSuccess = document.getElementById('volFormSuccess');

if (volForm) {
  volForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = volForm.querySelector('button[type="submit"]');
    btn.textContent = 'Submitting…';
    btn.disabled = true;
    setTimeout(() => {
      volForm.style.display = 'none';
      volFormSuccess.style.display = 'block';
    }, 900);
  });
}
