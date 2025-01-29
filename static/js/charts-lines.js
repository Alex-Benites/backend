/**
 * For usage, visit Chart.js docs https://www.chartjs.org/docs/latest/
 */
const lineConfig = {
  type: 'line',
  data: {
    labels: [], // Se llenará dinámicamente
    datasets: [
      {
        label: 'Respuestas',
        backgroundColor: '#0694a2',
        borderColor: '#0694a2',
        data: [], // Se llenará dinámicamente
        fill: false,
      },
    ],
  },
  options: {
    responsive: true,
    legend: {
      display: false,
    },
    tooltips: {
      mode: 'index',
      intersect: false,
    },
    hover: {
      mode: 'nearest',
      intersect: true,
    },
    scales: {
      x: {
        display: true,
        title: {
          display: true,
          text: 'Día',
        },
      },
      y: {
        display: true,
        title: {
          display: true,
          text: 'Número de respuestas',
        },
      },
    },
  },
};

// change this to the id of your chart element in HMTL
const lineCtx = document.getElementById('line');
window.myLine = new Chart(lineCtx, lineConfig);

// Función para procesar el JSON
const countCommentsByDay = (data) => {
  const counts = {};

  Object.values(data).forEach((record) => {
    const savedDate = record.saved;
    if (!savedDate) {
      return;
    }

    // Extraer solo la fecha (dd/mm/yyyy)
    const datePart = savedDate.split(",")[0];

    // Convertir al formato estándar YYYY-MM-DD para ordenar correctamente
    const [day, month, year] = datePart.split("/");
    const formattedDate = `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}`;

    // Contar ocurrencias por día
    counts[formattedDate] = (counts[formattedDate] || 0) + 1;
  });

  // Ordenar fechas cronológicamente
  const sortedDates = Object.keys(counts).sort();

  return {
    labels: sortedDates,
    counts: sortedDates.map(date => counts[date]),
  };
};

// Función para actualizar el gráfico
const updateLine = () => {
  fetch('/api/v1/landing')
    .then(response => response.json())
    .then(data => {
      let { labels, counts } = countCommentsByDay(data);

      // Actualizar el gráfico con los datos procesados
      window.myLine.data.labels = labels;
      window.myLine.data.datasets[0].data = counts;
      window.myLine.update();
    })
    .catch(error => console.error('Error:', error));
};

updateLine();
