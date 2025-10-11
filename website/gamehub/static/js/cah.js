class Card extends HTMLElement {
  constructor() {
    super();
    this.setAttribute("class", "cah-card");
    this.addEventListener("click", this.onclick);
  }

  onclick() {
    console.log(this);
  }
}

class BlackCard extends Card {
  /**
   * @param {int} whites
   */
  constructor(whites) {
    super();
    this.whites = whites;
  }
}
customElements.define("black-card", BlackCard);

class WhiteCard extends Card {
  constructor() {
    super();
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
});
