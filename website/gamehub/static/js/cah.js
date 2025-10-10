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

$(document).ready(() => {});
