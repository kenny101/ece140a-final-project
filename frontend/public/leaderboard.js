import { fetchAuthPages } from "./auth.js";
await fetchAuthPages();

const fetchError = document.getElementById("fetch-error");
function displaySection(id, projectName, members, scores) {
  const main = document.querySelector("main");
  const section = document.createElement("section");
  section.setAttribute("class", "w-full mx-auto px-10");
  section.innerHTML = `<section class="w-full mx-auto px-10">
<article class="bg-white shadow-md border border-gray-200 rounded-lg mb-5 p-5">
    <h3 class="text-gray-900 font-bold text-2xl tracking-tight mb-2">${projectName}</h3>
    <h4 class="text-gray-900 font-semibold text-xl tracking-tight mb-2">Team Members: ${members}</h4>
    <p class="font-normal text-gray-700 mb-3">Topic Scores: ${scores}</p>
    <a class="text-white bg-blue-700 hover:bg-blue-800 font-medium rounded-lg text-sm px-3 py-2" href="./comments-${id}">
        Comments
    </a>
</article>
</section>`;
  main.appendChild(section);
}

function loadLeaderboardMap() {
  const leaderboardString = localStorage.getItem("leaderboardMap");
  if (leaderboardString) {
    const leaderboardArray = JSON.parse(leaderboardString);
    return new Map(leaderboardArray);
  } else {
    return new Map();
  }
}

var leaderboardMap = new Map();
async function fetchData() {
  // Check if data exists in localstorage:
  if (localStorage.getItem("leaderboardMap")) {
    leaderboardMap = loadLeaderboardMap();
    if (leaderboardMap.size === 26) {
      for (let i = 1; i <= 26; i++) {
        displaySection(
          leaderboardMap.get(i).id,
          leaderboardMap.get(i).name,
          leaderboardMap.get(i).parsedMembers,
          leaderboardMap.get(i).topics
        );
      }
      return;
    }
  }

  // else fetch the data and load into localstorage for future use
  try {
    const teamEndpoints = Array.from({ length: 26 }, (_, i) => i + 1).map(
      (i) => `https://slidespace.icu/api/teams/${i}`
    );
    const teamResponses = await Promise.all(
      teamEndpoints.map((url) => fetch(url))
    );
    const teamData = await Promise.all(teamResponses.map((res) => res.json()));

    const scoresEndpoints = Array.from({ length: 26 }, (_, i) => i + 1).map(
      (i) => `https://slidespace.icu/api/teams/${i}/scores`
    );
    const scoresResponses = await Promise.all(
      scoresEndpoints.map((url) => fetch(url))
    );
    const scoresData = await Promise.all(
      scoresResponses.map((res) => res.json())
    );

    for (let i = 0; i <= 25; i++) {
      const { id, name, members } = JSON.parse(teamData[i].team);
      const parsedMembers = JSON.parse(members)
        .map((name) => name.trim())
        .join(", ");
      const { topic_1, topic_2, topic_3 } = JSON.parse(scoresData[i].scores);
      leaderboardMap.set(id, {
        id: id,
        name: name,
        parsedMembers: parsedMembers,
        topics: `${topic_1}, ${topic_2}, ${topic_3}`,
      });
      displaySection(
        id,
        name,
        parsedMembers,
        `${topic_1}, ${topic_2}, ${topic_3}`
      );
    }
  } catch (e) {
    console.log("error:", e)
    fetchError.classList.remove("hidden");
    return;
  } finally {
    localStorage.setItem(
      "leaderboardMap",
      JSON.stringify(Array.from(leaderboardMap.entries()))
    );
  }
}
fetchData();
