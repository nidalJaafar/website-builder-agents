from dotenv import load_dotenv
import os

from langchain_core.messages import SystemMessage, HumanMessage

from website_builder.prompts.developer_prompts import developer_system_prompt
from website_builder.prompts.requirements_prompts import requirements_system_prompt
from website_builder.prompts.task_manager_prompts import task_manager_system_prompt


def setup_environment():
    """Ensure environment is properly loaded"""
    load_dotenv()
    if not os.getenv('DEEPSEEK_API_KEY'):
        print("ERROR: DEEPSEEK_API_KEY not found in environment")
        print("Make sure your .env file is in the project root")
        exit(1)


def print_section_header(title):
    """Print a clear section header"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_step_info(step_name, details=None):
    """Print step information clearly"""
    print(f"\n[{step_name}]")
    if details:
        print(f"  {details}")


def test_requirements():
    """Test the requirements graph in isolation"""
    setup_environment()
    print_section_header("REQUIREMENTS GRAPH TEST")

    from website_builder.graphs.requirements_graph import build_requirements_graph

    print("Building requirements graph...")
    app = build_requirements_graph()

    initial_state = {
        "requirements_messages": [SystemMessage(content=requirements_system_prompt())],
        "requirements_data": ""
    }

    try:
        print("Requirements graph execution:")
        app.invoke(initial_state)

    except Exception as e:
        print(f"ERROR: {e}")


def test_task_manager():
    """Test the task manager graph in isolation"""
    setup_environment()
    print_section_header("TASK MANAGER GRAPH TEST")

    from website_builder.graphs.task_manager_graph import build_task_manager_graph

    print("Building task manager graph...")
    app = build_task_manager_graph()

    sample_requirements = """User: i want to build a website for a coffee shop 
Agent: Great! Let's start with the basics. What's the name of your coffee shop?
User: Special Brew
Agent: Perfect! Special Brew sounds like a great name. 

What should the website accomplish for your coffee shop? For example:
- Show your menu and prices
- Allow online ordering
- Share your location and hours
- Tell your story/brand
- Something else?
User: show menu and prices, share location and hours
Agent: Got it - menu/prices and location/hours are the main goals.

What main sections do you need on the website? For example:
- Home page
- Menu page
- About us
- Contact/location
- Any others?
User: yes these sound fine
Agent: Great! Let's focus on the content for each section.

What specific content should go on the Menu page? For example:
- Coffee drinks (espresso, latte, etc.)
- Food items (pastries, sandwiches)
- Prices for each item
- Any special categories or featured items?
User: yes these are good, coffee drinks and food items, each item should have a price and an image
Agent: Perfect! Now for the Contact/Location section - what specific information should be included?

For example:
- Address
- Phone number
- Hours of operation
- Email address
- Social media links
- Map/directions
User: phone number: 71123456, hours: all weel from 10am to 7pm   
Agent: Great! Do you have any design preferences for the website? For example:

- Specific colors you'd like to use
- Any particular style (modern, rustic, minimalist, etc.)
- Websites you like as inspiration
- Logo or branding elements to incorporate
User: the website should be minimalistic and modern, use black white grey and pastel green         
Agent: Excellent! I have all the essential information. Here's what I gathered:

**Business**: Special Brew coffee shop
**Purpose**: Show menu/prices and share location/hours
**Sections**: Home, Menu, About us, Contact/location
**Key content**:
- Menu page: Coffee drinks and food items with prices and images
- Contact: Phone 71123456, hours 10am-7pm all week
**Design**: Minimalistic and modern using black, white, grey, and pastel green

Is this complete enough to start building your website?
User: yes
Agent: Perfect! I have everything needed to start building your Special Brew coffee shop website. The design will be minimalistic and modern with your chosen color scheme, featuring all the key sections and content you specified.

