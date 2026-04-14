const gamesArray = Object.values(steamData);
const gameTags = gamesArray.map(game => Object.keys(game.tags).slice(0,5));
const gameLanguages = gamesArray.map(game => game.languages);
const topAverage = [...gamesArray].sort((a, b) => b.average_forever - a.average_forever).slice(0, 30);


// Fun recommendations
const mostEngaging = [...gamesArray].sort((a, b) => b.positive - a.positive).slice(0,500);
const randomTopGame = mostEngaging[Math.floor(Math.random() * mostEngaging.length)];
// var mostEngagingText = docum
// mostEnga.innerText = mostEngaging.game;
const titleElement = document.getElementById("mostEngagingTitle");
titleElement.href = `https://store.steampowered.com/app/${randomTopGame.appid}/`;
titleElement.innerText = `Looking for a game to play? Have you tried ${randomTopGame.name} yet?`;
const titleImgElement = document.getElementById("mostEngagingImg");
titleImgElement.src = `https://steamcdn-a.akamaihd.net/steam/apps/${randomTopGame.appid}/header.jpg`
// titleImgElement.onclick = "window.open(" + `https://store.steampowered.com/app/${randomTopGame.appid}/` +")";
const doughnutOptions = {
  maintainAspectRatio: false,
  elements:{
    arc:{
      borderColor: 'rgba(0, 0, 0, 0.6)',
      borderWidth: 12
    }
  },
  plugins: {
    legend: {
      labels: { color: 'white', font: { weight: 'bold' } }
    }
  }
};

new Chart(document.getElementById('chart'), {
  type: 'bar',
  data: {
    labels: topAverage.map(g => g.name),
    datasets: [{
      label: 'Total Owners (Users)',
      data: topAverage.map(g => g.average_forever),
      backgroundColor: 'rgba(54, 162, 235, 0.6)',
      borderColor: 'rgba(54, 162, 235, 1)',
      borderWidth: 1
    }]
  },
  options: {maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }
});

const tagCount = gameTags.flat();
const tag = [...new Set(tagCount)].sort((a, b) => tagCount.filter(tc => tc === b).length - tagCount.filter(tc => tc === a).length).slice(0, 10);

new Chart(document.getElementById('chart2'), {
  type: 'doughnut',
  data: {
    labels: tag,
    datasets: [{
      label: 'Supported Language (Per Game)',
      data: tag.map(t => tagCount.filter(tc => tc === t).length),
      backgroundColor: [ // Array required to differentiate slices
        'rgba(255, 0, 55, 0.6)', 'rgba(0, 153, 255, 0.6)', 'rgba(255, 183, 0, 0.6)',
        'rgba(59, 160, 160, 0.6)', 'rgba(108, 68, 187, 0.6)', 'rgba(105, 77, 49, 0.6)',
        'rgba(189, 0, 164, 0.6)', 'rgba(99, 88, 41, 0.6)', 'rgba(40, 159, 64, 0.6)',
        'rgba(210, 199, 199, 0.6)'
      ],
      borderWidth: 1
    }]
  },
  options: doughnutOptions
});

const langCount = gameLanguages.flatMap(i => i.split(","));
const lang = [...new Set(langCount)].sort((a, b) => langCount.filter(lc => lc === b).length - langCount.filter(lc => lc === a).length).slice(0, 10);

new Chart(document.getElementById("chart3"), {
  type: 'doughnut',
  data: {
    labels: lang,
    datasets: [{
      label: 'Game Tag (Per Game)',
      data: lang.map(l => langCount.filter(lc => lc === l).length),
      backgroundColor: [
        'rgba(255, 0, 55, 0.6)', 'rgba(0, 153, 255, 0.6)', 'rgba(255, 183, 0, 0.6)',
        'rgba(59, 160, 160, 0.6)', 'rgba(108, 68, 187, 0.6)', 'rgba(105, 77, 49, 0.6)',
        'rgba(189, 0, 164, 0.6)', 'rgba(99, 88, 41, 0.6)', 'rgba(40, 159, 64, 0.6)',
        'rgba(210, 199, 199, 0.6)'
      ],
      borderWidth: 1
    }]
  },
  options: doughnutOptions
});
