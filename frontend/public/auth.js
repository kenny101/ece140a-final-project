function getBearerToken() {
  const tokenRegex = /jwt=Bearer\s([^;]+)/;
  const match = document.cookie.match(tokenRegex);
  return match ? match[1] : null;
}

async function replaceBodyHTML(bodyHTML) {
  var currentBody = document.getElementsByTagName("body")[0];
  var parser = new DOMParser();
  var newBody = parser.parseFromString(bodyHTML, "text/html").body;
  currentBody.parentNode.replaceChild(newBody, currentBody);
}

// Sign out by deleting the jwt cookie and redirect to homepage
function signOut() {
  const signOutBtn = document.getElementById("sign_out_btn");
  if (signOutBtn) {
    document.getElementById("sign_out_btn").addEventListener("click", () => {
      document.cookie =
        "jwt" + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
      window.location.href = "/";
    });
  }
}

const UNAUTH_HTML = `
<body
    class="bg-blue-100 w-screen h-screen flex items-center justify-center h-screen flex-col"
  >
    <h1 class="text-5xl font-bold text-center text-gray-800 mb-20">
      Error 401: Unauthorized Access
    </h1>
    <img src="../assets/401-error.svg" alt="image of 404 error code" />
  </body>
`;

const authPages = new Set([
  "updates",
  "leaderboard",
  "profile",
  "blog-1",
  "blog-2",
  "blog-3",
  "comments",
]);

async function fetchAuthPages() {
  var currentPage = window.location.href.split("/");

  var check = currentPage[currentPage.length - 1].replace(/[\/#-\d\s]/g, "");
  if (check == "blog") {
    currentPage = currentPage[currentPage.length - 1].replace(/[\/#]/g, "");
  } else {
    currentPage = check;
  }

  for (let page of authPages) {
    if (String(currentPage) === String(page)) {
      try {
        const response = await fetch(`${page}-html/`, {
          headers: {
            Authorization: `Bearer ${getBearerToken()}`,
          },
        });
        const data = await response.json();
        if (data.html) {
          await replaceBodyHTML(data.html);
          signOut();
        } else {
          await replaceBodyHTML(UNAUTH_HTML);
        }
      } catch {
        await replaceBodyHTML(UNAUTH_HTML);
      }
    }
  }
}

export { getBearerToken, replaceBodyHTML, signOut, fetchAuthPages };

