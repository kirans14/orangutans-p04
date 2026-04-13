
const gamesArray = Object.values(steamData);
const gameNames = gamesArray.map(game => game.name);
const gameTags = gamesArray.map(game => Object.keys(game.tags).slice(0,5));
const gameLanguages = gamesArray.map(game => game.languages);


const text = document.getElementById("tester");
text.innerText = JSON.stringify(gameLanguages);

const ctx = document.getElementById('chart');
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
      label: '# of Votes',
      data: [12, 19, 3, 5, 2, 3],
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

var tagCount = gameTags.flat();
var tag = [...new Set(tagCount)]; // set slice to reduce amount
const rtx = document.getElementById('chart2');

const tagData = {
  labels: tag,
  datasets: [{
    label: 'Count',
    data: tag.map(t => tagCount.filter(tc => tc === t).length),
    fill: true,
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
  }]
};
const tagConfig = {
  type: 'radar',
  data: tagData,
  options: {
    elements: {
      line: {
        borderWidth: 6
      }
    },
    scales:{
      r:{
        pointLabels:{
          padding:20
        }
      }
    }
  },
};

new Chart(rtx, tagConfig);


var langCount = gameLanguages;
var lang = [...new Set(langCount)];
const rtx2 = document.getElementById("chart3");

const langData = {
  labels: language,
  datasets: [{
    label: 'Count',
    data: lang.map(l => langCount.filter(lc => lc == l).length),
    fill: true,
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
  }]
};
const langConfig = {
  type: 'radar',
  data: langData,
  options: {
    elements: {
      line: {
        borderWidth: 6
      }
    },
    scales:{
      r:{
        pointLabels:{
          padding:20
        }
      }
    }
  },
};

new Chart(rtx2, langConfig);