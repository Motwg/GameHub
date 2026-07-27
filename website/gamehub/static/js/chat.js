$(document).ready(() => {
  const textarea = $("#messages");
  const sendMessage = (msg) => {
    textarea.append(msg + "\n");
    textarea.scrollTop(textarea[0].scrollHeight);
  };

  const memberList = $("#members");
  const addMember = (m) => {
    const li = document.createElement("li");
    const span = document.createElement("span");
    li.innerHTML = m.username;
    li.setAttribute(
      "class",
      "list-group-item d-flex justify-content-between align-items-center",
    );
    span.innerHTML = m.is_ready ? "&#10004   " + m.points : m.points;
    span.setAttribute("class", "badge badge-primary badge-13");
    li.appendChild(span);
    memberList.append(li);
  };

  const refreshMembers = (members) => {
    memberList.empty();
    members.forEach((member) => {
      addMember(member);
    });
  };

  const openNav = () => {
    document.getElementById("sidebar").style.width = "370px";
    document.getElementById("main").style.marginRight = "370px";
  }

  const closeNav = () => {
    document.getElementById("sidebar").style.width = "0px";
    document.getElementById("main").style.marginRight = "0px";
  }

  // socket.io
  socket.on("connect", () => {
    console.log("User connected!");
  });

  socket.on("message", (data) => {
    sendMessage(data);
  });

  socket.on("new_connection", (data) => {
    sendMessage(data.username + " joined the room!");
    refreshMembers(data.members);
  });

  socket.on("lost_connection", (data) => {
    sendMessage(data.username + " left the room!");
    refreshMembers(data.members);
  });

  socket.on("refresh_members", (members) => {
    refreshMembers(members);
  });

  // hooks
  $("#sendMsgButton").click(() => {
    socket.send($("#message").val());
    $("#message").val("");
  });

  $("#message").keydown((event) => {
    if ((event.keyCode || event.which) == 13) {
      $("#sendMsgButton").click();
    }
  });

  let sidebarActive = true;
  $("#toggleSidebarBtn").click(() => {
    if (sidebarActive) {
      sidebarActive = false;
      closeNav();
    } else {
      sidebarActive = true;
      openNav();
    }
  });
});
