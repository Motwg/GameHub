class Card extends HTMLElement {
  constructor(text) {
    super();
    this.setAttribute("class", "cah-card");
    this.addEventListener("click", this.onclick);
    this.innerHTML = text;
  }

  onclick() {
    console.log(this);
    this.select;
  }
}

class BlackCard extends Card {
  constructor(text, whites) {
    super(text);
    this.whites = whites;
  }
}
customElements.define("black-card", BlackCard);

class WhiteCard extends Card {
  constructor(text) {
    super(text);
  }
}
customElements.define("white-card", WhiteCard);

$(document).ready(() => {
  $("#readyButton").on("click", () => {
    socket.emit("ready", socket.id);
  });

  socket.on("acc_ready", () => {
    $("#readyButton").prop("disabled", true);
    $("#readyButton").hide();
  });

  socket.on("game_stop", () => {
    $("#readyButton").prop("disabled", false);
    $("#readyButton").show();
  });

  socket.on("next_round", () => {
    socket.emit("my_cards", socket.id);
  });

  socket.on("my_cards", (cards) => {
    cards_container = $("#cards");
    cards.forEach((card) => {
      console.log(card);
      cards_container.append(new WhiteCard(card));
    });
  });
});
