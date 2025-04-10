document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript loaded.");

    // Function to load the reports content (both dynamic tables and charts)
    function loadContent() {
        const sectionLinks = document.querySelectorAll(".section-link");
        const defaultContent = document.getElementById("defaultContent");
        const dynamicContent = document.getElementById("dynamicContent");

        sectionLinks.forEach(link => {
            link.addEventListener("click", function (event) {
                event.preventDefault();
                const sectionId = this.getAttribute("data-section");

                // Hide the default content
                defaultContent.classList.add("d-none");

                // Show dynamic content
                dynamicContent.classList.remove("d-none");

                // Fetch new content from Django
                fetch(`/${sectionId}/`)
                    .then(response => response.text())
                    .then(html => {
                        dynamicContent.innerHTML = html;
                        setupTableToggling(); // Re-initialize table toggling after content loads
                        fetchChartData(); // Fetch and render the charts after content loads
                    })
                    .catch(error => {
                        console.error("Error loading content:", error);
                        dynamicContent.innerHTML = "<p>Failed to load content.</p>";
                    });
            });
        });
    }

    // Fetch and render charts via AJAX
    function fetchChartData() {
        // Fetch the data from the Django view
        fetch('/reports/')  // URL for your Django view that returns chart data
            .then(response => {
                // Check if the response is JSON
                if (!response.ok) {
                    throw new Error("Failed to fetch data");
                }
                return response.json(); // Return the JSON data
            })
            .then(data => {
                // Now render the charts using the fetched data
                renderPieChart(data.pie_chart_data);
                renderLineChart(data.line_graph_data);
            })
            .catch(error => {
                console.error("Error fetching chart data:", error);
            });
    }

    // Render Pie Chart
    function renderPieChart(pieChartData) {
        const pieChartCtx = document.getElementById('PieChart').getContext('2d');
        new Chart(pieChartCtx, {
            type: 'pie',
            data: {
                labels: Object.keys(pieChartData),
                datasets: [{
                    data: Object.values(pieChartData),
                    backgroundColor: ['blue', 'red', 'green'], // Customize colors as needed
                    borderColor: ['blue', 'red', 'green'],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true
            }
        });
    }

    // Render Line Chart
    function renderLineChart(lineGraphData) {
        const lineChartCtx = document.getElementById('LineChart').getContext('2d');
        new Chart(lineChartCtx, {
            type: 'line',
            data: {
                labels: lineGraphData.labels,
                datasets: [{
                    label: 'Votes vs Total Voters',
                    data: lineGraphData.values,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                    fill: false
                }]
            },
            options: {
                responsive: true
            }
        });
    }

    // Setup table toggling (keeping your original functionality)
    function setupTableToggling() {
        console.log("Setting up table toggling...");

        const toggles = document.querySelectorAll(".table-toggle");
        const tables = {
            voters: document.getElementById("voters-table"),
            candidates: document.getElementById("candidates-table"),
            votes: document.getElementById("votes-table"),
        };

        if (!toggles.length || !tables.voters) {
            console.log("Tables not found, exiting...");
            return;
        }

        // Set the first toggle as active by default
        toggles[0].classList.add("active");
        tables.voters.classList.remove("d-none");

        toggles.forEach(toggle => {
            toggle.addEventListener("click", function () {
                console.log("Tab clicked:", this.getAttribute("data-table"));

                // Remove active class from all toggles
                toggles.forEach(t => t.classList.remove("active"));

                // Hide all tables
                Object.values(tables).forEach(table => table.classList.add("d-none"));

                // Show the selected table
                const tableToShow = this.getAttribute("data-table");
                if (tables[tableToShow]) {
                    tables[tableToShow].classList.remove("d-none");
                }

                this.classList.add("active");
            });
        });

        console.log("Table toggling setup complete.");
    }

    // Observe dynamic content changes and reapply the toggling function
    function observeContentChange() {
        const contentBox = document.getElementById("dynamicContent");

        if (!contentBox) return;

        const observer = new MutationObserver(() => {
            console.log("Content changed, reloading table toggling...");
            setupTableToggling();
        });

        observer.observe(contentBox, { childList: true, subtree: true });
    }

    loadContent();  // Load content click handlers
    observeContentChange();  // Watch for content changes
});
