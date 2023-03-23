const resetFormHandler = {
  formDoc: document.getElementById("reset_form"),
  handleSubmit() {
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

      fetch("reset-password", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.getBearerToken()}`,
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((response) => {
          console.log("response:", response);
          if (response.detail == "success") {
            this.displayResetSuccess();
          }else{
            this.displayResetError();
          }
        })
        .catch((e) => {
          console.log("error:, ", 0);
        });
    });
  },
  getBearerToken() {
    const tokenRegex = /jwt=Bearer\s([^;]+)/;
    const match = document.cookie.match(tokenRegex);
    return match ? match[1] : null;
  },
  displayResetError() {
    const warningDoc = document.getElementById("reset_warning");
    const successDoc = document.getElementById("success_message");
    warningDoc.classList.toggle("hidden");
    if (!successDoc.classList.contains("hidden")){
      successDoc.classList.toggle("hidden");
    }

  },
  displayResetSuccess() {
    const warningDoc = document.getElementById("reset_warning");
    const successDoc = document.getElementById("success_message");
    successDoc.classList.toggle("hidden");
    if (!warningDoc.classList.contains("hidden")){
      warningDoc.classList.toggle("hidden");
    }
  },
};

resetFormHandler.handleSubmit();
// resetFormHandler.displayResetError();
