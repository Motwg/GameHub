class Card extends HTMLElement {
  constructor(text) {
    super();
    this.setAttribute("class", "cah-card");
    this.innerHTML = text;
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
  constructor(text, onclick) {
    super(text);
    if (onclick) {
      this.addEventListener("click", onclick);
    }
  }

  // onclick() {
  //   console.log(this);
  //   $(this).toggleClass("checked");
  //   if (this.contains("checked")) {
  //   } else {
  //   }
  // }
}
customElements.define("white-card", WhiteCard);

$(document).ready(() => {
  $("#readyButton").on("click", () => {
    socket.emit("ready", socket.id);
  });

  $("#confirmButton").on("click", () => {
    black = $("black-card");
    console.log(black.whites);
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
    cards_container = $("#cards");
    if (data.is_my_turn) {
      console.log("My turn");
      // TODO: implement my turn
    }
    let whites = 2;
    let checkList = [];
    $("#black-card").append(new BlackCard(data.black_card, whites));

    data.cards.forEach((card, ind) => {
      let whiteClick = (event) => {
        let el = event.target;
        console.log(el);
        $(el).toggleClass("checked");
        if (el.classList.contains("checked")) {
          checkList.append(el); // replace
          console.log(checkList);
        } else {
          checkList.remove(el); // replace
          console.log(checkList);
        }
      };
      let white = new WhiteCard(card, whiteClick);
      white.setAttribute("value", ind);
      // $(white).click(() => {
      //   whiteClick($(this.element));
      // });
      cards_container.append(white);

      // let text = `card-${ind}`;
      // let label = document.createElement("label");
      // label.setAttribute("for", text);

      // let input = document.createElement("input");
      // input.setAttribute("type", "radio");
      // input.setAttribute("name", "card");
      // input.setAttribute("id", text);
      // input.setAttribute("class", "visually-hidden");
      // cards_container.append(input);
      // label.append(new WhiteCard(card));
      // cards_container.append(label);
    });
  });
});
