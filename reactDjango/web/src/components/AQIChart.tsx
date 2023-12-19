/**
 * Line chart
 * https://react-chartjs-2.js.org/examples/line-chart
 */
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
    datetime: string,
    pm1_0_concentration: number,
    pm2_5_concentration: number,
    pm10_concentration: number,
};

const AQIChart = ({ data }: { data: DataEntry[] }) => {
    const labels = data.map(entry => {
        const datetime = new Date(entry.datetime);
        const timeOptions: Intl.DateTimeFormatOptions = { hour12: false, hour: '2-digit', minute: '2-digit' };
        const time = datetime.toLocaleTimeString([], timeOptions);
        const day = datetime.getDate().toString().padStart(2, '0');
        const month = (datetime.getMonth() + 1).toString().padStart(2, '0');
        const year = datetime.getFullYear();
        return `${day}.${month}.${year} ${time}`;
    });
    const datasets = [
        {
            label: 'PM1.0 Concentration',
            data: data.map(entry => entry.pm1_0_concentration),
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
        },
        {
            label: 'PM2.5 Concentration',
            data: data.map(entry => entry.pm2_5_concentration),
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
        },
        {
            label: 'PM10 Concentration',
            data: data.map(entry => entry.pm10_concentration),
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
            datetime: PropTypes.string.isRequired,
            pm1_0_concentration: PropTypes.number.isRequired,
            pm2_5_concentration: PropTypes.number.isRequired,
            pm10_concentration: PropTypes.number.isRequired,
        })
    ).isRequired,
};

export default AQIChart;
