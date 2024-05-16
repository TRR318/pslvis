import { sortableStaff } from "./sortable_staff.js";
import { history } from "./history.js";
import { heatmap } from "./heatmap.js";

function initialize() {
    // Send height to iframe parent
    window.parent.postMessage({ height: document.body.scrollHeight }, '*');

    // fix to delete orphaned tooltips
    document.querySelectorAll(".tooltip.bs-tooltip-auto").forEach(e => e.remove())
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(tr => new bootstrap.Tooltip(tr))

    chart.data.labels = labels;
    chart.data.datasets[0].data = data;
    chart.update();

    sortableStaff();

    history();

    heatmap();
}

document.addEventListener('DOMContentLoaded', function(){
    initialize();
  });

  document.body.addEventListener('htmx:afterSettle', initialize);