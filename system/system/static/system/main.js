document.addEventListener('DOMContentLoaded', () => {

    window.addEventListener('click', (event) => {
        const element = event.target;
        if (element.classList.contains('day-hour')) {
            event.preventDefault()
            const computedStyle = window.getComputedStyle(element);
            const bgcolor = computedStyle.backgroundColor;
            console.log(bgcolor);
            if (bgcolor === 'rgb(255, 255, 255)' || bgcolor === 'white' || bgcolor === 'rgb(0, 128, 0)' || bgcolor === 'green') {
                element.style.backgroundColor = 'red';
            } else if (bgcolor === 'rgb(255, 0, 0)' || bgcolor === 'red') {
                element.style.backgroundColor = 'yellow';
            } else if (bgcolor === 'rgb(255, 255, 0)' || bgcolor === 'yellow') {
                element.style.backgroundColor = 'green';
            }
       }
    });
});