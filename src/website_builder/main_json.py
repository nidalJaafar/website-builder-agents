from src.website_builder.graphs.json_parser_graph import build_json_parser_graph
from src.website_builder.models.state_models import JsonDecoderState


def run_json_parser():
    print("\nStarting JSON Parser...")
    print("=" * 50)

    json_parser = build_json_parser_graph()

    initial_state = JsonDecoderState(
        parsed_input_JSON={},
        parsed_text=[]
    )

    try:
        for step in json_parser.stream(initial_state):
            for node_name, state_update in step.items():
                print(f"Node: {node_name}")
                if "parsed_input_JSON" in state_update and state_update["parsed_input_JSON"]:
                    print(f"  Parsed JSON: {state_update['parsed_input_JSON']}")
                if "parsed_text" in state_update and state_update["parsed_text"]:
                    last_message = state_update["parsed_text"][-1]
                    print(f"  Output: {last_message.content}")
                print("=" * 50)

    except Exception as e:
        print(f"JSON Parser error: {e}")


def main():
    print("JSON Parser System")
    print("=" * 50)
    run_json_parser()


if __name__ == "__main__":
    main()
