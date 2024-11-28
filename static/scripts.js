document.addEventListener('DOMContentLoaded', () => {
    console.log('Site chargé avec succès!');

    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    if (dropdownToggle && dropdownMenu) {
        dropdownToggle.addEventListener('click', (event) => {
            event.preventDefault();
            // Afficher ou masquer le menu
            dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
        });
    } else {
        console.error('Menu déroulant introuvable.');
    }
});
