const deleteButton = document.querySelector(".button_delete");
const deleteModal = document.querySelector(".button_delete_modal");

deleteButton.addEventListener("click", () => {
  deleteModal.style.display = "block";
});

const closeModalButton = document.querySelector(".button_delete_content_close");

closeModalButton.addEventListener("click", () => {
  deleteModal.style.display = "none";
});
