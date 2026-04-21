
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


async function fetchAndRenderChart(url, canvasId, chartType, labelName) {
  try {
    // init and cleanups
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const chartData = await response.json();
    if (chartData.error) {
        console.error("Backend error:", chartData.error);
        return;
    }
    const existingChart = Chart.getChart(canvasId);
    if (existingChart) {
      existingChart.destroy();
    }

    // Pass formatted data to buildChart
    buildChart(canvasId, chartType, chartData.labels, chartData.data, labelName);
  } catch (error) {
    console.error(`Error loading data for ${canvasId}:`, error);
  }
}

async function loadRecommendation() {
  try {
    const res = await fetch('/api/homepage_recommendation');
    const randomTopGame = await res.json();

    if (randomTopGame && randomTopGame.app_id) {
      const titleElement = document.getElementById("mostEngagingTitle");
      titleElement.href = `https://store.steampowered.com/app/${randomTopGame.app_id}/`;
      titleElement.innerText = `Have you tried ${randomTopGame.name} yet?`;

      const titleImgElement = document.getElementById("mostEngagingImg");
      titleImgElement.src = `https://steamcdn-a.akamaihd.net/steam/apps/${randomTopGame.app_id}/header.jpg`;
    }
  } catch (error) {
    console.error("Error loading recommendation:", error);
  }
}

fetchAndRenderChart('/api/counts/tag_list/10', 'chart2', 'doughnut', 'Top 10 Tags');
fetchAndRenderChart('/api/counts/genre_list/10', 'chart3', 'doughnut', 'Top 10 Genres');
fetchAndRenderChart('/api/ranked/total_positive/25', 'rankedChart', 'bar', 'Positive Reviews');
loadRecommendation();

const metricSelector = document.getElementById('metricSelector');
if (metricSelector) {
  metricSelector.addEventListener('change', (e) => {
    const selectedMetric = e.target.value;
    const selectedLabel = e.target.options[e.target.selectedIndex].text
    fetchAndRenderChart(`/api/ranked/${selectedMetric}/25`, 'rankedChart', 'bar', selectedLabel);
  });
}


