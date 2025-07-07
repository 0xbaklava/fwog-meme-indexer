document.addEventListener('DOMContentLoaded', () => {
    const searchBar = document.getElementById('searchBar');
    const memeGrid = document.getElementById('memeGrid');

    fetch('/memes')
        .then(response => response.json())
        .then(memes => {
            displayMemes(memes);
            searchBar.addEventListener('input', () => {
                const query = searchBar.value.toLowerCase();
                const filteredMemes = memes.filter(meme =>
                    meme.description.toLowerCase().includes(query) ||
                    meme.tags.some(tag => tag.toLowerCase().includes(query))
                );
                displayMemes(filteredMemes);
            });
        });

    function displayMemes(memes) {
        memeGrid.innerHTML = '';
        memes.forEach(meme => {
            const card = document.createElement('div');
            card.className = 'meme-card';
            card.innerHTML = `
                <img src="${meme.path}" alt="${meme.description}">
                <p>${meme.description}</p>
            `;
            memeGrid.appendChild(card);
        });
    }
});