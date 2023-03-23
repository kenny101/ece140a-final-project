import { fetchAuthPages } from "./auth.js";
await fetchAuthPages();

const updateFormHandler = {
  formDoc: document.getElementById("update_form"),
  handleClick() {
    this.formDoc.addEventListener("submit", (e) => {
      e.preventDefault();
      const formData = new FormData(this.formDoc);

      const data = {
        username: formData.get("username"),
        email: formData.get("email"),
        student_id: formData.get("student_id"),
      };

      fetch("update-profile", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.getBearerToken()}`,
        },
        body: JSON.stringify(data),
      })
        .then((response) => response.json())
        .then((response) => {
          this.displayUpdatedText();
        })
        .catch((e) => {
          console.log("error", e);
        });
    });
  },
  getBearerToken() {
    const tokenRegex = /jwt=Bearer\s([^;]+)/;
    const match = document.cookie.match(tokenRegex);
    return match ? match[1] : null;
  },
  setFormValue(document_id, value) {
    const doc = document.getElementById(document_id);
    doc.value = value;
  },
  loadFormValues() {
    fetch("get-profile", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.getBearerToken()}`,
      },
    })
      .then((response) => response.json())
      .then((response) => {
        this.setFormValue("username", response[0].username);
        this.setFormValue("student_id", response[0].student_id);
        this.setFormValue("email", response[0].email);
      })
      .catch((e) => {
        console.log("error", e);
      });
  },
  displayUpdatedText() {
    const updatedText = document.getElementById("updated_text");
    updatedText.classList.remove("hidden");
  },
};

updateFormHandler.handleClick();
updateFormHandler.loadFormValues();
