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
});
