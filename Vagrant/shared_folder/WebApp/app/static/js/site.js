// Exemplo de dados recebidos do sensor
const dadosRecebidos = [10, 15, 20, 25, 30];

// Configuração inicial do gráfico
const config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Current from RPi Pico W',
            data: [],
            backgroundColor: 'rgba(50,205,50, 1)',
            borderColor: 'rgba(50,205,50, 1)',
            strokeColor: "rgba(220,220,220,1)",
            pointColor: "rgba(220,220,220,1)",
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Timestamp',
                    color: 'white'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.5)', // Change the color of the X-axis grid lines
                },
                ticks: {
                    color: 'white', // Change the color of the X-axis tick marks
                }
            },
            y: {
                display: true,
                title: {
                    display: true,
                    text: 'Current in A',
                    color: 'white'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.5)', // Change the color of the X-axis grid lines
                },
                ticks: {
                    color: 'white', // Change the color of the X-axis tick marks
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                labels: {
                    color: 'white', // Color for the legend labels
                }
            }
        },
        elements: {
            point: {
                pointStyle: 'rectRot', // Customize the data points' style (optional)
                radius: 7, // Adjust the data points' size (optional)
                backgroundColor: 'rgba(93, 155, 212, 1)', // Data points' background color
                borderColor: 'white', // Data points' border color
                borderWidth: 1 // Data points' border width
            }
        },
        layout: {
            padding: {
                left: 10,
                right: 10,
                top: 10,
                bottom: 10
            }
        },
    }
};

// Criação do gráfico
const ctx = document.getElementById('grafico').getContext('2d');
const chart = new Chart(ctx, config);


// Variável para armazenar o valor atual
let valorAtual = null;

const historicoValores = [];

// tensão 230V convertido dá 0,23kWh
//preço kWh = 0,13640 €/kWh
// logo a taxa de custo por hora é 0,23*0,13640
// sabendo que é por hora, divide-se por 60
const taxaCustoPorAmpere = (0.23*0.13640)/60;

// Função para calcular o custo com base nos amperes
function calcularCusto(amperes) {
    return amperes * taxaCustoPorAmpere;
}

function calcularCustoTotal(historico) {
    let custoTotal = 0;
    for (let i = 0; i < historico.length; i++) {
        custoTotal += calcularCusto(historico[i]);
    }
    return custoTotal;
}

// Function to update the graph with new data
function atualizarGrafico(dados) {
    // Remove the oldest data point if the number of data points exceeds 10
    if (chart.data.labels.length >= 20) {
        chart.data.labels.shift(); // Remove the first label
        chart.data.datasets[0].data.shift(); // Remove the first data point
    }
    
    // Add the current timestamp to the labels array
    chart.data.labels.push(new Date().toLocaleTimeString());

    // Add the new data point to the dataset
    chart.data.datasets[0].data.push(dados);

    // Update the entire datasets array
    chart.update({
        preservation: true // Preserve the current animation
    });

    historicoValores.push(dados);

    //valorAtual = dados;
    //document.getElementById('informacao1-valor').textContent = valorAtual;

    // Calcular o custo com base nos amperes
    const custo = calcularCusto(dados);
    // Atualizar o valor exibido na seção "Informação 2"
    document.getElementById('informacao2-valor').textContent = custo.toFixed(6); // Exibir com duas casas decimais

    // Calcular o custo total com base no histórico de valores
    const custoTotal = calcularCustoTotal(historicoValores);
    // Atualizar o valor exibido na secção "Custo Total"
    document.getElementById('custo-total-valor').textContent = custoTotal.toFixed(6); // Exibir com duas casas decimais

    // Verificar o alerta com base no último valor recebido
    const ultimoValor = dados[dados.length - 1];
}

const socket = io();

document.addEventListener('DOMContentLoaded', function() {

    // Receives the data from 
    socket.on('mqtt_data', (data) => {
        console.log("Received MQTT data: ", data)
        atualizarGrafico(data.payload);
        document.getElementById('informacao1-valor').textContent = data.payload;
    });

    // Get the checkbox element
    const checkbox = document.getElementById('pub-checkbox');

    // Add an event listener to the checkbox for the 'change' event
    checkbox.addEventListener('change', function() {
        // Get the boolean value (true if checked, false if unchecked)
        const value = checkbox.checked;
        // Log the value of the checkbox when it changes
        console.log("Checkbox value:", value);
        socket.emit('publish', JSON.stringify({ topic: 'STATUS', message: value }));
    });
});

