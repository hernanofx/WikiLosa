<script>
document.addEventListener('DOMContentLoaded', function() {
    // Verifica si el usuario ya ha visto el mensaje de bienvenida
    if (!localStorage.getItem('welcomeDisplayed')) {
        // Muestra la ventana de bienvenida
        alert('¡Bienvenido a Losa 0!');

        // Marca el mensaje como mostrado
        localStorage.setItem('welcomeDisplayed', 'true');
    }
});
</script>
