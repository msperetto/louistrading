let data = [];

async function loadData() {
  try {
    const response = await fetch("http://16.171.16.170:8000/backtests");
    if (!response.ok) throw new Error("Network response was not ok");
    data = await response.json();
    console.log("Loaded data:", data);
    populateFilters(data);
    updateDashboard();
  } catch (error) {
    console.error("Failed to load data:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadData();
  document.querySelectorAll("#filter_pair, #filter_start, #filter_end, #filter_metric").forEach(el => {
    el.addEventListener("change", updateDashboard);
  });
});

function populateFilters(data) {
  const uniquePairs = [...new Set(data.map(row => row.pair))];
  const pairSelect = document.getElementById("filter_pair");
  uniquePairs.forEach(val => {
    const opt = document.createElement("option");
    opt.value = val;
    opt.textContent = val;
    pairSelect.appendChild(opt);
  });
}

function filterData() {
  const pair = document.getElementById("filter_pair").value;
  const start = document.getElementById("filter_start").value;
  const end = document.getElementById("filter_end").value;

  return data.filter(row => {
    const rowDate = row.created_at.slice(0, 10);
    return (!pair || row.pair === pair) &&
           (!start || rowDate >= start) &&
           (!end || rowDate <= end);
  });
}

function updateDashboard() {
  const filtered = filterData();
  renderBubbleChart(filtered);
  renderTop10List(filtered);
  renderBarChart(filtered);
  renderLineChart(filtered);
  renderTable(filtered);
}

function renderBubbleChart(filteredData) {
  const trace = {
    x: filteredData.map(d => d.return_percent),
    y: filteredData.map(d => d.win_rate),
    text: filteredData.map(d => `
      <b>Test ID:</b> ${d.test_id}<br>
      <b>Pair:</b> ${d.pair}<br>
      <b>Period:</b> ${d.period}<br>
      <b>Strategy:</b> ${d.strategy_class}<br>
      <b>Return %:</b> ${d.return_percent}<br>
      <b>Win Rate:</b> ${d.win_rate}<br>
      <b>Sharpe Ratio:</b> ${d.sharpe_ratio}<br>
      <b>Profit Factor:</b> ${d.profit_factor}<br>
      <b>Max DD:</b> ${d.max_drawdown}<br>
      <b>Total Trades:</b> ${d.total_trades}
    `),
    mode: 'markers',
    marker: {
      size: filteredData.map(d => Math.max(10, Math.abs(d.return_percent))),
      sizemode: 'area',
      sizeref: 2.0 * Math.max(...filteredData.map(d => Math.abs(d.return_percent))) / (100**2),
      color: filteredData.map(d => d.sharpe_ratio),
      colorscale: 'Viridis',
      showscale: true,
      colorbar: { title: "Sharpe Ratio" }
    },
    hoverinfo: 'text'
  };
  const layout = {
    xaxis: { title: "Return %" },
    yaxis: { title: "Win Rate" },
    title: "",
    height: 400,
    margin: { t: 30 }
  };
  Plotly.newPlot('bubble_chart', [trace], layout, {responsive: true});
}

function renderTop10List(filteredData) {
  const metric = document.getElementById("filter_metric").value;
  const top10 = [...filteredData]
    .sort((a, b) => (metric === "max_drawdown" ? a[metric] - b[metric] : b[metric] - a[metric]))
    .slice(0, 10);

  const ul = document.getElementById("top10_list");
  ul.innerHTML = "";
  top10.forEach((d, i) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <b>${d.strategy_class}</b> (${d.pair}, ${d.period})<br>
      <span class="text-xs">Return: <b>${d.return_percent}</b> | Sharpe: <b>${d.sharpe_ratio}</b> | Win Rate: <b>${d.win_rate}</b> | PF: <b>${d.profit_factor}</b> | Max DD: <b>${d.max_drawdown}</b></span>
    `;
    ul.appendChild(li);
  });
}

function renderBarChart(filteredData) {
  const metric = document.getElementById("filter_metric").value;
  const sorted = [...filteredData].sort((a, b) => (metric === "max_drawdown" ? a[metric] - b[metric] : b[metric] - a[metric]));
  const trace = {
    x: sorted.map(d => d.strategy_class + " (" + d.pair + ")"),
    y: sorted.map(d => d[metric]),
    text: sorted.map(d => `Test ID: ${d.test_id}<br>Return: ${d.return_percent}<br>Sharpe: ${d.sharpe_ratio}<br>Win Rate: ${d.win_rate}`),
    type: 'bar',
    marker: { color: 'rgba(37,99,235,0.7)' },
    hoverinfo: 'text'
  };
  const layout = {
    xaxis: { title: "Strategy (Pair)", tickangle: -45, automargin: true },
    yaxis: { title: metric.replace("_", " ").toUpperCase() },
    height: 400,
    margin: { t: 30, b: 120 }
  };
  Plotly.newPlot('bar_chart', [trace], layout, {responsive: true});
}

function renderLineChart(filteredData) {
  // Optional: Return % over time for the filtered set
  const sorted = [...filteredData].sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
  const trace = {
    x: sorted.map(d => d.created_at),
    y: sorted.map(d => d.return_percent),
    mode: 'lines+markers',
    text: sorted.map(d => `Test ID: ${d.test_id}<br>Return: ${d.return_percent}`),
    line: { color: 'rgba(16,185,129,1)', width: 2 },
    marker: { size: 6 },
    hoverinfo: 'text'
  };
  const layout = {
    xaxis: { title: "Created At" },
    yaxis: { title: "Return %" },
    height: 400,
    margin: { t: 30 }
  };
  Plotly.newPlot('line_chart', [trace], layout, {responsive: true});
}

function renderTable(filteredData) {
  if ($.fn.dataTable.isDataTable('#results_table')) {
    $('#results_table').DataTable().clear().rows.add(filteredData).draw();
    return;
  }
  $('#results_table').DataTable({
    data: filteredData,
    columns: [
      { title: "Test ID", data: "test_id" },
      { title: "Pair", data: "pair" },
      { title: "Period", data: "period" },
      { title: "Strategy", data: "strategy_class" },
      { title: "Return %", data: "return_percent" },
      { title: "Buy & Hold", data: "return_buy_hold" },
      { title: "Sharpe", data: "sharpe_ratio" },
      { title: "Win Rate", data: "win_rate" },
      { title: "Profit Factor", data: "profit_factor" },
      { title: "Max DD", data: "max_drawdown" },
      { title: "Best", data: "best_trade" },
      { title: "Worst", data: "worst_trade" },
      { title: "Average", data: "average_trade" },
      { title: "Total Trades", data: "total_trades" },
      { title: "Start", data: "start_time" },
      { title: "End", data: "end_time" },
      { title: "Indicators", data: "best_indicators_combination" },
      { title: "Trend", data: "trend_class" }
    ],
    pageLength: 10,
    destroy: true
  });
}