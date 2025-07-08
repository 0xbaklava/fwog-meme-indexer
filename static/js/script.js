document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const memeGrid = document.getElementById('meme-grid');

    // Fetch memes
    fetch('/memes')
        .then(response => response.json())
        .then(memes => {
            // Render initial memes
            renderMemes(memes);

            // Search functionality
            searchInput.addEventListener('input', () => {
                const searchTerm = searchInput.value.toLowerCase();
                const filteredMemes = memes.filter(meme => 
                    meme.tags.some(tag => tag.toLowerCase().includes(searchTerm)) ||
                    meme.filename.toLowerCase().includes(searchTerm) ||
                    meme.description.toLowerCase().includes(searchTerm)
                );
                renderMemes(filteredMemes);
            });
        })
        .catch(error => console.error('Error fetching memes:', error));

    function renderMemes(memesToRender) {
        memeGrid.innerHTML = ''; // Clear existing memes
        memesToRender.forEach(meme => {
            const memeCard = document.createElement('div');
            memeCard.classList.add('meme-card');

            memeCard.innerHTML = `
                <img src="/static/${meme.path}" alt="${meme.filename}">
                <div class="meme-details">
                    <div class="meme-tags">
                        ${meme.tags.map(tag => `<span class="meme-tag">${tag}</span>`).join('')}
                    </div>
                </div>
            `;

            memeGrid.appendChild(memeCard);
        });
    }
});