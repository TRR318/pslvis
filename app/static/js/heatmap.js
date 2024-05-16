export function heatmap() {
    function getHeatmapColor(value) {
        const minColor = [255, 230, 230]; // Bright red
        const maxColor = [255, 0, 0];     // Dark red

        // Convert percentage string to a number
        const numValue = parseFloat(value.replace('%', ''));

        // Calculate ratio (0 to 1)
        const ratio = numValue / 100;

        // Calculate color
        const r = Math.round(minColor[0] + ratio * (maxColor[0] - minColor[0]));
        const g = Math.round(minColor[1] + ratio * (maxColor[1] - minColor[1]));
        const b = Math.round(minColor[2] + ratio * (maxColor[2] - minColor[2]));

        return `rgb(${r}, ${g}, ${b})`;
    }

    function applyHeatmap() {
        const cells = document.querySelectorAll('.proba-cell');
        cells.forEach(cell => {
            const value = cell.textContent.trim();
            if (value) {
                cell.style.backgroundColor = getHeatmapColor(value);
            }
        });
    }
    applyHeatmap();
}