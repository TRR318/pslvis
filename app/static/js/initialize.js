import { sortableStaff } from "./sortable_staff.js";
import { heatmap } from "./heatmap.js";

function initialize() {
  // Send height to iframe parent
  window.parent.postMessage({ height: document.body.scrollHeight }, '*');
  window.onload = () => window.parent.postMessage({ new_url: window.location.href }, '*');

  // fix to delete orphaned tooltips
  document.querySelectorAll(".tooltip.bs-tooltip-auto").forEach(e => e.remove())
  document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(tr => new bootstrap.Tooltip(tr))

  if ("chart" in window) {
    chart.data.labels = labels;
    chart.data.datasets[0].data = data;
    chart.update();
  }

  sortableStaff();

  heatmap();
}

document.addEventListener('DOMContentLoaded', initialize);
htmx.on('htmx:afterSettle', initialize);
