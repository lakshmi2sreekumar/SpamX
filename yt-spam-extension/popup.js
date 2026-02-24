document.getElementById("analyzeBtn").addEventListener("click", async () => {

    const status = document.getElementById("status");
    const resultsDiv = document.getElementById("results");

    status.innerText = "Analyzing...";
    resultsDiv.innerHTML = "";

    try {

        // get current tab
        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        // extract video id from tab url
        const url = new URL(tab.url);
        const videoId = url.searchParams.get("v");

        if (!videoId) {
            status.innerText = "Not a YouTube video";
            return;
        }

        // call backend
        const response = await fetch(
            `http://127.0.0.1:8000/api/analyze/?video_id=${videoId}`
        );

        const data = await response.json();

        let spamCount = 0;
        let hamCount = 0;

        data.results.forEach(r => {
            if (r.label === "spam")
                spamCount++;
            else
                hamCount++;
        });

        status.innerText = "Done";

        resultsDiv.innerHTML = `
            <p class="spam">Spam: ${spamCount}</p>
            <p class="ham">Non Spam: ${hamCount}</p>
        `;

    } catch (error) {

        status.innerText = "Error";
        console.error(error);

    }

});