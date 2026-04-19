let token = "";
let selectedTaskId = null;

// ✅ REGISTER
async function register() {
    let res = await fetch("https://task-manager-fastapi-jy71.onrender.com/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: email.value,
            password: password.value
        })
    });

    let data = await res.json();

    if (!res.ok) {
        alert(data.detail);
        return;
    }

    token = data.access_token;
    alert("Registered & Logged in!");
    getTasks();
}

// ✅ LOGIN
async function login() {
    let res = await fetch("https://task-manager-fastapi-jy71.onrender.com/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: email.value,
            password: password.value
        })
    });

    let data = await res.json();
    token = data.access_token;
    getTasks();
}

// ✅ CREATE TASK
async function createTask() {
    await fetch("https://task-manager-fastapi-jy71.onrender.com/tasks", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({title: task.value})
    });

    task.value = "";
    getTasks();
}

// ✅ GET TASKS
async function getTasks() {
    let res = await fetch("https://task-manager-fastapi-jy71.onrender.com/tasks", {
        headers: {"Authorization": "Bearer " + token}
    });

    let data = await res.json();

    tasks.innerHTML = "";

    data.forEach(t => {
        tasks.innerHTML += `
        <li 
            onclick="openPopup(${t.id}, '${t.title}', ${t.completed})"
            style="margin:10px; padding:10px; border:1px solid #ccc; cursor:pointer;"
        >
            <b>${t.title}</b>
            <span style="color:${t.completed ? 'green' : 'red'}">
                ${t.completed ? '✔' : '❌'}
            </span>
        </li>
        `;
    });
}



function openPopup(id, title, completed) {
    selectedTaskId = id;

    document.getElementById("popup").style.display = "block";
    document.getElementById("popupTitle").innerText = title;
    document.getElementById("popupStatus").innerText =
        completed ? "✔ Completed" : "❌ Pending";

    // Complete button
    document.getElementById("completeBtn").onclick = async () => {
        await fetch(`https://task-manager-fastapi-jy71.onrender.com/${id}`, {
            method: "PUT",
            headers: {"Authorization": "Bearer " + token}
        });
        closePopup();
        getTasks();
    };

    // Delete button
    document.getElementById("deleteBtn").onclick = async () => {
        await fetch(`https://task-manager-fastapi-jy71.onrender.com/tasks/${id}`, {
            method: "DELETE",
            headers: {"Authorization": "Bearer " + token}
        });
        closePopup();
        getTasks();
    };
}

function closePopup() {
    document.getElementById("popup").style.display = "none";
}