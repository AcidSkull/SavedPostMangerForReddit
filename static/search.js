Posts = document.getElementsByClassName('posts')
Titles = document.getElementsByClassName('title');
Searchbox = document.getElementById('searchbox')


Searchbox.addEventListener('oninput', () => {
    let pattern = document.getElementById('searchbox');

    for(let i = 0; i < Titles.length; ++i){
        if(Titles.textContent == pattern || pattern == ""){
            Posts[i].style.display = 'none';
        } else {
            Posts[i].style.display = '';
        }
    }
});