import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Streamlit Page
st.set_page_config(page_title="Real Estate Analytics", layout="wide", page_icon="🏡")

# Initialize Groq client with environment variable
@st.cache_resource
def init_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Please set GROQ_API_KEY in your .env file")
        st.stop()
    return Groq(api_key=api_key)

client = init_groq_client()

# Function to get AI insights for graphs
def get_ai_insights(graph_type, data_description, user_question=None):
    """Generate AI insights for specific graphs"""
    try:
        if user_question:
            # Detailed analysis when user asks a question
            prompt = f"""
            You are a senior real estate data analyst and market research expert with 15+ years of experience in property market dynamics.
            
            CONTEXT: A user is examining a {graph_type} that displays {data_description}.
            USER QUESTION: "{user_question}"
            
            Provide a comprehensive, detailed analysis addressing:
            
            1. DIRECT ANSWER: Address the user's specific question clearly and thoroughly
            
            2. DETAILED VISUAL INTERPRETATION: 
               - What specific patterns, trends, clusters, or anomalies are visible
               - Statistical significance of observed patterns
               - Data distribution characteristics and outliers
            
            3. COMPREHENSIVE MARKET ANALYSIS:
               - Supply and demand dynamics revealed by this data
               - Market efficiency indicators and pricing patterns
               - Geographic or demographic insights (if applicable)
               - Seasonal or temporal trends (if applicable)
            
            4. INVESTMENT INTELLIGENCE:
               - Specific high-opportunity areas or segments
               - Risk assessment based on data patterns
               - Portfolio diversification strategies
               - Market timing considerations
               - Comparative value analysis
            
            5. STAKEHOLDER-SPECIFIC RECOMMENDATIONS:
               - First-time buyers: Entry strategies and budget considerations
               - Real estate investors: ROI opportunities and risk mitigation
               - Property developers: Market gaps and development opportunities
               - Market analysts: Key metrics and predictive indicators
            
            6. QUANTITATIVE INSIGHTS:
               - Reference specific data points, percentages, and ranges where relevant
               - Statistical correlations and their implications
               - Performance benchmarks and market comparisons
            
            7. RISK FACTORS & LIMITATIONS:
               - Potential risks or market vulnerabilities
               - Data limitations and what additional analysis is needed
               - External factors that could impact these trends
            
            8. ACTIONABLE NEXT STEPS:
               - Specific recommendations for immediate action
               - Due diligence focus areas
               - Market monitoring strategies
            
            Provide a professional, data-driven analysis with specific insights. Target 500-600 words for comprehensive coverage.
            Use concrete examples and quantitative references where possible.
            """
        else:
            # Simple initial analysis - keep existing brief format
            prompt = f"""
            You are a real estate data analyst. Explain this {graph_type} showing {data_description} in simple terms.
            
            Focus on:
            1. What this visualization reveals about the real estate market
            2. Key patterns or trends visible
            3. What buyers/investors should know from this data
            4. Any notable outliers or interesting findings
            
            Keep it under 150 words and user-friendly.
            """
        
        # Set different parameters based on response type
        if user_question:
            temperature = 0.2  # More focused for detailed analysis
            max_tokens = 700   # More tokens for comprehensive response
        else:
            temperature = 0.7  # Original setting for brief insights
            max_tokens = 200   # Original token limit for brief responses
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analysis temporarily unavailable. Please try again. Error: {str(e)}"

