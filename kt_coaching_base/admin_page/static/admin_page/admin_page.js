document.addEventListener('DOMContentLoaded', (event) => {
    const genderCounts = JSON.parse(document.getElementById('gender_counts').textContent);
    const genderLabels = genderCounts.map(item => item.gender);
    const genderData = genderCounts.map(item => item.gender_count);

    const ctxGender = document.getElementById('gender_Chart').getContext('2d');
    new Chart(ctxGender, {
        type: 'pie',
        data: {
            labels: genderLabels,
            datasets: [{
                data: genderData,
                backgroundColor: [
                    'rgba(75, 192, 192, 0.6)', // light cyan
                    'rgba(153, 102, 255, 0.6)', // light purple
                ]
            }]
        },
        options: {
            responsive: true,
            legend: {
                display: false,
            },
            title: {
                display: true,
                text: 'Gender Distribution'
            },
            animation: {
                animateScale: true,
                animateRotate: true
            },
            plugins: {
                datalabels: {
                    display: true,
                    color: '#000',
                    font: {
                        size: 16,
                        weight: 'bold'
                    },
                    formatter: (value, context) => {
                        return context.chart.data.labels[context.dataIndex] + ': ' + value;
                    }
                }
            },
        }
    });
});
