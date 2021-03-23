var query = ''
var printed_lists = []



document.getElementById('save').addEventListener('click', () => {
    console.log(get_all_selected(query));
    printed_lists.push(get_all_selected(query));
    document.getElementById('qc').innerHTML = ''

})

refresh_event_listeners = () => {
    document.querySelectorAll('.question').forEach(e => {
        e.addEventListener('click', (evt) => {
            cl = e.classList.toString().split(' ');
            if (cl.indexOf('selected') == -1){ 
                e.classList.add('selected')
            } else {
                e.classList.remove('selected')
            }
        })
    })
}

get_all_selected = (query) => {
    
    lista = []

    document.querySelectorAll('.selected').forEach(e => lista.push(e.id));
    return {query,lista};
};


document.getElementById('sorch').addEventListener('click', async () => {
    query = document.getElementById('searchInputSm').value;
    if(query == '') return;
    document.getElementById('blurred').style.display = 'block'
    document.getElementById('blurred').style.opacity = '1'
    document.getElementById('sorchen').style.opacity = '1'
    let result_bert = (await axios.get(`http://localhost:5000/bert/${document.getElementById('searchInputSm').value}`)).data.data;
    let result_elastic = (await axios.get(`http://localhost:5000/elastic/${document.getElementById('searchInputSm').value}`)).data.data;
    let result_w2v = (await axios.get(`http://localhost:5000/word2vec/${document.getElementById('searchInputSm').value}`)).data.data;
    let result_tfidf = (await axios.get(`http://localhost:5000/tfidf/${document.getElementById('searchInputSm').value}`)).data.data;
    let result_d2v = (await axios.get(`http://localhost:5000/doc2vec/${document.getElementById('searchInputSm').value}`)).data.data;
    document.getElementById('sorchen').style.opacity = '0'
    document.getElementById('blurred').style.opacity = '0'
    setTimeout(() => document.getElementById('blurred').style.display = 'none', 1000)
    
    document.getElementById('qc').innerHTML = ''
    filenames = []
    for (let i=0; i < 10; i++) {
        
        for (let result of [result_bert, result_elastic, result_w2v, result_tfidf, result_d2v]){
            if (filenames.indexOf(result[i].fileName) == -1) {
                appdiv = `
                    <div id="${result[i].fileName}" class="question col-8 offset-2">
                        <h3 class="d-inline col-12">${result[i].title}</h3>
                        <p class="col-12">${result[i].sample}</p>
                    </div>
                    ${i==result.length-1?'':'<hr class="my-4 col-6 offset-3 bg-white">'}
                `
                filenames.push(result[i].fileName);
                document.getElementById('qc').innerHTML = document.getElementById('qc').innerHTML + appdiv;
            }
        }
        
    }
    refresh_event_listeners();
})


refresh_event_listeners();

var rotation = 0;
setInterval(()=> document.getElementById('sorchen').style.transform = `rotate(${rotation++ * 180}deg)`, 1000)