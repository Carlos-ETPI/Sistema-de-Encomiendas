$(document).ready(function() {
    // Función para validar el formulario antes de enviarlo
    $('#loginForm').submit(function(event) {
        var username = $('#id_username').val().trim();
        var password = $('#id_password').val().trim();
        
        // Validar que ambos campos no estén vacíos
        if (username.length === 0 || password.length === 0) {
            event.preventDefault(); // Detener el envío del formulario
            
            // Mostrar mensaje de error
            $('#error-message').text('Los campos de usuario y contraseña son requeridos.');
        }
    });
});