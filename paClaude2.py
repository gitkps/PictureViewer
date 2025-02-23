import tkinter as tk
from tkinter import ttk, Text
from PIL import Image, ImageTk
import os

class ImageAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Annotator")
        
        # Store images and comments
        self.image_files = []
        self.comments = {}
        self.current_index = 0
        
        # Get all image files in current directory
        valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        self.image_files = [f for f in os.listdir('.') if f.lower().endswith(valid_extensions)]
        
        if not self.image_files:
            tk.Label(root, text="No images found in current directory!").pack()
            return
            
        # Create GUI elements
        self.create_widgets()
        self.load_current_image()
        
    def create_widgets(self):
        # Image display
        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)
        
        # Comment box
        self.comment_box = Text(self.root, height=5, width=50)
        self.comment_box.pack(pady=10)
        
        # Navigation buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Previous", command=self.prev_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Next", command=self.next_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Done", command=self.generate_html).pack(side=tk.LEFT, padx=5)
        
    def load_current_image(self):
        # Load and display image
        image_path = self.image_files[self.current_index]
        image = Image.open(image_path)
        
        # Resize image to fit window while maintaining aspect ratio
        display_width = 500
        ratio = display_width / image.width
        display_height = int(image.height * ratio)
        
        image = image.resize((display_width, display_height), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        
        self.image_label.configure(image=photo)
        self.image_label.image = photo  # Keep a reference
        
        # Update window title with current image name
        self.root.title(f"Image Annotator - {image_path}")
        
        # Clear comment box
        self.comment_box.delete(1.0, tk.END)
        
        # If this image has a previous comment, load it
        if image_path in self.comments:
            self.comment_box.insert(1.0, self.comments[image_path])
            
    def save_current_comments(self):
        if self.image_files:
            current_image = self.image_files[self.current_index]
            current_comment = self.comment_box.get(1.0, tk.END.strip())
            if current_comment:  # Only save if there's actually a comment
                self.comments[current_image] = current_comment
            
    def next_image(self):
        if self.current_index < len(self.image_files) - 1:
            self.save_current_comments()  # Save current comments before moving
            self.current_index += 1
            self.load_current_image()
            
    def prev_image(self):
        if self.current_index > 0:
            self.save_current_comments()  # Save current comments before moving
            self.current_index -= 1
            self.load_current_image()
            
    def generate_html(self):
        self.save_current_comments()  # Save final comments
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .image-container {
                    margin: 20px auto;
                    width: 500px;
                }
                .comment-box {
                    width: 500px;
                    margin: 10px auto;
                    padding: 10px;
                    border: 1px solid #ccc;
                    white-space: pre-wrap;
                }
                img {
                    width: 500px;
                    height: auto;
                }
            </style>
        </head>
        <body>
        """
        
        for image_file in self.image_files:
            comment = self.comments.get(image_file, "").strip()
            if comment:  # Only include images that have comments
                html_content += f"""
                <div class="image-container">
                    <img src="{image_file}" alt="{image_file}">
                    <div class="comment-box">{comment}</div>
                </div>
                """
            
        html_content += """
        </body>
        </html>
        """
        
        with open("gallery.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        self.root.quit()

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnnotator(root)
    root.mainloop()