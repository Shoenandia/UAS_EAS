// Fetch and display charts
fetch('/api/student-stats')
    .then(response => response.json())
    .then(stats => {
        // GPA Chart
        new Chart(document.getElementById('gpaChart'), {
            type: 'bar',
            data: {
                labels: ['Min', 'Average', 'Max'],
                datasets: [{
                    label: 'IPK',
                    data: [stats.min_gpa, stats.avg_gpa, stats.max_gpa],
                    backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7af']
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 4
                    }
                }
            }
        });

        // Nilai Chart
        new Chart(document.getElementById('nilaiChart'), {
            type: 'bar',
            data: {
                labels: ['Min', 'Average', 'Max'],
                datasets: [{
                    label: 'Nilai',
                    data: [stats.min_nilai, stats.avg_nilai, stats.max_nilai],
                    backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7af']
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    });