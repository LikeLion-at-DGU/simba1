const fileInput = document.getElementById("chooseFile");
const preview = document.querySelector(".preview");


fileInput.addEventListener("change", function () {
  const file = fileInput.files[0];
  preview.innerHTML = "";
  if (file && file.type.startsWith("image/")) {
    if (fileInput.files.length > 0) {
      const files = Array.from(fileInput.files);
      files.forEach(function (file) {
        const reader = new FileReader();
        reader.onload = function (event) {
          const image = document.createElement("img");
          image.src = event.target.result;
          preview.appendChild(image);
        };
        reader.readAsDataURL(file);
      });
    }
  } 
});
