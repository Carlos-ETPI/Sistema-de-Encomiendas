//Se utiliza para medir el tiempo antes que desaparezca el mensaje de error
setTimeout(function() {
    document.querySelector('.toast').classList.add('d-none');
}, 5000);

//Se utiliza para mostrar mensajes de error
$(document).ready(function() {
    $('.toast').toast('show');
});

//se utiliza para la validacion de los campos usando Bootstrap
(function () {
    'use strict';

    
    var forms = document.querySelectorAll('.needs-validation');

    
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }

                form.classList.add('was-validated');
            }, false);
        });
})();