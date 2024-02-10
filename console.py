#!/usr/bin/python3

"""Introducing the Console class, the cornerstone of the Airbnb Project
   serving as its primary entry point and central command hub."""


from cmd import Cmd
from models import storage
from models.engine.errors import *
import shlex
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.user import User
from models.state import State
from models.place import Place
from models.review import Review

classes = storage.models


class HBNBCommand(Cmd):

    """Executes a multitude of essential HBNB commands
    ensuring seamless functionality and efficient operation."""

    prompt = "(hbnb) "

    def do_EOF(self, args):
        """Terminates program in non-interactive mode."""
        return True

    def do_quit(self, args):
        """The 'quit' command closes the program."""
        return True

    def emptyline(self):
        """Override empty line to perform no action."""
        pass

    def do_destroy(self, arg):
        """Delete an instance of a model by specifying its ModelName and ID."""
        args, x = analyze(arg)

        if not x:
            print("** class name missing **")
        elif x == 1:
            print("** instance id missing **")
        elif x == 2:
            try:
                storage.delete_by_id(*args)
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")
        else:
            print("** Too many argument for destroy **")
            pass

    def do_create(self, args):

        """Create a new instance of a model.

        Usage: create ModelName

        Prints an error if name is missing or name doesn't exist.
        """

        args, x = analyze(args)

        if not x:
            print("** class name missing **")
        elif args[0] not in classes:
            print("** class doesn't exist **")
        elif x == 1:
            # temp = classes[args[0]]()
            temp = eval(args[0])()
            print(temp.id)
            temp.save()
        else:
            print("** Too many argument for create **")
            pass

    def do_show(self, arg):
        """Show an instance of a model based on its ModelName and id.

        Usage: show MyModel instance_id

        Prints error messages if either MyModel
        or instance_id is missing or if the provided MyModel
        or instance_id is incorrect.
        """

        args, x = analyze(arg)

        if not x:
            print("** class name missing **")
        elif x == 1:
            print("** instance id missing **")
        elif x == 2:
            try:
                inst = storage.find_by_id(*args)
                print(inst)
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")
        else:
            print("** Too many argument for show **")
            pass

    def do_update(self, arg):
        """Update an instance based on its id.

        Usage: update Model id field value

        Throws errors for missing arguments.
        """

        args, x = analyze(arg)
        if not x:
            print("** class name missing **")
        elif x == 1:
            print("** instance id missing **")
        elif x == 2:
            print("** attribute name missing **")
        elif x == 3:
            print("** value missing **")
        else:
            try:
                storage.update_one(*args[0:4])
            except ModelNotFoundError:
                print("** class doesn't exist **")
            except InstanceNotFoundError:
                print("** no instance found **")

    def do_all(self, args):

        """Usage: all or all <class> or <class>.all()

        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        """

        args, x = analyze(args)

        if x < 2:
            try:
                print(storage.find_all(*args))
            except ModelNotFoundError:
                print("** class doesn't exist **")
        else:
            print("** Too many argument for all **")
            pass

    def default(self, arg):
        """Override default method to handle class methods."""
        if '.' in arg and arg[-1] == ')':
            if arg.split('.')[0] not in classes:
                print("** class doesn't exist **")
                return
            return self.handle_class_methods(arg)
        return Cmd.default(self, arg)

    def handle_class_methods(self, arg):

        """Handle class methods, such as <cls>.all(), <cls>.show(), etc."""

        printable = ("all(", "show(", "count(", "create(")
        try:
            val = eval(arg)
            for x in printable:
                if x in arg:
                    print(val)
                    break
            return
        except AttributeError:
            print("** invalid method **")
        except InstanceNotFoundError:
            print("** no instance found **")
        except TypeError as te:
            field = te.args[0].split()[-1].replace("_", " ")
            field = field.strip("'")
            print(f"** {field} missing **")
        except Exception as e:
            print("** invalid syntax **")
            pass

    def do_models(self, arg):
        """Print all registered models."""
        print(*classes)


def analyze(line: str):

    """Split lines by spaces."""

    args = shlex.split(line)
    return args, len(args)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
