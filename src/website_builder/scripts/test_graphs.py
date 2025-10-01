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

    sample_requirements = """User: i want to build a website for my clothing shop
Agent: What type of clothing shop is this? (For example: men's fashion, women's apparel, children's clothing, sportswear, vintage, etc.)
User: men's fashion
Agent: What should the website accomplish? (For example: sell products online, showcase your collection, generate leads, build brand awareness, etc.)
User: sell production online and showcase collection
Agent: What are the main sections you need on the website? (For example: Home, Shop, About, Contact, Lookbook, etc.)
User: all
Agent: Let me clarify - when you say "all," do you mean you want all of these sections:
- Home (main landing page)
- Shop (product catalog and shopping)
- About (your brand story)
- Contact (contact information and form)
- Lookbook (style inspiration and collection showcase)

Or are there other specific sections you'd like to include?
User: yes
Agent: What specific content should go in the About section? (For example: your brand story, mission, team information, company history, etc.)
User: team information
Agent: What contact information should be included on the website? (For example: phone number, email address, physical address, social media links, contact form, etc.)
User: phone number: 7123456
Agent: Here's what I gathered:
- Business: Men's fashion clothing shop
- Purpose: Sell products online and showcase collection
- Sections: Home, Shop, About, Contact, Lookbook
- Key content: About section will include team information
- Contact info: Phone number 7123456

Is this complete enough to start building your website, or would you like to add any design preferences, specific content for other sections, or additional contact details?
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

    sample_tasks = [
  {
    "id": "TASK_001",
    "title": "Create Multi-Page Project Structure and Core HTML Pages",
    "description": "Create complete project directory structure (website_project/css/, website_project/js/, website_project/images/) and all main HTML pages: index.html (Home), shop.html (Shop), about.html (About), contact.html (Contact), lookbook.html (Lookbook). Each page must include: sophisticated semantic HTML5 structure with ARIA landmarks, responsive meta tags, Open Graph meta data, consistent header with animated navigation (logo + menu), hero section with brand messaging, main content area with section-specific placeholders, and semantic footer with contact info. Header navigation must link correctly between all pages. Include phone number 7123456 in contact page and footer.",
    "files": ["website_project/index.html", "website_project/shop.html", "website_project/about.html", "website_project/contact.html", "website_project/lookbook.html", "website_project/css/", "website_project/js/", "website_project/images/"],
    "success_criteria": "All 5 HTML pages created with proper semantic structure, consistent navigation linking between pages, phone number included in contact page, all directories exist, pages validate as HTML5 with proper meta tags",
    "dependencies": "None"
  },
  {
    "id": "TASK_002",
    "title": "Implement Advanced CSS Framework with Sophisticated Styling System",
    "description": "Create website_project/css/styles.css with comprehensive CSS framework featuring: CSS Grid master layout system, custom CSS properties for brand colors and typography, advanced responsive design with mobile-first approach using clamp() for fluid typography, sophisticated animations using @keyframes for micro-interactions, glassmorphism effects for modern UI elements, advanced hover states with transform3d transitions, parallax scrolling capabilities, and intersection observer-ready animation classes. Include specific styling for: navigation animations, hero section gradients, product card layouts, team member displays, and lookbook masonry grid.",
    "files": ["website_project/css/styles.css"],
    "success_criteria": "Complete CSS framework with modern styling techniques, responsive design system, animation classes, custom properties for consistent theming, ready to enhance all HTML pages",
    "dependencies": "TASK_001"
  },
  {
    "id": "TASK_003",
    "title": "Build Sophisticated JavaScript Interactions and E-commerce Functionality",
    "description": "Create website_project/js/main.js with advanced JavaScript features: smooth page transitions between multi-page navigation, product filtering system for shop page with debounced search, interactive image galleries for lookbook with touch gesture support, team member modal displays for about page, real-time form validation for contact page with custom styling, shopping cart functionality with local storage persistence, and intersection observer animations for scroll-triggered content reveals. Implement event delegation for optimal performance and progressive enhancement approach.",
    "files": ["website_project/js/main.js"],
    "success_criteria": "JavaScript provides seamless multi-page navigation, functional product filtering, interactive galleries, form validation, shopping cart functionality, and scroll animations across all pages",
    "dependencies": "TASK_001, TASK_002"
  },
  {
    "id": "TASK_004",
    "title": "Create Page-Specific Content and Advanced Interactive Elements",
    "description": "Enhance each HTML page with sophisticated content structures: Home page with featured products carousel and brand storytelling sections, Shop page with product grid featuring filtering by category/size/price with smooth animations, About page with team member cards that reveal detailed bios on interaction, Contact page with multi-step form and real-time validation feedback, Lookbook page with masonry grid layout and full-screen image modal viewing. Implement CSS Grid asymmetrical layouts, overlapping elements, and magazine-style designs for visual sophistication.",
    "files": ["website_project/index.html", "website_project/shop.html", "website_project/about.html", "website_project/contact.html", "website_project/lookbook.html", "website_project/css/styles.css", "website_project/js/main.js"],
    "success_criteria": "All pages feature advanced interactive elements, sophisticated layouts, smooth animations, and professional men's fashion aesthetic with complete e-commerce functionality",
    "dependencies": "TASK_001, TASK_002, TASK_003"
  },
  {
    "id": "TASK_005",
    "title": "Final Optimization, Performance Enhancements and SEO Implementation",
    "description": "Optimize all files for production: minify CSS and JavaScript, implement lazy loading for images, add comprehensive SEO meta tags including structured data for products, ensure WCAG 2.1 AA accessibility compliance, optimize navigation for screen readers, implement service worker for offline functionality, add social media sharing capabilities, and perform cross-browser testing. Include performance optimizations like image compression recommendations and critical CSS inlining.",
    "files": ["website_project/index.html", "website_project/shop.html", "website_project/about.html", "website_project/contact.html", "website_project/lookbook.html", "website_project/css/styles.css", "website_project/js/main.js"],
    "success_criteria": "Website achieves high performance scores, full accessibility compliance, comprehensive SEO implementation, cross-browser compatibility, and professional production readiness",
    "dependencies": "TASK_001, TASK_002, TASK_003, TASK_004"
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
