function openDialog(dialogClass) {
    document.querySelector("#overlay").style.display = "block";
    const dialog = document.querySelector(`.dialog.${dialogClass}`);
    dialog.style.display = "flex";
    return dialog
}

function closeDialog(dialogClass) {
    document.querySelector("#overlay").style.display = "none";
    document.querySelector(`.dialog.${dialogClass}`).style.display = "none";
}

function closeAllDialogs() {
    document.querySelector("#overlay").style.display = "none";
    const popups = document.querySelectorAll(".dialog");
    popups.forEach(popup => popup.style.display = "none");
}

function openFileAddDialog() {
    const dialog = openDialog('add')
    dialog.querySelector('.dialog-form').action = `/file/create`
}

function openFileEditDialog(file_id) {
    fetch(`/file/${file_id}`, {method: "GET"})
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch file data");
            }
            return response.json();
        })
        .then(file => {
            const dialog = openDialog('edit')
            dialog.querySelector('.dialog-form').action = `/file/${file.id}/update`
            dialog.querySelector('#file_name').value = file.name;
            dialog.querySelector('#file').value = file.url.split(/\\|\//).pop();
            dialog.querySelector(".file-button.download").href = `/file/${file.id}/download`
            dialog.querySelector('#allowed-users').value = file.users.map(user => user.username).join(', ');
            file.users.forEach(user => {
                dialog.querySelector(`.dropdown-element input#User\\ ${user.id}`).checked = true;
            });
            dialog.querySelector('.dialog-button.danger').href = `/file/${file.id}/delete`
        })
        .catch(error => {
            console.error("Error fetching file data:", error);
        });
}

function openUserAddDialog() {
    const dialog = openDialog('add')
    dialog.querySelector('.dialog-form').action = `/user/create`
}

function openUserEditDialog(user_id) {
    fetch(`/user/${user_id}`, {method: "GET"})
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch file data");
            }
            return response.json();
        })
        .then(user => {
            const dialog = openDialog('edit')
            dialog.querySelector('.dialog-form').action = `/user/${user.id}/update`
            dialog.querySelector('#username').value = user.username;
            dialog.querySelector('#is-admin').checked = user.is_admin;
            dialog.querySelector('.dialog-button.danger').href = `/user/${user.id}/delete`
        })
        .catch(error => {
            console.error("Error fetching file data:", error);
        });
}


function triggerFileUpload(dialogType) {
    const dialog = document.getElementsByClassName(`dialog ${dialogType}`)[0];
    dialog.querySelector("#fileInput").click();
}

function handleFileUpload(event, dialogType) {
    const file = event.target.files[0];
    if (file) {
        const dialog = document.getElementsByClassName(`dialog ${dialogType}`)[0];
        dialog.querySelector("#file").value = file.name;
    }
}

function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
}

function selectUser(checkbox, dialogType) {
    const dialog = document.querySelector(`.dialog.${dialogType}`);
    const inputField = dialog.querySelector("#allowed-users");
    const selectedUsers = inputField.value ? inputField.value.split(", ") : [];

    if (checkbox.checked) {
        selectedUsers.push(checkbox.value);
    } else {
        const index = selectedUsers.indexOf(checkbox.value);
        if (index >= 0) {
            selectedUsers.splice(index, 1);
        }
    }

    inputField.value = selectedUsers.join(", ");
}

function checkUsernameAvailability(input) {
    const user_input = input.value
    const warning_field = document.getElementById('auth_warning')
    const send_button = document.getElementsByClassName('dialog-button success')[0]

    fetch(`/user/${user_input}`, {method: "GET"})
        .then(response => {
            if (response.ok) {
                warning_field.style.display = 'block'
                warning_field.innerText = "This username is already taken. Please select another one."
                send_button.disabled = true
            } else {
                warning_field.style.display = 'none'
                send_button.disabled = false
            }
        })
}

document.addEventListener("click", function (event) {
    const openButtons = document.querySelectorAll(".dropdown-button");
    const dropdownMenus = document.querySelectorAll(".dropdown-menu");

    function listContains(list, element) {
        return Array.from(list).some(listElement => listElement.contains(element));
    }

    if (!listContains(dropdownMenus, event.target) && !listContains(openButtons, event.target)) {
        dropdownMenus.forEach(dropdownMenu => dropdownMenu.style.display = "none")
    }
});