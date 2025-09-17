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

    sample_requirements = """
     User: i want to build a website for my coffee shop
Assistant: That's wonderful! A great website can really help your coffee shop stand out and connect with customers. I'd love to help you plan this out properly.

Let me start by asking: What are the main goals you want to achieve with this website? Are you primarily looking to showcase your coffee shop's atmosphere, take online orders, promote events, or something else entirely?
User: i want to showcase my coffee shop and my menu with my working hours and some pictures of the items i sell and my shop
Assistant: Perfect! That gives me a clear picture of your core needs. A beautiful showcase website that highlights your coffee shop's atmosphere, menu, and hours is exactly what many successful coffee shops use to build their brand.

Now, I'd like to understand your target audience better. Who are your main customers? Are they mostly local residents, office workers, students, tourists, or a mix of these groups? This will help us design the website to appeal to the right people.
User: everyone is welcome
Assistant: That's great - being welcoming to everyone is a wonderful approach for a coffee shop! 

Since you're aiming to appeal to a broad audience, I'd like to understand what makes your coffee shop unique. What's the atmosphere or special vibe you want to convey through your website? Are you more of a cozy neighborhood spot, a modern minimalist cafe, or do you have a particular theme or specialty that sets you apart?
User: it is very minimalist, and quite relaxing people can work, students can study, u can come grab a coffee and read your book
Assistant: That sounds like a wonderful atmosphere! A minimalist, relaxing space that serves as a productive work environment and peaceful retreat is exactly the kind of vibe that will translate beautifully to a website.

Now, let's talk about your menu. What types of items do you offer? Are we talking primarily coffee and pastries, or do you have a more extensive food menu? This will help us plan how to best showcase your offerings.
User: yes just coffee and some homemade pastries 
Assistant: Perfect! Keeping it simple with coffee and homemade pastries really aligns with that minimalist, focused approach.

For the menu section, would you like to feature:
- Just a simple list of coffee options and pastry items, or 
- More detailed descriptions with photos of each item to really showcase their quality and appeal?

This will help us design the most effective way to present your offerings to customers.
User: simple list, but i also want the prices and some pictures, it is not required for each item to have a picture maybe 4 or 5 for the entire menu
Assistant: Excellent - that's a great balance. A clean list with prices and a few high-quality photos will create that minimalist yet appealing presentation you're going for.

Now, let's talk about the practical information. What are your current operating hours? And do you have different hours for weekdays vs weekends, or any special holiday hours we should account for on the website?
User: i open all the week from 10 am to 6pm
Assistant: Great! Consistent hours make it easy for customers to remember when they can visit.

Now, let's talk about the visual aspect. Do you already have photos of your coffee shop interior and some of your coffee/pastry items that we could use, or would you need help with photography for the website?
User: yes i have them
Assistant: Perfect! Having your own photos will give the website a genuine, authentic feel that really captures your coffee shop's atmosphere.

Now, let's think about the structure. Besides the menu and hours, are there any other sections you'd like to include? For example:
- An "About Us" section telling your story
- Contact information/location details
- Social media links
- Any special features like seasonal drinks or loyalty programs?
User: yes all of these sound good
Assistant: Excellent! That gives us a really comprehensive structure for your website.

Now, let's talk about the technical side. Do you already have a domain name (website address) in mind for your coffee shop, or would you need help with that? Also, are you thinking of managing the website content yourself, or would you prefer someone to handle updates for you?
User: yes i have a domain name and yes someone will be managing it for me
Assistant: Perfect! Having the domain name sorted and someone to manage the website makes the process much smoother.

Now, let's talk about the design aesthetic. Since you mentioned your coffee shop is minimalist and relaxing, would you prefer:
- A very clean, modern design with plenty of white space
- A warmer, more cozy aesthetic with natural tones
- Or something else that captures your specific vibe?

Do you have any existing brand colors or a logo we should incorporate?
User: clean with modern design
Assistant: Perfect! A clean, modern design will beautifully complement your coffee shop's minimalist and relaxing atmosphere.

Now, let's talk about the final practical consideration. Do you have a specific timeline in mind for when you'd like the website to be completed? And are there any budget considerations or constraints we should be aware of as we plan this project?
User: yes immediately
Assistant: I understand you'd like to move forward quickly! Let me summarize everything we've discussed to make sure I have all your requirements correctly:

## Summary of Your Coffee Shop Website Requirements:

**Business Goals:**
- Showcase your minimalist, relaxing coffee shop atmosphere
- Display menu with coffee and homemade pastries
- Feature operating hours (10am-6pm daily)
- Include photos of shop interior and menu items

**Website Structure:**
- Home page with atmosphere showcase
- Simple menu list with prices (4-5 photos total)
- Hours section
- About Us section with your story
- Contact information/location
- Social media links

**Design Preferences:**
- Clean, modern design aesthetic
- Minimalist approach matching your shop's vibe
- Professional photography already available

**Technical Setup:**
- Domain name already secured
- Content management handled by someone else
- Quick implementation timeline

Does this summary cover everything you need? Are you ready to move forward with creating the project plan?
User: yes
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

    sample_tasks = [{'id': 'TASK_001', 'title': 'Create Project Foundation and Complete HTML Structure',
                     'description': 'Create directory structure and complete HTML file with all semantic sections: header, navigation, hero, menu, about, hours, contact, and footer with proper content structure',
                     'files': ['index.html', 'css/', 'js/', 'images/'],
                     'success_criteria': 'All directories exist, HTML has complete structure with all required sections, semantic HTML5 tags, and basic content placeholders',
                     'dependencies': 'None'},
                    {'id': 'TASK_002', 'title': 'Implement Complete CSS Foundation and Layout System',
                     'description': 'Create CSS reset, variables, typography, and complete layout system for all sections with modern minimalist design foundation',
                     'files': ['css/styles.css'],
                     'success_criteria': 'CSS file contains complete reset, CSS variables for colors/typography, base styles, and layout structure for all sections',
                     'dependencies': 'TASK_001'},
                    {'id': 'TASK_003', 'title': 'Build Complete Header and Navigation System',
                     'description': 'Implement complete header with logo space, responsive navigation menu, and mobile hamburger functionality with CSS styling',
                     'files': ['index.html', 'css/styles.css'],
                     'success_criteria': 'Header section complete with responsive navigation, mobile menu functionality, and proper styling matching minimalist design',
                     'dependencies': 'TASK_002'},
                    {'id': 'TASK_004', 'title': 'Create Hero Section and Atmosphere Showcase',
                     'description': 'Build hero section with background image placeholder, compelling headline, and atmosphere description with complete styling',
                     'files': ['index.html', 'css/styles.css'],
                     'success_criteria': 'Hero section complete with image container, headline, descriptive text, and responsive styling for atmosphere showcase',
                     'dependencies': 'TASK_003'},
                    {'id': 'TASK_005', 'title': 'Implement Complete Menu Section with Pricing',
                     'description': 'Create menu section with coffee and pastry categories, item lists with prices, and image placeholders for 4-5 featured items',
                     'files': ['index.html', 'css/styles.css'],
                     'success_criteria': 'Menu section complete with categorized items, prices, image containers, and clean minimalist styling matching requirements',
                     'dependencies': 'TASK_004'}, {'id': 'TASK_006', 'title': 'Build About Us and Hours Sections',
                                                   'description': 'Create About Us section with story content and Hours section with daily schedule (10am-6pm) including proper styling',
                                                   'files': ['index.html', 'css/styles.css'],
                                                   'success_criteria': 'About section with complete story content and Hours section with clear schedule display, both properly styled',
                                                   'dependencies': 'TASK_005'},
                    {'id': 'TASK_007', 'title': 'Implement Contact Section and Footer',
                     'description': 'Create contact section with location info and footer with social media links, copyright, and complete styling',
                     'files': ['index.html', 'css/styles.css'],
                     'success_criteria': 'Contact section with location details and footer with social media links, both fully styled and responsive',
                     'dependencies': 'TASK_006'},
                    {'id': 'TASK_008', 'title': 'Add Responsive Design and Mobile Optimization',
                     'description': 'Implement complete responsive design system with media queries for all breakpoints and mobile optimization',
                     'files': ['css/styles.css'],
                     'success_criteria': 'Complete responsive design system with media queries ensuring proper display on all device sizes',
                     'dependencies': 'TASK_007'},
                    {'id': 'TASK_009', 'title': 'Add JavaScript Interactivity and Final Polish',
                     'description': 'Implement smooth scrolling, mobile menu functionality, and final polish animations with vanilla JavaScript',
                     'files': ['js/script.js', 'index.html', 'css/styles.css'],
                     'success_criteria': 'JavaScript file with smooth scrolling, mobile menu toggle, and final interactive enhancements complete',
                     'dependencies': 'TASK_008'},
                    {'id': 'TASK_010', 'title': 'Final Validation and Performance Optimization',
                     'description': 'Perform final HTML/CSS validation, optimize images placeholders, and ensure cross-browser compatibility',
                     'files': ['index.html', 'css/styles.css', 'js/script.js'],
                     'success_criteria': 'All code validated, performance optimized, and ready for content population with actual images',
                     'dependencies': 'TASK_009'}]

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
