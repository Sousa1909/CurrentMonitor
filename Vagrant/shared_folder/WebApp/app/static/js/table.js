// table.js
document.addEventListener('DOMContentLoaded', () => {
    fetch('/get_data') 
        .then(response => response.json())
        .then(data => {
            const tableBody = document.querySelector('#data-table tbody');
            data.forEach(entry => {
                const row = document.createElement('tr');
                const timestampCell = document.createElement('td');
                const topicCell = document.createElement('td');
                const payloadCell = document.createElement('td');

                timestampCell.textContent = entry.timestamp;
                topicCell.textContent = entry.topic;
                payloadCell.textContent = entry.payload;

                row.appendChild(timestampCell);
                row.appendChild(topicCell);
                row.appendChild(payloadCell);

                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});