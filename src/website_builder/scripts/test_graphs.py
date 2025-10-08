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
        "title": "Project Setup and Basic HTML Structure",
        "description": "Create the core HTML files and the CSS directory structure. Each HTML file should have the basic boilerplate, including a `head` with a title, a `meta viewport` tag for responsiveness, and a link to the stylesheet. The `body` of each file should include placeholder `header`, `main`, and `footer` sections.",
        "files": [
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/index.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/menu.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/about.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/contact.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/css/style.css"
        ],
        "success_criteria": "All HTML files are created with basic boilerplate. The CSS file is created and linked correctly in all HTML files. Opening any HTML file in a browser shows a blank page with the correct title (e.g., 'Sweet Moments - Home').",
        "dependencies": "None"
    },
    {
        "id": "TASK_002",
        "title": "Implement Global Styles and Typography",
        "description": "In `css/style.css`, set up the foundational styles for the entire website. This includes defining the color palette as CSS variables, setting up a basic CSS reset, and importing and applying a font from Google Fonts. The body should have a soft cream background and warm brown text color.",
        "files": [
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/css/style.css"
        ],
        "details": {
            "implementation": "At the top of `style.css`, add an `@import` for the 'Montserrat' and 'Playfair Display' fonts from Google Fonts. Create a `:root` selector to define CSS variables for the color scheme. Apply a universal box-sizing rule and basic resets for margin and padding. Set default font styles on the `body` element.",
            "content": {
                "google_fonts_import": "@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Playfair+Display:wght@700&display=swap');",
                "css_variables": {
                    "--color-cream": "#F5F5DC",
                    "--color-brown": "#A0522D",
                    "--color-rose-gold": "#B76E79",
                    "--color-dark-brown": "#654321",
                    "--font-heading": "'Playfair Display', serif",
                    "--font-body": "'Montserrat', sans-serif"
                },
                "body_styles": {
                    "font-family": "var(--font-body)",
                    "background-color": "var(--color-cream)",
                    "color": "var(--color-dark-brown)",
                    "line-height": "1.6"
                },
                "heading_styles": {
                    "font-family": "var(--font-heading)",
                    "color": "var(--color-brown)",
                    "font-weight": "700"
                }
            }
        },
        "success_criteria": "The website's background is soft cream, default text is warm brown, and the specified Google Fonts are applied to headings and body text across all pages.",
        "dependencies": "TASK_001"
    },
    {
        "id": "TASK_003",
        "title": "Build Reusable Header and Navigation",
        "description": "Create a consistent header and navigation bar that will appear on all pages. The header should contain the bakery name 'Sweet Moments' as a logo/link to the homepage, and a navigation menu with links to Home, Menu, About, and Contact.",
        "files": [
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/index.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/menu.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/about.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/contact.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/css/style.css"
        ],
        "details": {
            "html_structure": "In each HTML file, add `<header class='main-header'>` containing a `div` for the logo `<a href='index.html' class='logo'>Sweet Moments</a>` and a `<nav>` with a `ul` of links.",
            "layout": "Use Flexbox on `.main-header`. Set `display: flex`, `justify-content: space-between`, and `align-items: center`.",
            "spacing": "The header should have `padding: 1rem 5%`.",
            "typography": "The logo `.logo` should use `font-family: var(--font-heading)`, `font-size: 1.8rem`, `color: var(--color-brown)`, and `text-decoration: none`. Nav links should have `font-size: 1rem` and `text-decoration: none`.",
            "colors": "Nav links color should be `var(--color-dark-brown)`.",
            "hover_states": "On hover, navigation links (`nav a`) should change color to `var(--color-rose-gold)` and have a `text-decoration: underline`."
        },
        "success_criteria": "A header appears on all four pages with the logo on the left and navigation links on the right. Links navigate to the correct pages and display hover effects.",
        "dependencies": "TASK_002"
    },
    {
        "id": "TASK_004",
        "title": "Build Reusable Footer",
        "description": "Create a consistent footer that will appear on all pages. The footer should contain the bakery's address and phone number.",
        "files": [
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/index.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/menu.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/about.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/contact.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/css/style.css"
        ],
        "details": {
            "html_structure": "In each HTML file, add `<footer class='main-footer'>` containing two paragraphs: one for the address and one for the phone number. Add a third paragraph for a copyright notice.",
            "content": {
                "address": "123 Baker Street, Portland",
                "phone": "555-0123",
                "copyright": "&copy; 2023 Sweet Moments"
            },
            "layout": "Use Flexbox for the footer content. Set `display: flex`, `justify-content: space-around`, and `align-items: center`.",
            "styling": "The footer should have a `background-color: var(--color-brown)`, `color: var(--color-cream)`, and `padding: 2rem 5%`. Text should be centered.",
            "typography": "Set `font-size: 0.9rem`."
        },
        "success_criteria": "A footer appears at the bottom of all four pages, displaying the correct contact information and copyright notice with the specified styling.",
        "dependencies": "TASK_002"
    },
    {
        "id": "TASK_005",
        "title": "Develop Home Page Content",
        "description": "Build the content for the home page (`index.html`). This includes a welcoming hero section and a 'Featured Pastries' section.",
        "files": [
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/index.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/css/style.css"
        ],
        "details": {
            "hero_section": {
                "html": "Create a `<section class='hero'>` with an `h1` ('Handcrafted Goodness, Baked with Love') and a `p` ('Welcome to Sweet Moments, where every bite is a memory.').",
                "layout": "Center the text horizontally and vertically. Use `display: flex`, `flex-direction: column`, `justify-content: center`, `align-items: center`.",
                "styling": "Give the section `min-height: 60vh` and `padding: 2rem`.",
                "typography": "`h1` should have `font-size: 3rem`, and `p` should have `font-size: 1.2rem`."
            },
            "featured_section": {
                "html": "Create a `<section class='featured-pastries'>` with an `h2` ('Our Featured Pastries') and a `div` container (`.pastry-cards`) for the items.",
                "cards_html": "Inside `.pastry-cards`, create three `div` elements with class `.card`. Each card should contain an `h3` (e.g., 'Artisanal Croissants'), a `p` ('Flaky, buttery, and baked to perfection.'), and a placeholder for an image `div` with a background color for now.",
                "layout": "Use Flexbox for `.pastry-cards` (`display: flex`, `justify-content: center`, `gap: 2rem`).",
                "card_styling": "Each `.card` should have `padding: 1.5rem`, `background-color: #FFFFFF`, `border-radius: 8px`, and a subtle `box-shadow: 0 4px 8px rgba(0,0,0,0.1)`."
            }
        },
        "success_criteria": "The home page displays a large, centered welcome message and a section below it with three styled cards representing featured pastries.",
        "dependencies": "TASK_003"
    },
    {
        "id": "TASK_006",
        "title": "Develop Menu Page Content",
        "description": "Build the content for the menu page (`menu.html`). Display all menu items and their prices in a clean, easy-to-read format.",
        "files": [
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/menu.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/css/style.css"
        ],
        "details": {
            "html_structure": "In `main`, add a `<section class='menu-section'>` with an `h1` ('Our Menu'). Inside, create a `div` with class `.menu-grid`.",
            "menu_items": [
                {
                    "name": "Croissants",
                    "price": "$3.50"
                },
                {
                    "name": "Sourdough Bread",
                    "price": "$6.00"
                },
                {
                    "name": "Chocolate Cake",
                    "price": "$25.00"
                },
                {
                    "name": "Cupcakes",
                    "price": "$4.00 each"
                }
            ],
            "item_html": "For each menu item, create a `div` with class `.menu-item` inside `.menu-grid`. Each `.menu-item` will contain an `h3` for the name and a `p` for the price.",
            "layout": "Use CSS Grid for `.menu-grid`: `display: grid`, `grid-template-columns: repeat(2, 1fr)`, `gap: 2rem`.",
            "styling": "Each `.menu-item` should have a `border-bottom: 2px dotted var(--color-brown)` and `padding-bottom: 1rem`. Use flexbox within `.menu-item` to align the name to the left and price to the right (`justify-content: space-between`)."
        },
        "success_criteria": "The menu page displays a title and a grid of all four menu items, each with its name and price clearly listed and styled as specified.",
        "dependencies": "TASK_003"
    },
    {
        "id": "TASK_007",
        "title": "Develop About Us Page Content",
        "description": "Build the content for the 'About Us' page (`about.html`). This page will have a title and a paragraph explaining the bakery's history.",
        "files": [
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/about.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/css/style.css"
        ],
        "details": {
            "html_structure": "Inside `main`, create a `<section class='about-section'>` with an `h1` ('Our Story') and a `p` tag.",
            "content": "The paragraph should contain the text: 'We are a family-owned bakery, proudly serving the Portland community with handcrafted pastries and breads since 1995. Our passion is creating delicious moments for you and your loved ones.'",
            "layout": "The section should have a `max-width: 800px`, `margin: 0 auto`, and `padding: 4rem 2rem`. Text should be centered.",
            "typography": "The `h1` should have `font-size: 2.5rem` and the `p` should have `font-size: 1.1rem` and `line-height: 1.8`."
        },
        "success_criteria": "The About Us page displays the title and paragraph with the specified content and styling, centered on the page.",
        "dependencies": "TASK_003"
    },
    {
        "id": "TASK_008",
        "title": "Develop Contact Page Layout and Form",
        "description": "Build the layout and static form for the contact page (`contact.html`). It will include contact details and a form for users to send a message.",
        "files": [
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/contact.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/css/style.css"
        ],
        "details": {
            "html_structure": "Inside `main`, create a `<section class='contact-section'>` with an `h1` ('Get In Touch'). Inside, create a `div` with class `.contact-container` that will hold two child divs: `.contact-info` and `.contact-form-container`.",
            "contact_info_html": "In `.contact-info`, add `h3` tags for 'Address' and 'Phone' with paragraphs containing '123 Baker Street, Portland' and '555-0123'.",
            "form_html": "In `.contact-form-container`, create a `<form id='contact-form'>` with `label` and `input` fields for Name (text), Email (email), a `textarea` for Message, and a `button` of type 'submit' with text 'Send Message'.",
            "layout": "Use CSS Grid for `.contact-container`: `display: grid`, `grid-template-columns: 1fr 1fr`, `gap: 3rem`.",
            "form_styling": "Inputs and textarea should have `width: 100%`, `padding: 0.75rem`, `margin-bottom: 1rem`, `border: 1px solid var(--color-brown)`, `border-radius: 4px`. The submit button should have `background-color: var(--color-rose-gold)`, `color: white`, `padding: 0.75rem 1.5rem`, `border: none`, `cursor: pointer`, and `transition: background-color 0.3s`.",
            "hover_states": "The submit button should darken slightly on hover (e.g., `filter: brightness(0.9)`)."
        },
        "success_criteria": "The contact page displays the address and phone number alongside a fully styled, but non-functional, contact form.",
        "dependencies": "TASK_003"
    },
    {
        "id": "TASK_009",
        "title": "Implement Contact Form Validation and Submission Feedback",
        "description": "Add JavaScript to handle the contact form. It should validate that all fields are filled and the email is valid. On successful submission, it should show a confirmation message.",
        "files": [
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/contact.html",
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/js/main.js"
        ],
        "details": {
            "setup": "Create the `js/main.js` file and link it at the bottom of `contact.html` using `<script src='js/main.js' defer></script>`.",
            "trigger": "The script will add an event listener to the form's `submit` event.",
            "functionality": [
                "1. Prevent the default form submission using `event.preventDefault()`.",
                "2. Get the values from the name, email, and message fields.",
                "3. **Validation:** Check if name is empty. Check if message is empty. Check if email is a valid format (using a simple regex like `/^\\S+@\\S+\\.\\S+$/`).",
                "4. **Error State:** If any field is invalid, add an 'error' class to the corresponding input (which can be styled in CSS with a red border) and display a small error message below it. Do not proceed.",
                "5. **Success State:** If all fields are valid, display a success message to the user (e.g., create a `p` element with text 'Thank you for your message!' and append it after the form). Then, clear the form fields."
            ]
        },
        "success_criteria": "Submitting the form with empty fields or an invalid email shows an error. Submitting a valid form prevents page reload, shows a success message, and clears the form.",
        "dependencies": "TASK_008"
    },
    {
        "id": "TASK_010",
        "title": "Implement Responsive Design",
        "description": "Add media queries to `css/style.css` to ensure the website is usable and looks elegant on mobile devices (e.g., screen widths below 768px).",
        "files": [
            "website_project/aecccfaf-f59f-402f-bb17-004b0c8ad189/css/style.css"
        ],
        "details": {
            "implementation": "Use a media query: `@media (max-width: 768px) { ... }`",
            "responsive_changes": [
                "**Header:** Change the flex-direction to `column` and center the items. The nav links should stack vertically.",
                "**Hero Section:** Decrease the `h1` font size to `2rem`.",
                "**Featured Pastries:** Change the flex-direction of `.pastry-cards` to `column` so cards stack vertically.",
                "**Menu Page:** Change the `.menu-grid` to a single column layout: `grid-template-columns: 1fr`.",
                "**Contact Page:** Change the `.contact-container` to a single column layout: `grid-template-columns: 1fr`."
            ]
        },
        "success_criteria": "When the browser window is resized to be narrower than 768px, the layout adjusts correctly: navigation stacks, grid layouts become single-column, and text is readable.",
        "dependencies": "TASK_009"
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
