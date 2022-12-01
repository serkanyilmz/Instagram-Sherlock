from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Style
import webbrowser
import os
import time

settings = {"row number": 20, "canvas height": 450, "files": "found", "color1": "#DCF0F2", "color2": "#F2C84B",
            "bgcolor": "#DCF0F2"}

titles = {"situations": "Following Situations", "requests": "Requests", "followers": "Followers",
          "followings": "Following", "both_follow": "Follow Each Other",
          "not_you_follow_back": "Not You Follow Back", "not_follow_you_back": "Not Follow You Back",
          "pending": "Pending", "received": "Received", "recent": "Recently",
          "close": "Close Friends", "hide_story_from": "Hide Story From", "hide_story": "Hide Story",
          "unfollowed": "Unfollowed",
          "restricted": "Restricted", "blocked": "Blocked",
          "unneces_hide_story": "Unnecessary"}

messages = {"followers": "Accounts that follow you",
            "followings": "Accounts you choose to see content from",
            "both_follow": "List of accounts that you follow and follow your account.",
            "not_you_follow_back": "List of accounts that follow you but you do not follow back.",
            "not_follow_you_back": "List of accounts that you follow but do not follow back your account.",
            "pending": "Follow requests you’ve sent that haven’t been confirmed or deleted yet",
            "received": "All follow requests you've received since you opened your account.",
            "recent": "Follow requests you recently sent that were either confirmed or deleted",
            "close": "Accounts that you've added to your Close Friends",
            "hide_story_from": "Accounts that you've hidden your story from",
            "unneces_hide_story": "Accounts that unnecessarily hided story which even do not follow you",
            "unfollowed": "Accounts that you've recently stopped following",
            "restricted": "Accounts that you've restricted",
            "blocked": "Accounts that you've blocked",
            "try again": "FILES COULD NOT BE FOUND\n\nPlease copy your downloaded Instagram information to 'data' "
                         "file.\n\nIt must be like:\n/Instagram Sherlock/data/followers_and_following",
            "download link": "\nIf you have not downloaded your Instagram information yet you can use this "
                             "button.\nYou need to choose HTML. It can take some time."}


def open_instagram(nickname):
    webbrowser.open(f"https://www.instagram.com/{nickname}/")


class BUTTON:
    def __init__(self, the_frame, the_list, a, row, column):
        x = Button(the_frame, text=f"{a + 1}. {the_list[a]}", bd=0, bg=settings["bgcolor"], cursor="hand2",
                   command=lambda: open_instagram(the_list[a]))
        x.grid(row=row, column=column, sticky="w")


class TAB:
    def __init__(self, name, the_list, main="notebook"):
        if main != "notebook":
            try:
                globals()[main + "_notebook"]
            except:
                self.tab = ttk.Frame(notebook)
                notebook.add(self.tab, text=titles[main])
                globals()[main + "_notebook"] = ttk.Notebook(self.tab)
                globals()[main + "_notebook"].pack(expand=1, fill=BOTH)
            parent = globals()[main + "_notebook"]
        else:
            parent = notebook
        self.tab = ttk.Frame(parent)
        parent.add(self.tab, text=f"{titles[name]}  ({len(the_list)})")
        msg = Label(self.tab, text=messages[name], padx=10, pady=10, bg=settings["bgcolor"])
        msg.pack(anchor="nw", pady=5)
        the_canvas = Canvas(self.tab, height=settings["canvas height"], bg=settings["bgcolor"])
        the_canvas.pack(side=TOP, fill=BOTH, expand=1)
        sb = ttk.Scrollbar(self.tab, orient=HORIZONTAL, command=the_canvas.xview)
        sb.pack(side=BOTTOM, fill=X)
        the_canvas.config(xscrollcommand=sb.set, bg=settings["bgcolor"])
        the_canvas.bind('<Configure>', lambda e: the_canvas.config(scrollregion=the_canvas.bbox("all")))
        the_frame = Frame(the_canvas, bg=settings["bgcolor"])
        the_canvas.create_window((0, 0), window=the_frame, anchor="nw")
        row = 0
        column = 0
        for a in range(len(the_list)):
            BUTTON(the_frame, the_list, a, row, column)
            row += 1
            if row == settings["row number"]:
                row = 0
                column += 1


