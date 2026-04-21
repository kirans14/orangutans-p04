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

async function loadUserTrends() {
    try {
        const response = await fetch('/api/user_data');
        if (!response.ok) {
            console.error("failed to fetch user data. status:", response.status);
            return;
        }
        const data = await response.json();
        if (data.error) {
            console.error("API Error:", data.error);
            return;
        }
        buildChart('mostPlayedChart', 'doughnut', data.genre_playtime.labels, data.genre_playtime.data, 'Playtime (Minutes)');
        buildChart('playtimeChart', 'bar', data.most_played.labels, data.most_played.data, 'Total Playtime (Minutes)');
        buildChart('reviewChart', 'pie', data.reviews.labels, data.reviews.data, 'Review Count');

        const topGamesContainer = document.getElementById('topGamesList');
        const limit = Math.min(5, data.most_played.labels.length);

        for (let i = 0; i < limit; i++) {
          const name = data.most_played.labels[i];
          const appId = data.most_played.app_ids[i];
          const gameLink = document.createElement('a');

          gameLink.href = `https://store.steampowered.com/app/${appId}/`;
          gameLink.target = "_blank";
          gameLink.className = "flex items-center gap-4 bg-[var(--steam-bg)] p-1 hover:bg-[var(--steam-bl)]";

          const gameImg = document.createElement('img');
          gameImg.src = `https://steamcdn-a.akamaihd.net/steam/apps/${appId}/header.jpg`;
          gameImg.alt = name;
          gameImg.className = "w-32 h-auto rounded shadow-sm object-cover";
          
          const nameSpan = document.createElement('span');
          nameSpan.className = "text-lg text-white";
          nameSpan.textContent = name;

          gameLink.appendChild(gameImg);
          gameLink.appendChild(nameSpan);
          topGamesContainer.appendChild(gameLink);
        }

        const topCategoriesContainer = document.getElementById('topCategoriesList');
        topCategoriesContainer.innerHTML = ''; 
        const limitCategories = Math.min(5, data.genre_playtime.labels.length);

        for (let i = 0; i < limitCategories; i++) {
            const tagName = data.genre_playtime.labels[i];
            const safeTagUrl = encodeURIComponent(tagName);

            const tagLink = document.createElement('a');
            tagLink.href = `https://store.steampowered.com/tags/en/${safeTagUrl}/`;
            tagLink.target = "_blank";
            tagLink.className = "flex items-center gap-4 bg-[var(--steam-bg)] px-4 py-2 hover:bg-white hover:text-[var(--steam-bg)] text-white";
            tagLink.textContent = tagName; 
            topCategoriesContainer.appendChild(tagLink);
        }

    } catch (error) {
        console.error("Error loading charts:", error);
    }
}

loadUserTrends();