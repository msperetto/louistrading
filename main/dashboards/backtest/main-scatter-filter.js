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
  renderSharpeRatioBarChart(filtered);
  renderSharpeRatioBoxPlot(filtered);
  renderSharpeRatioHistogram(filtered);
  renderMaxDDBarChart(filtered);
  renderTop10List(filtered);
  renderBarChart(filtered);
  renderLineChart(filtered);
  renderTable(filtered);
  renderStrategyPerformanceOverview(filtered);
  renderEquityCurve(filtered);
  renderSharpeVsDrawdown(filtered);
  renderReturnsDistribution(filtered);
  renderPerformanceByPeriod(filtered);
  renderTrendAnalysis(filtered);
  renderBuyConditionAnalysis(filtered);
  renderMonthlyYearlyReturns(filtered);
  renderTradeDurationAnalysis(filtered);
  renderProfitFactorOverTime(filtered);
  renderCorrelationMatrix(filtered);
  renderCumulativeReturnVsBuyHold(filtered);
}


// Helper to update charts based on selection
function updateChartsWithSelection(selectedData) {
  renderSharpeRatioBarChart(selectedData);
  renderSharpeRatioBoxPlot(selectedData);
  renderSharpeRatioHistogram(selectedData);
  renderMaxDDBarChart(selectedData);
  renderTop10List(selectedData);
  renderBarChart(selectedData);
  renderLineChart(selectedData);
  renderTable(selectedData);
  renderStrategyPerformanceOverview(selectedData);
  renderEquityCurve(selectedData);
  renderSharpeVsDrawdown(selectedData);
  renderReturnsDistribution(selectedData);
  renderPerformanceByPeriod(selectedData);
  renderTrendAnalysis(selectedData);
  renderBuyConditionAnalysis(selectedData);
  renderMonthlyYearlyReturns(selectedData);
  renderTradeDurationAnalysis(selectedData);
  renderProfitFactorOverTime(selectedData);
  renderCorrelationMatrix(selectedData);
  renderCumulativeReturnVsBuyHold(selectedData);
}

let bubbleChartInitialized = false;

function renderBubbleChart(filteredData) {
  const maxReturn = Math.max(...filteredData.map(d => Math.abs(d.return_percent)), 1);
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
      size: filteredData.map(d => Math.max(6, Math.abs(d.return_percent))), // smaller minimum
      sizemode: 'area',
      sizeref: 4.0 * maxReturn / (70**2), // increase divisor for smaller bubbles
      opacity: 0.5, // more transparent
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
    margin: { t: 30 },
    dragmode: 'lasso'
  };
  Plotly.newPlot('bubble_chart', [trace], layout, {responsive: true});

  // using this if to only attach event listeners once, so we can reset the chart with
  // double click
  if (!bubbleChartInitialized) {
    const bubbleDiv = document.getElementById("bubble_chart");
    bubbleDiv.on('plotly_selected', (eventData) => {
      if (!eventData || !eventData.points || eventData.points.length === 0) {
        // If no points are selected, reset to all filteredData
        updateChartsWithSelection(filteredData);
        return;
      }

      // Extract selected points and update charts
      const selectedIndices = eventData.points.map(p => p.pointIndex);
      const selectedData = selectedIndices.map(i => filteredData[i]);
      updateChartsWithSelection(selectedData);
    });

    bubbleDiv.on('plotly_deselect', () => {
      // Reset to all filteredData when deselected
      updateChartsWithSelection(filteredData);
    });

    bubbleChartInitialized = true;
  }
}

