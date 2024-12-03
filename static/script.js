const chatWindow = document.getElementById("chat-window");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");

// Add message to chat window
function addMessage(message, isBot = false) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", isBot ? "bot-message" : "user-message");

    if (isBot) {
        // Typewriter effect
        let i = 0;
        const typewriter = setInterval(() => {
            messageDiv.innerHTML += message.charAt(i);
            i++;
            if (i > message.length) clearInterval(typewriter);
        }, 50);
    } else {
        messageDiv.textContent = message;
    }

    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to bottom
}

// Handle form submission
chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userMessage = chatInput.value.trim();
    if (!userMessage) return;

    // Add user message
    addMessage(userMessage);

    // Clear input
    chatInput.value = "";

    // Add typing indicator
    const typingIndicator = document.createElement("div");
    typingIndicator.className = "typing";
    typingIndicator.textContent = "TestGPT is thinking...";
    chatWindow.appendChild(typingIndicator);

    // Fetch bot response
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage }),
        });
        const data = await response.json();

        // Remove typing indicator
        chatWindow.removeChild(typingIndicator);

        // Add bot message
        addMessage(data.reply, true);
    } catch (error) {
        console.error("Error:", error);
        chatWindow.removeChild(typingIndicator);
        addMessage("Error: Unable to connect to the server.", true);
    }
});
