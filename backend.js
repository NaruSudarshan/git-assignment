// Fake backend route simulation
function submitTodoItem(itemName, itemDescription) {
    return { itemName, itemDescription, status: "stored in DB" };
}
