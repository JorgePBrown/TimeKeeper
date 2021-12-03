# %%
import getpass
from commands import HelpCommand, ListCommand, NowCommand, StartCommand, TickCommand, EndCommand, RemoveCommand, StatCommand

fname = f"/home/{getpass.getuser()}/.timekeeper.txt"
# %%
def get_args(argv):
    ret = {}
    try:
        args, remainder =  getopt.getopt(argv, "hiln:", ["help", "amend", "duration="])
        ret = {k.replace("-", ""): v for k, v in args}
        ret["remainder"] = remainder
        ret["task"] = None if len(remainder) == 0 else remainder[0]
    except getopt.GetoptError as e:
        print(f"Error: {e.msg}\n")
    return ret

def execute(command, tasks, **args):
    commands = {
        "help": HelpCommand(), 
        "list": ListCommand(),
        "tick": TickCommand(),
        "start": StartCommand(),
        "end": EndCommand(),
        "now": NowCommand(),
        "rm": RemoveCommand(),
        "stat": StatCommand()
    }
    try:
        commands[command].exec(tasks, args)
    except KeyError:
        print("Unknown command.")
        execute("help")

# %%
if __name__ == '__main__':
    import sys
    import getopt
    from tasks import Task
    
    if sys.argv[1].startswith("-"):
        args = get_args(sys.argv[1:])
        if "-h" in args or "--help" in args:
            command = "help"
        else:
            command = None
    else:
        command = sys.argv[1]
        args = get_args(sys.argv[2:])

    try:
        with open(fname, "r") as f:
            tasks = Task.from_file(f)
    except FileNotFoundError:
        with open(fname, "w") as f:
            tasks = Task()
            tasks.to_file(f)

    execute(command, tasks, **args)

    with open(fname, "w") as f:    
        tasks.to_file(f)