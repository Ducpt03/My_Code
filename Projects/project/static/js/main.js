/*===== LOGIN SHOW and HIDDEN =====*/
const signUp = document.getElementById("sign-up"),
  signIn = document.getElementById("sign-in"),
  loginIn = document.getElementById("login-in"),
  loginUp = document.getElementById("login-up");

signUp.addEventListener("click", () => {
  // Remove classes first if they exist
  loginIn.classList.remove("block");
  loginUp.classList.remove("none");

  // Add classes
  loginIn.classList.toggle("none");
  loginUp.classList.toggle("block");
});

signIn.addEventListener("click", () => {
  // Remove classes first if they exist
  loginIn.classList.remove("none");
  loginUp.classList.remove("block");

  // Add classes
  loginIn.classList.toggle("block");
  loginUp.classList.toggle("none");
}) <
  script >
  document.addEventListener("DOMContentLoaded", (event) => {
    const passwordInput = document.getElementById("password");
    const passwordStrength = document.getElementById("password-strength");
    let isPasswordVisible = true; // Biến này để kiểm tra xem mật khẩu có đang hiển thị hay không

    passwordInput.addEventListener("input", () => {
      const strength = getPasswordStrength(passwordInput.value);
      if (passwordInput.value === "") {
        passwordStrength.innerText = ""; // Nếu mật khẩu trống thì không hiển thị độ mạnh
      } else {
        updatePasswordStrengthUI(strength);
      }
    });

    passwordInput.addEventListener("focus", () => {
      if (!isPasswordVisible) {
        passwordStrength.innerText = ""; // Khi mật khẩu được tập trung (focus), nếu nó không hiển thị, không hiển thị độ mạnh
      }
    });

    passwordInput.addEventListener("blur", () => {
      if (!isPasswordVisible && passwordInput.value !== "") {
        const strength = getPasswordStrength(passwordInput.value);
        updatePasswordStrengthUI(strength);
      }
    });

    function getPasswordStrength(password) {
      let strength = 0;
      if (password.length >= 8) strength++; // length
      if (password.match(/[A-Z]/)) strength++; // uppercase letter
      if (password.match(/[a-z]/)) strength++; // lowercase letter
      if (password.match(/[0-9]/)) strength++; // number
      if (password.match(/[^A-Za-z0-9]/)) strength++; // special character
      return strength;
    }

    function updatePasswordStrengthUI(strength) {
      switch (strength) {
        case 0:
        case 1:
          passwordStrength.innerText = "Weak";
          passwordStrength.style.color = "red";
          passwordInput.style.borderColor = "red";
          break;
        case 2:
        case 3:
          passwordStrength.innerText = "Medium";
          passwordStrength.style.color = "orange";
          passwordInput.style.borderColor = "orange";
          break;
        case 4:
        case 5:
          passwordStrength.innerText = "Strong";
          passwordStrength.style.color = "green";
          passwordInput.style.borderColor = "green";
          break;
      }
    }
  });
