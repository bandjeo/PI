var algorithms = {
    "1": "TF-IDF",
    "2": "Word2Vec",
    "3": "Doc2Vec",
    "4": "BERT",
    "5": "Elastic search"
}

var showResults = () => {
    document.getElementById('no-results').style.display = 'none';
    document.getElementById('results').style.display = 'block';
}

var getAlg = () => {
    let dropDown = document.getElementById("alg");
    return dropDown.options[dropDown.selectedIndex].value
}

var getAlgSm = () => {
    let dropDown = document.getElementById("alg-sm");
    return dropDown.options[dropDown.selectedIndex].value
}

document.getElementById("alg").addEventListener("change", (ev)=>{
    document.getElementById("alg-sm").value = getAlg();
});

document.getElementById("alg-sm").addEventListener("change", (ev)=>{
    document.getElementById("alg").value = getAlgSm();
});

document.getElementById('search-btn').addEventListener('click', (ev) => {
    document.getElementById('searchInputSm').value = document.getElementById('searchInput').value;
    alert(`
    Searched term: ${document.getElementById('searchInput').value}
    Algorithm type: ${algorithms[getAlg()]}`);
    showResults();

})

document.getElementById('search-btn-sm').addEventListener('click', (ev) => {
    alert(`
    Searched term: ${document.getElementById('searchInputSm').value}
    Algorithm type: ${algorithms[getAlg()]}`);
})

document.getElementById('logo').addEventListener('click', () => location.reload());
document.getElementById('logo-md').addEventListener('click', () => location.reload());