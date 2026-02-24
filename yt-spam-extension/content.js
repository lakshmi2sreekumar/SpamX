// Prevent duplicate processing
const processedElements = new WeakSet();

console.log("✅ Spam extension loaded");


// ================================
// Highlight comment
// ================================

function highlightComment(comment, label) {

    const container = comment.closest("ytd-comment-thread-renderer");

    if (!container) return;

    container.style.padding = "6px";
    container.style.borderRadius = "8px";

    if (label === "spam") {

        container.style.backgroundColor = "#ffcccc";
        container.style.border = "2px solid red";

    } else {

        container.style.backgroundColor = "#ccffcc";
        container.style.border = "2px solid green";

    }

}

// ================================
// Add Label (FIXED)
// ================================

function addLabel(comment, label) {

    const container = comment.closest("ytd-comment-thread-renderer");

    if (!container) return;

    // THIS is the correct visible header section
    const header = container.querySelector("#header-author");

    if (!header) {

        console.log("Header not found");
        return;

    }

    // prevent duplicate label
    if (header.querySelector(".spam-label")) return;


    const newLabel = document.createElement("span");

    newLabel.className = "spam-label";

    newLabel.innerText = label.toUpperCase();

    newLabel.style.marginLeft = "8px";
    newLabel.style.fontSize = "12px";
    newLabel.style.fontWeight = "bold";
    newLabel.style.padding = "2px 6px";
    newLabel.style.borderRadius = "6px";


    if (label === "spam") {

        newLabel.style.backgroundColor = "red";
        newLabel.style.color = "white";

    } else {

        newLabel.style.backgroundColor = "green";
        newLabel.style.color = "white";

    }


    // ADD beside username and time
    header.appendChild(newLabel);

}


// ================================
// Analyze comments
// ================================

async function analyzeComments() {

    const comments =
        document.querySelectorAll("#content-text");


    comments.forEach(async (comment) => {

        if (processedElements.has(comment)) return;

        processedElements.add(comment);


        const text = comment.innerText.trim();

        if (!text) return;


        console.log("Checking:", text);


        try {

            const response =
                await fetch(
                    "http://127.0.0.1:8000/api/classify/",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({
                            text: text
                        })
                    }
                );


            const result =
                await response.json();


            console.log("Result:", result);


            highlightComment(comment, result.label);

            addLabel(
                comment,
                result.label,
                result.confidence
            );


        } catch (error) {

            console.error(
                "API error:",
                error
            );

        }

    });

}



// ================================
// Initial run
// ================================

setTimeout(analyzeComments, 3000);



// ================================
// Observe new comments
// ================================

const observer =
    new MutationObserver(() => {

        analyzeComments();

    });


observer.observe(document.body, {

    childList: true,

    subtree: true

});
