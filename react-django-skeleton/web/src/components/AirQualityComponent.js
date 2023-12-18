// AirQualityComponent.js
import React from 'react';
import useAirQuality from '../hooks/useAirQuality';

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
            <h1>Air Quality Data</h1>
            <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
    );
};

export default AirQualityComponent;