Good luck with your website project!
     """

    initial_state = {
        "requirements_data": sample_requirements,
        "tasks_messages": [SystemMessage(content=task_manager_system_prompt()),
                           HumanMessage(
                               content=f"Based on this requirements conversation, create a project plan: {sample_requirements}"
                           ), ],
        "parsed_tasks": []
    }

    print(f"Input requirements: {sample_requirements}")

    try:
        print("Executing task manager graph...")
        result = app.invoke(initial_state)

        task_count = len(result.get('parsed_tasks', []))
        print(f"\nGenerated {task_count} tasks:")

        for i, task in enumerate(result.get('parsed_tasks', [])):  # Show first 5
            task_title = task.get('title', 'Unknown Task')
            print(f"  {i + 1:2d}. {task_title}")

    except Exception as e:
        print(f"ERROR: {e}")


def test_developer():
    import asyncio
    asyncio.run(test_developer_async())


async def test_developer_async():
    """Test the developer graph in isolation"""
    setup_environment()
    print_section_header("DEVELOPER GRAPH TEST")

    from website_builder.graphs.developer_graph import build_developer_graph

    print("Building developer graph...")
    app = await build_developer_graph()

    sample_tasks = [
  {
    "id": "TASK_001",
    "title": "Create Complete HTML Structure and Content",
    "description": "Create index.html with full semantic structure: header with 'Special Brew' logo and navigation (Home, Menu, About Us, Contact), hero section with coffee shop branding, main content areas for all sections, contact information with phone (71123456) and hours (10am-7pm daily), and footer. Include placeholder comments for menu items and images.",
    "files": ["index.html"],
    "success_criteria": "HTML file exists with complete semantic structure, all navigation links, contact information with correct phone and hours, and placeholder content for all sections",
    "dependencies": "None"
  },
  {
    "id": "TASK_002",
    "title": "Create Complete CSS Styling and Layout",
    "description": "Create styles.css with minimalistic modern design using black, white, grey, and pastel green color scheme. Implement responsive grid layout, typography styling, navigation styling, section spacing, and mobile-first responsive design with breakpoints at 768px and 1024px. Ensure proper contrast and readability.",
    "files": ["css/styles.css"],
    "success_criteria": "CSS file provides complete styling for all HTML elements, responsive design works on mobile/tablet/desktop, color scheme is properly implemented, and layout is visually appealing",
    "dependencies": "TASK_001"
  },
  {
    "id": "TASK_003",
    "title": "Add Menu Content and Styling",
    "description": "Update index.html with complete menu section containing coffee drinks and food items, each with name, price, and image placeholder. Add specific CSS styling for menu items including grid layout, card design, and image containers. Include at least 6 coffee items and 4 food items with realistic pricing.",
    "files": ["index.html", "css/styles.css"],
    "success_criteria": "Menu section displays properly with items in responsive grid, each item has name/price/image area, styling matches overall design theme",
    "dependencies": "TASK_002"
  },
  {
    "id": "TASK_004",
    "title": "Add JavaScript Interactivity and Final Polish",
    "description": "Create script.js with smooth scrolling navigation, mobile menu toggle functionality, and any interactive elements. Perform final CSS optimizations for spacing, typography, and responsive behavior. Ensure all sections are properly aligned and the site is fully functional across devices.",
    "files": ["js/script.js", "css/styles.css"],
    "success_criteria": "Navigation works smoothly, mobile menu functions properly, site is fully responsive and polished, all interactive elements work as expected",
    "dependencies": "TASK_003"
  }
]

    initial_state = {
        "parsed_tasks": sample_tasks,
        "current_task_index": 0,
        "project_status": "in_progress",
        "developer_messages": [SystemMessage(content=developer_system_prompt())]
    }

    print(f"Testing with {len(sample_tasks)} sample task(s)")

    try:
        print("Streaming developer graph execution:")
        async for step in app.astream(initial_state, config={"recursion_limit": 5000}):
            print(step)
            for node_name, state_data in step.items():
                print_step_info(f"Node: {node_name}")

                # Print current task info
                if "current_task_index" in state_data:
                    task_index = state_data["current_task_index"]
                    print(f"  Current task index: {task_index}")

                # Print project status
                if "project_status" in state_data:
                    status = state_data["project_status"]
                    print(f"  Project status: {status}")

                # Print developer messages
                if "developer_messages" in state_data and state_data["developer_messages"]:
                    last_message = state_data["developer_messages"][-1]
                    message_type = type(last_message).__name__
                    print(f"  Last message type: {message_type}")

                    # Check for tool calls
                    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
                        for tool_call in last_message.tool_calls:
                            tool_name = tool_call.get('name', 'Unknown')
                            tool_id = tool_call.get('id', 'Unknown')
                            tool_args = tool_call.get('args', {})

                            print(f"  Tool called: {tool_name}")
                            print(f"  Tool arguments: {tool_args}")

                            # Look for the tool result in the messages
                            tool_result = None
                            if "developer_messages" in state_data:
                                for msg in state_data["developer_messages"]:
                                    # Check if this is a ToolMessage with matching tool_call_id
                                    if (hasattr(msg, 'tool_call_id') and
                                            hasattr(msg, 'content') and
                                            msg.tool_call_id == tool_id):
                                        tool_result = msg.content
                                        break

                            if tool_result:
                                print(f"  Tool result: {tool_result}")
                            else:
                                print(f"  Tool result: (not yet available)")
                    # In your test loop, add this check:
                    if type(last_message).__name__ == "ToolMessage":
                        print(f"  Tool result content: {last_message.content}")
                        print(f"  Tool call ID: {getattr(last_message, 'tool_call_id', 'None')}")

    except Exception as e:
        print(f"ERROR: {e}")


def test_orchestrator():
    """Test the full orchestrator"""
    setup_environment()
    print_section_header("ORCHESTRATOR GRAPH TEST")

    from website_builder.graphs.orchestrator_graph import build_orchestrator_graph

    print("Building orchestrator graph...")
    app = build_orchestrator_graph()

    initial_state = {
        "user_input": "",
        "current_phase": "starting",
        "requirements_output": "",
        "tasks_output": [],
        "development_output": "",
        "project_status": "starting",
        "final_result": ""
    }

    try:
        print("Executing orchestrator graph...")
        result = app.invoke(initial_state)

        print("\nOrchestrator execution completed")
        print(f"Final project status: {result.get('project_status', 'unknown')}")

        if result.get('final_result'):
            print(f"Final result: {result['final_result']}")

    except Exception as e:
        print(f"ERROR: {e}")