class READ:
    def __init__(self, name, link, main="notebook"):
        if os.path.exists(f"./data/{link}.html"):
            self.html = open(f"./data/{link}.html", "r", encoding="utf8").read()
            self.soup = BeautifulSoup(self.html, "html.parser")
            self.list_code = self.soup.find_all("a")
            self.list = []
            for account in self.list_code:
                self.list.append(account.text)
            TAB(name, self.list, main)


def look():
    if os.path.exists(f"./data/followers_and_following"):
        run()
    else:
        if settings["files"] == "found":
            global not_found
            not_found = Frame(root, bg=settings["bgcolor"], pady=100)
            not_found.pack()
            try_again_label = Label(not_found, text=messages["try again"], bg=settings["bgcolor"])
            try_again_label.pack(pady=10)
            try_again_button = Button(not_found, text="Try Again", bg=settings["bgcolor"], command=look)
            try_again_button.pack()
            help_label = Label(not_found, text=messages["download link"], bg=settings["bgcolor"])
            help_label.pack(pady=10)
            link_button = Button(not_found, text="Download Link", bg=settings["bgcolor"],
                                 command=lambda: open_instagram("download/request"))
            link_button.pack()
            settings["files"] = "not found"


def run():
    if settings["files"] == "not found":
        not_found.destroy()
    up_time = time.strftime('%d.%m.%Y %H:%M',
                            time.localtime(os.path.getmtime(f"./data/followers_and_following/followers.html")))
    lab_time = Label(root, text=f"Last update time : {up_time}", bg=settings["bgcolor"])
    lab_time.pack(padx=10, pady=5, anchor="w")
    global notebook
    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill=BOTH, padx=5)
    followers = READ("followers", "followers_and_following/followers", "situations")
    followings = READ("followings", "followers_and_following/following", "situations")
    both_follow_list = []
    not_you_follow_back_list = []
    for person in followers.list:
        if person in followings.list:
            both_follow_list.append(person)
        else:
            not_you_follow_back_list.append(person)
    not_follow_you_back_list = []
    for person in followings.list:
        if person not in followers.list:
            not_follow_you_back_list.append(person)
    TAB("not_follow_you_back", not_follow_you_back_list, "situations")
    TAB("not_you_follow_back", not_you_follow_back_list, "situations")
    TAB("both_follow", both_follow_list, "situations")
    READ("pending", "followers_and_following/pending_follow_requests", "requests")
    READ("recent", "followers_and_following/recent_follow_requests", "requests")
    READ("received", "followers_and_following/follow_requests_you've_received", "requests")
    READ("close", "followers_and_following/close_friends")
    hide_story = READ("hide_story_from", "followers_and_following/hide_story_from", "hide_story")
    unnecessary_hide_story = []
    for person in hide_story.list:
        if person not in followers.list:
            unnecessary_hide_story.append(person)
    TAB("unneces_hide_story", unnecessary_hide_story, "hide_story")
    READ("unfollowed", "followers_and_following/recently_unfollowed_accounts")
    READ("restricted", "followers_and_following/restricted_accounts")
    READ("blocked", "followers_and_following/blocked_accounts")


root = Tk()
root.title("Instagram Sherlock")
root.configure(background=settings["bgcolor"])
root.geometry("800x600")
root.resizable(True, False)
style = Style()
style.theme_create("theme", parent="alt", settings={
    "TFrame": {"configure": {"background": settings["bgcolor"]}},
    "TScrollbar": {"configure": {"background": settings["bgcolor"]}},
    "TNotebook": {"configure": {"background": settings["bgcolor"]}},
    "TNotebook.Tab": {
        "configure": {"padding": [5, 1], "background": settings["color1"]},
        "map": {"background": [("selected", settings["color2"])],
                "expand": [("selected", [1, 1, 1, 0])]}}})
style.theme_use("theme")
look()
root.mainloop()
