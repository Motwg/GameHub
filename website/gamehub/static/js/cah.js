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
    socket.emit("get_turn_data", socket.id);
    $("#confirmButton").prop("disabled", false);
    $("#confirmButton").show();
  });

  socket.on("get_turn_data", (data) => {
    cards_container = $("#cards");
    if (data.is_my_turn) {
      console.log("My turn");
      // TODO: implement my turn
    }

    $("#black-card").append(new BlackCard(data.black_card, 1));

    data.cards.forEach((card, ind) => {
      let text = `card-${ind}`;
      let label = document.createElement("label");
      label.setAttribute("for", text);

      let input = document.createElement("input");
      input.setAttribute("type", "radio");
      input.setAttribute("name", "card");
      input.setAttribute("id", text);
      // input.setAttribute("value", text);
      input.setAttribute("class", "visually-hidden");
      cards_container.append(input);
      label.append(new WhiteCard(card));
      cards_container.append(label);
    });
  });
});
