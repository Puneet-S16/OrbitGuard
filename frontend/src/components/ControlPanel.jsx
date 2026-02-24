import React, { useState } from 'react';
import { Activity, AlertTriangle, Clock, Target } from 'lucide-react';

export default function ControlPanel({ onPredict, loading, results, error }) {
    const [id1, setId1] = useState('25544'); // ISS
    const [id2, setId2] = useState('48274'); // Example payload

    const handleSubmit = (e) => {
        e.preventDefault();
        if (id1 && id2) {
            onPredict(id1, id2);
        }
    };

    return (
        <div className="control-panel">
            <h1 className="title">
                <Target size={28} color="#00d2ff" />
                OrbitGuard
            </h1>
            <div className="subtitle">Satellite Collision Risk Predictor</div>

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div className="input-group">
                    <label>NORAD ID 1</label>
                    <input
                        type="text"
                        value={id1}
                        onChange={(e) => setId1(e.target.value)}
                        placeholder="e.g. 25544"
                        required
                    />
                </div>
                <div className="input-group">
                    <label>NORAD ID 2</label>
                    <input
                        type="text"
                        value={id2}
                        onChange={(e) => setId2(e.target.value)}
                        placeholder="e.g. 48274"
                        required
                    />
                </div>
                <button type="submit" className="analyze-btn" disabled={loading}>
                    {loading ? 'Analyzing Orbits...' : 'Analyze Collision Risk'}
                </button>
            </form>

            {error && (
                <div className="error-message">
                    <AlertTriangle size={16} style={{ display: 'inline', marginRight: '6px', verticalAlign: 'middle' }} />
                    {error}
                </div>
            )}

            {results && (
                <div className="results-panel">
                    <div className="result-header">Analysis Results</div>

                    <div className="result-item">
                        <span className="result-label">Minimum Distance</span>
                        <span className="result-value">{results.minDistance} km</span>
                    </div>

                    <div className="result-item">
                        <span className="result-label">Risk Level</span>
                        <span className={`result-value risk-${results.riskLevel.toLowerCase()}`}>
                            {results.riskLevel}
                        </span>
                    </div>

                    <div className="result-item">
                        <span className="result-label">Risk Score</span>
                        <span className="result-value">{results.score} / 100</span>
                    </div>

                    <div className="result-item">
                        <span className="result-label">Closest Approach (UTC)</span>
                        <span className="result-value">
                            {new Date(results.timeOfApproach).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                    </div>
                </div>
            )}
        </div>
    );
}
