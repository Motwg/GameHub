$(document).ready(() => {
  textarea = $("#messages");
  sendMessage = (msg) => {
    textarea.append(msg + "\n");
    textarea.scrollTop(textarea[0].scrollHeight);
  };

  // socket.io
  let socket = io(hostname);

  socket.on("connect", () => {
    console.log("User connected!");
  });

  socket.on("message", (data) => {
    sendMessage(data);
  });

  socket.on("new_connection", (data) => {
    sendMessage(data + " joined room!");
  });

  socket.on("lost_connection", (data) => {
    sendMessage(data + " left room!");
  });

  $("#sendMsgButton").on("click", () => {
    socket.send($("#message").val());
    $("#message").val("");
  });
});
