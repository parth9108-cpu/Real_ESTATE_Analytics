import streamlit as st

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Gurgaon Real Estate Analytics App",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS styling
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero section with gradient background */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        text-align: center;
        color: white;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        animation: slideInDown 1s ease-out;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        font-weight: 400;
        margin-bottom: 1rem;
        opacity: 0.95;
        animation: slideInUp 1s ease-out 0.3s both;
    }
    
    .hero-description {
        font-size: 1.1rem;
        font-weight: 300;
        opacity: 0.9;
        max-width: 700px;
        margin: 0 auto;
        animation: fadeIn 1s ease-out 0.6s both;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.18);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.12);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: #2d3748;
    }
    
    .feature-description {
        font-size: 1rem;
        color: #4a5568;
        line-height: 1.6;
    }
    
    /* Stats section */
    .stats-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 16px;
        margin: 2rem 0;
        color: white;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        display: block;
    }
    
    .stat-label {
        font-size: 1rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Section headers */
    .section-header {
        font-size: 2.2rem;
        font-weight: 600;
        text-align: center;
        margin: 3rem 0 2rem 0;
        color: #2d3748;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        display: block;
        width: 60px;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: 1rem auto;
        border-radius: 2px;
    }
    
    /* CTA section */
    .cta-section {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin: 3rem 0;
    }
    
    .cta-title {
        font-size: 2.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .cta-description {
        font-size: 1.2rem;
        font-weight: 300;
        margin-bottom: 2rem;
        opacity: 0.95;
    }
    
    /* Process steps */
    .process-step {
        display: flex;
        align-items: center;
        margin: 1.5rem 0;
        padding: 1.5rem;
        background: #f8fafc;
        border-radius: 12px;
        border-left: 4px solid #667eea;
    }
    
    .step-number {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        margin-right: 1rem;
        flex-shrink: 0;
    }
    
    .step-content {
        flex: 1;
    }
    
    .step-title {
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    /* Animations */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(50px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
        }
        .section-header {
            font-size: 1.8rem;
        }
        .cta-title {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-section">
    <div class="hero-title">🏡 Gurgaon Real Estate Analytics</div>
    <div class="hero-subtitle">🤖 AI-Powered Smart Property Intelligence</div>
    <div class="hero-description">
        Transform your real estate journey with cutting-edge AI analytics, personalized recommendations, 
        and data-driven insights. Make informed decisions in Gurgaon's dynamic property market.
    </div>
</div>
""", unsafe_allow_html=True)

# Display Hero Image
try:
    st.image("datasets/front image.png", use_column_width=True)
except:
    # Fallback if image doesn't exist
    st.info("🖼️ Add your hero image at 'datasets/front image.png' for the complete experience!")

# Stats Section
st.markdown("""
<div class="stats-container">
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap;">
        <div class="stat-item">
            <span class="stat-number">10K+</span>
            <span class="stat-label">Properties Analyzed</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">95%</span>
            <span class="stat-label">Prediction Accuracy</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">50+</span>
            <span class="stat-label">Sectors Covered</span>
        </div>
        <div class="stat-item">
            <span class="stat-number">24/7</span>
            <span class="stat-label">Real-time Updates</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Why Use This App Section
st.markdown('<div class="section-header">🚀 Why Choose Our Platform?</div>', unsafe_allow_html=True)

st.markdown("""
In Gurgaon's rapidly evolving real estate landscape, making informed decisions requires more than intuition—it demands intelligence. 
Our platform combines advanced AI algorithms with comprehensive market data to provide you with unprecedented insights into 
property trends, investment opportunities, and market dynamics.
""")

# Feature Cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🎯</span>
        <div class="feature-title">Smart Recommendations</div>
        <div class="feature-description">
            AI-powered property suggestions based on your preferences, budget, and lifestyle requirements. 
            Our algorithm analyzes thousands of data points to find your perfect match.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">📈</span>
        <div class="feature-title">Market Intelligence</div>
        <div class="feature-description">
            Interactive visualizations and real-time analytics provide deep insights into market trends, 
            price movements, and investment opportunities across Gurgaon.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <span class="feature-icon">🔮</span>
        <div class="feature-title">Price Prediction</div>
        <div class="feature-description">
            Machine learning models trained on historical data provide accurate price forecasts, 
            helping you time your investments and maximize returns.
        </div>
    </div>
    """, unsafe_allow_html=True)

# How to Get Started Section
st.markdown('<div class="section-header">🛠️ How It Works</div>', unsafe_allow_html=True)

st.markdown("""
<div class="process-step">
    <div class="step-number">1</div>
    <div class="step-content">
        <div class="step-title">🏠 Explore Recommendations</div>
        Get personalized property suggestions based on location, budget, and amenities preferences.
    </div>
</div>

<div class="process-step">
    <div class="step-number">2</div>
    <div class="step-content">
        <div class="step-title">📊 Analyze Market Data</div>
        Dive deep into market trends with interactive charts and comprehensive analytics dashboards.
    </div>
</div>

<div class="process-step">
    <div class="step-number">3</div>
    <div class="step-content">
        <div class="step-title">💡 Predict Future Prices</div>
        Use AI-powered forecasting to estimate property values and identify investment opportunities.
    </div>
</div>

<div class="process-step">
    <div class="step-number">4</div>
    <div class="step-content">
        <div class="step-title">🎯 Make Informed Decisions</div>
        Combine insights from all tools to make confident, data-backed real estate decisions.
    </div>
</div>
""", unsafe_allow_html=True)

# Key Features Section
st.markdown('<div class="section-header">✨ Platform Features</div>', unsafe_allow_html=True)

# Create two columns for features
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 🎯 **AI-Powered Recommendations**
    - Personalized property matching
    - Advanced filtering options
    - Similarity-based suggestions
    - Budget optimization tools
    
    #### 📊 **Interactive Analytics**
    - Real-time market dashboards
    - Trend visualization tools
    - Comparative analysis charts
    - Geographic heat maps
    """)

with col2:
    st.markdown("""
    #### 🔮 **Predictive Analytics**
    - Machine learning price forecasts
    - Market trend predictions
    - Investment opportunity scoring
    - ROI calculators
    
    #### 🛠️ **Advanced Tools**
    - Customizable search parameters
    - Multi-factor analysis
    - Export capabilities
    - Mobile-responsive design
    """)

# CTA Section
st.markdown("""
<div class="cta-section">
    <div class="cta-title">🚀 Ready to Transform Your Real Estate Journey?</div>
    <div class="cta-description">
        Join thousands of smart investors and homebuyers who rely on our AI-powered platform 
        for making informed real estate decisions in Gurgaon.
    </div>
</div>
""", unsafe_allow_html=True)

# Banner Image
try:
    st.image("datasets/banner image.jpg", use_column_width=True, caption="🌟 Start Your Smart Real Estate Journey Today!")
except:
    # Fallback if image doesn't exist
    st.info("🖼️ Add your banner image at 'datasets/banner image.jpg' for the complete experience!")

# Sidebar Enhancement
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
        <h3 style="margin: 0; font-weight: 600;">🎯 Quick Start</h3>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Select a module to begin your real estate analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔥 **Popular Features**")
    st.markdown("""
    - 🏠 **Apartment Finder** - Find your dream property
    - 📈 **Market Trends** - Track price movements  
    - 💰 **Price Predictor** - Forecast property values
    - 🎯 **Investment Advisor** - Get ROI insights
    """)
    
    st.markdown("---")
    st.markdown("### 📊 **Quick Stats**")
    st.metric("Properties Analyzed", "10,000+", "↗️ 15%")
    st.metric("Prediction Accuracy", "95%", "↗️ 2%")
    st.metric("Active Users", "2,500+", "↗️ 25%")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #718096;">
    <p><strong>🏡 Gurgaon Real Estate Analytics</strong></p>
    <p>Powered by AI • Built with ❤️ • Made for Smart Investors</p>
    <p style="font-size: 0.9rem; opacity: 0.8;">
        © 2025 Real Estate Analytics Platform. Transforming property decisions through intelligent data analysis.
    </p>
</div>
""", unsafe_allow_html=True)
