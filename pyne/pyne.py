"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
import os
from pcconfig import config
import requests
import pynecone as pc


class State(pc.State):
    """The app state."""
    prompt = ""
    image_url = ""
    image_processing = False
    image_made = False
    
    URL = "https://pixabay.com/api/?key="
    
    def process_image(self):
        """Set the image processing flag to true and indicate image is not made yet."""
        self.image_processing = True
        self.image_made = False   
        
    def get_image(self):
        """Get the image from the input."""
        api_url = self.URL+os.getenv("API_KEY")+"&q="+self.prompt+"&image_type=photo&pretty=true"
        res = requests.get(api_url)
        self.image_url = res.json()["hits"][0]['largeImageURL']
        self.image_processing = False
        self.image_made = True


def index() -> pc.Component:
    return pc.center(
        pc.vstack(
            
        pc.vstack(
            pc.heading("Get image from Pixabay", font_size="2em"),
            pc.vstack(
                pc.input(placeholder="Enter your keyword", width="100%", on_blur=State.set_prompt),
                pc.button("Search for image", on_click=[State.process_image, State.get_image], width="100%", _hover={"color": "rgb(107,99,246)",}),
            
                width="60%",
                padding_top="2em",
                padding_bottom="1em"
            ),
            pc.divider(),
            pc.cond(
                State.image_processing,
                pc.circular_progress(is_indeterminate=True),
                pc.cond(
                    State.image_made,
                    pc.image(
                        src=State.image_url,
                        width="70%",
                        padding_top="1em"
                    )
                )
            ),
            bg="#ffffff",
            width="80%",
            max_width="1000px",
            padding="2em",
            shadow="lg",
            border_radius="lg",
        ),
        pc.box(   
            pc.text("I tried to use pynecone for the first time, this lib is super awesome. This code is based on the pynecone tutorial code on their Github."),
            color="white",
            width="80%",
            padding_top="2em",
        )
        ),
        width="100%",
        height="100vh",
        bg="linear-gradient(to right, #0f2027, #203a43, #2c5364);",
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, title="Pynecone:Get-Me-Some-Image")
app.compile()
