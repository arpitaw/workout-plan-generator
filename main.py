import streamlit as st
from src.llm_client import generate_workout_plan
from src.validators import validate_inputs
import config
from datetime import datetime


st.set_page_config(page_title="Workout Plan Generator", page_icon="💪", layout="centered")

st.title("Workout Plan Generator")
st.caption("Fill in your details to get a personalized weekly workout plan.")

with st.form("workout_form"):
    fitness_goal = st.selectbox("Fitness goal", config.FITNESS_GOALS)
    experience_level = st.selectbox("Experience level", config.EXPERIENCE_LEVELS)
    days_per_week = st.slider("Days available per week", min_value=1, max_value=7, value=3)
    equipment_access = st.selectbox("Equipment access", config.EQUIPMENT_OPTIONS)
    injuries_limitations = st.text_area(
        "Injuries or limitations (optional)",
        placeholder="e.g. bad knees, no overhead pressing, lower back sensitivity",
    )
    
    col1, col2 = st.columns(2)
    with col1:
        submitted = st.form_submit_button("Generate Plan")
    with col2:
        regenerate_submitted = st.form_submit_button("Regenerate Plan")

# Check which button was pressed
button_pressed = None
if submitted:
    button_pressed = "generate"
elif regenerate_submitted:
    button_pressed = "regenerate"

if button_pressed in ["generate", "regenerate"]:
    # Validate inputs
    is_valid, error_message = validate_inputs(
        fitness_goal=fitness_goal,
        experience_level=experience_level,
        days_per_week=days_per_week,
        equipment_access=equipment_access,
    )

    if not is_valid:
        st.warning(error_message)
    else:
        try:
            with st.spinner("Generating your workout plan..."):
                plan = generate_workout_plan(
                    fitness_goal=fitness_goal,
                    experience_level=experience_level,
                    days_per_week=days_per_week,
                    equipment_access=equipment_access,
                    injuries_limitations=injuries_limitations,
                )
            
            # Store the generated plan in session state
            st.session_state["last_plan"] = plan
            st.session_state["plan_metadata"] = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "fitness_goal": fitness_goal,
                "experience_level": experience_level,
                "days_per_week": days_per_week,
                "equipment_access": equipment_access
            }
            
            st.success(f"✅ Plan {button_pressed}d successfully!")

        except RuntimeError as re:
            st.error(str(re))
            st.info("Please check your API key, network connection, or try again in a moment.")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

# Always show the plan if it exists in session state
if "last_plan" in st.session_state:
    st.divider()
    st.markdown("### Your Weekly Plan")
    
    # Show metadata
    if "plan_metadata" in st.session_state:
        meta = st.session_state["plan_metadata"]
        st.caption(
            f"**Goal:** {meta['fitness_goal']} | "
            f"**Level:** {meta['experience_level']} | "
            f"**Days:** {meta['days_per_week']} | "
            f"**Equipment:** {meta['equipment_access']} | "
            f"Generated: {meta['timestamp']}"
        )
    
    # Display the plan
    st.markdown(st.session_state["last_plan"])
    
    # Action buttons after plan generation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download as TXT file
        txt_filename = f"workout_plan_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        st.download_button(
            label="📥 Download as TXT",
            data=st.session_state["last_plan"],
            file_name=txt_filename,
            mime="text/plain",
        )
    
    with col2:
        # Download as Markdown file
        md_content = f"# Workout Plan\n\n**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n## Plan\n{st.session_state['last_plan']}"
        md_filename = f"workout_plan_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        st.download_button(
            label="📝 Download as MD",
            data=md_content,
            file_name=md_filename,
            mime="text/markdown",
        )
    
    with col3:
        # Swap exercise feature
        if st.button("🔄 Swap an Exercise", use_container_width=True):
            st.session_state["show_swap"] = not st.session_state.get("show_swap", False)
    
    # Show swap UI if enabled
    if st.session_state.get("show_swap", False):
        st.divider()
        st.markdown("#### 🔄 Swap an Exercise")
        
        # Extract exercises from the plan (simple regex-less approach)
        lines = st.session_state["last_plan"].split('\n')
        exercise_lines = [line for line in lines if ':' in line and any(word in line.lower() for word in ['squat', 'push', 'pull', 'press', 'curl', 'row', 'lunge'])]
        
        if exercise_lines:
            exercise_to_swap = st.selectbox(
                "Select an exercise to swap:",
                exercise_lines,
                key="swap_select"
            )
            
            swap_reason = st.text_input(
                "Why swap this exercise? (optional)",
                placeholder="e.g. 'too intense', 'no equipment', 'bad fit'"
            )
            
            if st.button("Generate Alternative", key="swap_generate"):
                with st.spinner("Finding a better exercise..."):
                    swap_prompt = f"Suggest a direct alternative for '{exercise_to_swap}'. User's reason: '{swap_reason}'. Keep same muscle group, similar difficulty. Format: 'Alternative: [exercise] - sets x reps (reason)'"
                    
                    # Reuse the same llm_client but adjust the prompt for just one exercise
                    try:
                        from groq import Groq
                        client = Groq(api_key=config.GROQ_API_KEY)
                        
                        response = client.chat.completions.create(
                            model=config.GROQ_MODEL,
                            messages=[
                                {"role": "system", "content": "You are a fitness expert suggesting exercise alternatives."},
                                {"role": "user", "content": swap_prompt}
                            ],
                            temperature=0.7,
                            max_tokens=200,
                        )
                        
                        alternative = response.choices[0].message.content if response.choices else ""
                        if alternative:
                            st.success(f"**Alternative:** {alternative}")
                            st.info("Copy and replace this in your plan above.")
                        else:
                            st.warning("Could not generate an alternative.")
                    except Exception:
                        st.error("Failed to generate alternative.")
        else:
            st.info("Could not identify exercises automatically. Try the regenerate button instead.")

elif button_pressed is None:
    # Initial state with no plan yet
    st.info("👈 Fill out the form and click 'Generate Plan' to create your workout.")
else:
    # Form was submitted but no plan in session state (likely an error)
    st.warning("Plan generation failed or was cancelled.")

with st.expander("Setup Instructions"):
    st.code(
        """# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key in .env
GROQ_API_KEY=your_api_key_here

# 3. Run the app
streamlit run main.py
""",
        language="bash",
    )
