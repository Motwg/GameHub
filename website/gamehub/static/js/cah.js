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
    this.checked = [];
  }

  dimMaster() {
    this.classList.add("dimmed-master");
  }

  dimConfirm() {
    this.classList.add("dimmed-confirm");
  }

  uncheck() {
    this.checked.length = 0;
    this.childNodes.forEach((card) => {
      card.classList.remove("checked");
    });
  }

  changeCards(cards, limit) {
    this.textContent = "";
    this.checked.length = 0;
    this.classList.remove("dimmed-master");
    this.classList.remove("dimmed-confirm");

    cards.forEach((card, ind) => {
      let whiteClick = (event) => {
        let t = event.target;

        if (t.classList.contains("checked")) {
          t.classList.remove("checked");
          this.checked.splice(this.checked.indexOf(ind), 1);
        } else {
          if (this.checked.length < limit) {
            t.classList.add("checked");
            this.checked.push(ind);
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

class CardCarousel extends HTMLElement {
  constructor() {
    super();
    this.cards = [];
    this.page = 0;
    this.container = document.createElement("div");
    this.container.setAttribute("class", "card-container");

    const prev = document.createElement("button");
    prev.innerText = "←";
    prev.setAttribute("class", "btn btn-primary");
    prev.addEventListener("click", () => {
      this.previousPage();
    });

    const next = document.createElement("button");
    next.innerText = "→";
    next.setAttribute("class", "btn btn-primary");
    next.addEventListener("click", () => {
      this.nextPage();
    });
    this.append(prev);
    this.append(this.container);
    this.append(next);
  }

  showPage(number) {
    this.container.textContent = "";
    this.page = number % this.cards.length;
    this.cards[this.page].forEach((card) => {
      this.container.append(new WhiteCard(card));
    });
  }

  setCards(cards) {
    this.cards = cards;
    this.page = 0;
    this.showPage(0);
  }

  nextPage() {
    this.showPage(this.page + 1);
  }

  previousPage() {
    this.showPage(this.page - 1);
  }
}
customElements.define("card-carousel", CardCarousel);

$(document).ready(() => {
  const myCards = document.querySelector("card-container");
  const carousel = document.querySelector("card-carousel");

  $("#confirmButton").prop("disabled", true);
  $("#confirmButton").hide();

  $("#readyButton").on("click", () => {
    socket.emit("ready", socket.id);
  });

  $("#confirmButton").on("click", () => {
    if (myCards.checked.length == blackCardContainer.firstChild.gaps) {
      myCards.dimConfirm();
      socket.emit("confirm_cards", myCards.checked);
    }
  });

  $("#confirmWinner").on("click", () => {
    socket.emit("winner_chosen", carousel.cards[carousel.page]);
  });

  socket.on("acc_ready", () => {
    $("#readyButton").prop("disabled", true);
    $("#readyButton").hide();
    $("#confirmButton").show();
  });

  socket.on("game_stop", () => {
    $("#readyButton").prop("disabled", false);
    $("#readyButton").show();
    $("#confirmButton").prop("disabled", true);
  });

  const blackCardContainer = document.querySelector("#black-card");
  socket.on("next_round", () => {
    blackCardContainer.innerHTML = "";
    myCards.uncheck();
    socket.emit("get_turn_data", socket.id);
  });

  socket.on("send_turn_data", (data) => {
    blackCardContainer.appendChild(new BlackCard(data.black_card, data.gaps));
    myCards.changeCards(data.cards, data.gaps);

    // TODO: delete mark
    if (!data.is_my_turn) {
      $("#confirmButton").prop("disabled", true);
      // $("#confirmButton").hide();
      myCards.dimMaster();
    } else {
      $("#confirmButton").prop("disabled", false);
    }
  });

  socket.on("cards_confirmed", (cards) => {
    carousel.setCards(cards);
  });

  socket.on("chose_winner", (cards) => {
    console.log("Chosing winner...");
    // TODO: implement
  });
});
