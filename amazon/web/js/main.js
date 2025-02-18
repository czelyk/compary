// Amazon URL Scraper Integration
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('searchBtn').addEventListener('click', async () => {
        const url = document.getElementById('amazonUrl').value.trim();

        if (!url) {
            alert("Please enter a valid Amazon URL.");
            return;
        }

        try {
            const response = await fetch('http://localhost:8000/scrape', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url })
            });

            const result = await response.json();
            alert(result.message || result.error);
        } catch (error) {
            alert("Error: Unable to connect to the server.");
        }
    });
});
