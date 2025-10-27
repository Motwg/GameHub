let uniqueId = () => {
  // desired length of Id
  const idStrLen = 32;
  // always start with a letter -- base 36 makes for a nice shortcut
  let idStr = (Math.floor(Math.random() * 25) + 10).toString(36) + "_";
  // add a timestamp in milliseconds (base 36 again) as the base
  idStr += new Date().getTime().toString(36) + "_";
  // similar to above, complete the Id using random, alphanumeric characters
  do {
    idStr += Math.floor(Math.random() * 35).toString(36);
  } while (idStr.length < idStrLen);

  return idStr;
};

let openModalCreateActivity = () => {
  let modal = new bootstrap.Modal(
    document.getElementById("createActivityModal"),
    {},
  );
  modal.show();
};

let createActivity = () => {
  const params = {
    activity: document.getElementById("selectActivity").value,
    password: document.getElementById("password").value,
  };
  const xhr = new XMLHttpRequest();
  xhr.open("POST", roomUrl);
  xhr.setRequestHeader("Content-type", "application/json");
  xhr.responseType = "json";
  xhr.send(JSON.stringify(params));
  xhr.onload = () => {
    if (xhr.readyState == 4 && xhr.status == 201) {
      console.log("Activity created");
      window.location.replace(roomUrl);
    } else {
      console.log("Error: " + xhr.status);
    }
  };
};

let changeUsername = () => {
  let username = usernameInput.value;
  if (username.length > 3) {
    const params = {
      username: username,
    };
    const xhr = new XMLHttpRequest();
    xhr.open("POST", loginUrl);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.responseType = "json";
    xhr.send(JSON.stringify(params));
    xhr.onload = () => {
      if (xhr.readyState == 4 && xhr.status == 200) {
        localStorage.username = username;
        console.log("Username changed to " + username);
      } else {
        console.log("Error: " + xhr.status);
      }
    };
  }
};

let username = "";
const usernameInput = document.getElementById("usernameInput");
const usernameCurrent = document.getElementById("usernameCurrent");
// Load user
if (localStorage.uuid && localStorage.username) {
  username = localStorage.username;
  // Create UUID for new user
} else {
  let uuid = uniqueId();
  username = "Player_" + uuid.substring(2, 10);
  localStorage.uuid = uuid;
  localStorage.username = username;
}

usernameInput.value = username;
usernameCurrent.innerText = username;
changeUsername();
