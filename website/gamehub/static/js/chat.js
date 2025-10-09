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
  // socket.io
  let socket = io(hostname);

  socket.on("connect", () => {
    console.log("User connected!");
  });

  socket.on("message", (data) => {
    textarea = $("#messages");
    textarea.append(data + "\n");
    textarea.scrollTop(textarea[0].scrollHeight);
  });

  socket.on("new_connection", (data) => {
    console.log("new_connection: ", data);
  });

  socket.on("lost_connection", (data) => {
    console.log("lost_connection: ", data);
  });

  $("#sendMsgButton").on("click", () => {
    socket.send($("#message").val());
    $("#message").val("");
  });
});
