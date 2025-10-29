class Card extends HTMLElement {
  constructor(text) {
    super();
    this.setAttribute("class", "cah-card");
    this.innerHTML = text;
  }
}

class BlackCard extends Card {
  constructor(text, gaps) {
    super(text);
    this.gaps = gaps;
  }
}
customElements.define("black-card", BlackCard);

class WhiteCard extends Card {
  constructor(text, onclick) {
    super(text);
    if (onclick) {
      this.addEventListener("click", onclick);
    }
  }
}
customElements.define("white-card", WhiteCard);

class CardContainer extends HTMLElement {
  constructor() {
    super();
    this.setAttribute("class", "card-container");
    this.checked = [];
  }

  changeCards(cards, limit) {
    this.textContent = "";
    this.checked.length = 0;

    cards.forEach((card, ind) => {
      let whiteClick = (event) => {
        let t = event.target;
        console.log("Clicked " + t);

        if (t.classList.contains("checked")) {
          t.classList.remove("checked");
          this.checked.splice(this.checked.indexOf(ind), 1);
          console.log("Removing... \n" + this.checked);
        } else {
          if (this.checked.length < limit) {
            t.classList.add("checked");
            this.checked.push(ind);
            console.log("Pushing... \n" + this.checked);
          }
        }
      };
      let label = document.createElement("label");
      label.appendChild(new WhiteCard(card, whiteClick));
      this.append(label);
    });
  }
}
customElements.define("card-container", CardContainer);

$(document).ready(() => {
  $("#readyButton").on("click", () => {
    socket.emit("ready", socket.id);
  });

  $("#confirmButton").on("click", () => {
    black = $("black-card");
    console.log(black.whites);
    // TODO: implement
  });

  socket.on("acc_ready", () => {
    $("#readyButton").prop("disabled", true);
    $("#readyButton").hide();
  });

  socket.on("game_stop", () => {
    $("#readyButton").prop("disabled", false);
    $("#readyButton").show();
    $("#confirmButton").prop("disabled", true);
    $("#confirmButton").hide();
  });

  socket.on("next_round", () => {
    socket.emit("get_turn_data", socket.id);
    $("#confirmButton").prop("disabled", false);
    $("#confirmButton").show();
  });

  socket.on("get_turn_data", (data) => {
    $("#black-card").append(new BlackCard(data.black_card, data.gaps));
    let myCards = document.querySelector("card-container");
    myCards.changeCards(data.cards, data.gaps);
    
    if (data.is_my_turn) {
      console.log("My turn to be master");
      // TODO: implement my turn
    } else {
    }


  });
});
