// Exemplo de dados recebidos do sensor
const dadosRecebidos = [10, 15, 20, 25, 30];

// Configuração inicial do gráfico
const config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Dados do Sensor',
            data: [],
            backgroundColor: 'rgba(93, 155, 212, 0.2)',
            borderColor: 'rgba(93, 155, 212, 1)',
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
                    text: 'Tempo'
                }
            },
            y: {
                display: true,
                title: {
                    display: true,
                    text: 'Valor'
                }
            }
        }
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

// Função para verificar e atualizar o estado do botão de alerta
function verificarAlerta(valor) {
    const btnAlert = document.getElementById('condições').querySelector('#btnAlert');
    if (valor > 10) {
        console.log('Valor maior que 10');
        btnAlert.classList.add('piscar');
    } else {
        console.log('Valor menor que 10');
        btnAlert.classList.remove('piscar');
    }
}

// Function to update the graph with new data
function atualizarGrafico(dados) {
    // Remove the oldest data point if the number of data points exceeds 10
    if (chart.data.labels.length >= 10) {
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

    valorAtual = dados;
    document.getElementById('informacao1-valor').textContent = valorAtual;

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
    verificarAlerta(ultimoValor);
}

// Simulação de recebimento contínuo de dados do sensor
setInterval(() => {
    const novoDado = Math.random() * 100; // Gerar um novo dado aleatório
    atualizarGrafico(novoDado);
}, 1000); // Atualizar a cada segundo