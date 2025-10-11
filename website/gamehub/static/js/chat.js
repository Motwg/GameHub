$(document).ready(() => {
  let textarea = $("#messages");
  let sendMessage = (msg) => {
    textarea.append(msg + "\n");
    textarea.scrollTop(textarea[0].scrollHeight);
  };

  let memberList = $("#members");
  let addMember = (username, is_ready, value) => {
    let li = document.createElement("li");
    let span = document.createElement("span");
    li.innerHTML = username;
    li.setAttribute(
      "class",
      "list-group-item d-flex justify-content-between align-items-center",
    );
    span.innerHTML = is_ready ? "&#10004   " + value : value;
    console.log(span);
    span.setAttribute("class", "badge badge-primary");
    li.appendChild(span);
    memberList.append(li);
  };

  let refreshMembers = (members) => {
    memberList.empty();
    members.forEach((member) => {
      addMember(member[0], member[1], 0);
    });
  };

  // socket.io
  socket.on("connect", () => {
    console.log("User connected!");
  });

  socket.on("message", (data) => {
    sendMessage(data);
  });

  socket.on("new_connection", (data) => {
    sendMessage(data.username + " joined room!");
    refreshMembers(data.members);
  });

  socket.on("lost_connection", (data) => {
    sendMessage(data.username + " left room!");
    refreshMembers(data.members);
  });

  $("#sendMsgButton").on("click", () => {
    socket.send($("#message").val());
    $("#message").val("");
  });

  socket.on("change_status", (data) => {
    sendMessage(data.username + " is ready!");
    refreshMembers(data.members);
  });
});
