function startEdit(id) {
    document.getElementById(`user-display-${id}`).style.display = 'none';
    document.getElementById(`user-edit-${id}`).style.display = 'inline-flex';
    document.getElementById(`username-input-${id}`).focus();
}

function cancelEdit(id) {
    const savedName = document.getElementById(`username-${id}`).textContent.trim();
    document.getElementById(`username-input-${id}`).value = savedName;
    document.getElementById(`user-edit-${id}`).style.display = 'none';
    document.getElementById(`user-display-${id}`).style.display = 'flex';
    document.getElementById(`user-display-${id}`).style.justifyContent = 'space-between';
}