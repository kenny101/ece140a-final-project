import { fetchAuthPages } from "./auth.js";
await fetchAuthPages();

const signInFormHandler = {
  formDoc: document.getElementById("signin_form"),
  signinDoc: document.getElementById("signin_btn"),
  handleClick() {
    this.formDoc.addEventListener("submit", (e) => {
      e.preventDefault();
      localStorage.clear();
      const formData = new URLSearchParams(new FormData(this.formDoc));
      fetch("token", {
        method: "POST",
        body: formData,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      })
        .then((response) => response.json())
        .then((response) => {
          document.cookie = `jwt=Bearer ${response.access_token}; path=/; SameSite=None; Secure`;
          if (response.access_token !== undefined){
            window.location.href="updates";
          }else{
            this.displayLoginError();
          }
        })
        .catch(() => this.displayLoginError());
    });
  },
  getBearerToken() {
    const tokenRegex = /jwt=Bearer\s([^;]+)/;
    const match = document.cookie.match(tokenRegex);
    return match ? match[1] : null;
  },
  displayLoginError() {
    const warningDoc = document.getElementById("signin_warning");
    warningDoc.classList.remove("hidden");
  },
};

signInFormHandler.handleClick();
