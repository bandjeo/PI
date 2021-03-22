
function toggleTheme(todark) { 
    var theme = document.getElementById('themelink'); 

    if (theme.getAttribute('href') == 'public/css/light.css?cache=0' && todark) { 
        theme.setAttribute('href', 'public/css/dark.css?cache=0'); 
        localStorage.setItem('darkmode', true)
    } else if (theme.getAttribute('href') == 'public/css/dark.css?cache=0' && !todark){ 
        theme.setAttribute('href', 'public/css/light.css?cache=0'); 
        localStorage.setItem('darkmode', false)
    } 
} 

document.getElementById('theme').addEventListener('change', (e) => {
        toggleTheme(e.target.checked);
})


if (localStorage.getItem('darkmode') == undefined) {
    localStorage.setItem('darkmode', false)
} else if (localStorage.getItem('darkmode') == 'true') {
    toggleTheme(true);
    document.getElementById('theme').checked = true;
}