import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import MetricCard from '../../MetricCard/MetricCard';
import UpcomingMeetings from './UpcomingMeetings';
import { Package, Users, Calendar, TrendingUp } from 'lucide-react';
import dataService from '../../../services/dataService';
import { useNotification } from '../../../contexts/NotificationContext';
import './SubUserDashboard.css';

const SubUserDashboard = () => {
  const { showError } = useNotification();
  const [metrics, setMetrics] = useState({
    productsSold: { total: 0, thisMonth: 0, lastMonth: 0, change: 0, trend: 'up' },
    leadsGenerated: { total: 0, active: 0, inactive: 0, change: 0, trend: 'up' },
    upcomingMeetings: { total: 0, today: 0, thisWeek: 0, change: 0, trend: 'up' },
    performance: { score: 0, target: 100, achievement: 0, change: 0, trend: 'up' }
  });
  const [loading, setLoading] = useState(true);

  // Load dashboard data
  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [leads, deals, meetings] = await Promise.all([
        dataService.getLeads(),
        dataService.getDeals(),
        dataService.getMeetings()
      ]);

      const calculatedMetrics = calculateMetrics(leads, deals, meetings);
      setMetrics(calculatedMetrics);
    } catch (err) {
      console.error('Error loading dashboard data:', err);
      showError('Failed to load dashboard data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const calculateMetrics = (leads, deals, meetings) => {
    const now = new Date();
    const currentMonth = now.getMonth();
    const currentYear = now.getFullYear();
    const lastMonth = currentMonth === 0 ? 11 : currentMonth - 1;
    const lastMonthYear = currentMonth === 0 ? currentYear - 1 : currentYear;

    // Calculate leads metrics (real data)
    const totalLeads = leads.length;
    const activeLeads = leads.filter(lead => lead.status === 'New' || lead.status === 'Accepted' || lead.status === 'Pipelined').length;
    const inactiveLeads = leads.filter(lead => lead.status === 'Lost' || lead.status === 'Rejected').length;

    // Calculate meetings metrics (real data)
    const scheduledMeetings = meetings.filter(meeting => meeting.status === 'Scheduled');
    const totalMeetings = scheduledMeetings.length;
    
    // Calculate today's meetings
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    
    const todayMeetings = scheduledMeetings.filter(meeting => {
      const meetingDate = new Date(meeting.date);
      return meetingDate >= today && meetingDate < tomorrow;
    }).length;

    // Calculate this week's meetings
    const weekStart = new Date(today);
    weekStart.setDate(today.getDate() - today.getDay());
    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 7);
    
    const thisWeekMeetings = scheduledMeetings.filter(meeting => {
      const meetingDate = new Date(meeting.date);
      return meetingDate >= weekStart && meetingDate < weekEnd;
    }).length;

    return {
      // Dummy data for products sold
      productsSold: {
        total: 89,
        thisMonth: 23,
        lastMonth: 18,
        change: 28,
        trend: 'up'
      },
      // Real data for leads generated
      leadsGenerated: {
        total: totalLeads,
        active: activeLeads,
        inactive: inactiveLeads,
        change: 0, // Could be calculated based on previous periods
        trend: 'up'
      },
      // Real data for upcoming meetings
      upcomingMeetings: {
        total: totalMeetings,
        today: todayMeetings,
        thisWeek: thisWeekMeetings,
        change: 0, // Could be calculated based on previous periods
        trend: 'up'
      },
      // Dummy data for performance score
      performance: {
        score: 87,
        target: 100,
        achievement: 87,
        change: 8,
        trend: 'up'
      }
    };
  };

  const chartData = [
    { month: 'Jan', products: 18, leads: 25, meetings: 12 },
    { month: 'Feb', products: 22, leads: 32, meetings: 15 },
    { month: 'Mar', products: 28, leads: 38, meetings: 18 },
    { month: 'Apr', products: 24, leads: 35, meetings: 14 },
    { month: 'May', products: 32, leads: 45, meetings: 22 },
    { month: 'Jun', products: 26, leads: 42, meetings: 17 },
    { month: 'Jul', products: 35, leads: 50, meetings: 20 },
    { month: 'Aug', products: 38, leads: 55, meetings: 24 },
    { month: 'Sep', products: 31, leads: 48, meetings: 19 },
  ];

  return (
    <div className="sub-user-dashboard" style={{ minHeight: '100vh', background: 'white' }}>
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">NeoCRM - Salesman</h1>
          <p className="dashboard-subtitle">Welcome back! Here's what's happening with your sales performance today.</p>
        </div>
      </div>

      <div className="dashboard-content-container">
        <div className="dashboard-grid">
          {loading ? (
            <>
              <div className="metric-card-loading">
                <div className="loading-skeleton"></div>
              </div>
              <div className="metric-card-loading">
                <div className="loading-skeleton"></div>
              </div>
              <div className="metric-card-loading">
                <div className="loading-skeleton"></div>
              </div>
              <div className="metric-card-loading">
                <div className="loading-skeleton"></div>
              </div>
            </>
          ) : (
            <>
              <MetricCard
                title="Total Products Sold"
                value={metrics.productsSold.total}
                subtitle={`This Month: ${metrics.productsSold.thisMonth} | Last Month: ${metrics.productsSold.lastMonth}`}
                change={metrics.productsSold.change}
                trend={metrics.productsSold.trend}
                icon={Package}
                color="blue"
              />
              
              <MetricCard
                title="Leads Generated"
                value={metrics.leadsGenerated.total}
                subtitle={`Active: ${metrics.leadsGenerated.active} | Inactive: ${metrics.leadsGenerated.inactive}`}
                change={metrics.leadsGenerated.change}
                trend={metrics.leadsGenerated.trend}
                icon={Users}
                color="green"
              />
              
              <MetricCard
                title="Upcoming Meetings"
                value={metrics.upcomingMeetings.total}
                subtitle={`Today: ${metrics.upcomingMeetings.today} | This Week: ${metrics.upcomingMeetings.thisWeek}`}
                change={metrics.upcomingMeetings.change}
                trend={metrics.upcomingMeetings.trend}
                icon={Calendar}
                color="purple"
              />
              
              <MetricCard
                title="Performance Score"
                value={metrics.performance.score}
                subtitle={`Target: ${metrics.performance.target} | Achievement: ${metrics.performance.achievement}%`}
                change={metrics.performance.change}
                trend={metrics.performance.trend}
                icon={TrendingUp}
                color="orange"
              />
            </>
          )}
        </div>
      </div>

      <div className="dashboard-content-container">
        <div className="dashboard-bottom-grid">
          <div className="chart-container">
            <h2 className="chart-title">Sales Performance Overview</h2>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart
                data={chartData}
                margin={{
                  top: 20,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="1 1" stroke="#f3f4f6" />
                <XAxis 
                  dataKey="month" 
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: '#6b7280', fontSize: 11, fontWeight: 400 }}
                  tickMargin={8}
                />
                <YAxis 
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: '#6b7280', fontSize: 11, fontWeight: 400 }}
                  tickMargin={8}
                  domain={[0, 60]}
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'white',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                    padding: '8px 12px',
                    fontSize: '12px'
                  }}
                  labelStyle={{
                    color: '#374151',
                    fontWeight: 500,
                    marginBottom: '4px',
                    fontSize: '11px'
                  }}
                />
                <Legend 
                  wrapperStyle={{
                    paddingTop: '16px',
                    fontSize: '11px',
                    fontWeight: 400
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="products"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  dot={{ fill: '#3b82f6', strokeWidth: 2, r: 3 }}
                  activeDot={{ r: 5, stroke: '#3b82f6', strokeWidth: 2 }}
                  name="Products Sold"
                />
                <Line
                  type="monotone"
                  dataKey="leads"
                  stroke="#10b981"
                  strokeWidth={2}
                  dot={{ fill: '#10b981', strokeWidth: 2, r: 3 }}
                  activeDot={{ r: 5, stroke: '#10b981', strokeWidth: 2 }}
                  name="Leads Generated"
                />
                <Line
                  type="monotone"
                  dataKey="meetings"
                  stroke="#8b5cf6"
                  strokeWidth={2}
                  dot={{ fill: '#8b5cf6', strokeWidth: 2, r: 3 }}
                  activeDot={{ r: 5, stroke: '#8b5cf6', strokeWidth: 2 }}
                  name="Meetings Scheduled"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
          
          <UpcomingMeetings />
        </div>
      </div>
    </div>
  );
};

export default SubUserDashboard;
