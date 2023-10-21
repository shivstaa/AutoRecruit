import os
import subprocess
from dataclasses import dataclass

import fire

@dataclass
class InteractAI:
    """
    Interact.AI is a tool for building and deploying conversational AI applications.
    """

    def initialize_modals(self):
        modals_directory = "modals"
        modal_files = [f for f in os.listdir(modals_directory) if f.endswith("_modal.py")]

        session_name = "modals"
        subprocess.run(["tmux", "new-session", "-d", "-s", session_name])

        for i, modal_file in enumerate(modal_files):
            window_name = f"modal-{i}"
            script_path = os.path.join(modals_directory, modal_file)
            command = f"modal deploy {script_path}"

            if i == 0:
                subprocess.run(["tmux", "rename-window", "-t", f"{session_name}:0", window_name])
            else:
                subprocess.run(["tmux", "new-window", "-t", session_name, "-n", window_name])

            subprocess.run(["tmux", "send-keys", "-t", f"{session_name}:{window_name}", command, "C-m"])

        print(f"Deployment started in tmux session: {session_name}")
        print("Use 'tmux attach -t modals' to view the session.")
        print("Use 'Ctrl-b w' to navigate between windows within the session.")


if __name__ == "__main__":
    fire.Fire(InteractAI)
