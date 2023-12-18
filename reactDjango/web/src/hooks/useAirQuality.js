// useAirQuality.js
import { useQuery } from 'react-query';

const fetchAirQuality = async () => {
    const response = await fetch('http://localhost:8000/aqi');
    if (!response.ok) {
        throw new Error('Failed to fetch air quality data');
    }
    return response.json();
};

const useAirQuality = () => {
    return useQuery('airQuality', fetchAirQuality);
};

export default useAirQuality;