# Function to create AI chat interface for each graph
def create_graph_chat(graph_id, graph_type, data_description):
    """Create a chat interface for specific graph"""
    chat_key = f"chat_history_{graph_id}"
    
    # Initialize chat history for this graph
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
        # Add initial AI insight (brief format)
        initial_insight = get_ai_insights(graph_type, data_description)
        st.session_state[chat_key].append({"role": "assistant", "content": initial_insight})
    
    # Create expandable section for AI insights
    with st.expander(f"🤖 AI Insights for {graph_type.title()}", expanded=False):
        
        # Add helpful tips for better questions
        st.info("💡 **Ask detailed questions** for comprehensive analysis! Example: 'Which sectors offer the best ROI for investors?'")
        
        # Display chat history with enhanced formatting
        for i, message in enumerate(st.session_state[chat_key]):
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.write(f"**Question:** {message['content']}")
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    if i == 0:  # First message is the brief overview
                        st.markdown("### 📊 Quick Overview")
                        st.write(message["content"])
                    else:  # Subsequent messages are detailed analysis
                        st.markdown("### 🔍 Detailed Analysis")
                        st.markdown(message["content"])
        
        # Enhanced chat input with suggestions
        st.markdown("---")
        
        # Quick question suggestions based on graph type
        suggestions = get_question_suggestions(graph_type)
        
        if suggestions:
            st.markdown("**💭 Suggested Questions for Detailed Analysis:**")
            cols = st.columns(len(suggestions) if len(suggestions) <= 3 else 3)
            for i, suggestion in enumerate(suggestions[:3]):  # Show max 3 suggestions
                with cols[i % 3]:
                    if st.button(suggestion, key=f"suggest_{graph_id}_{i}", help="Click for detailed analysis"):
                        # Add user message
                        st.session_state[chat_key].append({"role": "user", "content": suggestion})
                        
                        # Get detailed AI response
                        ai_response = get_ai_insights(graph_type, data_description, suggestion)
                        st.session_state[chat_key].append({"role": "assistant", "content": ai_response})
                        
                        # Rerun to show new messages
                        st.rerun()
        
        # Chat input
        user_input = st.chat_input(f"Ask detailed questions about this {graph_type}...", key=f"input_{graph_id}")
        
        if user_input:
            # Add user message
            st.session_state[chat_key].append({"role": "user", "content": user_input})
            
            # Get detailed AI response
            ai_response = get_ai_insights(graph_type, data_description, user_input)
            st.session_state[chat_key].append({"role": "assistant", "content": ai_response})
            
            # Rerun to show new messages
            st.rerun()

def get_question_suggestions(graph_type):
    """Get relevant question suggestions based on graph type"""
    suggestions_map = {
        "geographical scatter plot": [
            "Which sectors offer the best value for money and why?",
            "What geographic patterns indicate investment opportunities?",
            "How should location influence my buying strategy?"
        ],
        "bar chart": [
            "Which sectors have the highest growth potential?",
            "What market factors drive these price differences?",
            "How should I diversify my portfolio across sectors?"
        ],
        "3D scatter plot": [
            "What's the optimal size-price-bedroom combination for investment?",
            "Which property configurations offer the best value?",
            "How does bedroom count impact pricing dynamics?"
        ],
        "animated line chart": [
            "What seasonal patterns should investors monitor?",
            "Which sectors show the most consistent growth?",
            "When is the optimal time to buy or sell?"
        ],
        "violin plot": [
            "Should I invest in houses or flats based on this data?",
            "What explains these price distribution patterns?",
            "Where can I find the best property deals?"
        ],
        "heatmap": [
            "Which property-sector combinations are overvalued?",
            "Where are the market inefficiencies I can exploit?",
            "What's the best ROI strategy based on this data?"
        ],
        "box plot": [
            "Which sectors offer the most price stability?",
            "How can I identify overvalued properties?",
            "What are the risk levels across different sectors?"
        ],
        "scatter plot": [
            "What factors drive the price-area relationship?",
            "Are larger properties always better investments?",
            "Where are the pricing anomalies I should investigate?"
        ],
        "bubble chart": [
            "Which property clusters represent the best opportunities?",
            "How should property size influence my investment strategy?",
            "What are the investment sweet spots in this market?"
        ],
        "distribution histogram": [
            "How do houses and flats compare as investment options?",
            "What do these distribution patterns tell us about market health?",
            "Where should different investor types focus?"
        ]
    }
    return suggestions_map.get(graph_type, [
        "What key insights should I know about this data?",
        "What investment opportunities does this reveal?",
        "How should this influence my property decisions?"
    ])

