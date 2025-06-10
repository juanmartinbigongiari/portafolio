document.addEventListener('DOMContentLoaded', () => {
    // Selecciona todas las secciones que queremos que aparezcan con el efecto
    const sections = document.querySelectorAll('.fade-in-section');

    // Opciones para Intersection Observer
    const observerOptions = {
        root: null, // El viewport es el elemento raíz
        rootMargin: '0px', // No hay margen adicional
        threshold: 0.15 // El callback se ejecutará cuando el 15% del elemento esté visible
    };

    // Callback que se ejecuta cuando la visibilidad de un elemento cambia
    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            // Si el elemento es visible (o más del 15% está visible)
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible'); // Agrega la clase para mostrarlo
                // Opcional: deja de observar el elemento una vez que se ha hecho visible
                // observer.unobserve(entry.target);
            } else {
                // Opcional: si quieres que el efecto se revierta al salir de la vista
                // entry.target.classList.remove('is-visible');
            }
        });
    };

    // Crea una nueva instancia de Intersection Observer
    const observer = new IntersectionObserver(observerCallback, observerOptions);

    // Observa cada una de las secciones
    sections.forEach(section => {
        observer.observe(section);
    });

    // Manejo del envío del formulario
    const contactForm = document.getElementById('contactForm');
    const formMessage = document.getElementById('formMessage');

    // Función para mostrar mensajes al usuario
    const showMessage = (message, type) => {
        formMessage.textContent = message;
        formMessage.className = `form-message show ${type}`; // Añade la clase de tipo y 'show'
        setTimeout(() => {
            formMessage.classList.remove('show'); // Oculta el mensaje después de un tiempo
        }, 5000); // Mensaje visible por 5 segundos
    };

    if (contactForm) {
        contactForm.addEventListener('submit', async (event) => { // Marca la función como async
            event.preventDefault(); // Evita el envío real del formulario

            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;

            // Datos a enviar al backend
            const formData = { name, email, subject, message };

            try {
                // Realiza la petición fetch al backend
                // ¡IMPORTANTE! Durante el desarrollo, usa http://localhost:5000
                // Cuando despliegues tu backend, reemplaza esto con la URL de tu backend desplegado.
                const response = await fetch('http://localhost:5000/send-email', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData),
                });

                const result = await response.json(); // Parsea la respuesta JSON del backend

                if (result.success) {
                    showMessage('¡Mensaje enviado con éxito! Te contactaré pronto.', 'success');
                    contactForm.reset(); // Limpiar el formulario si el envío fue exitoso
                } else {
                    showMessage(`Error al enviar el mensaje: ${result.message}`, 'error');
                }
            } catch (error) {
                console.error('Error de conexión o del servidor:', error);
                showMessage('Hubo un problema de conexión con el servidor. Por favor, inténtalo de nuevo más tarde.', 'error');
            }
        });
    }
});
