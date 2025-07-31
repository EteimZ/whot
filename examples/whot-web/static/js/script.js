function initGame(websocket) {
    websocket.addEventListener("open", () => {
        // Send an "init" event according to who is connecting.
        const params = new URLSearchParams(window.location.search);
        let event = { type: "init" };

        if (params.has("join")) {
            // Second player joins an existing game.
            event.join = params.get("join");
        } else {
            // First player starts a new game.
        }
        websocket.send(JSON.stringify(event));
    });
}

function addMiddleCardImage(text) {
    const cardImg = document.getElementById("card_top");
    const face = text["face"]
    const suit = text["suit"].toLowerCase();

    let path;

    if (suit != 'whot') {
        path = `assets/images/${suit}/${face}_${suit}.png`
    } else {
        path = `assets/images/20_whot.png`
    }
    cardImg.src = path;
}

function addOponnentCardImages(num_cards) {
    const opponent_cards = document.getElementById("opponent_cards");

    // Remove all children
    opponent_cards.replaceChildren();

    for (let i = 0; i < num_cards; i++) {
        // Create a new image element
        const newCard = document.createElement('img');
        // Set attributes for the image
        newCard.src = 'assets/images/whot_back.png'; // Path to the image
        newCard.alt = 'Opponent Card'; // Alternative text
        newCard.width = 100; // Set width
        newCard.height = 120; // Set height

        // Append the new image to the opponent_cards div
        opponent_cards.appendChild(newCard);
    }
}

function addPlayerCardImages(cards, websocket, player_id) {
    const player_cards = document.getElementById("player_cards");

    // Remove all children
    player_cards.replaceChildren();

    for (let i = 0; i < cards.length; i++) {
        // Create a new image element
        const newCard = document.createElement('img');

        const face = cards[i]["face"]
        const suit = cards[i]["suit"].toLowerCase();

        // Set attributes for the image
        if (suit != 'whot') {
            newCard.src = `assets/images/${suit}/${face}_${suit}.png`; // Path to the image
        } else {
            newCard.src = `assets/images/20_whot.png`
        }
        newCard.alt = 'Player Card'; // Alternative text
        newCard.width = 100; // Set width
        newCard.height = 120; // Set height

        newCard.onclick = () => {
            const event = {
                type: "play",
                card: i,
                player_id: player_id.textContent.split(" ")[1]
            };
            websocket.send(JSON.stringify(event));
        }

        // Append the new image to the opponent_cards div
        player_cards.appendChild(newCard);
    }
}

function receiveEvents(websocket, player_id) {

    websocket.addEventListener("message", ({ data }) => {

        const event = JSON.parse(data);

        switch (event.type) {

            case "init":
                // Create a container div for the join link
                const joinDiv = document.createElement("div");
                joinDiv.id = "join_link_container";

                // Add description
                const infoText = document.createElement("p");
                infoText.textContent = "Share this link to invite:";
                joinDiv.appendChild(infoText);

                // Add the actual join link
                const link = document.createElement("a");
                link.href = window.location.href + "?join=" + event.join;
                link.innerText = link.href;
                joinDiv.appendChild(link);

                // Append to the sidebar
                const sidebar = document.getElementById("sidebar");
                sidebar.appendChild(joinDiv);
                break;

            case "start":
                player_id.textContent = `Player_id: ${event.player_id}`
                break;

            case "play":
                updateCards(event, websocket);
                break;

            case "request":
                document.getElementById("suitModal").style.display = "flex";;
                break;

            case "win":
                showNotification(`${event.winner} wins!`);
                // No further messages are expected; close the WebSocket connection.
                websocket.close(1000);
                break;

            case "message":
                showNotification(event.message)
                break;

            default:
                throw new Error(`Unsupported event type: ${event.type}.`);
        }
    });
}

function showNotification(message) {
    // Remove any existing notification
    const existing = document.querySelector('.notification');
    if (existing) {
        existing.remove();
    }

    // Create new notification
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;

    // Add to page
    document.body.appendChild(notification);

    // Show with animation
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    // Remove after 15 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 300);
    }, 15000);
}

function updateCards(event, websocket) {
    current_player.textContent = `Current Player: ${event.game_state["current_player"]}`

    const opponent = Object.keys(event.game_state["players"]).filter(key => key !== event.player_id)

    addMiddleCardImage(event.game_state["pile_top"])
    addOponnentCardImages(event.game_state["players"][opponent[0]])
    addPlayerCardImages(event.game_state["players"][event.player_id], websocket, player_id)
}

window.addEventListener("DOMContentLoaded", () => {
    // Open the WebSocket connection and register event handlers.
    const market = document.getElementById("market");
    const player_id = document.getElementById("player_id");
    const modal = document.getElementById("suitModal");

    const websocket = new WebSocket(WEBSOCKET_URL);

    initGame(websocket);
    receiveEvents(websocket, player_id);

    // Add event handling on market card
    market.onclick = () => {
        const player = player_id.textContent.split(" ")
        const event = {
            type: "market",
            player_id: player[1]
        };
        websocket.send(JSON.stringify(event));
    }

    // Make requests 
    document.querySelectorAll(".suit-btn").forEach(button => {
        button.onclick = () => {
            const event = {
                type: "request",
                suit: button.id,
            };
            modal.style.display = "none";;
            websocket.send(JSON.stringify(event));
        };
    });

    websocket.onclose = function (event) {
        console.log("WebSocket closed:", event);
    };
});
