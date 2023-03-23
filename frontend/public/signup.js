const signUpFormHandler = {
  formDoc: document.getElementById("signup_form"),
  handleClick() {
    this.formDoc.addEventListener("submit", (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      const data = {
        username: formData.get("username"),
        first_name: formData.get("first_name"),
        last_name: formData.get("last_name"),
        email: formData.get("email"),
        student_id: formData.get("student_id"),
        hashed_password: formData.get("password"),
      };

      console.log("data", data);

      fetch("create-account", {
        credentials: "same-origin",
        method: "POST",
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        }
      })
        .then((response) => response.json())
        .then((response) => {
          document.cookie = `jwt=Bearer ${response.access_token}; path=/; SameSite=None; Secure`;
          if (response.access_token !== undefined) {
            window.location.href = "updates";
          } else {
            this.displaySignupError();
          }
        })
        .catch((e) => {
          this.displaySignUpError();
        });
    });
  },
  getBearerToken() {
    const tokenRegex = /jwt=Bearer\s([^;]+)/;
    const match = document.cookie.match(tokenRegex);
    return match ? match[1] : null;
  },
  displaySignUpError() {
    const warningDoc = document.getElementById("signup_warning");
    warningDoc.classList.remove("hidden");
  },
};

signUpFormHandler.handleClick();
