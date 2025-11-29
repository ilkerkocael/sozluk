document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const langToggle = document.getElementById('lang-toggle');
    const langMenu = document.getElementById('lang-menu');
    const currentLangPair = document.getElementById('current-lang-pair');
    const langOptions = document.querySelectorAll('.lang-option');

    const loading = document.getElementById('loading');
    const results = document.getElementById('results');
    const errorMessage = document.getElementById('error-message');

    const resultWord = document.getElementById('result-word');
    const definitionsList = document.getElementById('definitions-list');
    const contextsList = document.getElementById('contexts-list');

    let selectedLangPair = 'fr-tr';

    // Toggle Language Menu
    langToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        langMenu.classList.toggle('hidden');
    });

    // Close menu when clicking outside
    document.addEventListener('click', () => {
        langMenu.classList.add('hidden');
    });

    // Select Language
    langOptions.forEach(option => {
        option.addEventListener('click', () => {
            selectedLangPair = option.dataset.value;
            currentLangPair.textContent = option.textContent;
            langMenu.classList.add('hidden');
        });
    });

    // Handle Search
    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const word = searchInput.value.trim();
        if (!word) return;

        // UI Reset
        results.classList.add('hidden');
        errorMessage.classList.add('hidden');
        loading.classList.remove('hidden');

        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ word, lang_pair: selectedLangPair }),
            });

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            displayResults(data);

        } catch (error) {
            console.error('Error:', error);
            errorMessage.textContent = error.message || "Bir hata oluştu.";
            errorMessage.classList.remove('hidden');
        } finally {
            loading.classList.add('hidden');
        }
    });

    function displayResults(data) {
        resultWord.textContent = data.word;

        // Clear previous results
        definitionsList.innerHTML = '';
        contextsList.innerHTML = '';

        // Populate Definitions
        if (data.definitions && data.definitions.length > 0) {
            data.definitions.forEach(def => {
                const defEl = document.createElement('div');
                defEl.className = 'border-l-4 border-primary pl-4 py-1';
                defEl.innerHTML = `
                    <p class="text-gray-800 text-lg mb-2">${def.meaning}</p>
                    <div class="bg-gray-50 rounded-lg p-3 text-sm">
                        <p class="text-gray-600 mb-1">"${def.example}"</p>
                        <p class="text-gray-500 italic">${def.translation}</p>
                    </div>
                `;
                definitionsList.appendChild(defEl);
            });
        } else {
            definitionsList.innerHTML = '<p class="text-gray-500">Tanım bulunamadı.</p>';
        }

        // Populate Contexts
        if (data.contexts && data.contexts.length > 0) {
            data.contexts.forEach(ctx => {
                const ctxEl = document.createElement('div');
                ctxEl.className = 'bg-gray-50 rounded-xl p-4 border border-gray-100';
                ctxEl.innerHTML = `
                    <span class="inline-block px-2 py-1 bg-white rounded text-xs font-semibold text-gray-500 mb-2 border border-gray-200 uppercase tracking-wider">${ctx.context}</span>
                    <p class="text-gray-700 text-sm leading-relaxed">${ctx.explanation}</p>
                `;
                contextsList.appendChild(ctxEl);
            });
        } else {
            contextsList.innerHTML = '<p class="text-gray-500 col-span-2">Bağlam bilgisi bulunamadı.</p>';
        }

        results.classList.remove('hidden');
    }
});
