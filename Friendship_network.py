"""
COMP.CS.100 Project: Graphical User Interface
Friendship Network program.

I aim to create an advanced GUI program based on the Friendship Network program
in one previous exercise in Round 9. The program is used basically for
analyzing socializing life of people.

The program allows user to use 5 commands (explained below in
explanation_for_program), each of which is linked to a method:

- Print and Quit commands are straight forward commands, which means the program
will not take the entry into considerations.

- In contrast, if the user wants to use the other 3 commands, they need to
interact with the program through Entry box. The entry_display component will
show the user what to do or what he/ she wants to know.

Whenever there is an error happening, there will be a message box to announce
the user about the situation.

Part of the explanations for methods are based on the friendship-base1 from
Round 9.

Creator: Thi Minh Thuy Le <thuy.t.le@tuni.fi>
Student id number: 150533634
"""

from tkinter import *

from tkinter import messagebox

class Userinterface:

    def __init__(self):
        """"
        Constructor.
        """

        # Initialize the friendship network
        self.__network = {}

        # Create the interface with fixed size and title
        self.__mainwindow = Tk()
        self.__mainwindow.title("Friendship Network by Thuy Le")
        self.__mainwindow.geometry("500x700")
        self.__program_title = Label(self.__mainwindow, text="OUR FRIENDSHIP",
                                     font=("Arial Bold", 30))

        # Some guidelines for users
        explanation_for_program = "You can choose one of the commands: \n" \
                                  "Print: Neatly print out the friendship " \
                                  "network in alphabetical order. \n" \
                                  "Add: Add a new friendship between the first " \
                                  "person and others. \n" \
                                  "Friends: Print out in alphabetical order " \
                                  "all the friends of one person. \n" \
                                  "Common: Prints in alphabetical order the " \
                                  "common friends of two people. \n" \
                                  "Quit: Shut down the program."
        self.__guidelines = Label(self.__mainwindow,
                                  text = explanation_for_program)

        # Create 5 buttons for the commands
        self.__print_button = Button(self.__mainwindow, text = "Print",
                                     command = self.print)
        self.__add_button = Button(self.__mainwindow, text = "Add",
                                   command = self.add)
        self.__friends_button = Button(self.__mainwindow, text = "Friends",
                                       command = self.friends)
        self.__common_button = Button(self.__mainwindow, text = "Common",
                                      command = self.common)
        self.__quit = Button(self.__mainwindow, text = "Quit",
                             command = self.quit)

        # Create some components to interact with users
        self.__entry_place = Label(self.__mainwindow,
                                   text = "Give me the names, my user.",
                                   font=("Arial Bold",15))
        self.__entry_box = Entry(self.__mainwindow)
        self.__result_intro = Label(self.__mainwindow,
                                    text = "Let me tell you what you want to"
                                           " know...", font=("Arial Bold",15))
        self.__result_display = Label(self.__mainwindow, text = None)

        # Design the interface for all the components
        self.__program_title.grid(row = 0, column = 0, columnspan = 4)
        self.__guidelines.grid(row = 2, column = 0, columnspan = 4)
        self.__print_button.grid(row = 8, column = 0)
        self.__add_button.grid(row = 8, column = 1)
        self.__friends_button.grid(row = 8, column = 2)
        self.__common_button.grid(row = 8, column = 3)
        self.__quit.grid(row = 8, column = 4)
        self.__entry_place.grid(row = 4, column = 0, columnspan = 4)
        self.__entry_box.grid(row = 5, column = 0, columnspan = 4)
        self.__result_intro.grid(row = 6, column = 0, columnspan = 4)
        self.__result_display.grid(row = 7, column = 0, columnspan = 4)

        self.__mainwindow.mainloop()

    def reset_working_window(self):
        """
        If there happens some errors, the working window will be reset.
        """

        self.__result_display["text"] = "Please try another command."
        self.__entry_box["text"] = None

    def get_info(self):
        """
        Get the information entered by the users from entry box.
        """

        return self.__entry_box.get().strip().split()

    def add_friend(self, name1, name2):
        """
        Adds a friendship.

        The friendships are automatically considered to be a two way
        relationship, therefore, if A has B added as his friend, B will also
        have A added as her friend.

        :param name1: str, Person 1's name
        :param name2: str, Person 2's name
        """

        # Implement a sanity check here to make sure no one can be
        # added as his or her own friend.
        if name1 == name2:
            messagebox.showinfo("Oops!",
                                "A person cannot be his or her own friend."
                                " But it's still OK.")
            return

        # Add information about <name1> being <name2>'s friend and
        # <name2> being <name1>'s friend into the network.
        if name1 not in self.__network:
            self.__network[name1] = []
        if name2 not in self.__network:
            self.__network[name2] = []
        if name2 not in self.__network[name1]:
            self.__network[name1].append(name2)
        if name1 not in self.__network[name2]:
            self.__network[name2].append(name1)

    def add(self):
        """
        Adds a friendship.

        The friendships are automatically considered to be a two way
        relationship, therefore, if A has B added as his friend, B will also
        have A added as her friend.

        In case of any error, network will be left unmodified.
        """

        name_list = self.get_info()

        # Check the errors
        if len(name_list) < 2:
            messagebox.showinfo("Bad entry", "Please enter at least two names.")
            self.reset_working_window()
            return
        else:
            if name_check(name_list):
                for friend in name_list[1:]:
                    self.add_friend(name_list[0], friend)
                self.__result_display["text"] = "This friendship is saved. \n" \
                                                "Please use another command."
                return

    def print(self):
        """
        The function neatly prints out the friendship network.
        All the names and friends' names are printed in alphabetical order.
        Friends' names are printed after the name of the person whose friends
        they are.
        """

        self.reset_working_window()

        result = "The current friendship network is: \n"
        for name in sorted(self.__network):
            result += f"- {name}: "
            for friend_name in sorted(self.__network[name]):
                result += f" {friend_name}"
            result += f"\n"

        self.__result_display["text"] = result

    def friends(self):
        """
        Print out, in alphabetical order, all the friends of a person.

        A message box is created if the entry doesn't contain exactly
        one element which is a string of letters.

        A message box is also created if the name in the namelist does not
        exist in the friendship network.
        """

        name = self.get_info()

        # Check the errors
        if len(name) != 1:
            messagebox.showinfo("Bad entry", "Please enter exactly one name.")
            self.reset_working_window()
            return
        else:
            name = name[0]
            if name_check(name):
                # Check if <name> is an unknown person.
                if name not in self.__network:
                    messagebox.showinfo("Bad entry",
                                        f"Error: '{name}' is an unknown name.")
                    return

            # Give <name>'s friends in alphabetical order as described
            # in the instructions.
            result = f"The current friendship of {name} is: \n"
            for friend_name in sorted(self.__network[name]):
                result += f"{friend_name} \n"
            self.__result_display["text"] = result

    def common(self):
        """
        Prints, in alphabetical order, the common friends of the two persons.

        The following error conditions are possible:

        - There are more or less than two names in the entry.
        - Either of the names in the namelist contains some other characters
        than letters.
        - Either of the names in namelist does not exist in the network.
        """

        name_list = self.get_info()

        # Check the errors
        if len(name_list) != 2:
            messagebox.showinfo("Bad entry", "Please enter exactly two names.")
            self.reset_working_window()
            return
        elif name_check(name_list):
            for name in name_list:
                if name not in self.__network:
                    messagebox.showinfo("Bad entry", f"{name} is unknown.")
                    self.reset_working_window()
                    return

            name1 = name_list[0]
            name2 = name_list[1]

            # Just as a matter of common sense, let's agree that a person
            # does not have common friends with him/herself.
            if name1 == name2:
                messagebox.showinfo("Bad entry",
                                    f"{name1} has no common friends with "
                                    f"him/herself.")
                self.reset_working_window()
                return

            # Find the common friends of <name1> and <name2> and print them
            # in an alphabetical order.
            # If <name1> and <name2> do not have common friends,
            # print instead an error message.
            have_common = False
            for friend_name in sorted(self.__network[name1]):
                if friend_name in self.__network[name2]:
                    have_common = True
                    break
            if have_common == False:
                self.__result_display["text"] = (f"{name1} and {name2} "
                                                 f"have no common friends.")
            else:
                result = f"Common friends of {name1} and {name2} are: \n"
                for friend_name in sorted(self.__network[name1]):
                    if friend_name in self.__network[name2]:
                        result += f" - {friend_name} \n"
                self.__result_display["text"] = result

    def quit(self):
        """
        Ends the execution of the program.
        """

        self.__mainwindow.destroy()

def name_check(name_list):
    """
    Check if all the names entered are in the right form.
    :param name_list: the list of name entered by users, list
    :return: bool
    """

    for name in name_list:
        if not name.isalpha():
            messagebox.showinfo("Bad entry", "Please enter appropriate "
                                                 "names.")
            return False
    return True

def main():
    Friendship = Userinterface()

if __name__ == "__main__":
    main()
