/*
  Parses list items separated by commas into label : occurances
  for languages, genre
*/
function parseList(games, key, limit = 10) {
  if(typeof key !== 'string'){
    console.log("key needs to be a string!");
    return;
  }
  const items = games.flatMap(g => (g[key] || "")
    .split(',')
    .map(i => i.trim())
    .filter(Boolean)
    .map(item => ({ item, appid: g.appid })));
    
  const counts = items.reduce((result, {item, appid}) => {
    if (!result[item]) result[item] = { count: 0, ids: [] };
    result[item].count += 1;
    result[item].ids.push(appid);
    return result;
  }, {});

  const sorted = Object.entries(counts).sort((a,b) => b[1].count - a[1].count)
    .slice(0, limit);
  
  return {
    labels: sorted.map(i => i[0]),
    data: sorted.map(i => i[1].count),
    gameids: sorted.map(i => i[1].ids)
  };
}
/*
  Parses dictionary key into key : key count
  for tags
*/
function parseDictKey(games, key, limit) {
  if(typeof key !== 'string'){
    console.log("key needs to be a string!");
    return;
  }
  const items = games.flatMap(g => Object.keys(g[key] || {})
    .map(item => ({ item, appid: g.appid })));
    
  const counts = items.reduce((result, {item, appid}) => {
    if (!result[item]) result[item] = { count: 0, ids: [] };
    result[item].count += 1;
    result[item].ids.push(appid);
    return result;
  }, {});

  const sorted = Object.entries(counts).sort((a,b) => b[1].count - a[1].count)
    .slice(0, limit);
  
  return {
    labels: sorted.map(i => i[0]),
    data: sorted.map(i => i[1].count),
    gameids: sorted.map(i => i[1].ids)
  };
}

/*
  Parses direct integer comparisons per game into game : metric
  ccu, positive, average_forever
*/
function parseRanked(games, metric, limit = 10) {
  if(typeof metric !== 'string'){
    console.log("metric needs to be a string!");
    return;
  }
  const sorted = [...games]
    .sort((a, b) => (b[metric] || 0) - (a[metric] || 0)).slice(0, limit);
  return { 
    labels: sorted.map(g => g.name), 
    data: sorted.map(g => g[metric]),
    gameids: sorted.map(g => g.appid) 
  };
}

function renderRankedChart(metric, labelName) {
  const chartData = parseRanked(gamesArray, metric, 30);
  const canvasId = 'rankedChart';
  
  const existingChart = Chart.getChart(canvasId);
  if (existingChart) {
    existingChart.destroy();
  }

  buildChart(canvasId, 'bar', chartData.labels, chartData.data, labelName);
}

