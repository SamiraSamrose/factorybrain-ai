# FactoryBrain AI - User Guide

## Introduction

Welcome to FactoryBrain AI, an intelligent system for autonomous process optimization in smart manufacturing plants. This guide will help you navigate and use all features of the platform.

## Getting Started

### Accessing the System

1. Open web browser
2. Navigate to FactoryBrain AI URL (e.g., https://factorybrain.example.com)
3. You will see the login page

### Logging In

Enter credentials:
- **Username**: assigned username
- **Password**: password

Click "Sign In" to access the dashboard.

### User Roles

FactoryBrain AI has four user roles:

**Administrator**
- Full system access
- Manage users and settings
- Approve all operations
- View all reports

**Supervisor**
- Approve maintenance and procurement
- Assign tickets to technicians
- View all machines and analytics
- Generate reports

**Operator**
- View machine status
- Create maintenance tickets
- Receive alerts
- Submit sensor data

**Viewer**
- Read-only access
- View dashboards and reports
- No editing capabilities

## Dashboard Overview

### Main Dashboard

The dashboard provides real-time plant overview with key performance indicators (KPIs):

**KPI Cards** (top of dashboard):
- **Overall Efficiency**: Plant-wide operational efficiency percentage
- **Average Health**: Mean health score across all machines
- **Power Consumption**: Total power usage in kilowatts
- **Failure Risk**: Average probability of machine failures

**Charts Section**:
- **Efficiency Trend**: 24-hour efficiency history
- **Power Consumption**: Hourly power usage
- **Machine Status Distribution**: Pie chart of machine statuses
- **CO2 Reduction Progress**: Emissions reduction tracking

**Recent Alerts Section**:
- Latest system alerts by severity
- Click on alerts for more details
- Color-coded by priority (red=critical, orange=high, blue=medium, gray=low)

**Machine Status Overview**:
- Grid view of all machines
- Health scores and current status
- Click any machine for detailed view

### Navigation Menu

Located on the left sidebar:
- **Dashboard**: Main overview (you are here)
- **Machines**: Detailed machine monitoring
- **Analytics**: Advanced reports and visualizations
- **Maintenance**: Ticket and procurement management
- **Logout**: Sign out of the system

## Machine Monitoring

### Viewing All Machines

1. Click "Machines" in the navigation menu
2. You will see a table of all machines with:
   - Machine ID and Name
   - Type and Location
   - Current Status
   - Health Score
   - Temperature, Vibration, Pressure
   - Power Consumption
   - Efficiency

### Filtering Machines

Use the filters at the top:
- **Status Filter**: Show only operational, maintenance, standby, or offline machines
- **Search**: Enter machine ID to find specific machine

### Viewing Machine Details

1. Click "View" button next to any machine
2. A modal window opens with three tabs:

**Overview Tab**:
- Complete machine information
- Current sensor readings
- Maintenance schedule
- Operational statistics

**History Tab**:
- 24-hour sensor data chart
- Temperature, vibration, and health trends
- Zoom and pan to explore data

**Predictions Tab**:
- Failure probability
- Estimated time to failure
- Contributing risk factors
- Maintenance recommendations

### Understanding Health Scores

Health scores indicate overall machine condition:
- **90-100**: Excellent (green)
- **70-89**: Good (yellow)
- **50-69**: Fair (orange)
- **Below 50**: Critical (red)

## Alerts and Notifications

### Alert Types

**Anomaly Detected**:
- Unusual sensor readings detected
- Requires immediate inspection

**Failure Prediction**:
- Machine failure predicted within timeframe
- Schedule preventive maintenance

**Overheating**:
- Temperature exceeds safe limits
- Critical alert - immediate action required

**Vibration Alert**:
- Excessive vibration detected
- May indicate mechanical issues

**Pressure Abnormality**:
- Pressure outside normal range
- Check hydraulic systems

### Responding to Alerts

1. **View Alert**: Click on alert in dashboard
2. **Acknowledge**: Click "Acknowledge" button to confirm you've seen it
3. **Take Action**: Follow recommended steps
4. **Create Ticket**: If maintenance needed, create ticket
5. **Resolve**: Supervisor marks alert as resolved when fixed

### Voice Alerts

For critical alerts, you may receive voice notifications:
- Listen carefully to the message
- Note the machine ID and issue type
- Follow the verbal repair instructions
- Confirm receipt by acknowledging in system

## Analytics and Reporting

### Accessing Analytics

Click "Analytics" in the navigation menu to access advanced reporting.

### Key Metrics

**Energy Savings**:
- Total kilowatt-hours saved
- Cost savings in dollars
- Percentage reduction from baseline

**CO2 Reduction**:
- Kilograms of CO2 emissions prevented
- Progress toward 20% reduction target
- Environmental impact summary

**Cost Savings**:
- Maintenance cost reductions
- Procurement savings through negotiation
- Total operational cost savings

**Downtime Reduction**:
- Hours of downtime prevented
- Impact on production output
- Reliability improvements

### Viewing Reports

**KPI Trends**:
- Historical performance data
- Efficiency, health, and risk trends
- Customizable time ranges

**Energy Consumption**:
- Power usage over time
- Peak and off-peak patterns
- Optimization opportunities

**Machine Performance**:
- Individual machine statistics
- Efficiency rankings
- Uptime percentages

**Maintenance Statistics**:
- Ticket volume and resolution times
- Preventive vs. corrective maintenance
- Cost analysis

**Optimization Report**:
- Summary of AI-driven improvements
- Top optimization actions
- Recommendations for further gains

### Exporting Reports

1. Click "Export Report" button
2. Select desired format (PDF recommended)
3. Report downloads to your device
4. Share with stakeholders as needed

## Maintenance Management

### Viewing Maintenance Tickets

1. Click "Maintenance" in navigation
2. View list of all tickets
3. Filter by status, priority, or machine

### Creating a Maintenance Ticket

1. Click "Create Ticket" button
2. Fill in the form:
   - **Machine ID**: Select affected machine
   - **Title**: Brief description
   - **Description**: Detailed issue explanation
   - **Priority**: Low, Medium, High, or Critical
   - **Failure Type**: Select from dropdown
3. Click "Create Ticket"
4. Ticket is assigned unique ID (e.g., MT-20241208103000)

### Ticket Lifecycle

**Open**:
- Ticket created, awaiting assignment
- Supervisors can assign to technicians

**In Progress**:
- Technician working on issue
- Can update with progress notes

**Pending Parts**:
- Waiting for spare parts delivery
- Procurement order linked

**Completed**:
- Issue resolved
- Actual downtime and cost recorded

### Assigning Tickets (Supervisors Only)

1. Click "View" on ticket
2. Click "Assign Ticket"
3. Enter technician username
4. Technician receives notification

### Completing Tickets

1. Click "View" on ticket
2. Click "Mark Complete"
3. Enter:
   - Completion notes
   - Actual downtime (hours)
   - Actual cost
4. Submit to close ticket

## Procurement Management

### Viewing Inventory

1. Navigate to Maintenance section
2. Scroll to Inventory table
3. See all spare parts with quantities

### Low Stock Alerts

Parts with quantity at or below reorder

level are highlighted:

Automatic reordering available
Manual order option

Requesting Spare Parts

Click "Request Parts" button
Fill in form:

Part Name: Description
Part Number: SKU or part ID
Quantity: Number needed
Urgency: Priority level
Related Machine: (optional) Which machine needs it
Related Ticket: (optional) Link to maintenance ticket


Submit request
Procurement Agent negotiates with suppliers
Best deal selected automatically

Approving Orders (Supervisors Only)

View procurement orders
Orders in "Requested" status need approval
Click "Approve" on order
Order status changes to "Ordered"
Supplier fulfills order

Tracking Deliveries

View "Estimated Delivery" date
Status updates: Requested → Ordered → Shipped → Delivered
Receive notification when parts arrive

Cost Savings
The system automatically negotiates with suppliers:

Original quoted price shown
Negotiated price displayed
Savings calculated per order
Total savings tracked in analytics

Best Practices
Daily Operations

Check Dashboard Daily:

Review KPIs for any concerning trends
Address critical alerts immediately
Acknowledge all alerts promptly


Monitor High-Risk Machines:

Focus on machines with low health scores
Review failure predictions regularly
Schedule preventive maintenance proactively


Respond to Alerts Quickly:

Critical alerts require immediate action
High-priority alerts within 1 hour
Medium-priority within 4 hours



Maintenance

Create Detailed Tickets:

Provide complete problem description
Include symptoms and observations
Attach photos if applicable


Update Ticket Status:

Log progress notes
Update when waiting for parts
Record actual time and costs


Close Tickets Properly:

Document what was done
Note any additional issues found
Verify machine operational before closing



Energy Optimization

Review Energy Reports Weekly:

Check CO2 reduction progress
Identify high-consumption machines
Implement recommendations


Schedule Off-Peak Operations:

Run non-critical tasks during off-peak hours
Reduces energy costs
Contributes to CO2 reduction goals


Monitor Power Trends:

Watch for unusual spikes
Investigate sustained high consumption
Report anomalies



Troubleshooting
Cannot Log In

Verify username and password are correct
Check Caps Lock is off
Contact administrator if forgotten password
Try different browser if issue persists

Dashboard Not Loading

Refresh browser (F5 or Ctrl+R)
Clear browser cache
Check internet connection
Try incognito/private browsing mode

Machine Data Not Updating

Check "Last Updated" timestamp
Verify machine is online and sending data
Refresh page
Report to technical support if persists

Cannot Create Ticket

Verify you have Operator role or higher
Check all required fields filled
Ensure machine ID is valid
Contact support if error persists

Charts Not Displaying

Enable JavaScript in browser
Disable ad blockers temporarily
Try different browser
Clear browser cache

Keyboard Shortcuts

Ctrl + D: Go to Dashboard
Ctrl + M: Go to Machines
Ctrl + A: Go to Analytics
Ctrl + T: Go to Maintenance
Esc: Close modal windows
F5: Refresh current page

Mobile Access
FactoryBrain AI is responsive and works on mobile devices:

Use landscape orientation for best experience
Charts may be simplified on small screens
All core functionality available
Touch gestures supported

Getting Help
In-App Help

Hover over question mark icons for tooltips
Click "Help" in user menu for documentation
Use search function to find specific features


System Requirements
Browsers:

Chrome 90+
Firefox 88+
Safari 14+
Edge 90+

Network:

Minimum 5 Mbps internet connection
WebSocket support required
HTTPS enabled

Display:

Minimum resolution: 1280x720
Recommended: 1920x1080 or higher

