const fileInput = document.getElementById("chooseFile");
const preview = document.querySelector(".preview");
const nextButton = document.querySelector('.next_button input[type="submit"]');


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
    // 이미지 파일이 선택된 경우 버튼 활성화
    nextButton.classList.add("active");
    nextButton.style.cursor = "pointer";
  } else {
    console.log("이미지 파일을 선택해주세요.");

    // 이미지 파일이 선택되지 않은 경우 버튼 비활성화
    nextButton.classList.remove("active");
    nextButton.style.cursor = "not-allowed";
  }
});
