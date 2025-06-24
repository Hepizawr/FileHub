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

function refreshPage() {
    window.location.reload();
}

function getFormDataFromInputs(inputs) {
    const formData = new FormData();
    Array.from(inputs).forEach(input => {
        switch (input.type) {
            case "checkbox":
            case "radio":
                // formData.append(input.name, input.checked);
                formData.append(input.name, input.checked || '');
                break;
            case "file":
                formData.append(input.name, input.files[0] || '');
                break;
            default:
                formData.append(input.name, input.value || '');
        }
    });
    return formData;
}

async function submitDeleteRequest(URL) {
    return fetch(URL, {method: "DELETE"})
}

async function submitData(URL, method, formData) {
    return fetch(URL, {method: method, body: formData})
}

async function getData(URL) {
    const response = await fetch(URL, {method: "GET"})
    return response.ok ? await response.json() : null;
}

function openAddDialog(url) {
    const dialog = openDialog("add")
    const submitButton = dialog.querySelector("*[type='submit']")
    submitButton.addEventListener('click', async (e) => {
        e.preventDefault();
        const inputs = dialog.querySelectorAll("*[name]");
        const formData = getFormDataFromInputs(inputs);
        const response = await submitData(url, "POST", formData);
        response.ok && refreshPage();
    });
}

async function openFileEditDialog(file_id) {
    const dialog = openDialog('edit');

    const url = `/api/files/${file_id}`;
    const data = await getData(url);
    dialog.querySelector('#file_name').value = data.name;
    dialog.querySelector('#file').value = data.name + data.format;
    dialog.querySelector(".file-button.download").href = url + "/download"
    dialog.querySelector('#allowed-users').value = data.users.map(user => user.username).join(', ');
    data.users.forEach(user => {
        dialog.querySelector(`.dropdown-element input#User\\ ${user.id}`).checked = true;
    });
    const submitButton = dialog.querySelector("*[type='submit']")
    submitButton.addEventListener('click', async (e) => {
        e.preventDefault();
        const inputs = dialog.querySelectorAll("*[name]");
        const formData = getFormDataFromInputs(inputs);
        const response = await submitData(url, "PATCH", formData);
        response.ok && refreshPage();
    });
    const deleteButton = dialog.querySelector("*[type='delete']")
    deleteButton.addEventListener("click", async (e) => {
        e.preventDefault()
        const response = await submitDeleteRequest(url);
        response.ok && refreshPage();
    });
}

async function openUserEditDialog(user_id) {
    const dialog = openDialog('edit');

    const url = `/api/users/${user_id}`;
    const data = await getData(url);
    dialog.querySelector('#username').value = data.username;
    dialog.querySelector('#is_admin').checked = data.is_admin;
    const submitButton = dialog.querySelector("*[type='submit']")
    submitButton.addEventListener('click', async (e) => {
        e.preventDefault();
        const inputs = dialog.querySelectorAll("*[name]");
        const formData = getFormDataFromInputs(inputs);
        const response = await submitData(url, "PATCH", formData);
        response.ok && refreshPage();
    });
    const deleteButton = dialog.querySelector("*[type='delete']")
    deleteButton.addEventListener("click", async (e) => {
        e.preventDefault();
        const response = await submitDeleteRequest(url);
        response.ok && refreshPage();
    });
}

async function downloadFile(URL) {
    const response = await fetch(URL, {method: "GET"})
    if (!response.ok) {
        const data = await response.json()
        return alert(data.message)
    }
    const downloadLink = document.createElement("a");
    downloadLink.href = URL;
    return downloadLink.click();
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

    fetch(`api/users/${user_input}`, {method: "GET"})
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