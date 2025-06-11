let data = [];

async function loadData() {
  try {
    const response = await fetch("http://16.171.16.170:8000/backtest_results");
    if (!response.ok) throw new Error("Network response was not ok");
    data = await response.json();
    populateFilters(data);
    updateView();
  } catch (error) {
    console.error("Failed to load data:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadData();
  document.querySelectorAll("select, input").forEach(el => {
    el.addEventListener("change", updateView);
  });
});

function populateFilters(data) {
  const uniquePairs = [...new Set(data.map(row => row.pair))];
  const uniqueStrategies = [...new Set(data.map(row => row.strategy_class))];
  const uniquePeriods = [...new Set(data.map(row => row.period))];

  const addOptions = (id, values) => {
    const select = document.getElementById(id);
    values.forEach(val => {
      const opt = document.createElement("option");
      opt.value = val;
      opt.textContent = val;
      select.appendChild(opt);
    });
  };

  addOptions("filter_pair", uniquePairs);
  addOptions("filter_strategy", uniqueStrategies);
  addOptions("filter_period", uniquePeriods);
}

function filterData() {
  const pair = document.getElementById("filter_pair").value;
  const strategy = document.getElementById("filter_strategy").value;
  const period = document.getElementById("filter_period").value;
  const date = document.getElementById("filter_date").value;

  return data.filter(row => {
    return (!pair || row.pair === pair) &&
           (!strategy || row.strategy_class === strategy) &&
           (!period || row.period === period) &&
           (!date || new Date(row.created_at).toISOString().slice(0,10) === date);
  });
}

function renderCharts(filteredData) {
  const x = filteredData.map(d => d.test_id);
  const returnPercent = filteredData.map(d => d.return_percent);
  const sharpe = filteredData.map(d => d.sharpe_ratio);
  const winRate = filteredData.map(d => d.win_rate);

  const layout = { title: "Performance Comparison", barmode: "group" };
  const trace1 = { x, y: returnPercent, name: 'Return %', type: 'bar' };
  const trace2 = { x, y: sharpe, name: 'Sharpe Ratio', type: 'bar' };
  const trace3 = { x, y: winRate, name: 'Win Rate', type: 'bar' };

  Plotly.newPlot('chart_div', [trace1, trace2, trace3], layout);
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
      { title: "Average", data: "average_trade" }
    ],
    pageLength: 10
  });
}

function updateView() {
  const filtered = filterData();
  renderCharts(filtered);
  renderTable(filtered);
}

document.addEventListener("DOMContentLoaded", () => {
  populateFilters(data);
  updateView();

  document.querySelectorAll("select, input").forEach(el => {
    el.addEventListener("change", updateView);
  });
});