const steamTheme = {
  doughnut: {
    colors: [
      'rgba(255, 0, 55, 0.6)', 'rgba(0, 153, 255, 0.6)', 'rgba(255, 183, 0, 0.6)',
      'rgba(59, 160, 160, 0.6)', 'rgba(108, 68, 187, 0.6)', 'rgba(105, 77, 49, 0.6)',
      'rgba(189, 0, 164, 0.6)', 'rgba(99, 88, 41, 0.6)', 'rgba(40, 159, 64, 0.6)',
      'rgba(210, 199, 199, 0.6)'
    ],
    options: {
      maintainAspectRatio: false,
      elements: { arc: { borderColor: 'rgba(0, 0, 0, 0.6)', borderWidth: 12 } },
      plugins: { legend: { labels: { color: 'white', font: { weight: 'bold' } } } }
    }
  },
  pie: {
    colors: [
      'rgba(255, 0, 55, 0.6)', 'rgba(0, 153, 255, 0.6)', 'rgba(255, 183, 0, 0.6)',
      'rgba(59, 160, 160, 0.6)', 'rgba(108, 68, 187, 0.6)', 'rgba(105, 77, 49, 0.6)',
      'rgba(189, 0, 164, 0.6)', 'rgba(99, 88, 41, 0.6)', 'rgba(40, 159, 64, 0.6)',
      'rgba(210, 199, 199, 0.6)'
    ],
    options: {
      maintainAspectRatio: false,
      elements: { arc: { borderColor: 'rgba(0, 0, 0, 0.6)', borderWidth: 4 } },
      plugins: { legend: { labels: { color: 'white' } } }
    }
  },
  bar: {
    colors: 'rgba(54, 162, 235, 0.6)',
    borderColor: 'rgba(54, 162, 235, 1)',
    options: {
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
        x: { ticks: { color: 'white' }, grid: { display: false } }
      },
      plugins: { legend: { labels: { color: 'white' } } }
    }
  },
  line: {
    colors: 'rgba(54, 162, 235, 0.2)',
    borderColor: 'rgba(54, 162, 235, 1)',
    options: {
      maintainAspectRatio: false,
      elements: { line: { tension: 0.4, borderWidth: 2 }, point: { radius: 4, backgroundColor: 'rgba(54, 162, 235, 1)' } },
      scales: {
        y: { beginAtZero: true, ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
        x: { ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } }
      },
      plugins: { legend: { labels: { color: 'white' } } }
    }
  },
  radar: {
    colors: 'rgba(54, 162, 235, 0.4)',
    borderColor: 'rgba(54, 162, 235, 1)',
    options: {
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
          grid: { color: 'rgba(255, 255, 255, 0.1)' },
          pointLabels: { color: 'white' },
          ticks: { backdropColor: 'transparent', color: 'white' }
        }
      },
      plugins: { legend: { labels: { color: 'white' } } }
    }
  },
  polarArea: {
    colors: [
      'rgba(255, 0, 55, 0.6)', 'rgba(0, 153, 255, 0.6)', 'rgba(255, 183, 0, 0.6)',
      'rgba(59, 160, 160, 0.6)', 'rgba(108, 68, 187, 0.6)'
    ],
    options: {
      maintainAspectRatio: false,
      scales: {
        r: {
          grid: { color: 'rgba(255, 255, 255, 0.1)' },
          ticks: { backdropColor: 'transparent', color: 'white' }
        }
      },
      plugins: { legend: { labels: { color: 'white' } } }
    }
  },
  scatter: {
    colors: 'rgba(54, 162, 235, 0.8)',
    borderColor: 'rgba(54, 162, 235, 1)',
    options: {
      maintainAspectRatio: false,
      scales: {
        y: { ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
        x: { ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } }
      },
      plugins: { legend: { labels: { color: 'white' } } }
    }
  },
  bubble: {
    colors: 'rgba(54, 162, 235, 0.6)',
    borderColor: 'rgba(54, 162, 235, 1)',
    options: {
      maintainAspectRatio: false,
      scales: {
        y: { ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } },
        x: { ticks: { color: 'white' }, grid: { color: 'rgba(255, 255, 255, 0.1)' } }
      },
      plugins: { legend: { labels: { color: 'white' } } }
    }
  },
  default: {
    colors: 'rgba(54, 162, 235, 0.6)',
    options: { maintainAspectRatio: false }
  }
};

function buildChart(canvasId, type, labels, data, datasetLabel) {
  const theme = steamTheme[type] || steamTheme.default;

  return new Chart(document.getElementById(canvasId), {
    type: type,
    data: {
      labels: labels,
      datasets: [{
        label: datasetLabel,
        data: data,
        backgroundColor: theme.colors,
        borderColor: theme.borderColor || theme.colors,
        borderWidth: 1
      }]
    },
    options: theme.options
  });
}

const gamesArray = Object.values(steamData);

const tagData = parseDictKey(gamesArray, 'tags', 10);
const reviewData = parseRanked(gamesArray, 'positive', 30);
const languagesData = parseList(gamesArray, 'languages', 10);


// console.log(tagData);
// console.log(reviewData);
// console.log(languagesData);

buildChart('chart2', 'doughnut', tagData.labels, tagData.data, 'Number of Games containing (User Defined)');
// buildChart('chart', 'bar', reviewData.labels, reviewData.data, 'Number of Positive Reviews');
buildChart('chart3', 'doughnut', languagesData.labels, languagesData.data, 'Number of Games Supporting')

const metricSelector = document.getElementById('metricSelector');
renderRankedChart('positive', 'Positive Reviews');
metricSelector.addEventListener('change', (e) => {
  const selectedMetric = e.target.value;
  const selectedLabel = e.target.options[e.target.selectedIndex].text;
  
  renderRankedChart(selectedMetric, selectedLabel);
});

// Barebones recommendation system
const mostEngaging = [...gamesArray].sort((a, b) => b.positive - a.positive).slice(0,500);
const randomTopGame = mostEngaging[Math.floor(Math.random() * mostEngaging.length)];

const titleElement = document.getElementById("mostEngagingTitle");
titleElement.href = `https://store.steampowered.com/app/${randomTopGame.appid}/`;
titleElement.innerText = `Looking for a game to play? Have you tried ${randomTopGame.name} yet?`;

const titleImgElement = document.getElementById("mostEngagingImg");
titleImgElement.src = `https://steamcdn-a.akamaihd.net/steam/apps/${randomTopGame.appid}/header.jpg`