function renderSharpeRatioBarChart(filteredData) {
  if (!filteredData || filteredData.length === 0) {
    Plotly.purge('sharpe_ratio_bar_chart');
    return;
  }
  // sort by sharpe_ratio ascending
  const sorted = [...filteredData].sort((a, b) => a.sharpe_ratio - b.sharpe_ratio);

  const trace = {
    x: sorted.map(d => String(d.test_id)),
    y: sorted.map(d => d.sharpe_ratio),
    text: sorted.map(d => `Sharpe: ${d.sharpe_ratio}<br>Testid: ${d.test_id}`),
    type: 'bar',
    marker: { color: 'rgba(16,185,129,0.7)' },
    hoverinfo: 'text'
  };
  const layout = {
    title: "Sharpe Ratio - per Test",
    xaxis: { title: "Test ID", type: "category", tickangle: -45, automargin: true },
    yaxis: { title: "Sharpe Ratio" },
    height: 400,
    margin: { t: 30, b: 120 }
  };
  Plotly.newPlot('sharpe_ratio_bar_chart', [trace], layout, {responsive: true});
}

function renderSharpeRatioHistogram(filteredData) {
  if (!filteredData || filteredData.length === 0) {
    Plotly.purge('sharpe_ratio_histogram');
    return;
  }
  const trace = {
    x: filteredData.map(d => d.sharpe_ratio),
    type: 'histogram',
    marker: { color: 'rgba(16,185,129,0.7)' }
  };
  const layout = {
    title: "Sharpe Ratio Distribution",
    xaxis: { title: "Sharpe Ratio" },
    yaxis: { title: "Frequency" },
    height: 400,
    margin: { t: 30 }
  };
  Plotly.newPlot('sharpe_ratio_histogram', [trace], layout, {responsive: true});
}

function renderSharpeRatioBoxPlot(filteredData) {
  if (!filteredData || filteredData.length === 0) {
    Plotly.purge('sharpe_ratio_boxplot');
    return;
  }
  const strategies = [...new Set(filteredData.map(d => d.strategy_class))];
  const traces = strategies.map(s => ({
    y: filteredData.filter(d => d.strategy_class === s).map(d => d.sharpe_ratio),
    type: 'box',
    name: s
  }));
  const layout = {
    title: "Sharpe Ratio by Strategy",
    yaxis: { title: "Sharpe Ratio" },
    height: 400,
    margin: { t: 30 }
  };
  Plotly.newPlot('sharpe_ratio_boxplot', traces, layout, {responsive: true});
}


