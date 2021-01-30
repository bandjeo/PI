var algorithms = {
    "1": "/tfidf/",
    "2": "Word2Vec",
    "3": "Doc2Vec",
    "4": "BERT",
    "5": "/elastic/"
}

var showResults = (data) => {
    document.getElementById('no-results').style.display = 'none';

    document.getElementById('result-container').innerHTML = data.length===0? '<h3 class="mx-5 my-4">No results found</h3>':data.map(e => `
                    <div class="mb-4 col-11 offset-1">
                        <div class="col-12 d-block text-muted small">/public/acts/${e.fileName}</div>
                        <a class="col-12 mt-1 d-block h4 cursor-pointer" target="_blank" href="/public/acts/${e.fileName}" >${e.title}</a>
                        <p class="col-5 d-block">${e.sample}...</p>    
                    </div>
    `).join('\n')
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
    // alert(`
    // Searched term: ${document.getElementById('searchInput').value}
    // Algorithm type: ${algorithms[getAlg()]}`);
    axios.get(`${algorithms[getAlg()]}${document.getElementById('searchInput').value}`).then(e => {
        showResults(e.data.data);
    })

})

document.getElementById('search-btn-sm').addEventListener('click', (ev) => {
    // alert(`
    // Searched term: ${document.getElementById('searchInputSm').value}
    // Algorithm type: ${algorithms[getAlg()]}`);
    axios.get(`${algorithms[getAlg()]}${document.getElementById('searchInputSm').value}`).then(e => {
        showResults(e.data.data);
    })
})

document.getElementById('logo').addEventListener('click', () => location.reload());
document.getElementById('logo-md').addEventListener('click', () => location.reload());