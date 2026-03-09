import pygame as pg
import redditwarp.SYNC
from ..state import State
from .title_screen import TitleScreen

class NewsScreen(State):
    
    # Initializes the NewsScreen object and calls the constructor of the parent State class so that inherited variables are initialized.
    def __init__(self):
        super().__init__(None)
        self.temple_logo = pg.image.load("assets/backgrounds/temple_logo.png")
        self.temple_logo = pg.transform.scale(self.temple_logo, (100, 100))
        self.posts = []
        self.font = pg.font.Font(None, 24)
        self.title_font = pg.font.Font(None, 48)
        self.fetch_news()
        
    # Fetches posts from reddit and appends dictionaries to the list to store the title, username, and link of the top 3 posts in the past week from Temple's subreddit.
    def fetch_news(self):
        client = redditwarp.SYNC.Client()
        posts = client.p.subreddit.pull.top('Temple', amount = 3, time = 'week')
        post1 = next(posts)
        self.posts.append({"title": post1.title, "author": post1.author_display_name, "link": post1.permalink})
        post2 = next(posts)
        self.posts.append({"title": post2.title, "author": post2.author_display_name, "link": post2.permalink})
        post3 = next(posts)
        self.posts.append({"title": post3.title, "author": post3.author_display_name, "link": post3.permalink})

    def handle_events(self, events):
        # Main game loop is in secondchance.py and events stores user input.
        for event in events:
            # If user presses a key and the key is enter then proceed to the title screen.
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                self.manager.set_state(TitleScreen)
                   
    # Render everything to screen. Display the top 3 posts from last week if they exist. Use the dictionaries to render to the screen.
    def draw(self):
        super().draw()
        self.screen.fill((160, 0, 0))
        title = self.title_font.render("Top 3 Posts from Temple's Subreddit within", True, "white")
        self.screen.blit(title, (0, 15))
        title = self.title_font.render("the Last Week", True, "white")
        self.screen.blit(title, (250, 55))
        if len(self.posts) > 0:
            post = self.posts[0]
            title1 = self.font.render("Title: " + post["title"], True, "white")
            self.screen.blit(title1, (50, 180))
            user1 = self.font.render("User: u/" + str(post["author"]), True, "white")
            self.screen.blit(user1, (50, 210))
            link1 = self.font.render("Link: " + post["link"], True, "white")
            self.screen.blit(link1, (50, 240))
        if len(self.posts) >= 2:
            post = self.posts[1]
            title2 = self.font.render("Title: " + post["title"], True, "white")
            self.screen.blit(title2, (50, 300))
            user2 = self.font.render("User: u/" + str(post["author"]), True, "white")
            self.screen.blit(user2, (50, 330))
            link2 = self.font.render("Link: " + post["link"], True, "white")
            self.screen.blit(link2, (50, 360))
        if len(self.posts) >= 3:
            post = self.posts[2]
            title3 = self.font.render("Title: " + post["title"], True, "white")
            self.screen.blit(title3, (50, 420))
            user3 = self.font.render("User: u/" + str(post["author"]), True, "white")
            self.screen.blit(user3, (50, 450))
            link3 = self.font.render("Link: " + post["link"], True, "white")
            self.screen.blit(link3, (50, 480))
        prompt = self.font.render("Press Enter to proceed to the title screen.", True, "white")
        self.screen.blit(prompt, (50, 560))
        self.screen.blit(self.temple_logo, (700, 0))