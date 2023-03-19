import { fetchAuthPages } from "./auth.js";
await fetchAuthPages();

const commentsHandler = {
  commentsForm: document.getElementById("comments_form"),
  commenterDoc: document.getElementById("commenter"),
  displayComment(username, date, comment, comment_id) {
    let hidden = "";
    if (this.getUsernameFromPayload() != username) {
      hidden = "hidden";
    }
    const main = document.querySelector("main");
    const section = document.createElement("section");
    section.setAttribute(
      "class",
      "grid grid-cols-1 gap-4 p-4 mb-2 border rounded-lg bg-neutral-100 shadow-md"
    );
    section.innerHTML = `
        <div class="flex gap-4">
          <img src="https://img.icons8.com/dotty/80/null/cat-profile.png" />
          <div class="flex flex-col w-full">
            <div class="flex flex-row justify-between">
              <p
                class=" text-2xl whitespace-nowrap truncate overflow-hidden"
              >
                ${username}
              </p>
              <div class="${hidden}">
                <a
                  class="text-gray-500 text-xl p-1 px-2 hover:bg-neutral-300 rounded-xl"
                  ><i class="fa-solid fa-pen-to-square" id="edit-btn-${comment_id}"></i
                ></a>
                <a
                  class="text-gray-500 text-xl p-1 px-2 hover:bg-neutral-300 rounded-xl"
                  ><i class="fa-solid fa-trash" id="delete-btn-${comment_id}"></i
                ></a>
              </div>
            </div>
            <p class="text-gray-400 text-sm">${date}</p>
          </div>
        </div>
        <p class="-mt-4 text-gray-500">
          ${comment}
        </p>
    `;
    main.appendChild(section);

    const editBtn = document.getElementById(`edit-btn-${comment_id}`);
    const deleteBtn = document.getElementById(`delete-btn-${comment_id}`);
    editBtn.addEventListener("click", async () => {
      console.log("edit was clicked");
    });

    deleteBtn.addEventListener("click", async () => {
      console.log("delete was clicked");
      section.remove();
      this.deleteComment(String(comment_id));
    });
  },
  getCommentId() {
    const localUrl = window.location.href;
    const regex = /.*-(\d+)$/;
    const match = localUrl.match(regex);
    if (match && match[1]) {
      return match[1];
    } else {
      return null;
    }
  },
  handleSubmit() {
    this.commentsForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const commentText = this.commentsForm.querySelector("textarea").value;
      const data = {
        username: this.getUsernameFromPayload(),
        comment: commentText,
        comment_id: this.getCommentId(),
        date: this.getCurrentDateTime(),
      };
      const url = `post-comment`;
      const response = await this.makeReq(url, data, "POST");
      console.log("comment_id:", response.comment_id);
      this.displayComment(
        data.username,
        data.date,
        data.comment,
        response.comment_id
      );
    });
  },
  getTitleById() {
    const main = document.querySelector("main");
    const mainHeading = main.querySelector("h1");
    const id = parseInt(this.getCommentId());
    const leaderboardMap = JSON.parse(localStorage.getItem("leaderboardMap"));
    for (let i = 0; i < leaderboardMap.length; i++) {
      if (leaderboardMap[i][0] === id) {
        mainHeading.textContent = leaderboardMap[i][1].name;
        return;
      }
    }
    mainHeading.textContent = "Title was not found";
  },
  getUsernameFromPayload() {
    const token = this.getBearerToken();
    const parts = token.split(".");
    const payload = JSON.parse(atob(parts[1]));
    const sub = payload.sub;
    return sub;
  },
  async setTitle() {
    const response = await fetch(
      `https://slidespace.icu/api/teams/${this.getCommentId()}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    var data = await response.json();

    // Parse the JSON string in the team property
    const title = JSON.parse(data.team).name;
    const main = document.querySelector("main");
    const mainHeading = main.querySelector("h1");
    mainHeading.textContent = title;
  },
  async makeReq(url, body, method) {
    const headerData = {
      method: method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.getBearerToken()}`,
      },
    };
    if (method !== "GET") {
      headerData.body = JSON.stringify(body);
    }
    const response = await fetch(url, headerData);
    return response.json();
  },
  async loadAllComments() {
    const data = {
      jwt: this.getBearerToken(),
      username: this.getUsernameFromPayload(),
    };
    const url = `load-comments-${this.getCommentId()}`;
    const allComments = await this.makeReq(url, data, "GET");
    for (const commentKey in allComments) {
      const { username, comment, date, id } = allComments[commentKey];
      this.displayComment(username, date, comment, id);
    }
  },
  async deleteComment(id) {
    console.log("id", { comment_id: id });
    const data = { comment_id: id };
    const response = await this.makeReq("delete-comment", data, "DELETE");

    console.log("delete response:", response);
  },

  getBearerToken() {
    const tokenRegex = /jwt=Bearer\s([^;]+)/;
    const match = document.cookie.match(tokenRegex);
    return match ? match[1] : null;
  },
  getCurrentDateTime() {
    const currentDate = new Date();
    const day = currentDate.getDate();
    const month = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ][currentDate.getMonth()];
    const year = currentDate.getFullYear();
    const time = currentDate.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
    return `${month} ${day}, ${year} at ${time}`;
  },
};
commentsHandler.getTitleById();
commentsHandler.loadAllComments();
commentsHandler.handleSubmit();