# Sidebar Navigation
st.sidebar.header("🔍 Dashboard Navigation")
section = st.sidebar.radio("Go to", ["🏡 Overview", "📊 Data Visualization", "🔍 Insights"])

# Load Data
try:
    new_df = pd.read_csv('datasets/data_viz1.csv')
    feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))
except FileNotFoundError as e:
    st.error(f"Data file not found: {e}")
    st.stop()

new_df['total_area'] = new_df['built_up_area']

# Group Data for Map Visualization
group_df = new_df.groupby('sector').mean(numeric_only=True)[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']]

# --- Overview Section ---
if section == "🏡 Overview":
    st.title("🏡 Real Estate Analytics Dashboard")
    
    # Display Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏠 Total Properties", len(new_df))
    col2.metric("📍 Unique Sectors", new_df['sector'].nunique())
    col3.metric("💰 Avg Price (₹)", f"{new_df['price'].mean():,.0f}CR")
    col4.metric("📏 Avg Built-up Area", f"{new_df['built_up_area'].mean():,.0f} sq.ft")
    
    st.markdown("---")
    
    # Sector Price per Sqft Geomap
    st.subheader("🌍 Sector Price per Sqft Geomap")
    fig_map = px.scatter_mapbox(
        group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
        mapbox_style="carto-positron", width=1100, height=600, hover_name=group_df.index
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    # AI Chat for Map
    create_graph_chat("geomap", "geographical scatter plot", "price per square foot across different sectors with built-up area as bubble size")
    
    st.markdown("---")
    
    # Avg Price per Sector Bar Chart
    st.subheader("📊 Average Price per Sector")
    fig_bar = px.bar(group_df, x=group_df.index, y='price', color='price', title='Average Price per Sector',
                     color_continuous_scale='Viridis')
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # AI Chat for Bar Chart
    create_graph_chat("sector_bar", "bar chart", "average property prices across different sectors")
    
    st.markdown("---")

    # 3D Scatter Plot
    st.subheader("🔍 3D Scatter Plot: Price, Built-up Area & Bedrooms")
    fig_3d = px.scatter_3d(new_df, x='built_up_area', y='price', z='bedRoom',
                           color='property_type', title="Price vs Built-up Area vs Bedrooms",
                           color_continuous_scale='Viridis')
    
    fig_3d.update_layout(
        scene=dict(
            xaxis_title='Built-up Area (sq.ft)',
            yaxis_title='Price (₹)',
            zaxis_title='Bedrooms (BHK)'
        ),
        width=1000, height=700
    )
    
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # AI Chat for 3D Plot
    create_graph_chat("3d_scatter", "3D scatter plot", "relationship between property price, built-up area, and number of bedrooms, colored by property type")
    
    st.markdown("---")

    st.subheader("📈 Sector-wise Property Price Trend Over Time")
    new_df['month'] = (new_df.index % 12) + 1

    price_trend = new_df.groupby(['sector', 'month'], as_index=False)['price'].mean()

    fig_animated = px.line(
        price_trend, x="sector", y="price", color="sector",
        animation_frame="month", title="📈 Sector-wise Property Price Trend Over Time",
        labels={"price": "Avg Price (₹)", "sector": "Sector"},
        markers=True
    )

    st.plotly_chart(fig_animated, use_container_width=True)
    
    # AI Chat for Animated Line Chart
    create_graph_chat("price_trend", "animated line chart", "sector-wise property price trends over months showing market dynamics")

# --- Data Visualization Section ---
elif section == "📊 Data Visualization":
    st.title("📊 Data Visualization")
    
    st.markdown("---")
    
    # Property Price Distribution by Property Type (Violin Plot)
    st.subheader("🏡 Property Price Distribution by Property Type")
    fig_violin = px.violin(new_df, x='property_type', y='price', box=True, points="all", title="Property Price Distribution by Property Type")
    st.plotly_chart(fig_violin, use_container_width=True)
    
    # AI Chat for Violin Plot
    create_graph_chat("violin_plot", "violin plot", "property price distribution comparing houses vs flats with quartiles and data density")
    
    st.markdown("---")
    
    st.subheader("🏡 Price Distribution per Square Foot (Heatmap)")

    price_heatmap_data = new_df.pivot_table(values="price_per_sqft", index="sector", columns="property_type", aggfunc="mean")

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=price_heatmap_data.values,
        x=price_heatmap_data.columns,
        y=price_heatmap_data.index,
        colorscale='Viridis',
        colorbar=dict(title='Price per Sqft'),
    ))

    fig_heatmap.update_layout(
        title="Price Distribution per Square Foot",
        xaxis_title="Property Type",
        yaxis_title="Sector",
        height=600,
        width=1000,
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # AI Chat for Heatmap
    create_graph_chat("heatmap", "heatmap", "price per square foot across sectors and property types showing market heat zones")
    
    st.markdown("---")
    
    # Property Price Distribution by Sector
    st.subheader("📊 Price Distribution by Sector")
    fig_box = px.box(new_df, x='sector', y='price', color='sector', title='Price Distribution Across Sectors')
    st.plotly_chart(fig_box, use_container_width=True)
    
    # AI Chat for Box Plot
    create_graph_chat("box_plot", "box plot", "price distribution across sectors showing medians, quartiles, and outliers")

    st.markdown("---")
    
    # Price vs Built-up Area Scatter Plot
    st.subheader("📉 Price vs Built-up Area")
    fig_scatter = px.scatter(new_df, x="built_up_area", y="price", color="property_type", title="Price vs Built-up Area", trendline="ols")
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # AI Chat for Scatter Plot
    create_graph_chat("scatter_area", "scatter plot", "correlation between property price and built-up area with trend lines by property type")
    
    st.markdown("---")
    
    # Price vs Number of Bedrooms (BHK)
    st.subheader("🛏️ Price vs Number of Bedrooms")
    fig_bhk_scatter = px.scatter(new_df, x="bedRoom", y="price", color="property_type", title="Price vs Number of Bedrooms", trendline="ols")
    st.plotly_chart(fig_bhk_scatter, use_container_width=True)
    
    # AI Chat for BHK Scatter
    create_graph_chat("scatter_bhk", "scatter plot", "relationship between property price and number of bedrooms with trend analysis")
    
    st.markdown("---")
    
    # Price per Sqft vs Latitude/Longitude (Location Scatter)
    st.subheader("📍 Price per Sqft vs Location")
    fig_loc_scatter = px.scatter(new_df, x="longitude", y="latitude", color="price_per_sqft", size='built_up_area', hover_name="sector",
                                 title="Price per Sqft vs Latitude/Longitude", color_continuous_scale=px.colors.cyclical.IceFire)
    st.plotly_chart(fig_loc_scatter, use_container_width=True)
    
    # AI Chat for Location Scatter
    create_graph_chat("location_scatter", "location scatter plot", "geographical distribution of price per square foot showing location-based pricing patterns")

# --- Insights Section ---
elif section == "🔍 Insights":
    st.title("🔍 Insights")
    
    # BHK Price Comparison Box Plot
    st.subheader("💰 BHK Price Comparison")
    fig_bhk_price = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')
    st.plotly_chart(fig_bhk_price, use_container_width=True)
    
    # AI Chat for BHK Comparison
    create_graph_chat("bhk_comparison", "box plot", "price comparison across different BHK configurations (1-4 bedrooms)")
    
    st.markdown("---")
    
    # Side by Side Property Type Price Distribution
    st.subheader("📈 Property Type Price Distribution")
    fig_distplot, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(new_df[new_df['property_type'] == 'house']['price'], label='House', kde=True, color='blue', ax=ax)
    sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], label='Flat', kde=True, color='red', ax=ax)
    ax.legend()
    st.pyplot(fig_distplot)
    
    # AI Chat for Distribution Plot
    create_graph_chat("dist_plot", "distribution histogram", "price distribution comparison between houses and flats with density curves")
    
    st.markdown("---")
    
    # Average Price by Bedroom Count
    st.subheader("🏠 Average Price by BHK")
    avg_price_bhk = new_df.groupby('bedRoom')['price'].mean().reset_index()
    fig_avg_bhk = px.bar(avg_price_bhk, x='bedRoom', y='price', color='price', title='Average Price by BHK')
    st.plotly_chart(fig_avg_bhk, use_container_width=True)
    
    # AI Chat for Average Price BHK
    create_graph_chat("avg_bhk", "bar chart", "average property prices by bedroom count showing pricing tiers")
    
    st.markdown("---")
    
    # Price per Sqft by Property Type
    st.subheader("🏡 Price per Sqft by Property Type")
    fig_price_sqft = px.box(new_df, x="property_type", y="price_per_sqft", color="property_type", title="Price per Sqft by Property Type")
    st.plotly_chart(fig_price_sqft, use_container_width=True)
    
    # AI Chat for Price per Sqft
    create_graph_chat("price_sqft_type", "box plot", "price per square foot comparison between property types")
    
    st.markdown("---")

    st.subheader("💡 Cluster Analysis: Price vs. Built-up Area across Sectors")

    fig_bubble = px.scatter(
        new_df, x="built_up_area", y="price", size="price", color="sector",
        hover_name="sector", title="Property Price Clusters: Built-up Area vs. Price",
        labels={"built_up_area": "Built-up Area (sq.ft)", "price": "Price (₹)"},
        opacity=0.7, size_max=40
    )

    fig_bubble.update_layout(
        width=1000, height=600,
        xaxis_title="Built-up Area (sq.ft)",
        yaxis_title="Price (₹)",
        legend_title="Sector"
    )

    st.plotly_chart(fig_bubble, use_container_width=True)
    
    # AI Chat for Cluster Analysis
    create_graph_chat("cluster_analysis", "bubble chart", "property price clusters showing relationship between built-up area and price across different sectors")