function renderMaxDDBarChart(filteredData) {
  if (!filteredData || filteredData.length === 0) {
    Plotly.purge('max_dd_bar_chart');
    return;
  }

  // Sort by max_drawdown ascending
  const sorted = [...filteredData].sort((a, b) => a.max_drawdown - b.max_drawdown);
  const trace = {
    x: sorted.map(d => String(d.test_id)),
    y: sorted.map(d => d.max_drawdown),
    text: sorted.map(d => `Max DD: ${d.max_drawdown}`),
    type: 'bar',
    marker: { color: 'rgba(16,185,129,0.7)' },
    hoverinfo: 'text'
  };
  const layout = {
    title: "Maximum Drawdown per Test",
    xaxis: { title: "Test ID", type:"category", tickangle: -45, automargin: true },
    yaxis: { title: "Max DD" },
    height: 400,
    margin: { t: 30, b: 120 }
  };
  Plotly.newPlot('max_dd_bar_chart', [trace], layout, {responsive: true});
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

// Strategy Performance Overview (Aggregated Table)
function renderStrategyPerformanceOverview(filteredData) {
  // Group by strategy_name and aggregate metrics
  const grouped = {};
  filteredData.forEach(d => {
    const key = d.strategy_class;
    if (!grouped[key]) {
      grouped[key] = { count: 0, sum_return: 0, sum_win: 0, sum_sharpe: 0, sum_drawdown: 0, sum_trades: 0, sum_pf: 0 };
    }
    grouped[key].count += 1;
    grouped[key].sum_return += d.return_percent;
    grouped[key].sum_win += d.win_rate;
    grouped[key].sum_sharpe += d.sharpe_ratio;
    grouped[key].sum_drawdown += d.max_drawdown;
    grouped[key].sum_trades += d.total_trades;
    grouped[key].sum_pf += d.profit_factor;
  });
  const tableData = Object.entries(grouped).map(([strategy, vals]) => ({
    strategy,
    avg_return: (vals.sum_return / vals.count).toFixed(2),
    avg_win_rate: (vals.sum_win / vals.count).toFixed(2),
    avg_sharpe: (vals.sum_sharpe / vals.count).toFixed(2),
    avg_drawdown: (vals.sum_drawdown / vals.count).toFixed(2),
    total_trades: vals.sum_trades,
    avg_profit_factor: (vals.sum_pf / vals.count).toFixed(2)
  }));
  $('#strategy_performance_table').DataTable({
    data: tableData,
    columns: [
      { title: "Strategy", data: "strategy" },
      { title: "Average Return %", data: "avg_return" },
      { title: "Win Rate", data: "avg_win_rate" },
      { title: "Sharpe Ratio", data: "avg_sharpe" },
      { title: "Max Drawdown", data: "avg_drawdown" },
      { title: "Total Trades", data: "total_trades" },
      { title: "Profit Factor", data: "avg_profit_factor" }
    ],
    destroy: true
  });
}

// Equity Curve (Line Chart)
function renderEquityCurve(filteredData) {
  // Group by strategy, calculate cumulative return
  const strategies = [...new Set(filteredData.map(d => d.strategy_class))];
  const traces = strategies.map(strategy => {
    const stratData = filteredData.filter(d => d.strategy_class === strategy)
      .sort((a, b) => new Date(a.end_time) - new Date(b.end_time));
    let cumReturn = 0;
    const x = [], y = [];
    stratData.forEach(d => {
      cumReturn += d.return_percent;
      x.push(d.end_time);
      y.push(cumReturn);
    });
    return {
      x, y, mode: 'lines+markers', name: strategy
    };
  });
  Plotly.newPlot('equity_curve_chart', traces, {
    title: "Equity Curve",
    xaxis: { title: "Time" },
    yaxis: { title: "Cumulative Return (%)" }
  }, {responsive: true});
}

// Sharpe Ratio vs. Max Drawdown (Scatter Plot)
function renderSharpeVsDrawdown(filteredData) {
  const strategies = [...new Set(filteredData.map(d => d.strategy_class))];
  const trace = {
    x: strategies.map(s => {
      const strat = filteredData.filter(d => d.strategy_class === s);
      return strat.reduce((a, b) => a + b.max_drawdown, 0) / strat.length;
    }),
    y: strategies.map(s => {
      const strat = filteredData.filter(d => d.strategy_class === s);
      return strat.reduce((a, b) => a + b.sharpe_ratio, 0) / strat.length;
    }),
    text: strategies,
    mode: 'markers',
    marker: {
      size: strategies.map(s => {
        const strat = filteredData.filter(d => d.strategy_class === s);
        return strat.reduce((a, b) => a + b.total_trades, 0) / strat.length;
      }),
      color: 'rgba(37,99,235,0.7)',
      opacity: 0.7
    }
  };
  Plotly.newPlot('sharpe_drawdown_chart', [trace], {
    title: "Risk-Return Profile: Sharpe Ratio vs. Max Drawdown",
    xaxis: { title: "Maximum Drawdown (%)" },
    yaxis: { title: "Sharpe Ratio" }
  }, {responsive: true});
}

// Returns Distribution (Histogram & Box Plot)
function renderReturnsDistribution(filteredData) {
  // Histogram
  const traceHist = {
    x: filteredData.map(d => d.return_percent),
    type: 'histogram',
    marker: { color: 'rgba(16,185,129,0.7)' }
  };
  Plotly.newPlot('returns_histogram', [traceHist], {
    title: "Distribution of Trade Returns",
    xaxis: { title: "Return (%)" },
    yaxis: { title: "Frequency" }
  }, {responsive: true});
  // Box Plot by strategy
  const strategies = [...new Set(filteredData.map(d => d.strategy_class))];
  const tracesBox = strategies.map(s => ({
    y: filteredData.filter(d => d.strategy_class === s).map(d => d.return_percent),
    type: 'box',
    name: s
  }));
  Plotly.newPlot('returns_boxplot', tracesBox, {
    title: "Return Distribution by Strategy",
    yaxis: { title: "Return (%)" }
  }, {responsive: true});
}

// Performance by Period (Bar Chart)
function renderPerformanceByPeriod(filteredData) {
  const periods = [...new Set(filteredData.map(d => d.label_period))];
  const strategies = [...new Set(filteredData.map(d => d.strategy_class))];
  const traces = strategies.map(s => ({
    x: periods,
    y: periods.map(p => {
      const vals = filteredData.filter(d => d.label_period === p && d.strategy_class === s);
      return vals.length ? vals.reduce((a, b) => a + b.return_percent, 0) / vals.length : 0;
    }),
    name: s,
    type: 'bar'
  }));
  Plotly.newPlot('performance_period_chart', traces, {
    title: "Strategy Performance by Time Period",
    xaxis: { title: "Period" },
    yaxis: { title: "Average Return (%)" }
  }, {responsive: true});
}

// Trend Analysis (Grouped Bar Chart)
function renderTrendAnalysis(filteredData) {
  const trends = [...new Set(filteredData.map(d => d.trend_class))];
  const strategies = [...new Set(filteredData.map(d => d.strategy_class))];
  const traces = strategies.map(s => ({
    x: trends,
    y: trends.map(t => {
      const vals = filteredData.filter(d => d.trend_class === t && d.strategy_class === s);
      return vals.length ? vals.reduce((a, b) => a + b.return_percent, 0) / vals.length : 0;
    }),
    name: s,
    type: 'bar'
  }));
  Plotly.newPlot('trend_analysis_chart', traces, {
    title: "Performance in Different Market Trends",
    xaxis: { title: "Market Trend" },
    yaxis: { title: "Average Return (%)" }
  }, {responsive: true});
}

// Buy/Sell Condition Analysis (Sunburst)
function renderBuyConditionAnalysis(filteredData) {
  // Example: Use filter_buy and trigger_buy as hierarchy
  const sunburstData = filteredData.map(d => ({
    ids: `${d.filter_buy}-${d.trigger_buy}`,
    labels: [d.filter_buy, d.trigger_buy],
    parents: ["", d.filter_buy],
    values: [d.return_percent, d.return_percent]
  }));
  const trace = {
    type: "sunburst",
    ids: sunburstData.map(d => d.ids),
    labels: sunburstData.map(d => d.labels[1]),
    parents: sunburstData.map(d => d.parents[1]),
    values: sunburstData.map(d => d.values[1]),
    branchvalues: "total"
  };
  Plotly.newPlot('buy_condition_chart', [trace], {
    title: "Buy Condition Performance",
  }, {responsive: true});
}

// Monthly/Yearly Returns (Heatmap)
function renderMonthlyYearlyReturns(filteredData) {
  // Group by year/month
  const months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
  const years = [...new Set(filteredData.map(d => new Date(d.end_time).getFullYear()))].sort();
  const z = years.map(y =>
    months.map((m, i) => {
      const vals = filteredData.filter(d => {
        const date = new Date(d.end_time);
        return date.getFullYear() === y && date.getMonth() === i;
      });
      return vals.length ? vals.reduce((a, b) => a + b.return_percent, 0) / vals.length : 0;
    })
  );
  Plotly.newPlot('monthly_yearly_chart', [{
    z, x: months, y: years, type: 'heatmap', colorscale: 'Viridis'
  }], {
    title: "Monthly Returns",
    xaxis: { title: "Month" },
    yaxis: { title: "Year" }
  }, {responsive: true});
}

// Trade Duration Analysis (Scatter Plot)
function renderTradeDurationAnalysis(filteredData) {
  const trace = {
    x: filteredData.map(d => {
      const start = new Date(d.start_time);
      const end = new Date(d.end_time);
      return (end - start) / (1000*60*60); // duration in hours
    }),
    y: filteredData.map(d => d.return_percent),
    text: filteredData.map(d => `Win Rate: ${d.win_rate}`),
    mode: 'markers',
    marker: { color: filteredData.map(d => d.win_rate), colorscale: 'Viridis', size: 8, opacity: 0.7 }
  };
  Plotly.newPlot('trade_duration_chart', [trace], {
    title: "Trade Duration vs. Return",
    xaxis: { title: "Trade Duration (hours)" },
    yaxis: { title: "Return (%)" }
  }, {responsive: true});
}

// Profit Factor Over Time (Line Chart)
function renderProfitFactorOverTime(filteredData) {
  const strategies = [...new Set(filteredData.map(d => d.strategy_class))];
  const traces = strategies.map(s => {
    const stratData = filteredData.filter(d => d.strategy_class === s)
      .sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
    return {
      x: stratData.map(d => d.created_at),
      y: stratData.map(d => d.profit_factor),
      mode: 'lines+markers',
      name: s
    };
  });
  Plotly.newPlot('profit_factor_chart', traces, {
    title: "Rolling Profit Factor",
    xaxis: { title: "Time" },
    yaxis: { title: "Profit Factor" }
  }, {responsive: true});
}

// Correlation Matrix (Heatmap)
function renderCorrelationMatrix(filteredData) {
  const strategies = [...new Set(filteredData.map(d => d.strategy_class))];
  // Build matrix
  const matrix = strategies.map(s1 =>
    strategies.map(s2 => {
      const vals1 = filteredData.filter(d => d.strategy_class === s1).map(d => d.return_percent);
      const vals2 = filteredData.filter(d => d.strategy_class === s2).map(d => d.return_percent);
      if (vals1.length && vals2.length) {
        // Pearson correlation
        const mean1 = vals1.reduce((a, b) => a + b, 0) / vals1.length;
        const mean2 = vals2.reduce((a, b) => a + b, 0) / vals2.length;
        const num = vals1.map((v, i) => (v - mean1) * (vals2[i % vals2.length] - mean2)).reduce((a, b) => a + b, 0);
        const den = Math.sqrt(
          vals1.map(v => (v - mean1) ** 2).reduce((a, b) => a + b, 0) *
          vals2.map(v => (v - mean2) ** 2).reduce((a, b) => a + b, 0)
        );
        return den ? num / den : 0;
      }
      return 0;
    })
  );
  Plotly.newPlot('correlation_matrix_chart', [{
    z: matrix, x: strategies, y: strategies, type: 'heatmap', colorscale: 'RdBu', zmin: -1, zmax: 1
  }], {
    title: "Strategy Correlation Matrix",
    xaxis: { title: "Strategy" },
    yaxis: { title: "Strategy" }
  }, {responsive: true});
}

// Cumulative Return vs. Buy & Hold (Line Chart)
function renderCumulativeReturnVsBuyHold(filteredData) {
  // Assume filteredData is for one strategy/pair/period
  let cumStrategy = 0, cumBuyHold = 0;
  const x = [], yStrat = [], yHold = [];
  filteredData.sort((a, b) => new Date(a.end_time) - new Date(b.end_time)).forEach(d => {
    cumStrategy += d.return_percent;
    cumBuyHold += d.return_buy_hold;
    x.push(d.end_time);
    yStrat.push(cumStrategy);
    yHold.push(cumBuyHold);
  });
  Plotly.newPlot('cumulative_vs_buyhold_chart', [
    { x, y: yStrat, mode: 'lines+markers', name: 'Strategy' },
    { x, y: yHold, mode: 'lines+markers', name: 'Buy & Hold' }
  ], {
    title: "Cumulative Return vs. Buy & Hold",
    xaxis: { title: "Time" },
    yaxis: { title: "Cumulative Return (%)" }
  }, {responsive: true});
}

// Reset Selection Button
document.getElementById("reset-selection-btn").addEventListener("click", () => {
  // Reset all charts to show the full filtered data
  updateChartsWithSelection(filterData());
});
