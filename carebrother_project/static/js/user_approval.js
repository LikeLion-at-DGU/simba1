const tbody = document.querySelector("tbody");

tbody.addEventListener("click", (event) => {
  const target = event.target;

  if (target.classList.contains("image-button")) {
    const modal = target.nextElementSibling;
    modal.style.display = "block";
  }

  if (target.classList.contains("modal_content_close")) {
    const modal = target.parentNode.parentNode;
    modal.style.display = "none";
  }

  if (target.classList.contains("approval")) {
    const modal = target.nextElementSibling;
    modal.style.display = "block";
  }

  if (target.classList.contains("refusal")) {
    const modal = target.nextElementSibling;
    modal.style.display = "block";
  }
});
