import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import PropTypes from 'prop-types';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top' as const,
        },
        title: {
            display: true,
            text: 'AQI Chart',
        },
    },
};

type DataEntry = {
    timestamp: string,
    pm1_0_concentration: string,
    pm2_5_concentration: string,
    pm10_concentration: string,
};

const AQIChart = ({ data }: { data: DataEntry[] }) => {
    const labels = data.map(entry => new Date(entry.timestamp).toLocaleTimeString());
    const datasets = [
        {
            label: 'PM1.0 Concentration',
            data: data.map(entry => parseFloat(entry.pm1_0_concentration)),
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
        },
        {
            label: 'PM2.5 Concentration',
            data: data.map(entry => parseFloat(entry.pm2_5_concentration)),
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
        },
        {
            label: 'PM10 Concentration',
            data: data.map(entry => parseFloat(entry.pm10_concentration)),
            borderColor: 'rgba(255, 205, 86, 1)',
            backgroundColor: 'rgba(255, 205, 86, 0.5)',
        },
    ];

    const chartData = { labels, datasets };
    return <Line options={options} data={chartData} />;
};

AQIChart.propTypes = {
    data: PropTypes.arrayOf(
        PropTypes.shape({
            id: PropTypes.number.isRequired,
            timestamp: PropTypes.string.isRequired,
            pm1_0_concentration: PropTypes.string.isRequired,
            pm2_5_concentration: PropTypes.string.isRequired,
            pm10_concentration: PropTypes.string.isRequired,
        })
    ).isRequired,
};

export default AQIChart;
