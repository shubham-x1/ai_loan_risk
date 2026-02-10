import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

const API_URL = 'https://ai-loan-risk.onrender.com/';

function App() {
  const [activeTab, setActiveTab] = useState('predict');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [applications, setApplications] = useState([]);
  const [stats, setStats] = useState(null);

  const [formData, setFormData] = useState({
    gender: 'Male',
    married: 'Yes',
    dependents: '0',
    education: 'Graduate',
    self_employed: 'No',
    applicant_income: 5000,
    coapplicant_income: 0,
    loan_amount: 150,
    loan_amount_term: 360,
    credit_history: 1.0,
    property_area: 'Urban'
  });

  useEffect(() => {
    if (activeTab === 'dashboard') {
      fetchApplications();
      fetchStats();
    }
  }, [activeTab]);

  const fetchApplications = async () => {
    try {
      const response = await axios.get(`${API_URL}/applications?limit=10`);
      setApplications(response.data);
    } catch (error) {
      console.error('Error fetching applications:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name.includes('income') || name.includes('amount') || name === 'loan_amount_term'
        ? parseInt(value) || 0
        : name === 'credit_history'
        ? parseFloat(value)
        : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);

    try {
      const response = await axios.post(`${API_URL}/predict`, formData);
      setResult(response.data);
    } catch (error) {
      alert('Error: ' + (error.response?.data?.detail || 'Failed to predict'));
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (score) => {
    if (score < 30) return '#10b981';
    if (score < 60) return '#f59e0b';
    return '#ef4444';
  };

  const COLORS = ['#10b981', '#ef4444'];

  return (
    <div className="App">
      <header className="header">
        <h1>🏦 AI Loan Risk & Approval System</h1>
        <p>Intelligent Credit Decisioning Platform</p>
      </header>

      <div className="tabs">
        <button 
          className={activeTab === 'predict' ? 'active' : ''} 
          onClick={() => setActiveTab('predict')}
        >
          📝 New Application
        </button>
        <button 
          className={activeTab === 'dashboard' ? 'active' : ''} 
          onClick={() => setActiveTab('dashboard')}
        >
          📊 Dashboard
        </button>
      </div>

      {activeTab === 'predict' && (
        <div className="container">
          <div className="form-section">
            <h2>Loan Application Form</h2>
            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div className="form-group">
                  <label>Gender</label>
                  <select name="gender" value={formData.gender} onChange={handleChange}>
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Married</label>
                  <select name="married" value={formData.married} onChange={handleChange}>
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Dependents</label>
                  <select name="dependents" value={formData.dependents} onChange={handleChange}>
                    <option value="0">0</option>
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3+">3+</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Education</label>
                  <select name="education" value={formData.education} onChange={handleChange}>
                    <option value="Graduate">Graduate</option>
                    <option value="Not Graduate">Not Graduate</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Self Employed</label>
                  <select name="self_employed" value={formData.self_employed} onChange={handleChange}>
                    <option value="Yes">Yes</option>
                    <option value="No">No</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Property Area</label>
                  <select name="property_area" value={formData.property_area} onChange={handleChange}>
                    <option value="Urban">Urban</option>
                    <option value="Semiurban">Semiurban</option>
                    <option value="Rural">Rural</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Applicant Income (₹/month)</label>
                  <input 
                    type="number" 
                    name="applicant_income" 
                    value={formData.applicant_income} 
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Coapplicant Income (₹/month)</label>
                  <input 
                    type="number" 
                    name="coapplicant_income" 
                    value={formData.coapplicant_income} 
                    onChange={handleChange}
                  />
                </div>

                <div className="form-group">
                  <label>Loan Amount (₹ thousands)</label>
                  <input 
                    type="number" 
                    name="loan_amount" 
                    value={formData.loan_amount} 
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label>Loan Term (months)</label>
                  <select name="loan_amount_term" value={formData.loan_amount_term} onChange={handleChange}>
                    <option value="360">360 (30 years)</option>
                    <option value="180">180 (15 years)</option>
                    <option value="120">120 (10 years)</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Credit History</label>
                  <select name="credit_history" value={formData.credit_history} onChange={handleChange}>
                    <option value="1.0">Good (1.0)</option>
                    <option value="0.0">Poor (0.0)</option>
                  </select>
                </div>
              </div>

              <button type="submit" className="submit-btn" disabled={loading}>
                {loading ? '🔄 Processing...' : '🚀 Analyze Application'}
              </button>
            </form>
          </div>

          {result && (
            <div className={`result-section ${result.approved ? 'approved' : 'rejected'}`}>
              <h2>{result.approved ? '✅ APPROVED' : '❌ REJECTED'}</h2>
              
              <div className="metrics">
                <div className="metric">
                  <label>Approval Probability</label>
                  <div className="value">{(result.approval_probability * 100).toFixed(1)}%</div>
                </div>
                
                <div className="metric">
                  <label>Risk Score</label>
                  <div className="value" style={{ color: getRiskColor(result.risk_score) }}>
                    {result.risk_score.toFixed(1)}/100
                  </div>
                </div>
                
                {result.approved && (
                  <div className="metric">
                    <label>Suggested Interest Rate</label>
                    <div className="value">{result.suggested_interest_rate.toFixed(2)}%</div>
                  </div>
                )}
                
                {result.fraud_flag && (
                  <div className="metric fraud">
                    <label>⚠️ Fraud Alert</label>
                    <div className="value">High Risk</div>
                  </div>
                )}
              </div>

              <div className="explanation">
                <h3>AI Explanation</h3>
                <p>{result.explanation}</p>
              </div>
            </div>
          )}
        </div>
      )}

      {activeTab === 'dashboard' && stats && (
        <div className="container">
          <h2>Analytics Dashboard</h2>
          
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Applications</h3>
              <div className="stat-value">{stats.total_applications}</div>
            </div>
            <div className="stat-card approved">
              <h3>Approved</h3>
              <div className="stat-value">{stats.approved}</div>
            </div>
            <div className="stat-card rejected">
              <h3>Rejected</h3>
              <div className="stat-value">{stats.rejected}</div>
            </div>
            <div className="stat-card">
              <h3>Approval Rate</h3>
              <div className="stat-value">{stats.approval_rate.toFixed(1)}%</div>
            </div>
          </div>

          <div className="charts">
            <div className="chart">
              <h3>Approval Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={[
                      { name: 'Approved', value: stats.approved },
                      { name: 'Rejected', value: stats.rejected }
                    ]}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {COLORS.map((color, index) => (
                      <Cell key={`cell-${index}`} fill={color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>

            <div className="chart">
              <h3>Recent Applications</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={applications.slice(0, 10)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="applicant_income" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="risk_score" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="applications-table">
            <h3>Recent Applications</h3>
            <table>
              <thead>
                <tr>
                  <th>Income</th>
                  <th>Loan Amount</th>
                  <th>Status</th>
                  <th>Risk Score</th>
                  <th>Interest Rate</th>
                </tr>
              </thead>
              <tbody>
                {applications.map((app, idx) => (
                  <tr key={idx}>
                    <td>₹{app.applicant_income}</td>
                    <td>₹{app.loan_amount}k</td>
                    <td>
                      <span className={`status ${app.approved ? 'approved' : 'rejected'}`}>
                        {app.approved ? 'Approved' : 'Rejected'}
                      </span>
                    </td>
                    <td style={{ color: getRiskColor(app.risk_score) }}>
                      {app.risk_score.toFixed(1)}
                    </td>
                    <td>{app.suggested_interest_rate.toFixed(2)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;