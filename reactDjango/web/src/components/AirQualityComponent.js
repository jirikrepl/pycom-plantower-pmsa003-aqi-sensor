import React from 'react';
import useAirQuality from '../hooks/useAirQuality';
import AQIChart from './AQIChart';

const AirQualityComponent = () => {
    const { data, error, isLoading } = useAirQuality();

    if (isLoading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error fetching data: {error.message}</div>;
    }

    return (
        <div>
            <AQIChart data={data} />
            <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
    );
};

export default AirQualityComponent;
