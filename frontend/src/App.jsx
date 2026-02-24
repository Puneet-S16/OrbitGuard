import { useState } from 'react'
import axios from 'axios'
import GlobeViewer from './components/GlobeViewer'
import ControlPanel from './components/ControlPanel'
import './index.css'

function App() {
    const [loading, setLoading] = useState(false)
    const [results, setResults] = useState(null)
    const [error, setError] = useState(null)
    const [orbitData, setOrbitData] = useState({})

    const handlePredict = async (id1, id2) => {
        setLoading(true)
        setError(null)
        setResults(null)
        setOrbitData({})

        try {
            const response = await axios.post('http://localhost:8000/predict_collision', {
                norad_id_1: id1,
                norad_id_2: id2
            })

            const data = response.data
            setResults({
                minDistance: data.min_distance_km,
                timeOfApproach: data.time_of_closest_approach,
                riskLevel: data.risk_level,
                score: data.collision_probability_score
            })

            setOrbitData({
                path1: data.path1,
                path2: data.path2,
                closest_point: data.closest_point
            })

        } catch (err) {
            setError(err.response?.data?.detail || "Failed to fetch prediction data. Ensure backend is running.")
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="app-container">
            <ControlPanel
                onPredict={handlePredict}
                loading={loading}
                results={results}
                error={error}
            />
            <div className="globe-container">
                <GlobeViewer orbitData={orbitData} />
            </div>
        </div>
    )
}

export default App
