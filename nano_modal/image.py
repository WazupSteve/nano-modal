"""
image class : builder pattern
"""


class Image:
    def __init__(self):
        self.base_image = "python:3.11-slim"
        self.pip_packages = []
        self.commands = []

    @classmethod
    def python(cls, version="3.11"):
        """
        factory method to create image with specific python version
        Image.python("3.11")  # Creates a new Image instance
        """
        # receives class and not instance
        img = cls()  # cls is the class itself ( image )
        img.base_image = f"python:{version}-slim"
        return img

    def pip_install(self, *packages):
        """
        add pip packages to install in container
        """
        # * packages is a tuple of all arguments
        self.pip_packages.extend(packages)
        return self  # essential for chaining

    def run_commands(self, *cmds):
        """
        add shell commands to run in container before the function
        """
        self.commands.extend(cmds)
        return self

    def to_dict(self):
        """
        serialize the image config to dict format
        """
        return {
            "base_image": self.base_image,
            "pip_packages": self.pip_packages,
            "commands": self.commands,
        }

    @classmethod
    def from_dict(cls, data):
        """
        reconstruct image from dict
        """
        image = cls()
        image.base_image = data.get("base_image", "python:3.11-slim")
        image.pip_packages = data.get("pip_packages", [])
        image.commands = data.get("commands", [])
        return image
