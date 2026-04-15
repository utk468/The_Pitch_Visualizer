#  The Pitch Visualizer | AI Storyboard Pro

**The Pitch Visualizer** is a high-performance, node-based orchestration service that transforms narrative sales pitches into cinematic, multi-panel storyboards in seconds. 

By leveraging **LangGraph** for workflow reasoning and **Parallel SDXL Generation**, it eliminates the creative bottleneck between a conceptual "pitch" and a visual "vision."

---

##  The Achievement: What’s Inside
We have transformed a standard narrative tool into a production-ready creative suite:

###  Performance & Parallelism
*   **Parallel Image Synthesis**: Optimized with `asyncio.gather`, the engine triggers multiple **Stable Diffusion XL** instances simultaneously, reducing storyboard generation time by up to 70%.
*   **Intelligent Refinement**: Uses **Groq (Llama-3.3-70b)** to intelligently deconstruct text into logical visual beats and then "over-engineer" them into detailed, expert-level AI prompts.

###  Advanced LangGraph Architecture
The system uses a sophisticated linear graph to ensure narrative continuity:
1.  **Deconstructor Node**: Segments raw text into 3-5 distinct visual scenes.
2.  **Refiner Node**: Transforms scenes into high-fidelity visual descriptions (Lighting, Camera Angle, Composition).
3.  **Generator Node**: Orchestrates the HFU Inference Client for high-resolution image output.

###  Premium User Experience
*   **Cinematic Dashboard**: A custom-built, glassmorphic "Director's Cut" interface with a deep-black aesthetic and neon-orange accents.
*   **Interactive Storyboarding**: Features a "Compact Pro" grid with hover-to-expand text animations, allowing for rapid visual review.
*   **History Sidebar**: Full MongoDB persistence with thread management, item deletion, and authenticated session retrieval.

---

##  Technology Stack
- **Core Orchestration**: [LangGraph](https://langchain-ai.github.io/langgraph/) (Stateful Workflows)
- **High-Speed Inference**: [Groq](https://groq.com/) (Llama-3.3-70b-versatile)
- **Visual Engine**: [StabilityAI SDXL 1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0)
- **Database**: [MongoDB](https://www.mongodb.com/) (Motor/Async Driver)
- **Backend Framework**: FastAPI (High-performance Python)
- **Authentication**: JWT & Bcrypt (Secure Director Profiles)

---

##  Getting Started

### 1. Configure the Director's Cabinet
Create a `.env` file in the root directory:
```env
GROQ_API_KEY="your_groq_key"
HF_API_KEY="your_hf_token"
MONGODB_URI="your_mongo_uri"
DATABASE_NAME="pitch_visualizer_db"
JWT_SECRET_KEY="your_super_secret_key"
```

### 2. Launch the Service
```bash
pip install -r requirements.txt
python app.py
```
*The server will initialize at `http://localhost:8000`*


Deployment & Production
Ready for scale. The included render.yaml allows for instant deployment to high-availability environments with persistent volume support.
Live Demo: https://pitch-visualizer-izin.onrender.com
