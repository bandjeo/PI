var query = ''
var printed_lists = []
var documentos = []

list_of_selected = []

up = (id) => {
    i = list_of_selected.indexOf(id);
    if(i == 0) return;
    temp = list_of_selected[i];
    list_of_selected[i] = list_of_selected[i-1];
    list_of_selected[i-1] = temp;
    redraw_sortable()
}

dn = (id) => {
    i = list_of_selected.indexOf(id);
    if(i == list_of_selected.length - 1) return;
    temp = list_of_selected[i];
    list_of_selected[i] = list_of_selected[i+1];
    list_of_selected[i+1] = temp;
    redraw_sortable()
}

redraw_sortable = () => {
    document.getElementById('sorter').innerHTML = list_of_selected.map(e => `<div class="dragdrop row my-3">
        <div class="col-7 border-mysuccess">${documentos.find(x => x.fileName == e).title}</div>
        <div class="col-5">
            <span id="u_${e}" class="col-5 btn btn-success mr-1 upbtn">&#9650;</span>
            <span id="d_${e}" class="col-5 btn btn-warning ml-1 dnbtn">&#9660;</span>
        </div>
    </div>`).join('\n')
    refresh_event_listeners_right();


}

document.getElementById('save').addEventListener('click', () => {
    function download(content, fileName, contentType) {
        var a = document.createElement("a");
        var file = new Blob([content], {type: contentType});
        a.href = URL.createObjectURL(file);
        a.download = fileName;
        a.click();
    }
    download(JSON.stringify(get_all_selected(query), null, 4), `${Math.random().toString().split('.')[1]}.json`, 'text/plain');


    console.log(get_all_selected(query));
    printed_lists.push(get_all_selected(query));
    document.getElementById('qc').innerHTML = ''
    list_of_selected = []
    document.getElementById('sorter').innerHTML = ''
})

refresh_event_listeners_right = () => {
    document.querySelectorAll('.upbtn').forEach(x => x.addEventListener('click', (evt) => up(evt.target.id.split('_')[1])))
    document.querySelectorAll('.dnbtn').forEach(x => x.addEventListener('click', (evt) => dn(evt.target.id.split('_')[1])))
}

refresh_event_listeners = () => {
    refresh_event_listeners_right();
    document.querySelectorAll('.question').forEach(e => {
        e.addEventListener('click', (evt) => {
            cl = e.classList.toString().split(' ');
            if (cl.indexOf('selected') == -1){ 
                e.classList.add('selected')
                list_of_selected.push(e.id);
            } else {
                e.classList.remove('selected')
                list_of_selected = list_of_selected.filter(x => x != e.id);
            }
            redraw_sortable();
        })
    })
}

get_all_selected = (query) => {
    return {query, lista: list_of_selected};
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
    filenames = []
    documentos = []
    document.getElementById('qc').innerHTML = ''
    for (let i=0; i < 10; i++) {
        for (let result of [result_bert, result_elastic, result_w2v, result_tfidf, result_d2v] ){
            if (result.length - 1 < i) continue;
            if (filenames.indexOf(result[i].fileName) == -1) {
                documentos.push(result[i]);
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



var rotation = 0;
setInterval(()=> document.getElementById('sorchen').style.transform = `rotate(${rotation++ * 180}deg)`, 1000)