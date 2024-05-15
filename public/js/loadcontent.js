function loadContent(pageUrl) {
    fetch(pageUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.text();
        })
        .then(html => {
            document.getElementById('main-content').innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading the page: ', error);
            document.getElementById('main-content').innerHTML = '<p>Error loading the content.</p>';
        });
}