# Enhanced Global AI Assistant in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("🧠 Expert AI Consultant")

# Global chat history
if "global_chat" not in st.session_state:
    st.session_state.global_chat = []

# Global chat input in sidebar
st.sidebar.markdown("*Get comprehensive real estate insights*")
global_input = st.sidebar.text_area(
    "Ask detailed questions:", 
    key="global_input",
    height=100,
    placeholder="e.g., What's the best investment strategy based on current market data?"
)

if st.sidebar.button("Get Expert Analysis", key="global_send") and global_input:
    # Add user message
    st.session_state.global_chat.append({"role": "user", "content": global_input})
    
    # Get comprehensive AI response for general questions
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": """You are a senior real estate market analyst and investment advisor with 20+ years of experience. 
                Provide comprehensive, data-driven insights about real estate markets, trends, investment strategies, and market analysis. 
                Always include specific actionable recommendations and consider different stakeholder perspectives (investors, buyers, developers).
                Be detailed and thorough, focusing on practical insights and strategic recommendations."""},
                {"role": "user", "content": global_input}
            ],
            temperature=0.2,
            max_tokens=500
        )
        ai_response = response.choices[0].message.content
        st.session_state.global_chat.append({"role": "assistant", "content": ai_response})
    except Exception as e:
        st.session_state.global_chat.append({"role": "assistant", "content": f"Expert consultation temporarily unavailable. Please try again. Error: {str(e)}"})

# Display enhanced global chat in sidebar
if st.session_state.global_chat:
    with st.sidebar:
        st.subheader("📋 Recent Expert Consultation:")
        for message in st.session_state.global_chat[-2:]:  # Show last 2 messages
            if message["role"] == "user":
                st.text_area("Your Question:", value=message['content'][:100] + ("..." if len(message['content']) > 100 else ""), height=50, disabled=True)
            else:
                st.text_area("Expert Response:", value=message['content'][:150] + ("..." if len(message['content']) > 150 else ""), height=80, disabled=True)
        
        if st.button("Clear History"):
            st.session_state.global_chat = []
            st.rerun()
