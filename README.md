# LeadGenerationwithAI
# MarketingLeads With AI
# B2B & B2C Leads With AI
A powerful lead generation application that leverages Groq's advanced language models to find and validate potential business leads, complete with a modern Streamlit interface for easy interaction.

Features

- 🎯 Real-time lead generation using Groq's advanced LLMs
- 🔍 Smart lead search with detailed information:
  - Full name and position
  - Company details and location
  - Verified LinkedIn profiles and contact information
  - Relevance assessment for each lead
- 💬 Interactive Lead Generation Assistant for:
  - Lead generation strategies
  - Marketing email templates
  - Business development tactics
  - Sales outreach methods
  - Lead qualification guidance
- 🎨 Modern, user-friendly Streamlit interface
- ✅ LinkedIn profile validation
- 🔐 Secure API key management with environment variables
 Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `.env` file in the project root and add your Groq API key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

Usage

1. **Lead Generation**:

   - Enter your search criteria in the lead generation section
   - Get detailed, verified leads with complete professional information
   - Each lead includes verified LinkedIn profiles and contact details

2. Lead Generation Assistant**:
   - Get expert advice on lead generation and outreach
   - Generate customized email templates
   - Receive strategic guidance for lead qualification
   - Analyze market insights and competitor information

 Security Notes

- Store your Groq API key in the `.env` file (never commit this file)
- The application automatically loads environment variables securely
- All API requests are made with proper authentication
