$(document).ready(() => {
  let textarea = $("#messages");
  let sendMessage = (msg) => {
    textarea.append(msg + "\n");
    textarea.scrollTop(textarea[0].scrollHeight);
  };

  let memberList = $("#members");
  let addMember = (m) => {
    console.log(m);
    let li = document.createElement("li");
    let span = document.createElement("span");
    li.innerHTML = m.username;
    li.setAttribute(
      "class",
      "list-group-item d-flex justify-content-between align-items-center",
    );
    span.innerHTML = m.is_ready ? "&#10004   " + m.points : m.points;
    span.setAttribute("class", "badge badge-primary");
    li.appendChild(span);
    memberList.append(li);
  };

  let refreshMembers = (members) => {
    memberList.empty();
    members.forEach((member) => {
      addMember(member);
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

  socket.on("refresh_members", (members) => {
    refreshMembers(members);
  });

  $("#sendMsgButton").on("click", () => {
    socket.send($("#message").val());
    $("#message").val("");
  });
});
