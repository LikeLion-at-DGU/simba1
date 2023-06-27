

/* ID */
const idInput = document.getElementById("idInput");
const clearIdButton = document.getElementById("clearId");
const idErrorMessage = document.getElementById("IdErrorMessage");
clearIdButton.addEventListener("click", function () {
  idInput.value = "";
});

idInput.addEventListener("input", function () {
  const inputValue = idInput.value.trim();
  if (inputValue.length !== 10) {
    idErrorMessage.style.visibility = "visible";
  } else {
    idErrorMessage.style.visibility = "hidden";
  }
});


/* 비밀번호 */
const passwordInput = document.querySelector('input[name="password"]');
const passwordToggle = document.getElementById("passwordToggle");
const passwordErrorMessage = document.getElementById("passwordErrorMessage");

passwordToggle.addEventListener("click", function () {
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    passwordToggle.classList.remove("fa-eye");
    passwordToggle.classList.add("fa-eye-slash");
  } else {
    passwordInput.type = "password";
    passwordToggle.classList.remove("fa-eye-slash");
    passwordToggle.classList.add("fa-eye");
  }
});

passwordInput.addEventListener("input", function () {
  const inputValue = passwordInput.value.trim();
  const passwordPattern = /^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,16}$/;
  if (!passwordPattern.test(inputValue)) {
    passwordErrorMessage.style.visibility = "visible";
  } else {
    passwordErrorMessage.style.visibility = "hidden";
  }
});

/* 비밀번호 체크 */
const passwordCheckInput = document.querySelector(
  'input[name="password-check"]'
);
const passwordCheckToggle = document.getElementById("passwordCheckToggle");
const passwordCheckErrorMessage = document.getElementById(
  "passwordCheckErrorMessage"
);

function validatePassword() {
  const passwordValue = passwordInput.value.trim();
  const passwordCheckValue = passwordCheckInput.value.trim();

  if (passwordValue !== passwordCheckValue) {
    passwordCheckErrorMessage.style.visibility = "visible";
  } else {
    passwordCheckErrorMessage.style.visibility = "hidden";
  }
}

passwordInput.addEventListener("input", validatePassword);
passwordCheckInput.addEventListener("input", validatePassword);

passwordCheckToggle.addEventListener("click", function () {
  if (passwordCheckInput.type === "password") {
    passwordCheckInput.type = "text";
    passwordCheckToggle.classList.remove("fa-eye");
    passwordCheckToggle.classList.add("fa-eye-slash");
  } else {
    passwordCheckInput.type = "password";
    passwordCheckToggle.classList.remove("fa-eye-slash");
    passwordCheckToggle.classList.add("fa-eye");
  }
});



/* 닉네임 */
const nicknameInput = document.getElementById("nicknameInput");
const clearNickNameButton = document.getElementById("clearNickname");
const nicknameErrorMessage = document.getElementById("nicknameErrorMessage");

clearNickNameButton.addEventListener("click", function () {
  nicknameInput.value = "";
});

function validateNickname() {
  const nicknameValue = nicknameInput.value.trim();

  if (nicknameValue.length < 2) {
    nicknameErrorMessage.style.visibility = "visible";
  } else {
    nicknameErrorMessage.style.visibility = "hidden";
  }
}

nicknameInput.addEventListener("input", validateNickname);

/* 버튼 활성화/비활성화 */
/* 모든 입력값이 다 들어있고, 에러메시지가 하나도 없을 때 => 버튼 활성화 */
const signUpForm = document.getElementById("sign-up-form");
const inputFields = signUpForm.querySelectorAll("input[required]");
const nextButton = document.querySelector('.next_button input[type="submit"]');

function checkInputFields() {
  let allFilled = true;

  inputFields.forEach(function (input) {
    if (input.value.trim() === "") {
      allFilled = false;
    }
  });

  const errorMessages = signUpForm.getElementsByClassName("error-message");
  let allErrorsHidden = true;

  for (let i = 0; i < errorMessages.length; i++) {
    if (errorMessages[i].style.visibility === "visible") {
      allErrorsHidden = false;
      break;
    }
  }

  if (allFilled && allErrorsHidden) {
    nextButton.classList.add("active");
    nextButton.style.cursor = "pointer";
  } else {
    nextButton.classList.remove("active");
    nextButton.style.cursor = "not-allowed";
  }
}

inputFields.forEach(function (input) {
  input.addEventListener("input", checkInputFields);
});

